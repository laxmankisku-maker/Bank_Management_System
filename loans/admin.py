from django.contrib import admin
from .models import Loan
from transactions.models import Transaction
from transactions.constants import LOAN

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'account', 'amount', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('account__account_no',)
    actions = ['approve_loan', 'reject_loan']

    def approve_loan(self, request, queryset):
        for loan in queryset:
            if loan.status == 'PENDING':
                loan.status = 'APPROVED'
                loan.save()
                
                # Update user balance
                account = loan.account
                account.balance += loan.amount
                account.save(update_fields=['balance'])
                
                # Create Transaction record
                Transaction.objects.create(
                    account=account,
                    amount=loan.amount,
                    balance_after_transaction=account.balance,
                    transaction_type=LOAN
                )
        self.message_user(request, "Selected loans have been approved and funds disbursed.")
    approve_loan.short_description = "Approve selected loans"

    def reject_loan(self, request, queryset):
        queryset.filter(status='PENDING').update(status='REJECTED')
    reject_loan.short_description = "Reject selected loans"
