from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from news.models import NewsCheck, NewsItem

@login_required
def check(request, nc_id=None):
    my_nc = NewsCheck.objects.filter(user=request.user)
    if nc_id:
        nc = get_object_or_404(NewsCheck, id=nc_id)
        if nc.user != request.user:
            raise Http404
        try:
            start = my_nc.filter(time__lt=nc.time).order_by('-time')[0].time
        except:
            start = None
        end = nc.time
    else:
        try:
            start = my_nc.order_by('-time')[0].time
        except:
            start = None
        end = None
        nc = NewsCheck()
        nc.user = request.user
        nc.save()

    ni = NewsItem.objects.all()
    if start:
        ni = ni.filter(created__gt=start)
    if end:
        ni = ni.filter(created__lt=end)

    if start:
        ni = ni.order_by('-score')[:5]
    else:
        ni = ni.order_by('-created')[:5]

    prev = NewsCheck.objects.filter(user=request.user)
    if nc_id:
        prev = prev.filter(time__lt=nc.time)

    prev = prev.order_by('-time')[:5]

    return render_to_response('news/home.html', {'user': request.user, 'news': ni, 'nc': prev, 'start': start})
