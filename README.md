# AtoML App

[![Maintainability](https://api.codeclimate.com/v1/badges/d0aa66af28e0076b14f7/maintainability)](https://codeclimate.com/github/pcjennings/flask_AtoML/maintainability)

The backend for AtoML. It assumes that a model has been optimized and saved previously.

To run the app, use:

```shell
  $ export FLASK_APP=run_atoml.py
  $ flask run
```

To make the app publicly visible, use:

```shell
  $ flask run --host=0.0.0.0
```

### Requirements

*   numpy
*   mendeleev
