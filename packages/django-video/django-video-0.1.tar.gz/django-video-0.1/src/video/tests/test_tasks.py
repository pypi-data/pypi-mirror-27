import pytest
from video.tasks import process_clips, process_images, upload, map_to_images
from os.path import join, dirname

test_file = "test_data/10257640.mp4"


@pytest.mark.django_db
def test_upload():
    filepath = join(dirname(__file__), test_file)
    videos = upload(filepath)

    assert len(videos) == 1
    assert videos[0].hash == 'cee0d481230189ea2e84ddce5cdec96b'

    return videos[0]


@pytest.mark.django_db
def test_process_clips():
    video = test_upload()

    clips = process_clips(video, threshold=0.01, min_delta_time=0.1)
    assert len(clips) == 4
    return clips


@pytest.mark.django_db
def test_process_images():
    video = test_upload()

    images = process_images(video)
    assert len(images) == 8
    return images


@pytest.mark.django_db
def test_map_to_images():
    video = test_upload()
    images = process_images(video)

    results = map_to_images(video, lambda image: image.hash)

    assert results == [k.hash for k in images]
