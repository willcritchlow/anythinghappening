from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from news.models import NewsCheck, NewsItem
import reddit
from datetime import datetime

@login_required
def home(request):
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
def temp(request):
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
            ni.save()
        except:
            print "%s already in database" % ni
