from django.contrib import admin
from .models import BankAccountType, User, UserAddress, UserBankAccount

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')

@admin.register(BankAccountType)
class BankAccountTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'annual_interest_rate', 'interest_calculation_per_year')

@admin.register(UserBankAccount)
class UserBankAccountAdmin(admin.ModelAdmin):
    list_display = ('account_no', 'user', 'account_type', 'balance')
    search_fields = ('account_no', 'user__email')
    list_filter = ('account_type',)

@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'country')
