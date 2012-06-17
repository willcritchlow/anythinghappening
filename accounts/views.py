from django.shortcuts import render_to_response, redirect
from accounts.forms import UserCreateForm
from django.template import RequestContext
from django.contrib.auth import authenticate, login

def create(request):

    return render_to_response('accounts/login.html', {}, context_instance=RequestContext(request))
