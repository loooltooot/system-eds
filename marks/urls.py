from django.urls import path

from .views import IndexView, AddMarkView, ShowMarksView, EditMarkView

app_name = 'marks'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('groups/<int:pk>/subjects/<int:sub_pk>/', ShowMarksView.as_view(), name='show'),
    path('groups/<int:pk>/subjects/<int:sub_pk>/addmark/', AddMarkView.as_view(), name='addmark'),
    path('groups/<int:pk>/subjects/<int:sub_pk>/editmark/', EditMarkView.as_view(), name='editmark'),
]
