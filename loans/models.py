from django.db import models
from accounts.models import UserBankAccount

LOAN_TYPE = (
    ('STUDENT', 'Student Loan'),
    ('HOUSE', 'House Loan'),
    ('COMMUNITY', 'Community Loan'),
)

LOAN_STATUS = (
    ('PENDING', 'Pending'),
    ('APPROVED', 'Approved'),
    ('REJECTED', 'Rejected'),
    ('PAID', 'Paid'),
)

class Loan(models.Model):
    account = models.ForeignKey(
        UserBankAccount,
        related_name='loans',
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    interest_rate = models.DecimalField(decimal_places=2, max_digits=5, default=10.0)
    duration_months = models.PositiveIntegerField()
    loan_type = models.CharField(max_length=10, choices=LOAN_TYPE, default='HOUSE')
    income_document = models.FileField(upload_to='loan_documents/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=LOAN_STATUS, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Loan {self.id} for {self.account.account_no}"

    @property
    def monthly_installment(self):
        # Simple interest calculation: (Principal + Total Interest) / Duration
        total_interest = (self.amount * self.interest_rate * self.duration_months) / (100 * 12)
        total_payable = self.amount + total_interest
        return round(total_payable / self.duration_months, 2)
