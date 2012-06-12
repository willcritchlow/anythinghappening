from django.core.management.base import BaseCommand
import reddit
from datetime import datetime
from news.models import NewsItem

class Command(BaseCommand):
    help = 'Gets upated top stories from reddit'

    def handle(self, *args, **options):
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
