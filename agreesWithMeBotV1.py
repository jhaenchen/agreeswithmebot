import praw
import time
import random
import pprint
import requests
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
	'Whoa, who said that, Shakespeare?',
	'Yeah, you tell him!',
	'Honestly it\'s comments like these that make me smile.',
	'That\'s incredible! Literally amazing!',
	'What\'s it like being so amazing?',
	'Just like grandma used to say. Wise words.',
	'This made me start believing in god again. Amen.',
	'I\'ve been on this earth forty years and only now just realized what I\'ve been missing: your words.',
	'This whole bot thing is overrated. I\'m just going to keep printing your comment forever instead. Because it\'s awesome.',
	'Pretty. damn. smart.'
	'My mom saw this and said she\'s sending you cookies. Thank you.',
	'How do you always manage to fit so much meaning into so few words?',
	'Deeper than the marina trench.',
	'God? Is that you?',
	'I\'m working on another bot just to keep up with how much I agee with you.',
	'How do you spell that? Because Im getting a tattoo of it.',
	'Ah yes. Mark 23:12. A wise verse.']

appendPhrase = '\n\n^(Need some backup?) [^"/u/agreeswithmebot"](https://github.com/jhaenchen/agreeswithmebot)'
while True:
	try:
		print "checking..."
		#Check my messages
		for message in r.get_unread(unset_has_mail=True, update_user=True):
			if("!agree" in message.body.lower() or  "/u/agreeswithmebot" in message.body.lower()):

				if ("!parent" in message.body.lower()):
					print "Got child  message, sending parent reply"
					parent = r.get_info(thing_id=message.parent_id)
					if(isinstance(parent, praw.objects.Comment)):
						parent.reply(agreePhrases[random.randrange(0,len(agreePhrases))]+appendPhrase)
					else:
						message.reply(agreePhrases[random.randrange(0,len(agreePhrases))]+appendPhrase)
				else:
					print "Got message, sending reply"
					message.reply(agreePhrases[random.randrange(0,len(agreePhrases))]+appendPhrase)
			message.mark_as_read()
		print "sleeping..."
		time.sleep(210)
	except requests.exceptions.ReadTimeout:
		"Read timeout. Will try again."
	except praw.errors.HTTPException:
		print "Http exception. Will try again."
	except praw.errors.RateLimitExceeded as error:
		print '\tSleeping for %d seconds' % error.sleep_time
            	time.sleep(error.sleep_time)		
	except praw.errors.APIException:
		print "API exception. Will try again."
	except (KeyboardInterrupt, SystemExit):
		print "Safe exit..."
		raise
	except:
		print "Unhandled exception, bail!"
		r.send_message('therealjakeh', 'AgreesWithMeBot', 'Just went down! Help!')
		raise


