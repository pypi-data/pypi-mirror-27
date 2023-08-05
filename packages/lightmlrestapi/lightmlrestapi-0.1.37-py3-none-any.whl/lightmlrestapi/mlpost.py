"""
@file
@brief Machine Learning Post request
"""
import ujson
import falcon


class MachineLearningPost(object):
    """
    Implements a post request, no authentification
    is required. The model ingests a vector *X*
    and outputs another one or a number *Y*.
    """

    def __init__(self, predict_function):
        """
        @param      predict_function    predict function
        """
        self._predict = predict_function

    def on_post(self, req, resp):
        """
        @param      req         request
        @param      resp        ...
        """
        # To get the parameters
        # req.get_params
        js = req.stream.read()
        args = ujson.loads(js)
        X = args["X"]
        try:
            res = self._predict([X])
        except Exception as e:
            raise falcon.HTTPBadRequest('Unable to predict', str(e))

        resp.status = falcon.HTTP_201
        resp.body = ujson.dumps({"Y": res})

    @staticmethod
    def dummy_application(app=None):
        """
        Defines a dummy application using this API.

        @param      app     application, if None, creates one
        @return             app
        """
        from sklearn import datasets
        from sklearn.linear_model import LogisticRegression

        iris = datasets.load_iris()
        X = iris.data[:, :2]  # we only take the first two features.
        y = iris.target
        clf = LogisticRegression()
        clf.fit(X, y)

        if app is None:
            app = falcon.API()
        app.add_route('/', MachineLearningPost(clf.predict_proba))
        return app
