from django.shortcuts import render

from django.http import HttpResponse

def doctor_list(request):
    return HttpResponse("Doctor List")

def doctor_detail(request, pk):
    return HttpResponse(f"Doctor Detail {pk}")

def doctor_search(request):
    return HttpResponse("Doctor Search")
