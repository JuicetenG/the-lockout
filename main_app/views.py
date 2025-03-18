from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Gear
from .mixins import ImageUploadMixin


class Home(LoginView):
    template_name = 'home.html'

@login_required
def gear_index(request):
    gear_types = Gear.objects.values_list('type', flat=True).distinct()
    selected_type = request.GET.get('type', None)
    if selected_type:
        gear = Gear.objects.filter(type=selected_type)
    else:
        gear = Gear.objects.all()

    return render(request, 'gear/gear-index.html', {'gear': gear, 'gear_types': gear_types, 'selected_type': selected_type})

class GearCreate(ImageUploadMixin, LoginRequiredMixin, CreateView):
    model = Gear
    fields = ['make', 'model', 'type', 'cost', 'trade']
    success_url = '/gear/' 

class GearUpdate(LoginRequiredMixin, UpdateView):
    model = Gear
    fields = [ 'cost', 'trade']
    success_url = '/gear/'

class GearDelete(LoginRequiredMixin, DeleteView):
    model = Gear
    success_url = '/gear/'

@login_required
def gear_detail(request, gear_id):
    gear = Gear.objects.get(id=gear_id)
    return render(request, 'gear/gear-detail.html', {'gear': gear})

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('gear-index')
        else:
            error_message = 'Invalid sign up - try again'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)


