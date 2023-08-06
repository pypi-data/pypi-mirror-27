from django import forms
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.html import format_html
from jet.admin import CompactInline

from .models import App, Clip, Image, Label, Video

# Register your models here.


class LabelActionAdmin(admin.ModelAdmin):
    def all_labels(self, obj):
        return ','.join(map(unicode, obj.labels.all()))

    class AddLabelForm(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        labels = forms.ModelMultipleChoiceField(
            Label.objects.filter(auto=False))

    def remove_label(self, request, queryset):
        form = None
        if 'apply' in request.POST:
            form = self.AddLabelForm(request.POST)

            if form.is_valid():
                labels = form.cleaned_data['labels']

                for object in queryset:
                    object.labels.remove(*labels)

                self.message_user(request, 'Sucessfully removed %s labels' % (queryset.count()))
                return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = self.AddLabelForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        return render(
            request,
            'admin/remove_label.html',
            {
                'objects': queryset,
                'label_form': form,
            }
        )

    remove_label.short_description = "Remove labels"

    def add_label(self, request, queryset):
        form = None

        if 'apply' in request.POST:
            form = self.AddLabelForm(request.POST)

            if form.is_valid():
                labels = form.cleaned_data['labels']

                for object in queryset:
                    object.labels.add(*labels)

                self.message_user(request, "Successfully added %s labels" % (queryset.count()))
                return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = self.AddLabelForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        return render(
            request,
            'admin/add_label.html',
            {
                'objects': queryset,
                'label_form': form,
            }
        )

    add_label.short_description = "Add labels"


class ClipInline(CompactInline):
    model = Clip


class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'preview', 'date', 'text', 'app')
    list_filter = ('app', )
    actions = ('set_app', )
    list_per_page = 15

    class SetAppForm(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        app = forms.ModelChoiceField(App.objects.all())

    def set_app(self, request, queryset):
        form = None

        if 'apply' in request.POST:
            form = self.SetAppForm(request.POST)

            if form.is_valid():
                app = form.cleaned_data['app']

                for object in queryset:
                    object.app = app
                    object.save()

                self.message_user(request, "Successfully added %s app" % (queryset.count()))
                return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = self.SetAppForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        return render(
            request,
            'admin/set_app.html',
            {
                'objects': queryset,
                'label_form': form,
            }
        )

    set_app.short_description = "Set App"

    def preview(self, obj):
        if obj.file:
            return format_html(
                u'<video style="height:200px" controls preload="metadata"><source src="{}" type="video/mp4"></video>',
                obj.file.url
            )

    inlines = [
        ClipInline
    ]


class ImageInline(CompactInline):
    model = Image


class LabelAdmin(admin.ModelAdmin):
    list_display = ('type', 'name', 'auto')


class ClipAdmin(LabelActionAdmin):
    list_display = ('__unicode__', 'start_time', 'preview', 'all_labels')
    list_filter = ('video__app', 'video', )
    list_per_page = 10

    inlines = [
        ImageInline
    ]

    actions = ['add_label', 'remove_label']

    def preview(self, obj):
        try:
            return format_html(
                u'<video style="height:200px" controls preload="metadata"><source src="{}" type="video/mp4"></video>',
                obj.file.url
            )
        except:
            return "no preview"


class ImageAdmin(LabelActionAdmin):
    list_display = ('__unicode__', 'second', 'preview', 'all_labels')
    list_filter = ('video__app', 'labels', 'video')

    actions = ['add_label', 'remove_label']

    def preview(self, obj):
        if obj.thumbnail:
            return format_html(
                u'<a href="{}"><img style="max-height:200px" src="{}"></a>',
                obj.thumbnail.url,
                obj.thumbnail.url
            )


admin.site.register(App)
admin.site.register(Video, VideoAdmin)
admin.site.register(Clip, ClipAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Label, LabelAdmin)
