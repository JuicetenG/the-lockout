import uuid
import boto3
from django.core.exceptions import ValidationError

S3_BASE_URL = 's3.us-east-1.amazonaws.com' 
BUCKET = 'thelockout'

class ImageUploadMixin:
    def handle_image_upload(self, form):
        form.instance.user = self.request.user
        
        image_file = self.request.FILES.get('image')
        if image_file:
            s3 = boto3.client('s3')
            key = f'gear_images/{uuid.uuid4().hex[:6]}{image_file.name[image_file.name.rfind("."):]}'  # Unique filename
            try:
                s3.upload_fileobj(image_file, BUCKET, key)
                image_url = f"https://{BUCKET}.s3.amazonaws.com/{key}" 
                form.instance.image = image_url  # Assign image URL before saving
            except Exception as e:
                form.instance.image = None  # Fallback if upload fails

    def form_valid(self, form):
        form.instance.user = self.request.user  # Assign the user
        self.handle_image_upload(form)  # Handle the image upload

        response = super().form_valid(form)  # Call parent form_valid
        return response