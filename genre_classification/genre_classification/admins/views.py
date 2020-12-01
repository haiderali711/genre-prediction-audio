from django.shortcuts import render
from django.utils import timezone

from admins.models import MLModel


def admin_view(request):
    models = MLModel.objects.order_by('-created_on')
    return render(request, 'admins/admins.html', {'models': models})


# def activate_model(request):
#     print("activate model called")
#     return render(request, 'admins/admins.html')
