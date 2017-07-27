from flask import Blueprint, request, jsonify, render_template
from ..parser import parseText

feature_mod = Blueprint('feature', __name__, template_folder='templates', static_folder='static')

@feature_mod.route('/feature', methods=['GET', 'POST'])
def feature():
    if request.method == 'POST':
        query = request.form['liner-text']
        if query is not None:
        	parsedOutput, featureNames, sentimentNames, catalystNames, negativeNames, featureSent, sentList, negSent, catSent= parseText(query)
        	
        	scores={}
        	for sentiment in sentimentNames:
        		if sentiment in sentList:
        			scores[sentiment]=sentList[sentiment]
        		else:
        			scores[sentiment] = ['0.12','0.5']

        	scores['बहुत'] = ['1.5']

        	print(featureSent)
        	print(negSent)
        	print(catSent)

        return render_template('projects/feature.html', data=[query, featureNames, sentimentNames, featureSent, parsedOutput, catalystNames, negativeNames, scores, negSent, catSent])
    else:
        return render_template('projects/feature.html')