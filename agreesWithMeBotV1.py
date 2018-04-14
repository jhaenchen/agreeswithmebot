import praw
import time
import random
from pprint import pprint
import re
import requests
from threading import Thread
r = praw.Reddit('agreeswithme'
		'Url:http://imtoopoorforaurl.com')

r.login()
already_done=[]

def findNegCommentsAndDelete():
	while(1):
		comments = r.user.get_comments('new')
		for comment in comments:
			if(comment.score < 0):
				comment.delete()
		time.sleep(500)

thread = Thread(target = findNegCommentsAndDelete)
thread.start()


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
	'Pretty. damn. smart.',
	'Fo shizzle ma dawg.',
	'I think I saw that carved into some Mayan ruins. Amazing wisdom from a forgotten age.',
	'My mom saw this and said she\'s sending you cookies. Thank you.',
	'How do you always manage to fit so much meaning into so few words?',
	'Deeper than the marina trench.',
	'God? Is that you?',
	'I\'m working on another bot just to keep up with how much I agree with you.',
	'How do you spell that? Because Im getting a tattoo of it.',
	'Ah yes. Mark 23:12. A wise verse.']

appendPhrase = '\n\n^(Need some backup?) ^"/u/agreeswithmebot"! ^| ^(I delete negative comments)'
#appendPhrase = '\n\n *** \n^^(Need) ^^(backup?) ^[^"/u/agreeswithmebot"!](https://reddit.com/u/agreeswithmebot)\n\n^[^Contribute](https://www.reddit.com/r/agreeswithmebot/submit?text=%20&title=Agree:%3Cyour%20text%20here%3E) ^[^an](https://www.reddit.com/r/agreeswithmebot/submit?text=%20&title=Agree:%3Cyour%20text%20here%3E) ^[^agreement](https://www.reddit.com/r/agreeswithmebot/submit?text=%20&title=Agree:%3Cyour%20text%20here%3E) ^^(|) ^[^Github](https://github.com/jhaenchen/agreeswithmebot) ^^(|) ^[^Subreddit](https://reddit.com/r/agreeswithmebot)'

#appendPhrase = '\n\n *** \n^^(Need) ^^(backup?) ^[^"/u/agreeswithmebot"!](https://reddit.com/r/agreeswithmebot) ^^|| ^^[Add](https://www.reddit.com/r/agreeswithmebot/submit?text=%20&title=Agree:%3Cyour%20text%20here%3E) ^^an ^^agreement'

def generateQuote(message):
	#Remove links so periods don't get noticed and elipses'
	text = re.sub(r'\(.*?\)|\.{3,}|\[|\]','', message.body)
	segments = text.split(".")
	#Sometimes it gives us an empty string if the comment ends with a period
	#So let's strip it out'
	if (len(segments[len(segments)-1]) == 0):
		segments.pop();
	chosenSentence = segments[random.randrange(0, len(segments))]
	#If the sentence starts with a newline remove that
	chosenSentence = re.sub(r'\n{1,}','',chosenSentence)
	chosenSentence.replace("/u/agreeswithmebot", '')
	return "\n>" + chosenSentence + "\n\n"

while True:
	try:
		print("checking...")
		#Check my messages
		for message in r.get_unread(unset_has_mail=True, update_user=True):
			if("!agree" in message.body.lower() or  "/u/agreeswithmebot" in message.body.lower()):
				if ("!parent" in message.body.lower()):
					print("Got child  message, sending parent reply")
					parent = r.get_info(thing_id=message.parent_id)
					if(isinstance(parent, praw.objects.Comment)):
						quote = generateQuote(parent)
						print(quote)
						if(parent.author.name == "agreeswithmebot"):
							quote = 'Uh oh, we got ourselves a smart guy here! Try again :)'
							newComment = message.reply(quote)
							user = message.author
							r.send_message(user.name, 'AgreesWithMeBot', 'Hey, you seem pretty clever. Maybe contribute to our [github](https://github.com/jhaenchen/agreeswithmebot)?')
						else:
							newComment = parent.reply(quote+agreePhrases[random.randrange(0,len(agreePhrases))]+appendPhrase)
							user = message.author
							r.send_message(user.name, 'AgreesWithMeBot', 'Hey, I sent [your agreement]('+newComment.permalink+'). Just a heads up.')
					elif(isinstance(parent, praw.objects.Submission)):
						parent.add_comment(agreePhrases[random.randrange(0,len(agreePhrases))]+appendPhrase)
						user = message.author
						newComment = parent.reply(quote+agreePhrases[random.randrange(0,len(agreePhrases))]+appendPhrase)
						r.send_message(user.name, 'AgreesWithMeBot', 'Hey, I sent [your agreement]('+newComment.permalink+'). Just a heads up.')
					else:
						message.reply(agreePhrases[random.randrange(0,len(agreePhrases))]+appendPhrase)
				else:
					print("Got message, sending reply")
					quote = generateQuote(message)
					print(quote)
					message.reply(quote+agreePhrases[random.randrange(0,len(agreePhrases))]+appendPhrase)
			message.mark_as_read()
		print("sleeping...")
		time.sleep(15)
	except requests.exceptions.ReadTimeout:
		print("Read timeout. Will try again.")
	except praw.errors.Forbidden:
		print("Im banned from there.")
		user = message.author
		r.send_message(user.name, 'AgreesWithMeBot', 'Hey, I\'m banned from \\r\\'+message.subreddit.display_name+'. Sorry.')
		message.mark_as_read()
	except praw.errors.HTTPException as e:
		pprint(vars(e))	
		print(e)
		print("Http exception. Will try again.")
	except praw.errors.RateLimitExceeded as error:
		print('\tSleeping for %d seconds' % error.sleep_time)
		time.sleep(error.sleep_time)		
	except requests.exceptions.ConnectionError:
		print("ConnectionError. Will try again.")
	except praw.errors.APIException:
		print("API exception. Will try again.")
	except (KeyboardInterrupt, SystemExit):
		print("Safe exit...")
		raise
	except:
		print("Unhandled exception, bail!")
		r.send_message('therealjakeh', 'AgreesWithMeBot', 'Just went down! Help!')
		raise


