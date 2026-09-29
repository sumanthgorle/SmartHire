from rest_framework import serializers
from .models import Resume


class ResumeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resume
        fields = [
            'id',
            'candidate',
            'resume_file',
            'uploaded_at',
            'extracted_text',
            'skills'
        ]