from django.core.management import BaseCommand
from ...models import *

class Command(BaseCommand):
    help = "My test command"

    def add_arguments(self, parser):
        parser.add_argument('cmdarg',type=int,nargs='*' ,default=[2,2,3])

    def handle(self, *args, **options):
        no_of_banks=options.get('cmdarg', None)[0]
        no_of_customer = options.get('cmdarg', None)[1]
        no_of_accounts = options.get('cmdarg', None)[2]

        if bank.objects.all().exists():
            last_bank_id=bank.objects.all().order_by('-bank_id').values("bank_id")[:1][0]['bank_id']
            bank_id_starts_from=self.getting_new_bank_id(last_bank_id)

        else:
            bank_id_starts_from="B01"

        if account.objects.all().exists():
            last_act_id = account.objects.all().order_by('-act_id').values("act_id")[:1][0]['act_id']
            act_id_starts_from = self.getting_new_account_id(last_act_id)

        else:
            act_id_starts_from=1000000000
        self.creating_records(no_of_banks ,no_of_customer,no_of_accounts,bank_id_starts_from,act_id_starts_from)

#################################################################################################################

    def creating_records(self,no_of_banks ,no_of_customer,no_of_accounts, bank_id_starts_from,act_id_starts_from):
        bank_queries=[]
        account_queries = []
        customer_queries = []
        transaction_queries = []
        for i in range(no_of_banks):
            new_bank=bank(bank_id=bank_id_starts_from,bank_name="BANK"+str(i+1),bank_ifsc="BANK000"+str(i),bank_city="Bangalore")
            cust_name = 0
            for j in range(no_of_accounts*no_of_customer):

                if j%no_of_accounts==0:
                    cust_name=cust_name+1

                new_account=account(act_id=act_id_starts_from,bank_id=new_bank,act_type="SB")
                new_customer=customer(act_id=new_account,cust_name="customer"+str(cust_name),cust_balance=1000,cust_email="abc@def.com",cust_dob="1992-12-12",cust_address="Tarams")
                new_transaction=transaction(act_id=new_account, transaction_amount=1000)
                act_id_starts_from=self.getting_new_account_id(act_id_starts_from)
                account_queries.append(new_account)
                customer_queries.append(new_customer)
                transaction_queries.append(new_transaction)


            bank_id_starts_from = self.getting_new_bank_id(bank_id_starts_from)

            bank_queries.append(new_bank)

        self.commit(bank_queries, customer_queries, transaction_queries, account_queries)



    def commit(self,bank_queries,customer_queries,transaction_queries,account_queries):
        bank.objects.bulk_create(bank_queries)
        account.objects.bulk_create(account_queries)
        customer.objects.bulk_create(customer_queries)
        transaction.objects.bulk_create(transaction_queries)

    #################################################################################################################






    def getting_new_bank_id(self,last_id):
        num = 0
        for i in last_id:
            if i.isdigit():
                num = num * 10 + int(i)

        num+=1
        if num <= 9:
            id_starts_from = "B0" + str(num )
        else:
            id_starts_from = "B" + str(num )

        return id_starts_from

    def getting_new_account_id(self,last_id):
        return last_id+1