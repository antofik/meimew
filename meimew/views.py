from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.core.files.uploadedfile import UploadedFile
import json
from models import File
import random
import string


def home(request):    
    return render_to_response('home.html', {}, context_instance=RequestContext(request))


def entry(request, name):
    files = File.objects.filter(username=name)
    return render_to_response('entry.html', {'name': name, 'files': files}, context_instance=RequestContext(request))


def generate_slug(N):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(N))


def upload(request, name):
    if request.method == 'POST':
        if request.FILES is None:
            return HttpResponseBadRequest('No file[] found')

        file = request.FILES[u'files[]']
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size

        entry = File()
        entry.filename = filename
        entry.username = name
        entry.size = file_size
        entry.slug = generate_slug(8)
        entry.data = file
        entry.save()

        uploaded = [{'name': filename, 'size': file_size}]

        mimetype = 'text/plain'
        if 'HTTP_ACCEPT_ENCODING' in request.META.keys():
            if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
                mimetype = 'application/json'
        return HttpResponse(json.dumps({'files': uploaded}), mimetype=mimetype)
    else:
        raise Http404


def download(request, slug):
    try:
        file = File.objects.get(slug=slug)
        return redirect("/media/user-files/%s/%s/%s" % (file.username, file.created.date().isoformat(), file.filename))
    except:
        raise Http404