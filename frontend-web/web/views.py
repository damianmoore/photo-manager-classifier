from braces import views
from django.views.generic import View

from . import VERSION
from .classify import Classifier


class IndexView(views.CsrfExemptMixin, views.JsonRequestResponseMixin, View):
    def get(self, request, *args, **kwargs):
        return self.render_json_response({'service': 'image_classifier', 'version': VERSION})


class CategoriesView(views.CsrfExemptMixin, views.JsonRequestResponseMixin, View):
    require_json = True

    def get(self, request, *args, **kwargs):
        return self.render_json_response({
            'path': self.request_json['path'],
            'categories': Classifier().classify(self.request_json['path']),
            'version': VERSION,
        })
