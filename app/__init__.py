from flask import Flask, url_for
from .home.views import home_mod
from .feature.views import feature_mod
import os


app = Flask(__name__, static_folder='static')


app.register_blueprint(home_mod)
app.register_blueprint(feature_mod)


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
