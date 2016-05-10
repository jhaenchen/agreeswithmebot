import praw
import time
import random

r = praw.Reddit('agreeswithme'
		'Url:http://imtoopoorforaurl.com')
r.login()
already_done=[]

prawWords = ['!agree']


agreePhrases=[
	'Whoa, that makes so much sense. Thank you, sensei.',
	'Brilliant. Simply brilliant.',
	'This mans name? Albert Einstein.',
	'Damn. Couldnt have said it better my self.',
	'Whoa, who said that, Shakespeare?']

while True:
	user = r.get_redditor('therealjakeh')
	for thing in user.get_comments():
		op_text = thing.body.lower()
        	has_praw = any(string in op_text for string in prawWords)
        # Test if it contains a PRAW-related question
		if thing.id not in already_done and has_praw:
            		thing.reply(agreePhrases[random.randrange(0,len(agreePhrases))])
            		already_done.append(thing.id)
			print "Detected a post. Posting comment..."
	time.sleep(210)


