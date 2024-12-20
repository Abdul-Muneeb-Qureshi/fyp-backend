from django.urls import path
from .views import ProcessDocumentView , GenerateTopicsEntities , CheckTaskProgress , MostFrequentEntityView

urlpatterns = [
    path('process-document', ProcessDocumentView.as_view(), name='process-document'),
    path('generate_topics_entities', GenerateTopicsEntities.as_view(), name='generate_topics_entities'),
    path('check_task_progress/<str:progress_key>', CheckTaskProgress.as_view(), name='check_task_progress'),
    path('most-frequent-entity-query', MostFrequentEntityView.as_view(), name='most-frequent-entity-query'),



]