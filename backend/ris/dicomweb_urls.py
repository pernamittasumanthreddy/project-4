from django.urls import path
from ris.views import DICOMWebView

urlpatterns = [
    path('studies/', DICOMWebView.as_view(), name='dicomweb-studies'),
    path('studies/<str:study_uid>/metadata/', DICOMWebView.as_view(), {'action': 'metadata'}, name='dicomweb-metadata'),
    path('studies/<str:study_uid>/metadata', DICOMWebView.as_view(), {'action': 'metadata'}),
    path('studies/<str:study_uid>/series/<str:series_uid>/instances/<str:instance_uid>/', DICOMWebView.as_view(), name='dicomweb-instance'),
    path('studies/<str:study_uid>/series/<str:series_uid>/instances/<str:instance_uid>', DICOMWebView.as_view()),
    path('studies/<str:study_uid>/series/<str:series_uid>/instances/<str:instance_uid>/<str:action>/', DICOMWebView.as_view(), name='dicomweb-instance-action'),
    path('studies/<str:study_uid>/series/<str:series_uid>/instances/<str:instance_uid>/<str:action>', DICOMWebView.as_view()),
]
