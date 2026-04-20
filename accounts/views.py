'''from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, RedirectView, UpdateView

from .forms import UserRegistrationForm, UserAddressForm


User = get_user_model()


class UserRegistrationView(TemplateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/user_registration.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse_lazy('transactions:transaction_report')
            )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        registration_form = UserRegistrationForm(self.request.POST)
        address_form = UserAddressForm(self.request.POST)

        if registration_form.is_valid() and address_form.is_valid():
            user = registration_form.save()
            address = address_form.save(commit=False)
            address.user = user
            address.save()

            login(self.request, user)
            messages.success(
                self.request,
                (
                    f'Thank You For Creating A Bank Account. '
                    f'Your Account Number is {user.account.account_no}. '
                )
            )
            return HttpResponseRedirect(
                reverse_lazy('transactions:deposit_money')
            )

        return self.render_to_response(
            self.get_context_data(
                registration_form=registration_form,
                address_form=address_form
            )
        )

    def get_context_data(self, **kwargs):
        if 'registration_form' not in kwargs:
            kwargs['registration_form'] = UserRegistrationForm()
        if 'address_form' not in kwargs:
            kwargs['address_form'] = UserAddressForm()

        return super().get_context_data(**kwargs)


class UserLoginView(LoginView):
    template_name='accounts/user_login.html'
    redirect_authenticated_user = True


class LogoutView(RedirectView):
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/profile.html'
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('transactions:transaction_report')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'address_form' not in context:
            try:
                instance = self.request.user.address
            except AttributeError:
                instance = None
            context['address_form'] = UserAddressForm(instance=instance)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        try:
            instance = self.request.user.address
        except AttributeError:
            instance = None
        address_form = UserAddressForm(request.POST, instance=instance)

        if form.is_valid() and address_form.is_valid():
            form.save()
            address_form.save()
            messages.success(request, 'Profile updated successfully.')
            return self.form_valid(form)
        
        return self.render_to_response(
            self.get_context_data(form=form, address_form=address_form)
        )

# Cashier Views
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserBankAccount

@method_decorator(staff_member_required, name='dispatch')
class CashierDashboardView(TemplateView):
    template_name = 'accounts/cashier_dashboard.html'

    def post(self, request, *args, **kwargs):
        account_no = request.POST.get('account_no')
        try:
            account = UserBankAccount.objects.get(account_no=account_no)
            return redirect('accounts:cashier_update', pk=account.user.pk)
        except UserBankAccount.DoesNotExist:
            messages.error(request, "Account number not found.")
            return self.render_to_response(self.get_context_data())

@method_decorator(staff_member_required, name='dispatch')
class CashierCustomerUpdateView(UserUpdateView):
    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs.get('pk'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_cashier_view'] = True
        context['customer'] = self.get_object()
        return context
'''

from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, RedirectView, UpdateView

from .forms import UserRegistrationForm, UserAddressForm, UserLoginForm


User = get_user_model()


class UserRegistrationView(TemplateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/user_registration.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse_lazy('transactions:transaction_report')
            )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        registration_form = UserRegistrationForm(self.request.POST)
        address_form = UserAddressForm(self.request.POST)

        if registration_form.is_valid() and address_form.is_valid():
            user = registration_form.save()
            address = address_form.save(commit=False)
            address.user = user
            address.save()

            login(self.request, user)
            messages.success(
                self.request,
                (
                    f'Thank You For Creating A Bank Account. '
                    f'Your Account Number is {user.account.account_no}. '
                )
            )
            return HttpResponseRedirect(
                reverse_lazy('transactions:deposit_money')
            )

        return self.render_to_response(
            self.get_context_data(
                registration_form=registration_form,
                address_form=address_form
            )
        )

    def get_context_data(self, **kwargs):
        if 'registration_form' not in kwargs:
            kwargs['registration_form'] = UserRegistrationForm()
        if 'address_form' not in kwargs:
            kwargs['address_form'] = UserAddressForm()

        return super().get_context_data(**kwargs)


class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True


class LogoutView(RedirectView):
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/profile.html'
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('transactions:transaction_report')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'address_form' not in context:
            try:
                instance = self.request.user.address
            except AttributeError:
                instance = None
            context['address_form'] = UserAddressForm(instance=instance)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        try:
            instance = self.request.user.address
        except AttributeError:
            instance = None
        address_form = UserAddressForm(request.POST, instance=instance)

        if form.is_valid() and address_form.is_valid():
            form.save()
            address_form.save()
            messages.success(request, 'Profile updated successfully.')
            return self.form_valid(form)
        
        return self.render_to_response(
            self.get_context_data(form=form, address_form=address_form)
        )


# Cashier Views
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserBankAccount

@method_decorator(staff_member_required, name='dispatch')
class CashierDashboardView(TemplateView):
    template_name = 'accounts/cashier_dashboard.html'

    def post(self, request, *args, **kwargs):
        account_no = request.POST.get('account_no')
        try:
            account = UserBankAccount.objects.get(account_no=account_no)
            return redirect('accounts:cashier_update', pk=account.user.pk)
        except UserBankAccount.DoesNotExist:
            messages.error(request, "Account number not found.")
            return self.render_to_response(self.get_context_data())

@method_decorator(staff_member_required, name='dispatch')
class CashierCustomerUpdateView(UserUpdateView):
    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs.get('pk'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_cashier_view'] = True
        context['customer'] = self.get_object()
        return context