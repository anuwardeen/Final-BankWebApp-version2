from django.contrib import admin
from .models import *


class bankAdmin(admin.ModelAdmin):
    list_display = ("bank_id","bank_name","bank_ifsc",)
    list_filter = ('bank_name',)
    search_fields = ('bank_id',)

class customerAdmin(admin.ModelAdmin):
    list_display = ("act_id","cust_name","cust_balance",)
    list_filter = ('act_id',)
    search_fields = ('act_id',)

class accountAdmin(admin.ModelAdmin):
    list_display = ("act_id","bank_id",)
    list_filter = ('act_id',)
    search_fields = ('act_id',)

class transactionAdmin(admin.ModelAdmin):
    list_display = ("act_id","transaction_details","transaction_amount",)
    list_filter = ('transaction_details',)
    search_fields = ('act_id',)

admin.site.register(bank,bankAdmin)
admin.site.register(customer,customerAdmin)
admin.site.register(transaction,transactionAdmin)
admin.site.register(account,accountAdmin)