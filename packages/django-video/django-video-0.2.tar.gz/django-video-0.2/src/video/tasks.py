import hashlib
import os
from concurrent.futures import ThreadPoolExecutor

import glob2
from django.core.files import File
from djworkspace.store import local, store
from ffmpeg import get_dimension, get_duration, sample_clips, sample_images

from .models import Clip, Image, Video


def _hash(filepath):
    m = hashlib.md5()

    with open(filepath) as ifile:
        m.update(ifile.read())

    return m.hexdigest()


def upload(file_or_folder, to_storage=True):
    if os.path.isdir(file_or_folder):
        paths = glob2.glob(u'%s/**/.mp4' % file_or_folder)
    elif os.path.isfile(file_or_folder):
        paths = [file_or_folder]
    else:
        raise NotImplementedError()

    output = []
    for filepath in paths:
        title = os.path.basename(filepath)

        video = Video.objects.create(
            title=title,
            hash=_hash(filepath),
            duration=get_duration(filepath),
            dimension=get_dimension(filepath)
        )

        if not video.file and to_storage:
            store(video.file, filepath)
        else:
            video.url = filepath

        video.save()

        output.append(video)

    return output


def _get_video_filepath(video):
    if video.url and os.path.exists(video.url):
        return video.url

    return local(video.file)


def process_images(video, fps=1):
    second = 0

    filepath = _get_video_filepath(video)

    output = []
    for image_path in sample_images(filepath, fps):
        image, _ = Image.objects.get_or_create(
            video=video,
            second=second,
            defaults={
                "hash": _hash(image_path)
            }
        )

        if not image.thumbnail:
            store(image.thumbnail, image_path)

        second += fps
        output.append(image)

    return output


def process_clips(video, threshold=0.3, min_delta_time=3, dummy=False):
    filepath = _get_video_filepath(video)

    output = []
    for scene_info, clip_path in sample_clips(filepath, threshold, min_delta_time):
        clip, _ = Clip.objects.get_or_create(
            video=video,
            start_time=scene_info['from_ts'],
            end_time=scene_info['to_ts'],
            defaults={
                "duration": scene_info["duration"],
                "hash": _hash(clip_path)
            }
        )

        if not clip.file:
            store(clip.file, clip_path)

        output.append(clip)

    return output


def map_to_images(video, filter, worker=5, timeout=None):
    with ThreadPoolExecutor(worker) as e:
        return list(e.map(filter, video.image_set.all().order_by('second'), timeout=timeout))
