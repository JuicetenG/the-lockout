from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('gear/', views.gear_index, name='gear-index'),
    # path('gear/create/', views.GearCreate.as_view(), name='gear-create'),
    # path('gear/<int:gear_id>/', views.gear_detail, name='gear-detail'),
]