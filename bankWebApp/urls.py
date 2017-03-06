from django.conf.urls import url
from . import views

urlpatterns = (

    url(r'^$', views.index, name="index"),

    url(r'^bank/details/$', views.bank_based_details, name="bank_details"),

    url(r'^bank/(?P<bank_id>\w+)/accounts/$', views.accounts_based_details, name="account_details"),

    url(r'^bank/customer/(?P<act_id>\d+)/$', views.customers_based_details, name="customer_details"),

    url(r'^bank/customer/(?P<act_id>\d+)/transactions/$', views.transactions_based_details, name="transaction_details"),

    url(r'^add/customer/to/bank/$', views.add_new_customer_to_bank, name="new_customer"),

    url(r'^bank/do/transaction/$', views.do_transaction, name="do_transaction"),

    url(r'^bank/addNewBank/$', views.add_bank, name="add_new_bank"),

    url(r'^register/NewUser/', views.add_new_user.as_view(), name="add_new_user"),

    url(r'^transfer/money/$',views.transfer_money.as_view(),name="transfer_money"),

    url(r'^delete/$',views.deleteing_data,name="delete_data"),

    url(r'^delete/bank/$',views.deleting_bank,name="delete_bank"),

    url(r'^delete/account$',views.delete_account,name="delete_account"),

)
