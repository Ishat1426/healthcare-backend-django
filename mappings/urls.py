from django.urls import path

from .views import MappingDetailView, MappingListCreateView

urlpatterns = [
    path('', MappingListCreateView.as_view()),
    path('<int:pk>/', MappingDetailView.as_view()),
]
