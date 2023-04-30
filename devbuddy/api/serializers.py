from rest_framework.serializers import ModelSerializer
from base.models import User, Team, Project

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
        
class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'