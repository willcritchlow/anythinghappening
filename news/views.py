from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.exceptions import ValidationError
from news.models import NewsCheck, NewsItem
import reddit
from datetime import datetime

@login_required
def home(request):
    try:
        r = reddit.Reddit('willcritchlow anythinginterestingbot')
        submissions = r.get_subreddit('worldnews').get_top('week')
        for submission in submissions:
            ni = NewsItem()
            ni.slug = submission.id
            ni.title = submission.title
            ni.url = submission.url
            ni.comment_url = submission.permalink
            ni.created = datetime.fromtimestamp(submission.created_utc)
            ni.score = submission.score
            try:
                ni.validate_unique()
                ni.save()
            except ValidationError:
                print "%s already in database" % ni
    except:
        print "Problem getting information from reddit"
    try:
        last_check = NewsCheck.objects.filter(user=request.user).order_by('-time')[0]
        relevant_news = NewsItem.objects.filter(created__gt=last_check.time).order_by('-score')[:5]
    except:
        relevant_news = None
    nc = NewsCheck()
    nc.user = request.user
    nc.save()
    return render_to_response('news/home.html', {'user': request.user, 'news': relevant_news})

@login_required
def check(request, nc_id):
    nc = get_object_or_404(NewsCheck, id=nc_id)
    if nc.user != request.user:
        raise Http404

    try:
        previous_nc = NewsCheck.objects.filter(time__lt=nc.time).order_by('-time')[0]
        start_time = previous_nc.time
    except:
        start_time = nc.time

    ni = NewsItem.objects.filter(created__gt=start_time).filter(created__lt=nc.time)

    return render_to_response('news/check.html', {'nc': nc, 'ni': ni})
