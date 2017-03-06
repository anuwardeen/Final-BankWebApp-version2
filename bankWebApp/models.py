from django.db import models
from django.contrib.auth.models import User


class bank(models.Model):

    bank_id=models.CharField(max_length=3,primary_key=True)
    bank_name=models.CharField(max_length=20)
    bank_city=models.CharField(max_length=30)
    bank_ifsc=models.CharField(max_length=10)

    def __str__(self):
        return self.bank_id



class account(models.Model):

    account_choices=(('SB', "Savings Bank Account"),
                     ('CA', "Current Account"),)

    act_id = models.IntegerField(primary_key=True)
    bank_id = models.ForeignKey(bank, on_delete=models.CASCADE)
    act_type=models.CharField(max_length=2, choices=account_choices)

    def __str__(self):
        return str(self.act_id)



class customer(models.Model):

    act_id = models.ForeignKey(account, on_delete=models.CASCADE)
    cust_name = models.CharField(max_length=20)
    cust_balance = models.IntegerField()
    cust_email=models.CharField(max_length=30)
    cust_dob=models.DateField()
    cust_address=models.TextField(max_length=50)


    def __str__(self):
        return self.cust_name



class transaction(models.Model):

    transaction_choices = (("CR.",'Credit'),
                       ("DB.",'Debit'),)

    act_id=models.ForeignKey(account, on_delete=models.CASCADE)
    transaction_details=models.CharField(max_length=3, choices=transaction_choices, default="DB.")
    transaction_amount= models.IntegerField()
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = "updated"

    def __str__(self):
        return str(self.transaction_amount)
#
# class verification(models.Model):
#     act_id=models.ForeignKey(account, on_delete=models.CASCADE)
#     pan_id=models.CharField(max_length=10,default="XXXXXXXXXX")
#     driving_license
#

class userPermission(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    bank_id = models.CharField(max_length=3)