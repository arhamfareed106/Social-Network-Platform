from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ImageDraw
import os

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(max_length=500, blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # Ensure default image exists before saving
        default_path = os.path.join('media', 'default.jpg')
        if not os.path.exists(default_path):
            # Create a default image if it doesn't exist
            img = Image.new('RGB', (300, 300), color='gray')
            draw = ImageDraw.Draw(img)
            draw.ellipse([50, 50, 250, 250], fill='white')
            img.save(default_path)

        # Save the profile
        super().save(*args, **kwargs)

        # Resize avatar if needed
        try:
            if self.avatar and os.path.exists(self.avatar.path):
                img = Image.open(self.avatar.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.avatar.path)
        except (FileNotFoundError, ValueError):
            # If the image file is missing or invalid, use the default
            self.avatar = 'default.jpg'
            self.save()
