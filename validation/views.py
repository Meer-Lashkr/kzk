from django.shortcuts import render


def coming_soon(request):
    return render(request, 'validation/coming_soon.html')
