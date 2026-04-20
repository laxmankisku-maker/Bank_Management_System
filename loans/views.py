from django.views.generic import CreateView, ListView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Loan
from transactions.models import Transaction
from transactions.constants import LOAN

class LoanTypeSelectionView(LoginRequiredMixin, TemplateView):
    template_name = 'loans/loan_type_selection.html'

class LoanRequestView(LoginRequiredMixin, CreateView):
    model = Loan
    fields = ['amount', 'duration_months', 'income_document']
    template_name = 'loans/loan_request.html'
    success_url = reverse_lazy('loans:loan_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loan_type'] = self.kwargs.get('loan_type', 'HOUSE').upper()
        return context

    def form_valid(self, form):
        loan = form.save(commit=False)
        loan.account = self.request.user.account
        loan.loan_type = self.kwargs.get('loan_type', 'HOUSE').upper()
        loan.save()
        messages.success(self.request, f"{loan.get_loan_type_display()} request submitted successfully. Waiting for admin approval.")
        return super().form_valid(form)

class LoanListView(LoginRequiredMixin, ListView):
    model = Loan
    template_name = 'loans/loan_list.html'
    context_object_name = 'loans'

    def get_queryset(self):
        return Loan.objects.filter(account=self.request.user.account).order_by('-created_at')
