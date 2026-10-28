from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from doctors.serializers import DoctorSerializer
from patients.models import Patient

from .models import PatientDoctorMapping
from .serializers import MappingSerializer


def user_mappings(user):
    return PatientDoctorMapping.objects.filter(patient__created_by=user)


class MappingListCreateView(generics.ListCreateAPIView):
    serializer_class = MappingSerializer

    def get_queryset(self):
        return user_mappings(self.request.user).order_by('id')


class MappingDetailView(APIView):
    def get(self, request, pk):
        # Here pk is a patient id: return the doctors assigned to that patient.
        patient = get_object_or_404(Patient, pk=pk, created_by=request.user)
        mappings = patient.mappings.select_related('doctor').order_by('id')
        return Response(DoctorSerializer([m.doctor for m in mappings], many=True).data)

    def delete(self, request, pk):
        # Here pk is a mapping id.
        mapping = get_object_or_404(user_mappings(request.user), pk=pk)
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
