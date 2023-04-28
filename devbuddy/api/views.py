from urllib import response
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ReviewSerializer

# Create your views here.
@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/user/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an active user'
        }
    ]
    return Response(routes)