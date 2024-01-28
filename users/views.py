from rest_framework.views import APIView
from rest_framework import response,status
from rest_framework.permissions import IsAuthenticated
from .models import User  
import json

