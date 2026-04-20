import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banking_system.settings')
django.setup()

from accounts.models import BankAccountType

if not BankAccountType.objects.exists():
    BankAccountType.objects.create(
        name='Savings',
        maximum_withdrawal_amount=1000,
        annual_interest_rate=5,
        interest_calculation_per_year=2
    )
    BankAccountType.objects.create(
        name='Current',
        maximum_withdrawal_amount=5000,
        annual_interest_rate=0,
        interest_calculation_per_year=1
    )
    print("Initial account types created.")
else:
    print("Account types already exist.")
