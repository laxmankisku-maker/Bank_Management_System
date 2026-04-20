import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banking_system.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(email='admin@bank.com').exists():
    User.objects.create_superuser('admin@bank.com', 'admin123')
    print("Superuser created: admin@bank.com / admin123")
else:
    print("Superuser already exists.")
