import numpy as np
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
from collections import Counter
import tweepy
import boto3.session
import _pickle
import h5py
import gc


session = boto3.session.Session(region_name='ap-south-1')
s3client = session.client('s3', config=boto3.session.Config(signature_version='s3v4', region_name='ap-south-1'),
                          aws_access_key_id='**',
                          aws_secret_access_key='**+T')


def most_common(lst):
    return max(set(lst), key=lst.count)


def load_from_s3(str):
    response = s3client.get_object(Bucket='mlsite-bucket', Key=str)
    body = response['Body']
    if '.h5' in str:
        f = open(body, 'rb')
        h = h5py.File(f, 'r')
        detector = load_model(h)
    else:
        detector = _pickle.loads(body.read())
    return detector


def load_offline(str):
    with open(str, 'rb') as f:
        dump = _pickle.load(f)
    return dump


word2index = load_offline('app/static/models/word2index.pkl')
vectorizer = load_offline('app/static/models/vectorizer.pkl')


def init_model():
    lstm_model = load_model('app/static/models/lstm.h5')
    cnn_model = load_model('app/static/models/cnn.h5')
    cnn_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    lstm_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    graph = tf.get_default_graph()
    return lstm_model, cnn_model, graph


lmodel, cnn, graph = init_model()
logistic = load_offline('app/static/models/logisticreg.pkl')
adaboost = load_offline('app/static/models/adaboost.pkl')
bernoulli = load_offline('app/static/models/bernoullinb.pkl')
decisiontree = load_offline('app/static/models/decisiontree.pkl')
gradientboost = load_offline('app/static/models/gradientboost.pkl')
knn = load_offline('app/static/models/knn.pkl')
randomforest = load_offline('app/static/models/randomforest.pkl')
multinomialnb = load_offline('app/static/models/multinomialnb.pkl')
svm10 = load_offline('app/static/models/svm10.pkl')

auth = tweepy.OAuthHandler('hXJ8TwQzVya3yYwQN1GNvGNNp', 'diX9CFVOOfWNli2KTAYY13vZVJgw1sYlEeOTxsLsEb2x73oI8S')
auth.set_access_token('2155329456-53H1M9QKqlQbEkLExgVgkeallweZ9N74Aigm9Kh',
                      'waDPwamuPkYHFLdVNZ5YF2SNWuYfGHDVFue6bEbEGjTZb')

api = tweepy.API(auth)


def clean(query):
    return vectorizer.transform([query])


# def pencode(text):
#     vector = np.zeros(12429)
#     for i, word in enumerate(text.split(' ')):
#         try:
#             vector[word2index[word]] = 1
#         except KeyError:
#             vector[i] = 0
#     return vector


def lencode(text):
    vector = []
    for word in text.split(' '):
        try:
            vector.append(word2index[word])
        except KeyError:
            vector.append(0)
    padded_seq = pad_sequences([vector], maxlen=100, value=0.)
    return padded_seq


def word_feats(text):
    return dict([(word, True) for word in text.split(' ')])


def predictor(query):
    clean_query = clean(query)
    ada = adaboost.predict(clean_query)
    ber = bernoulli.predict(clean_query)
    lg = logistic.predict(clean_query)
    dt = decisiontree.predict(clean_query)
    gb = gradientboost.predict(clean_query.toarray())
    knnp = knn.predict(clean_query)
    rf = randomforest.predict(clean_query)
    mnb = multinomialnb.predict(clean_query)
    svm = svm10.predict(clean_query)

    with graph.as_default():
        lout = lmodel.predict(lencode(query))
        cnn_out = cnn.predict(lencode(query))
        lout = np.argmax(lout, axis=1)
        cnn_out = np.argmax(cnn_out, axis=1)

    return [ada.tolist()[0],
            ber.tolist()[0],
            dt.tolist()[0],
            gb.tolist()[0],
            knnp.tolist()[0],
            rf.tolist()[0],
            mnb.tolist()[0],
            lg.tolist()[0],
            svm.tolist()[0],
            lout.tolist()[0],
            cnn_out.tolist()[0]]


def get_most_count(x):
    return Counter(x).most_common()[0][0]


def processing_results(query):
    predict_list = []
    line_sentiment = []
    for t in query:
        p = predictor(t)
        line_sentiment.append(most_common(p))
        predict_list.append(p)

    data = {'AdaBoost': 0,
            'BernoulliNB': 0,
            'DecisionTree': 0,
            'GradientBoost': 0,
            'KNNeighbors': 0,
            'RandomForest': 0,
            'MultinomialNB': 0,
            'Logistic Regression': 0,
            'SVM': 0,
            'LSTM network': 0,
            'Convolutional Neural Network': 0}

    # overal per sentence
    predict_list = np.array(predict_list)
    i = 0
    for key in data:

        data[key] = get_most_count(predict_list[:, i])
        i += 1

    # all the sentences with 3 emotions
    predict_list = predict_list.tolist()
    emotion_sents = [0, 0, 0]
    for p in predict_list:
        if most_common(p) == 0:
            emotion_sents[0] += 1
        elif most_common(p) == 1:
            emotion_sents[1] += 1
        else:
            emotion_sents[2] += 1

    # overall score
    score = most_common(list(data.values()))
    gc.collect()
    return data, emotion_sents, score, line_sentiment, query, len(query)
