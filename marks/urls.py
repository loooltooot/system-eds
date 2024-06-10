from django.urls import path

from .views import IndexView, AddMarkView, ShowMarksView, EditMarkView

app_name = 'marks'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('appointments/<int:pk>/', ShowMarksView.as_view(), name='show'),
    path('appointments/<int:pk>/addmark/', AddMarkView.as_view(), name='addmark'),
    path('appointments/<int:pk>/editmark/', EditMarkView.as_view(), name='editmark'),
]