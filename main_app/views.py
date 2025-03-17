from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Gear
import uuid
import boto3

S3_BASE_URL = 's3.us-east-1.amazonaws.com' 
BUCKET = 'thelockout'

class Home(LoginView):
    template_name = 'home.html'

def gear_index(request):
    gear_items = Gear.objects.filter(user=request.user)
    return render(request, 'gear/gear-index.html', {'gear': gear_items})

class GearCreate(CreateView):
    model = Gear
    fields = ['make', 'model', 'type', 'cost', 'trade']
    success_url = '/gear/' 

    # def form_valid(self, form):
    #     form.instance.user = self.request.user 
    #     return super().form_valid(form)
    def form_valid(self, form):
        print("🚀 form_valid executed!")  # Debugging output
        form.instance.user = self.request.user  # Assign the user
        
        image_file = self.request.FILES.get('image')
        print(f"📸 Image file: {image_file}")  # Debugging output

        if image_file:
            s3 = boto3.client('s3')
            key = f'gear_images/{uuid.uuid4().hex[:6]}{image_file.name[image_file.name.rfind("."):]}'  # Unique filename
            print(f"🔑 Generated S3 Key: {key}")  # Debugging output

            try:
                s3.upload_fileobj(image_file, BUCKET, key)
                image_url = f"https://{BUCKET}.s3.amazonaws.com/{key}" 
                
                form.instance.image = image_url  # Assign image URL before saving
                print(f"🎯 Form instance image field set: {form.instance.image}")  # Debugging output
                
            except Exception as e:
                print(f"❌ Error uploading image: {e}")
                form.instance.image = None  # Fallback if upload fails

        response = super().form_valid(form)
        print(f"✅ Gear object saved with ID: {form.instance.id} and Image URL: {form.instance.image}")  # Debugging output
        return response

    
class GearUpdate(UpdateView):
    model = Gear
    fields = [ 'cost', 'trade', 'image']
    success_url = '/gear/'

class GearDelete(DeleteView):
    model = Gear
    success_url = '/gear/'
    
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


