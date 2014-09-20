# coding=utf-8
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.core.files.uploadedfile import UploadedFile
import json
from models import File
import random
import string
from django.template.defaultfilters import filesizeformat


def home(request):
    backgrounds = [
        ("white", "rgba(114, 79, 79, 1)"),
        ("#581D1D", "white"),
        ("#383434", "white"),
        ("#474429", "white"),
        ("#470D3C", "white"),
        ("#120D47", "white"),
        ("#0D4047", "white"),
        ("#24470D", "white"),
        ("#47240D", "white"),
        ("#111111", "white"),
    ]
    background, color = random.choice(backgrounds)
    return render_to_response('home.html', {'background': background, 'color': color}, context_instance=RequestContext(request))


def entry(request, name):
    files = File.objects.filter(username=name).order_by('-created')
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
        entry.filename = unicode(filename)
        entry.username = unicode(name)
        entry.size = file_size
        entry.slug = generate_slug(8)
        entry.data = file
        entry.save()

        uploaded = [{'name': filename, 'size': filesizeformat(file_size), 'slug': entry.slug, 'date': entry.created.date().isoformat()}]

        return HttpResponse(json.dumps({'files': uploaded}))
    else:
        raise Http404


def download(request, slug):
    try:
        file = File.objects.get(slug=slug)
        file.downloaded_count += 1
        file.save()
        return redirect(file.data.url)
    except:
        raise Http404
