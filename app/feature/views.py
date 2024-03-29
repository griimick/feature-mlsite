from flask import Blueprint, request, jsonify, render_template
from ..parser import parseText,featurePolarity
from ..abbr import get_abbr_map

abbr_map = get_abbr_map()
feature_mod = Blueprint('feature', __name__, template_folder='templates', static_folder='static')

@feature_mod.route('/aspect-based', methods=['GET', 'POST'])
def feature():
    try:
        if request.method == 'POST':
            queryDoc = request.form['liner-text']
            abbr_expanded_text = ""

            for word in queryDoc.split():
                if word in abbr_map:
                    abbr_expanded_text += abbr_map[word]
                else:
                    abbr_expanded_text += word
                abbr_expanded_text += " " 

            queries = queryDoc.split('।')
            featureNames = []
            sentimentNames = []
            catalystNames = []
            negativeNames = []

            sentFeature = []
            negSent = []
            catSent = []

            polarityFeature = []
            scores = []

            parsedOutput = []

            dataRender = []
            count = []

            if queries is not None:
                queries.pop()
                print(len(queries))
                c =0;
                for query in queries:
                    print(query)
                    c = c+1
                    parsedOutputQ, scoreListQ, namesListQ, relationListQ = parseText(query)
                    
                    featureNames.append(namesListQ[0])
                    sentimentNames.append(namesListQ[1])
                    catalystNames.append(namesListQ[2])
                    negativeNames.append(namesListQ[3])
                
                    sentFeature.append(relationListQ[0])
                    negSent.append(relationListQ[1])
                    catSent.append(relationListQ[2])

                    polarityFeatureQ, scoresQ= featurePolarity(scoreListQ, namesListQ, relationListQ, parsedOutputQ)
                    
                    polarityFeature.append(polarityFeatureQ)
                    scores.append(scoresQ)
                    parsedOutput.append(parsedOutputQ)
                    count.append(c)
                    print(scoresQ)
                    print(polarityFeatureQ)
                    # print(negSent)
                    # print(catSent)
                    dataQ = [query, namesListQ[0], namesListQ[1], relationListQ[0], parsedOutputQ, namesListQ[2], namesListQ[3], scoresQ, relationListQ[1], relationListQ[2]]
                    dataRender.append(dataQ)

            return render_template('projects/feature.html', scores = scores ,outputs = polarityFeature, datas=dataRender, zip = zip(count,scores,polarityFeature, dataRender), queryDoc = queryDoc, abbr = abbr_expanded_text)
        else:
            return render_template('projects/feature.html')
    except Exception:
        return render_template('projects/feature.html', message='Something went wrong. Please try again.')
