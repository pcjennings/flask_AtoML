Flask AtoML

The backend for AtoML. It assumes that a model has been optimized and saved
previously.

To test you can type something like:

    export FLASK_APP=app.py
    flask run --host=0.0.0.0

    curl -H "Content-type: application/json" -X POST http://127.0.0.1:5000/ -d '{"m1": "Fe", "m2": "Fe", "facet": "110", "a": "CO", "conc": "0.5", "site": "BA"}'

It is also easy to test using something like [react console](restconsole.com).
