from django.urls import path

from .views import IndexView, AddMarkView

app_name = 'marks'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('groups/<int:pk>/subjects/<int:sub_pk>/', AddMarkView.as_view(), name='addmark')
]
