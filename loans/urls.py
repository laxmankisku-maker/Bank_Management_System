from django.urls import path
from .views import LoanRequestView, LoanListView, LoanTypeSelectionView

app_name = 'loans'

urlpatterns = [
    path('select/', LoanTypeSelectionView.as_view(), name='loan_type_selection'),
    path('request/<str:loan_type>/', LoanRequestView.as_view(), name='loan_request'),
    path('list/', LoanListView.as_view(), name='loan_list'),
]
