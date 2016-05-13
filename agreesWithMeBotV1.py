import praw
import time
import random
import pprint
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
	'What\'s it like being so amazing?']

appendPhrase = '\n\n^(Need some backup?) [^"/u/agreeswithmebot"](https://github.com/jhaenchen/agreeswithmebot)'
while True:
	try:
		print "checking..."
		#Check my messages
		for message in r.get_unread(unset_has_mail=True, update_user=True):
			if("!agree" in message.body.lower() or  "/u/agreeswithmebot" in message.body.lower()):

				if ("that" in message.body.lower()):
					print "Got child  message, sending parent reply"
					parent = r.get_info(thing_id=message.parent_id)
					#Respond with a random sentence from the available collection
					parent.reply(agreePhrases[random.randrange(0,len(agreePhrases))]+appendPhrase)
				else:
					print "Got message, sending reply"
					message.reply(agreePhrases[random.randrange(0,len(agreePhrases))]+appendPhrase)
			message.mark_as_read()
		print "sleeping..."
		time.sleep(210)
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
		raise


