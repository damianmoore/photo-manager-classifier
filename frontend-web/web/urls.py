from django.conf.urls import url

from .views import IndexView, CategoriesView


urlpatterns = [
    url(r'^categories', CategoriesView.as_view()),
    url(r'^', IndexView.as_view()),
]
