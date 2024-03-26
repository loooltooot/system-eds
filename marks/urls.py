from django.urls import path

from .views import IndexView

app_name = 'marks'
urlpatterns = [
    path('', IndexView.as_view(), name='index')
]
