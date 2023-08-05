"""
@file
@brief Machine Learning Post request
"""
import os
import falcon
import numpy
from .data import get_wiki_img
from ..mlapp import MachineLearningPost
from ..args import base642image, image2array


def dummy_application(app=None):
    """
    Defines a dummy application using this API.
    It returns a score produced by a model trained
    on `Iris datasets <http://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html>`_
    and two features.

    @param      app     application, if None, creates one
    @return             app

    .. exref::
        :title: Query a REST API with features

        This example shows how to query a REST API
        by sending a vector of features.
        You can start it by running:

        ::

            start_mlrestapi --name=dummy

        And then query it with:

        ::

            import requests
            import ujson
            features = ujson.dumps({'X': [0.1, 0.2]})
            r = requests.post('http://127.0.0.1:8081', data=features)
            print(r)
            print(r.json())

        It should return:

        ::

            {'Y': [[0.4994216179, 0.4514893599, 0.0490890222]]}
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


def _distance_img(img1, img2, arr1=None):
    """
    Computes the distance between two images.
    The function uses :epkg:`Pillow`.

    @param      img1    reference :epkg:`PIL:Image.Image`
    @param      img2    new image :epkg:`PIL:Image.Image`
    @param      arr1    img1 as an array if available (to avoid converting
                        the same image multiple times)
    @return             distance (in [0, 1]) or list of distances
    """
    arr1 = image2array(img1) if arr1 is None else arr1

    if isinstance(img2, list):
        return [_distance_img(img1, im2, arr1) for im2 in img2]
    else:
        im2 = img2
        if img1.size != im2.size:
            im2 = im2.resize(img1.size)
        if im2.mode != 'RGB':
            im2 = im2.convert('RGB')

        arr2 = image2array(im2)
        # raise Exception("THIS {0}-{1}-{2}".format(im2.size, img1.size, arr1 is None))
        diff = arr1.ravel() - arr2.ravel()
        total = numpy.abs(diff)
        return total.sum() / float(len(total)) / 255


def _distance_img_b64(img1, img2, arr1=None):
    """
    Calls @see fn _distance_img on an image encoded with :epkg:`*pyf:base64`.

    @param      img1    reference :epkg:`PIL:Image.Image`
    @param      img2    new image or list of images encoded with :epkg:`*pyf:base64`
    @param      arr1    img1 as an array if available (to avoid converting
                        the same image multiple times)
    @return             distance (in [0, 1]) or list of distances
    """
    if isinstance(img2, list):
        img2 = [base642image(img) for img in img2]
    else:
        img2 = base642image(img2)
    return _distance_img(img1, img2, arr1)


def dummy_application_image(app=None, options=None):
    """
    Defines a dummy application using this API
    and processing one image. The API ingests
    an image, resizes it to 224x224 and returns
    a distance to an original image from
    subfolder *data*.

    @param      app         application, if None, creates one
    @param      options     if not empty, path to an image
    @return                 app

    .. exref::
        :title: Query a REST API with an image

        This example shows how to query a REST API
        by sending an image.
        You can start it by running:

        ::

            start_mlrestapi --name=dummyimg

        And then query it with:

        ::

            import requests
            import ujson
            from lightmlrestapi.args import image2base64
            img = "path_to_image"
            b64 = image2base64(img)[1]
            features = ujson.dumps({'X': b64})
            r = requests.post('http://127.0.0.1:8081', data=features)
            print(r)
            print(r.json())

        It should return something like:

        ::

            {'distance': [0.21]}
    """
    if options is None or not isinstance(options, str) or len(options) == 0:
        options = get_wiki_img()
    if not os.path.exists(options):
        raise FileNotFoundError("Unable to find image '{0}'.".format(options))
    from PIL import Image
    img_base = Image.open(get_wiki_img())
    if img_base.size != (224, 224):
        img_base = img_base.resize((224, 224))
        if img_base.mode != 'RGB':
            img_base = img_base.convert('RGB')

    if app is None:
        app = falcon.API()
    app.add_route(
        '/', MachineLearningPost(lambda X: _distance_img_b64(img_base, X)))
    return app


def dummy_application_fct(restapi_predict, app=None):
    """
    Defines an application as defined in the tutorial
    :ref:`l-dummy-function-application`.

    @param      restapi_predict     predict function
    @param      app                 application, if None, creates one
    """
    if app is None:
        app = falcon.API()
    app.add_route(
        '/', MachineLearningPost(lambda X: restapi_predict))
    return app


def dummy_application_neighbors(app=None):
    """
    Defines a dummy application using this API.
    It returns a list of neighbors with a score
    on `Iris datasets <http://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html>`_.

    @param      app     application, if None, creates one
    @return             app

    .. exref::
        :title: Query a REST API with an image and get neighbors

        A previous example shows how to send an image,
        this one illustrates a result which is a classifier result
        neither a regressor one but neighbors.
        You can start it by running:

        ::

            start_mlrestapi --name=dummyknn

        And then query it with:

        ::

            import requests
            import ujson
            features = ujson.dumps({'X': [0.1, 0.2]})
            r = requests.post('http://127.0.0.1:8081', data=features)
            print(r)
            print(r.json())

        It should return:

        ::

            {'Y': [[[41, 4.8754486973], [13, 5.0477717856], [8, 5.0774009099], [38, 5.1312766443], [60, 5.2201532545]]]}
    """
    from sklearn import datasets
    from sklearn.neighbors import NearestNeighbors
    iris = datasets.load_iris()
    X = iris.data[:, :2]  # we only take the first two features.
    knn = NearestNeighbors(n_neighbors=5)
    knn.fit(X)

    def to_serie(x):
        dist, ind = knn.kneighbors(x)
        res = []
        for i in range(0, len(x)):
            res.append([(int(j), float(s))
                        for j, s in zip(ind[i, :], dist[i, :])])
        return res

    if app is None:
        app = falcon.API()
    app.add_route(
        '/', MachineLearningPost(lambda x: to_serie(x)))
    return app


def dummy_application_neighbors_image(app=None, options=None):
    """
    Defines a dummy application using this API.
    It returns a list of one neighbor for an image
    and metadata (random).

    @param      app         application, if None, creates one
    @param      options     if not empty, path to an image
    @return                 app

    You can start it by running:

    ::

        start_mlrestapi --name=dummyknnimg

    And then query it with:

    ::

        import requests
        import ujson
        from lightmlrestapi.args import image2base64
        img = "path_to_image"
        b64 = image2base64(img)[1]
        features = ujson.dumps({'X': b64})
        r = requests.post('http://127.0.0.1:8081', data=features)
        print(r)
        print(r.json())

    It should return:

    ::

        {'Y': [[[41, 4.8754486973, {'name': 'wiki.png', description='something'}]]]}
    """
    if options is None or not isinstance(options, str) or len(options) == 0:
        options = get_wiki_img()
    if not os.path.exists(options):
        raise FileNotFoundError("Unable to find image '{0}'.".format(options))
    from PIL import Image
    img_base = Image.open(get_wiki_img())
    if img_base.size != (224, 224):
        img_base = img_base.resize((224, 224))
        if img_base.mode != 'RGB':
            img_base = img_base.convert('RGB')

    def mypredict(X):
        res = _distance_img_b64(img_base, X)
        final = []
        for r, x in zip(res, X):
            final.append([(0, r, dict(name=os.path.split(options)[1],
                                      description="image from wikipedia"))])
        return final

    if app is None:
        app = falcon.API()
    app.add_route(
        '/', MachineLearningPost(mypredict))
    return app
