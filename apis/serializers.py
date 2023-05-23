from rest_framework import serializers
from .models import Blog


class StressLevelInputSerializer(serializers.Serializer):
    anxiety_level = serializers.IntegerField()
    self_esteem = serializers.IntegerField()
    mental_health_history = serializers.IntegerField()
    depression = serializers.IntegerField()

    headache = serializers.IntegerField()
    blood_pressure = serializers.IntegerField()
    sleep_quality = serializers.IntegerField()
    breathing_problem = serializers.IntegerField()

    noise_level = serializers.IntegerField()
    living_conditions = serializers.IntegerField()
    safety = serializers.IntegerField()
    basic_needs = serializers.IntegerField()

    academic_performance = serializers.IntegerField()
    study_load = serializers.IntegerField()
    teacher_student_relationship = serializers.IntegerField()
    future_career_concerns = serializers.IntegerField()

    social_support = serializers.IntegerField()
    peer_pressure = serializers.IntegerField()
    extracurricular_activities = serializers.IntegerField()
    bullying = serializers.IntegerField()

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model= Blog
        fields = '__all__'