from urllib import response
from django.shortcuts import render
import io
from rest_framework.parsers import JSONParser
from .models import Person
from .serializers import PersonSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
# Create your views here.
def person_api(request):
    if request.method == 'GET':
        json_data = request.body
        # print(request.body)
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        # print(pythondata.get('id', None))
        id = pythondata.get('id', None)
        if pythondata.get('id',None):
            per = Person.objects.get(id = id)
            serializer = PersonSerializer(per)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type = 'application/json')

        per = Person.objects.all()
        serializer = PersonSerializer(per, many= True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type = 'application/json')

    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        serializer = PersonSerializer(data= pythondata)
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'Data Created'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type = 'application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type = 'application/json')

    if request.method == 'PUT':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        per = Person.objects.get(id= id)
        serializer = PersonSerializer(per, data= pythondata, partial = True)
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'Data Updated!!'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type = 'application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type = 'application/json')                 

    if request.method == 'DELETE':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        per = Person.objects.get(id = id)
        per.delete()
        res = {'msg': 'Data Deleted!!'}
        # json_data = JSONRenderer().render(res)
        # return HttpResponse(json_data, content_type = 'application/json')
        return JsonResponse(res, safe = False)
    




