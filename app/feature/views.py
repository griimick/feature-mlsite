from flask import Blueprint, request, jsonify, render_template
from ..parser import parseText,featurePolarity

feature_mod = Blueprint('feature', __name__, template_folder='templates', static_folder='static')

@feature_mod.route('/feature', methods=['GET', 'POST'])
def feature():
    if request.method == 'POST':
        query = request.form['liner-text']
        if query is not None:
            parsedOutput, scoreList, namesList, relationList= parseText(query)

            featureNames = namesList[0]
            sentimentNames = namesList[1]
            catalystNames = namesList[2]
            negativeNames = namesList[3]
            
            sentFeature = relationList[0]
            negSent = relationList[1]
            catSent = relationList[2]

            polarityFeature, scores= featurePolarity(scoreList, namesList, relationList, parsedOutput)
            #print(scores)
            # print(featureSent)
            # print(negSent)
            # print(catSent)

        return render_template('projects/feature.html', data=[query, featureNames, sentimentNames, sentFeature, parsedOutput, catalystNames, negativeNames, scores, negSent, catSent])
    else:
        return render_template('projects/feature.html')