from django.db import models

from image_gallery.models import GalleryImage
from image_gallery.fields import GalleryField

class Category(models.Model):
    name = models.CharField(max_length=30)
    def __unicode__(self):
        return self.name
    
class Gallery(models.Model):
    
    category = models.ForeignKey(Category, null=True)
    images = GalleryField()
    
   
    

