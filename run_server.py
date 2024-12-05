import os
import sys
import subprocess

def main():
    # Set the Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network.settings')
    
    # Add the project directory to Python path
    project_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(project_dir)
    
    # Import Django and set up the environment
    import django
    django.setup()
    
    # Run Daphne
    cmd = [
        'daphne',
        '-b', '127.0.0.1',
        '-p', '8000',
        'social_network.asgi:application'
    ]
    
    subprocess.run(cmd)
