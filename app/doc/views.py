from flask import Blueprint, request, render_template, flash, redirect
from ..load import processing_results
from werkzeug.utils import secure_filename
import os
import gc
import resource

doc_mod = Blueprint('doc', __name__, template_folder='templates', static_folder='static')

UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = {'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@doc_mod.route('/doc', methods=['GET', 'POST'])
def doc():
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                flash('File Upload failed. Please retry.')
                return render_template('projects/doc.html')
            file = request.files['file']
            if file.filename == '':
                flash('No file selected to upload')
                return render_template('projects/doc.html')
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                if not os.path.exists(UPLOAD_FOLDER):
                    os.mkdir(UPLOAD_FOLDER)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
            with open('./uploads/' + filename) as f:
                query = f.read()

            text = query.split('.')[:-1]
            if len(text) == 0:
                return render_template('projects/doc.html', message='Please separate each line with "." in the file')

            data, emotion_sents, score, line_sentiment, text, length = processing_results(text)

            return render_template('projects/doc.html', data=[data, emotion_sents, score, zip(text, line_sentiment), length])
        except UnicodeDecodeError:
            flash('Only UTF Encoded Files supported. Please try again.')
            return render_template('projects/doc.html')
        except Exception:
            flash('Something went wrong. Please try again.')
            return render_template('projects/doc.html')
    else:
        return render_template('projects/doc.html')
