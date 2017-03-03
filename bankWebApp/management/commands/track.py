from django.core.management import BaseCommand
from ...models import *

class Command(BaseCommand):
    help = "My test command"

    def add_arguments(self, parser):
        parser.add_argument('arguement',type=str,nargs='*' ,default=["B01","1000000000","2"])

    def handle(self, *args, **options):
        bank_id = options.get('arguement', None)[0]
        act_number = options.get('arguement', None)[1]
        no_of_trans = options.get('arguement', None)[2]
        bank1=bank.objects.filter(bank_id=bank_id)
        act1=account.objects.filter(bank_id=bank1, act_id=act_number)
        customer1=customer.objects.filter(act_id=act1)
        ntrans=transaction.objects.filter(act_id=act1).order_by('-updated')[:int(no_of_trans)]

        print(bank1[0].bank_id,"\t",bank1[0].bank_name,"\t",bank1[0].bank_ifsc,"\t",bank1[0].bank_city,"\t")
        print("|")
        print("| ")
        print("|_",act1[0].act_id,"\t",act1[0].bank_id,"\t",act1[0].act_type,sep=" ")
        print("   | ")
        print("   | ")
        print("   |  Act ID\t\tCustomer Name\tBalance\t\t   Email\tDateOfBirth\tAddress", )
        print("   |_", customer1[0].act_id,"\t",customer1[0].cust_name,"\t",customer1[0].cust_balance,"\t\t",customer1[0].cust_email,"\t",customer1[0].cust_dob,"\t",customer1[0].cust_address,"\t", sep=" ")
        print("     |")
        print("     |")
        print("     | Transactions")
        for i in range(len(ntrans)):
            print("     |_",ntrans[i].act_id,"\t",ntrans[i].transaction_details,"\t",ntrans[i].transaction_amount,"\t",ntrans[i].updated,sep=" ")