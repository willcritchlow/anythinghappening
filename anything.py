import reddit
from datetime import datetime

r = reddit.Reddit('willcritchlow anythinginterestingbot')
submissions = r.get_subreddit('worldnews').get_top('week')

print [datetime.fromtimestamp(x.created_utc) for x in submissions if datetime.fromtimestamp(x.created_utc) > datetime(2012,06,02,23,30,00)]
