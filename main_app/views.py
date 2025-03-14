from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Gear

class Home(LoginView):
    template_name = 'home.html'

def gear_index(request):
    gear_items = Gear.objects.filter(user=request.user)
    return render(request, 'gear/gear-index.html', {'gear': gear_items})

class GearCreate(CreateView):
    model = Gear
    fields = ['make', 'model', 'type', 'cost', 'trade', 'image']
    success_url = '/gear/' 

    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)
    

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


