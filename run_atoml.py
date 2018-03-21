"""Flask app for AtoML-CatApp model."""
import pickle
import flask
from flask_cors import CORS

from featurize.feature_generator import return_features

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
    with open('models/gp_model_01.pickle', 'rb') as modelfile:
        model = pickle.load(modelfile)
    return model


def _get_output(data):
    """Make the prediction on the input system."""
    # Load the GP model.
    model = _get_model()

    # Load the features for the test system.
    features = return_features(data)

    # Make the predictions.
    pred = model.predict(test_fp=features, uncertainty=True)
    result = {'energy': round(pred['prediction'][0], 3),
              'uncertainty': round(pred['uncertainty'][0], 3)}

    return list(features), result
