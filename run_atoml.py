"""Flask app for AtoML-CatApp model."""
import pickle
import flask
from flask_cors import CORS
import numpy as np

from featurize.catapp_user import return_features

app = flask.Flask(__name__)
CORS(app)


@app.route('/', methods=['GET', 'POST'])
def run_atoml_app():
    """The actual app to predict and generate output."""
    data = flask.request.json
    features, output = _get_output(data)
    return_dict = {'input': data, 'features': features, 'output': output}
    return_dict = flask.jsonify(**return_dict)

    return return_dict


def _get_model():
    """Load the generated model."""
    with open('models/catapp_gp_model.pickle', 'rb') as modelfile:
        model = pickle.load(modelfile)
    return model


def _get_output(data):
    """Make the prediction on the input system."""
    # Load the GP model.
    model = _get_model()

    # Load the features for the test system.
    features = np.array([return_features(data)])
    features = np.delete(features, [28, 33, 50, 55, 19], axis=1).tolist()

    # Make the predictions.
    pred = model.predict(test_fp=features, uncertainty=True)
    result = {'energy': round(float(pred['prediction'][0]), 3),
              'uncertainty': round(float(pred['uncertainty'][0]), 3)}

    return features, result
