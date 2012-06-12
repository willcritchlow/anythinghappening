from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.exceptions import ValidationError
from news.models import NewsCheck, NewsItem
import reddit
from datetime import datetime

@login_required
def check(request, nc_id=None):
    r = reddit.Reddit('willcritchlow anythinginterestingbot')
    submissions = r.get_subreddit('worldnews').get_top('week')
    for submission in submissions:
        try:
            ni = NewsItem.objects.get(slug=submission.id)
        except:
            ni = NewsItem()
            ni.slug = submission.id
            ni.title = submission.title
            ni.url = submission.short_link # use the short link to guarantee it will fit in the database
            ni.comment_url = submission.permalink
            ni.created = datetime.fromtimestamp(submission.created_utc)
        ni.score = submission.score
        try:
            ni.save()
        except:
            print "Error saving %s" % ni.title

    my_nc = NewsCheck.objects.filter(user=request.user)
    if nc_id:
        nc = get_object_or_404(NewsCheck, id=nc_id)
        if nc.user != request.user:
            raise Http404
        start = my_nc.filter(time__lt=nc.time).order_by('-time')[0].time
        end = nc.time
    else:
        start = my_nc.order_by('-time')[0].time
        end = None
        nc = NewsCheck()
        nc.user = request.user
        nc.save()

    ni = NewsItem.objects.filter(created__gt=start)
    if end:
        ni = ni.filter(created__lt=end)

    ni = ni.order_by('-score')[:5]

    prev = NewsCheck.objects.filter(user=request.user)
    if nc_id:
        prev = prev.filter(time__lt=nc.time)

    prev = prev.order_by('-time')[:5]

    return render_to_response('news/home.html', {'user': request.user, 'news': ni, 'nc': prev})
