from rest_framework import serializers

from .models import PatientDoctorMapping


class MappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctorMapping
        fields = ['id', 'patient', 'doctor', 'created_at']

    def validate_patient(self, patient):
        if patient.created_by != self.context['request'].user:
            raise serializers.ValidationError('Patient not found.')
        return patient
