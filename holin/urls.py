from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.contrib import admin
admin.autodiscover()

from app import views 
    

    
urlpatterns = patterns('',
    url(r'^site_edit/$', login_required(views.GalleryList.as_view()), name='file_upload_admin'),
    url(r'^category_add/$', views.AddCategory.as_view(), name='add_category'),
    url(r'^zip_upload/$', views.ZipUpload.as_view(), name = 'zip_upload_url'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',name="my_login"),
    # url(r'^add/$', views.AddGallery.as_view(), name='add'),

    url(r'^image_gallery/', include('image_gallery.urls', namespace='image_gallery')),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^get_pics/$', views.get_pics),
    
    url(r'^send-me-a-message/$', views.send_me_amessage),
    
    url(r'^$', views.main_page),
    
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
   )