# -*- coding: utf-8 -*- 
from django.views.generic import ListView
from django.views.generic.edit import CreateView,FormView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django import forms
from models import Gallery, Category
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from image_gallery.models import GalleryImage
import json,os, zipfile,imghdr
from django.core.files import File
from PIL import Image
from django.conf import settings
import random
from django.core.mail import  EmailMessage
#class GalleryList(ListView):
#    model = Gallery
#    def get (self, req, *k, **kw):
        

class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'id': self.object.pk,
                'name':self.object.name
            }
            return self.render_to_json_response(data)
        else:
            return response
"""            
class AddGallery(CreateView):
    model = Gallery
    def __init__(self,*k,**kw):
        
        super(AddGallery, self).__init__( *k, **kw)
        
        self.success_url = reverse('file_upload_url', args = [] )
        
    def form_valid(self, *k, **kw):
        print "VALID", k, kw
        return super(AddGallery, self).form_valid(*k, **kw)
    def form_invalid(self, form):
        
        print "INVALID"
        return super(AddGallery, self).form_invalid(form)
        
    def post(self, *k, **kw):
        
        print "POST"
        return super(AddGallery, self).post(*k, **kw)
"""

class GalleryList(CreateView):
    model = Gallery
    template_name='app/gallery_list.html'
    
    def __init__(self,*k,**kw):
        super(GalleryList, self).__init__( *k, **kw);
        
        self. success_url = reverse('file_upload_admin', args = [] )
    
    
    def get_context_data(self, **kw):
        ctx = super(GalleryList, self).get_context_data(**kw)
        ctx['object_list'] = self.model.objects.all()
        return ctx
    def form_valid(self, form):
        # print "VALID", dir(form)
        cat = form.cleaned_data['category']
        imgs = form.cleaned_data['images']
        print repr(cat.id), imgs
        gals = Gallery.objects.filter(category__id = cat.id)
        if gals.count() == 0:
            gal = Gallery.objects.create(category = cat)
        else:
            gal = gals[0]
        for i in imgs:
            gal.images.add(i)
        self.object = gal
        return HttpResponseRedirect(self.get_success_url() )
        #raise IndexError('123')
        #return super(GalleryList, self).form_valid(form)

class ZipUploadForm(forms.Form):
    file = forms.FileInput()

class ZipUpload(FormView):
    form_class = ZipUploadForm
    
    
    def form_valid(self, form):
        print form.cleaned_data
        file = self.request.FILES['file']
        name = file.name
        file_ids,urls = self.process_zipfile(file)
        
        res = {'success': True, 'file_ids': file_ids, 'thumb_urls':urls}
        return HttpResponse(json.dumps (res))
        # raise IndexError('dd')
     
    def process_zipfile(self, zip_):
        #if os.path.isfile(zip_.path):
            # TODO: implement try-except here
        zip = zipfile.ZipFile( zip_ )
        bad_file = zip.testzip()
        if bad_file:
            raise Exception('"%s" in the .zip archive is corrupt.' % bad_file)
        count = 1
        from cStringIO import StringIO
        created_files = []
        created_thumb_urls = []
        for filename in sorted(zip.namelist()):
            if filename.startswith('__'): # do not process meta files
                continue
            data = zip.read(filename)
            if len(data):
                
                file = File( StringIO(data))
                img = GalleryImage()
                img.image.save(filename, file)
                if self.request.user.is_authenticated():
                    img.owner = self.request.user
                img.save()
                if img.image.width > img.image.height :
                    #LANDSCAPE
                    orientation = False
                else:
                    orientation = True
                img.orientation = orientation
                
                img.thumbnail.save(os.path.basename(img.image.path), File(open(img.image.path)))
                thumb = Image.open(img.image.path)
                
                (w, h) = thumb.size
                side = min(w, h)
                thumb = thumb.crop([(w - side) / 2, (h - side) / 2, (w + side) / 2, (h + side) / 2])
                thumb.thumbnail((100,100), Image.ANTIALIAS)
                #print img.thumbnail.path
                thumb.save(img.thumbnail.path, quality=100)
                img.save()
                fsize = img.image.size
                
                max_fsize = 50000000
                #print fsize, max_fsize
                if fsize <= max_fsize:
                    type = imghdr.what(img.image.path).upper()
                    allowed_types = ['png', 'jpg','jpeg','gif']
                    #print "sized",type
                    
                    if type.lower() in allowed_types:
                        #print "allowed"
                        pil_img  = Image.open(img.image.path)
                        min_size = (100,100)
                        max_size = (5000,5000)
                        if pil_img.size[0] >= min_size[0] and pil_img.size[1] >= min_size[1]:
                            #print "good_size", pil_img.size, min_size, max_size
                            if pil_img.size[0] <= max_size[0] and pil_img.size[1] <= max_size[1]:
                                #print "good_size"
                                created_files.append(img.id)
                                created_thumb_urls.append(img.thumbnail.url)
                             
                
        zip.close()
        return created_files, created_thumb_urls
        #return gallery
class AddCategory(AjaxableResponseMixin,    CreateView):
    model = Category
    def __init__(self,*k,**kw):
        super(AddCategory, self).__init__( *k, **kw);
        
        self. success_url = reverse('file_upload_admin', args = [] )
def send_me_amessage(req):
    name = req.POST.get('name')
    email = req.POST.get('email')
    text = req.POST.get('text')
    if settings.DEBUG:
        sender = 'vg.stavenko@yandex.ru'
    else:
        sender = 'info@holin.pro'
    subj = u"Сообщение с сайта holin.pro !"
    body = u"""<h3>Пользователь воспользовался формой отсылки сообщения с сайта</h3>
    <ul>
    <li> Имя: %s </li>
    <li> email: %s </li>
    <li> Содержимое: %s </li>
    </ul>
    """ %( name, email, text)
    recv = settings.OWNER_EMAIL
    email = EmailMessage(subj, body, sender, [recv] )
    email.content_subtype = "html"
    try:
        email.send()
    except Exception as e:
        print e
    return HttpResponseRedirect('/')
    
    
    
def get_pics(req):
    cat =  int(req.GET.get('category_id'))
    portreits =  int(req.GET.get('portreits'))
    landscapes = int(req.GET.get('landscapes'))
    p_seen =  int(req.GET.get('p_seen'))
    l_seen =  int(req.GET.get('l_seen'))
    page =  int(req.GET.get('page',0))
    gc = GalleryImage.objects.filter(gallery__category__id = cat )
    lsQ = gc.filter(orientation = False) [l_seen:l_seen + landscapes] 
    psQ = gc.filter(orientation = True ) [p_seen:p_seen + portreits] 
    if lsQ.count() < landscapes:
        ids = [i.id for i in gc.filter(orientation = False)]
        random.shuffle(ids)
        addids = ids[:landscapes - lsQ.count()]
        lsQA = GalleryImage.objects.filter(id__in = addids)
        ls = list(lsQ)
        print "ls", len(ls)
        ls.extend(list(lsQA))
        print "ls", len(ls), lsQA.count()
        
    else:
        ls =list(lsQ)
        
    if psQ.count() < portreits:
        ids = [i.id for i in gc.filter(orientation = True)]
        print ids
        random.shuffle(ids)
        addids = ids[:portreits - psQ.count()]
        print addids
        psQA = GalleryImage.objects.filter(id__in = addids)
        
        ps = list(psQ)
        print "ps", len(ps)
        ps.extend(list(psQA))
        print "ps", len(ps), psQA.count()
    else:
        ps = list(psQ)
        
    print "lsp,", len(ls), len(ps)
    ls.extend(ps)
    print len(ls)
    arr = []
    for gi in ls:
        d = gi.__dict__
        d['url'] = gi.image.url
        d['t_url'] = gi.thumbnail.url
        
        del d['_state']
        del d['creation_time']
        del d['image']
        del d['thumbnail']
        arr.append(d)
    return HttpResponse(json.dumps(arr))
    
def main_page(req):
    m_gal = Category.objects.filter( name=u'Главная')[0]    
    w_gal = Category.objects.filter( name=u'Свадебная')[0]
    main = Gallery.objects.filter(category__id = m_gal.id)[0]
    wedding = Gallery.objects.filter(category__id = w_gal.id)[0]
    
    ctx = {}
    ctx['main_images'] = main.images.all()
    ctx['wedding_images'] = wedding.images.all()
    ctx.update(csrf(req))
    return render_to_response("index.html",ctx)
