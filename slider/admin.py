from django import forms
from django.db import models
from django.utils.html import format_html
from suit.admin import admin
from suit.admin import SortableModelAdmin
from .models import SlideItem


class AdminImageWidget(forms.ClearableFileInput):
    template_with_initial = (
        '<p class="file-upload">'
        '%(initial_text)s:<br /><img style="max-width: 350px;max-width: 350px;" src="%(initial_url)s" title="%(initial)s"/>'
        '%(clear_template)s<br />%(input_text)s: %(input)s'
        '</p>'
    )
    # template_with_clear = ('<span class="clearable-file-input">%s</span>' % forms.ClearableFileInput.template_with_clear)


@admin.register(SlideItem)
class SlideItemAdmin(SortableModelAdmin):
    def __init__(self, *argz, **kwargz):
        super(self.__class__, self).__init__(*argz, **kwargz)

    list_display = ('title', 'thumb', 'active', 'order')
    list_editable = ('active', 'order')
    list_filter = ('active',)
    search_fields = ('title', 'image',)
    sortable = 'order'

    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget},
    }

    def thumb(self, obj):
        return format_html(
            '<img src="{}" title="{}" style="max-width:50px;max-height:50px;"/>',
            obj.get_image_url(),
            obj.image
        )