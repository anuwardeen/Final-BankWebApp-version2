from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.views import View
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def index(request):
    return render(request, "bankWebApp/index.html")


@login_required
def bank_based_details(request):
    bank_details = bank.objects.all()
    context = {"details": bank_details}
    return render(request, "bankWebApp/bank_based_details.html",
                  context=context)


@login_required
def accounts_based_details(request, bank_id):
    act_details = account.objects.all().filter(bank_id=bank_id)
    context = {"details": act_details}
    return render(
        request, "bankWebApp/account_based_details.html", context=context)


@login_required
def customers_based_details(request, act_id):

    cust_details = customer.objects.all().filter(act_id=act_id)
    context = {"cust_details": cust_details}
    return render(
        request, "bankWebApp/customer_based_details.html", context=context)


@login_required
def transactions_based_details(request, act_id):

    trans_details = transaction.objects.all().filter(act_id=act_id)
    context = {"details": trans_details}
    return render(
        request, "bankWebApp/transaction_based_details.html", context=context)


@login_required
def add_new_customer_to_bank(request):
    if request.method == "POST":
        new_act_id = accountID()
        mybank = bank.objects.get(bank_name=request.POST.get("bank_name"))
        act_type = request.POST.get("act_type")
        cust_name = request.POST.get("cust_name")
        cust_balance = request.POST.get("cust_balance")
        cust_email = request.POST.get("cust_email")
        cust_dob = request.POST.get("cust_dob")
        cust_address = request.POST.get("cust_address")
        try:
            new_account = account.objects.create(
                bank_id=mybank, act_type=act_type, act_id=new_act_id)
            customer.objects.create(
                act_id=new_account,
                cust_name=cust_name,
                cust_balance=cust_balance,
                cust_email=cust_email,
                cust_dob=cust_dob,
                cust_address=cust_address)
            transaction.objects.create(
                act_id=new_account,
                transaction_amount=cust_balance)

        except Exception as e:
            print(e)

        else:

            return render(request, "bankWebApp/index.html")

    else:
        regf = add_customer_to_bank()
        bank_name = bank.objects.all()
        context = {"form": regf, "bank_name": bank_name}
        return render(request, "bankWebApp/add_new_customer.html", context)


def accountID():
    if account.objects.all():
        actid = account.objects.all().values(
            'act_id').order_by('-act_id')[0]['act_id']
        print(actid)
        print(type(actid))
        print(actid)
        new_act_id = int(actid) + 1
        return int(new_act_id)
    else:
        return 1000000000


@login_required
def do_transaction(request):
    transac_form = do_transactions()
    if request.method == "POST":
        act_id = request.POST.get("act_id")
        transaction_amount = request.POST.get("transaction_amount")
        transaction_details = request.POST.get("transaction_details")

        try:
            act_balance = customer.objects.filter(act_id=act_id).values(
                "cust_balance").order_by("-act_id")[0]['cust_balance']
            balance = balance_check(
                act_balance,
                transaction_amount,
                transaction_details)

        except Exception as e:
            print(e)
            return HttpResponse("this is exception")

        else:
            act_update = customer.objects.get(act_id=act_id)
            act_update.cust_balance = balance
            act_update.save()
            transaction.objects.create(
                act_id=account.objects.get(
                    act_id=act_id),
                transaction_details=transaction_details,
                transaction_amount=transaction_amount)
            return render(request, "bankWebApp/do_transactions.html",
                          {"form": transac_form})

    else:

        return render(request, "bankWebApp/do_transactions.html",
                      {"form": transac_form})


def balance_check(act_balance, transaction_amount, transaction_details):

    if transaction_details == "DB." and int(transaction_amount) > 0:
        return int(transaction_amount) + act_balance

    elif transaction_details == "CR." and int(transaction_amount) > 0:
        if act_balance > int(transaction_amount):
            return act_balance - int(transaction_amount)
        else:
            raise Exception

    else:
        raise Exception


@login_required
def add_bank(request):

    if request.method == "POST":
        form = add_new_bank(request.POST)

        if form.is_valid():
            form.save()
            return render(request, "bankWebApp/add_new_bank.html")

        else:
            return render(
                request, "bankWebApp/add_new_bank.html", {"form": form})
    else:
        form = add_new_bank()
        return render(request, "bankWebApp/add_new_bank.html", {"form": form})


class add_new_user(View):

    def get(self, request):
        return render(request, "registration/user_registration.html")

    def post(self, request):
        form = User.objects.create_user(
            request.POST.get("usernamesignup"),
            request.POST.get("emailsignup"),
            request.POST.get("passwordsignup"))
        return render(request, "registration/login.html")



class transfer_money(LoginRequiredMixin, View):

    def get(self, request):
        accounts = account.objects.all()
        return render(request, "bankWebApp/transfer_money.html",
                      {"accounts": accounts})

    def balance_check(self, act_balance, transaction_amount,
                      transaction_details):
        if transaction_details == "DB." and int(transaction_amount) > 0:
            return int(transaction_amount) + act_balance

        elif transaction_details == "CR." and int(transaction_amount) > 0:
            if act_balance > int(transaction_amount):
                return act_balance - int(transaction_amount)
            else:
                raise Exception

        else:
            raise Exception

    def post(self, request):
        from_act_id = request.POST.get("from_act_id")
        to_act_id = request.POST.get("to_act_id")
        transaction_amount = request.POST.get("transaction_amount")
        try:
            from_account = customer.objects.filter(
                act_id=from_act_id).values("cust_balance")[0]['cust_balance']
            print(from_account)
            to_account = customer.objects.filter(
                act_id=to_act_id).values("cust_balance")[0]['cust_balance']
            print(to_account)
            from_act_balance = self.balance_check(
                from_account, transaction_amount, "CR.")
            print(from_act_balance)
            to_act_balance = self.balance_check(
                to_account, transaction_amount, transaction_details="DB.")
            print(to_act_balance)

        except Exception as e:
            print(e)
            return render(request,"bankWebApp/autoredirect.html")

        else:
            from_act = customer.objects.get(act_id=from_act_id)
            from_act.cust_balance = from_act_balance
            from_act.save()

            to_act = customer.objects.get(act_id=to_act_id)
            to_act.cust_balance = to_act_balance
            to_act.save()

            transaction.objects.create(
                act_id=account.objects.get(
                    act_id=from_act_id),
                transaction_details="CR.",
                transaction_amount=transaction_amount)
            transaction.objects.create(
                act_id=account.objects.get(
                    act_id=to_act_id),
                transaction_details="DB.",
                transaction_amount=transaction_amount)
            return HttpResponseRedirect(reverse("index"))

#
# def total_no_of_accounts(request,cust_name,cust_dob):
#