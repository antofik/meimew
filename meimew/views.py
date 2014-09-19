from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.utils import simplejson

def home(request):    
    return render_to_response('home.html', {}, context_instance=RequestContext(request))