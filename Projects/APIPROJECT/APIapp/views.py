from django.shortcuts import render
from rest_framework.response import Response
from .serializer import *
from .models import *
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(['GET'])
def getall(request):
    stdata = studinfo.objects.all()
    serial = studinfoSerializer(stdata, many=True)
    return Response(serial.data)

@api_view(['GET'])
def getsingle(request, id):
    try:
        stdata = studinfo.objects.get(id=id)
    except studinfo.DoesNotExist:
        return Response({"error": "Data not found"}, status=status.HTTP_404_NOT_FOUND)
    serial = studinfoSerializer(stdata)
    return Response(serial.data)

@api_view(['POST'])
def postdata(request):
    serial = studinfoSerializer(data=request.data)
    if serial.is_valid():
        serial.save()
        return Response(serial.data, status=status.HTTP_201_CREATED)
    return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def updatedata(request, id):
    try:
        stdata = studinfo.objects.get(id=id)
    except studinfo.DoesNotExist:
        return Response({"error": "Data not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serial = studinfoSerializer(stdata, data=request.data, partial=(request.method == 'PATCH'))
    if serial.is_valid():
        serial.save()
        return Response(serial.data)
    return Response(serial.errors, status=status.HTTP_202_ACCEPTED)

@api_view(['DELETE'])
def deletedata(request, id):
    try:
        stdata = studinfo.objects.get(id=id)
        stdata.delete()
        return Response({"message": "Data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except studinfo.DoesNotExist:
        return Response({"error": "Data not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def api_root(request):
    return Response({
        "message": "Welcome to the Student Info API",
        "endpoints": {
            "getall": "/getall/",
            "getsingle": "/getsingle/<int:id>/",
            "postdata": "/postdata/",
            "updatedata": "/updatedata/<int:id>/",
            "deletedata": "/deletedata/<int:id>/"
        }
    })

