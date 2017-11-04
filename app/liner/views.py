from flask import Blueprint, request, render_template
from ..load import processing_results

liner_mod = Blueprint('liner', __name__, template_folder='templates', static_folder='static')


@liner_mod.route('/liner', methods=['GET', 'POST'])
def liner():
    if request.method == 'POST':
        query = request.form['liner-text']
        text = query.split('.')[:-1]
        if len(text) == 0:
            return render_template('projects/line.html', message='Please separate each line with "."')

        data, emotion_sents, score, line_sentiment, text, length = processing_results(text)
        return render_template('projects/line.html', data=[data, emotion_sents, score, zip(text, line_sentiment), length])
    else:
        return render_template('projects/line.html')
