"""Flask app for AtoML-CatApp model."""
import flask
import pickle
import numpy as np

from feature_generator import return_features

app = flask.Flask(__name__)


def get_input():
    """Define some static input for now."""
    d = {"m1": "Fe", "m2": "Fe", "facet": "110", "a": "CO", "conc": "0.5",
         "site": "AA"}
    return d


def get_model():
    """Load the generated model."""
    with open('gp_model_01.pickle', 'rb') as modelfile:
        model = pickle.load(modelfile)
    return model


def get_test_features(data):
    """Get the features for the input system."""
    inp = data  # get_input()
    return return_features(inp)


def get_output(data):
    """Make the prediction on the input system."""
    # Load the GP model.
    m = get_model()

    # Load the features for the test system.
    f = get_test_features(data)

    # Some global scaling data generated previously.
    scale_mean = np.asarray([2.57943925e+00, 1.87096963e+01, 8.80782710e+00,
                             1.39537967e+01, 1.75185613e+01, 2.23380634e+03,
                             2.99258991e+03, 2.04580280e+00, 1.58569306e+01,
                             6.83456600e+00, 2.10063668e+02, 8.91793224e+01,
                             3.95560748e+00, 1.75185613e+01, 6.10750673e+02,
                             4.87266355e+00, 1.01010514e+01, 4.72394860e+01,
                             9.88540304e+00, 1.11431143e+02, 1.63905960e+03,
                             3.18376748e+03, 1.17250626e+01, 5.35834054e+01,
                             3.67766355e+00, 2.07273364e+02, 1.38686332e+02,
                             1.98573014e+00, 1.11431143e+02, 4.16504626e+02,
                             4.86448598e+00, 9.56396028e+00, 4.64748832e+01,
                             1.13403914e+01, 1.09926375e+02, 1.65625103e+03,
                             3.28646982e+03, 1.04671682e+01, 6.46498832e+01,
                             3.78560164e+00, 2.09147196e+02, 1.43499416e+02,
                             1.89936332e+00, 1.09926375e+02, 4.31663672e+02,
                             7.02978972e-01, 5.76810748e+00, 2.02278037e+00,
                             9.73714953e+00, 1.96650117e+01, 9.37143692e+01,
                             2.12257944e+01, 2.21357518e+02, 3.29531064e+03,
                             6.47023730e+03, 2.21922307e+01, 1.18233289e+02,
                             7.46326519e+00, 4.16420561e+02, 2.82185748e+02,
                             3.88509346e+00, 2.21357518e+02, 8.48168298e+02],
                            np.float64)

    scale_dif = np.asarray([1.20000000e+01, 3.60000000e+01, 2.00000000e+01,
                            1.23400000e+02, 3.20860000e+01, 1.15172800e+04,
                            1.53720500e+04, 6.29600000e+00, 9.24068594e+01,
                            3.71400000e+01, 1.23800000e+03, 4.01000000e+02,
                            2.27000000e+01, 3.20860000e+01, 3.64536500e+03,
                            3.00000000e+00, 1.25000000e+01, 7.00000000e+01,
                            1.59000000e+01, 1.81998862e+02, 3.44572000e+03,
                            5.30027000e+03, 1.98711000e+01, 1.80200000e+02,
                            6.38000000e+00, 5.90000000e+01, 8.80000000e+01,
                            1.30000000e+00, 1.81998862e+02, 7.89620000e+02,
                            4.00000000e+00, 1.35000000e+01, 7.50000000e+01,
                            1.59000000e+01, 1.92981400e+02, 3.62520000e+03,
                            5.83981000e+03, 2.14210000e+01, 2.04760000e+02,
                            6.38000000e+00, 9.10000000e+01, 1.41000000e+02,
                            2.34000000e+00, 1.92981400e+02, 7.89620000e+02,
                            2.50000000e-01, 7.00000000e+00, 2.00000000e+00,
                            6.00000000e+00, 2.50000000e+01, 1.40000000e+02,
                            3.18000000e+01, 3.63997723e+02, 6.75414000e+03,
                            1.05898100e+04, 3.96700000e+01, 3.75960000e+02,
                            1.27600000e+01, 1.33000000e+02, 2.26000000e+02,
                            2.89000000e+00, 3.63997723e+02, 1.47840000e+03],
                           np.float64)

    # Scale the test features.
    tfp = (np.array([f], np.float64) - scale_mean) / scale_dif

    # Make the predictions.
    pred = m.predict(test_fp=tfp, uncertainty=True)
    result = [pred['prediction'][0], pred['uncertainty'][0]]

    return list(f), result


@app.route('/', methods=['GET', 'POST'])
def run_atoml_app():
    """The actual app to predict and generate output."""
    # data = get_input()
    if flask.request.headers['Content-Type'] == 'application/json':
        data = flask.request.json
    features, output = get_output(data)
    return_dict = {'input': data, 'features': features, 'output': output}
    return_dict = flask.jsonify(**return_dict)

    return return_dict

# To test you can type:

# export FLASK_APP=app.py
# flask run --host=0.0.0.0

# curl -H "Content-type: application/json" -X POST http://127.0.0.1:5000/ -d
# '{"m1": "Fe", "m2": "Fe", "facet": "110", "a": "CO", "conc": "0.5", "site":
# "BA"}'
