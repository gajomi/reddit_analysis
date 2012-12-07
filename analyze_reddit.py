from itertools import islice
from operator import itemgetter
import praw
from collections import Counter
from pprint import pprint as pretty

thing_limit = 100

#our bot
user_agent = "Weitz Reddit Analysis Team of Excellence (WRATE) v0.0.1"
r = praw.Reddit(user_agent=user_agent)

#a submission about fish eating pigeons
pigeon_fish_submission = r.get_submission(submission_id = "14dkff")
authors = authors_by_submission(pigeon_fish_submission)

#lets focus in on the author with the most "comment karma", and find out what subreddits they read
author = argmax_f(authors,lambda a: a.comment_karma)
author_comments = comments_by_author(author)
subreddit_counts = Counter(comment.submission.subreddit.display_name for comment in author_comments)
pretty(dict(subreddit_counts))

#lets now go to the first comments rubreddit and find out what other comments there are. What are people saying?
subreddit_comments = author_comments[0].subreddit
subreddit_comments = take(thing_limit,subreddit.get_comments(limit = thing_limit))
pretty([comment.body for comment in subreddit_comments])


def comments_by_submission(s):
    """Returns flat list of all comments in a submission"""
    return s.all_comments

def authors_by_submission(s):
    """Return a flat list of all authors in a submission"""
    return {comment.author for comment in s.all_comments if comment.author is not None}

def comments_by_author(author,limit = 100):
    """Returns a flat list of all the comments made by a specified author"""
    #reddit api automatically chunks things into 25 calls with 2 second delay, 100 seems to be a nice practical limit
    iter_comments = author.get_comments(limit = limit)
    return take(limit,iter_comments)

#utils below, to be factored out

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))
    
def argmax(pairs):
    """Returns argmax by ar val pairs"""
    return max(pairs, key=itemgetter(1))[0]

def argmax_f(X, f):
    """Argmax in the classical sense, finite args"""
    return argmax((x, f(x)) for x in X)

