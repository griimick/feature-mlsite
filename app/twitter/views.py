from flask import Blueprint, request, render_template
from ..load import processing_results, api
import string
import tweepy

twitter_mod = Blueprint('twitter', __name__, template_folder='templates', static_folder='static')

ascii_chars = set(string.printable)
ascii_chars.remove(' ')
ascii_chars.add('...')

def takeout_non_ascii(s):
    return list(filter(lambda x: x not in ascii_chars, s))

@twitter_mod.route('/twitter', methods=['GET', 'POST'])
def twitter():
    if request.method == 'POST':
        try:
            topic = request.form['topic'].strip()
            if topic == '':
                return render_template('projects/twitter.html', message='Please enter a valid topic')
            text = []
            for tweet in tweepy.Cursor(api.search, topic, lang='hi').items(50):
                temp = ''.join(takeout_non_ascii(tweet.text))
                if not len(temp) in range(3):
                    text.append(temp)
            data, emotion_sents, score, line_sentiment, text, length = processing_results(text)
            return render_template('projects/twitter.html', data=[data, emotion_sents, score, zip(text, line_sentiment), length])

        except Exception:
                return render_template('projects/twitter.html', message='Something went wrong. Please try again.')
    else:
        return render_template('projects/twitter.html')

