from rest_framework import viewsets

from .models import Patient
from .serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        # Users only see and manage the patients they created.
        return Patient.objects.filter(created_by=self.request.user).order_by('id')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
