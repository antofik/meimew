# coding=utf-8
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.core.files.uploadedfile import UploadedFile
import json
from models import File, Entry
import random
import string
import time
import datetime
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
    background, color = backgrounds[0]  # random.choice(backgrounds)
    return render_to_response('home.html', {'background': background, 'color': color},
                              context_instance=RequestContext(request))


def entry(request, name):
    files = File.objects.filter(username=name).order_by('-created')
    return render_to_response('home.html', {'name': name, 'files': files}, context_instance=RequestContext(request))


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

        uploaded = [{'name': filename, 'size': filesizeformat(file_size), 'slug': entry.slug,
                     'date': entry.created.date().isoformat()}]

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


class Database(object):
    @staticmethod
    def get(revision, family_password):
        result = []
        entries = Entry.objects.filter(family_id=family_password, revision__gt=revision)
        for entry in entries:
            result.append(entry.data)
        return result

    @staticmethod
    def store(new_revision, items):
        for item in items:
            obj, created = Entry.objects.get_or_create(id=item.id, defaults={
                'data': item.data,
                'revision': new_revision,
                'owner_id': item.owner_id,
                'family_id': item.family_id
            })
            obj.save()

    @staticmethod
    def set_family_password(owner_id, family_password):
        new_revision = time.time() + datetime.timedelta(days=3).total_seconds()
        Entry.objects.filter(owner_id=owner_id).update(family_id=family_password, revision=new_revision)
Database.items = []


class Item:
    def __init__(self, data):
        self.id = data['Id']
        self.data = data['Data']
        self.revision = float(data['Revision'])
        self.owner_id = data['Owner']
        self.family_id = str(data['FamilyPassword'])


def family_expenses(request):
    if request.method == "POST":
        owner_id = str(request.POST["PhoneId"])
        family_password = str(request.POST["FamilyPassword"])
        revision = float(request.POST["Revision"])
        items = json.loads(request.POST["Data"])
        items = [Item(item) for item in items]
        new_revision = time.time() + datetime.timedelta(days=3).total_seconds()
        Database.store(new_revision, items)
        data = Database.get(revision, family_password)
        return HttpResponse(json.dumps({"Revision": new_revision, "Data": data}))
    else:
        return redirect("/family-expensеs")

def change_family(request):
    if request.method == "POST":
        owner_id = str(request.POST["PhoneId"])
        family_password = str(request.POST["FamilyPassword"])
        Database.set_family_password(owner_id, family_password)
        return HttpResponse("ok")
    else:
        return redirect("/family-expensеs")




























