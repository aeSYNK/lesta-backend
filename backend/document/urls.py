from django.urls import path
from .views import UploadDocumentView, ResultsView

urlpatterns = [
    path('', UploadDocumentView.as_view(), name='upload'),
    path('results/<int:doc_id>/', ResultsView.as_view(), name='results'),
]