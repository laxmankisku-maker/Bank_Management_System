from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'amount', 'balance_after_transaction', 'transaction_type', 'timestamp')
    search_fields = ('account__account_no',)
    list_filter = ('transaction_type', 'timestamp')
