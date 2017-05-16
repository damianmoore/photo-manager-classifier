import json
import os

from caffe2.python import workspace
from django.conf import settings
import numpy as np
import skimage.io
import skimage.transform


CAFFE_MODELS = '/usr/local/caffe2/python/models'
CATEGORY_CODES = os.path.join(settings.BASE_DIR, 'data', 'alexnet_codes.json')


class Classifier(object):
    # Based on code from this tutorial:
    # https://github.com/caffe2/caffe2/blob/master/caffe2/python/tutorials/Loading_Pretrained_Models.ipynb

    code_table = {}
    model = None
    mean = None
    init_net = None
    predict_net = None

    def __init__(self):
        if not self.code_table:
            with open(CATEGORY_CODES) as codes:
                self.code_table = {int(k): v for k, v in json.loads(codes.read()).items()}

        caffe_models = os.path.expanduser(CAFFE_MODELS)
        model = 'squeezenet', 'init_net.pb', 'predict_net.pb', 'ilsvrc_2012_mean.npy', 227
        self.model = model

        mean_file = os.path.join(caffe_models, model[0], model[3])
        if not os.path.exists(mean_file):
            self.mean = 128
        else:
            mean = np.load(mean_file).mean(1).mean(1)
            self.mean = mean[:, np.newaxis, np.newaxis]

        init_net = os.path.join(caffe_models, model[0], model[1])
        predict_net = os.path.join(caffe_models, model[0], model[2])

        with open(init_net) as f:
            self.init_net = f.read()
        with open(predict_net) as f:
            self.predict_net = f.read()

    def get_category_from_code(self, code):
        return self.code_table.get(code, None)

    def crop_center(self, img, cropx, cropy):
        y, x, c = img.shape
        startx = x // 2 - (cropx // 2)
        starty = y // 2 - (cropy // 2)
        return img[starty:starty + cropy, startx:startx + cropx]

    def rescale(self, img, input_height, input_width):
        aspect = img.shape[1] / float(img.shape[0])
        if (aspect > 1):
            res = int(aspect * input_height)
            imgScaled = skimage.transform.resize(img, (input_width, res))
        if (aspect < 1):
            res = int(input_width / aspect)
            imgScaled = skimage.transform.resize(img, (res, input_height))
        if(aspect == 1):
            imgScaled = skimage.transform.resize(img, (input_width, input_height))
        return imgScaled

    def classify(self, path):
        input_image_size = self.model[4]

        img = skimage.img_as_float(skimage.io.imread(path)).astype(np.float32)
        img = self.rescale(img, input_image_size, input_image_size)
        img = self.crop_center(img, input_image_size, input_image_size)

        img = img.swapaxes(1, 2).swapaxes(0, 1)
        img = img[(2, 1, 0), :, :]
        img = img * 255 - self.mean

        img = img[np.newaxis, :, :, :].astype(np.float32)

        p = workspace.Predictor(self.init_net, self.predict_net)

        results = p.run([img])
        results = np.asarray(results)

        results = np.delete(results, 1)
        filtered_results = []

        for i, r in enumerate(results):
            if (float(r) > 0.01):
                filtered_results.append((self.get_category_from_code(i + 1), float(r)))

        return sorted(filtered_results, key=lambda result: result[1], reverse=True)
