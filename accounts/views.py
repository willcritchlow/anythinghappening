from django.shortcuts import render_to_response, redirect
from accounts.forms import MyUserCreationForm
from django.template import RequestContext
from django.contrib.auth import authenticate, login,logout

def logout_view(request):
    logout(request)
    return redirect('index')

def create(request):
    if 'next' in request.GET:
        next_page = request.GET['next']
    elif 'next' in request.POST:
        next_page = request.POST['next']
    else:
        next_page = ''
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request,user)
            if next_page:
                return redirect(next_page)
            else:
                return redirect('home')
    else:
        form = MyUserCreationForm()
    return render_to_response('accounts/create.html', {'form': form, 'next': next_page, 'user': request.user}, context_instance=RequestContext(request))
