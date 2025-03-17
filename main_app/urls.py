from django.urls import path
from . import views 


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('gear/', views.gear_index, name='gear-index'),
    path('gear/create/', views.GearCreate.as_view(), name='gear-create'),
    path('gear/<int:gear_id>/', views.gear_detail, name='gear-detail'),
    path('gear/<int:pk>/update/', views.GearUpdate.as_view(), name='gear-update'),
    path('gear/<int:pk>/delete/', views.GearDelete.as_view(), name='gear-delete'),
    path('accounts/signup/', views.signup, name='signup'),
]