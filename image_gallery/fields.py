# -*- coding: utf-8 -*-
from django.db import models

from image_gallery.models import GalleryImage
from image_gallery.forms import GalleryFormField


class GalleryField(models.ManyToManyField):
    def __init__(self, **kwargs):
        if('max_images' in kwargs):
            self.max_images = kwargs.pop('max_images')
        else:
            self.max_images = None
        # print dir(self.rel.to)
        
        self.help_text = kwargs.get('help_text')
        kwargs.setdefault('to', GalleryImage)
        super(GalleryField, self).__init__(**kwargs)
        
    def formfield(self, **kwargs):
        defaults = {'form_class': GalleryFormField,
                    'max_images': self.max_images, }
        defaults.update(kwargs)
        return super(GalleryField, self).formfield(**defaults)


from south.modelsinspector import add_introspection_rules
rules = [ ((GalleryField,),[],{'to':[GalleryImage,{"is_value":True}]}, )]
add_introspection_rules(rules, ["^image_gallery\.fields\.GalleryField"])
