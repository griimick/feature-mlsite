from flask import Blueprint, request, render_template
from ..load import processing_results
from ..abbr import get_abbr_map

abbr_map = get_abbr_map()
liner_mod = Blueprint('liner', __name__, template_folder='templates', static_folder='static')


@liner_mod.route('/liner', methods=['GET', 'POST'])
def liner():
    if request.method == 'POST':
        query = request.form['liner-text']
        text = query.split('.')[:-1]
        if len(text) == 0:
            return render_template('projects/line.html', message='Please separate each line with "."')

        abbr_expanded_text = ""
        for word in query.split():
            if word in abbr_map:
                abbr_expanded_text += abbr_map[word]
            else:
                abbr_expanded_text += word
            abbr_expanded_text += " " 

        data, emotion_sents, score, line_sentiment, text, length = processing_results(text)
        return render_template('projects/line.html', data=[data, emotion_sents, score, zip(text, line_sentiment), length, abbr_expanded_text])
    else:
        return render_template('projects/line.html')
