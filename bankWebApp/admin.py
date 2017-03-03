from django.contrib import admin
from .models import *

admin.site.register(bank)
admin.site.register(customer)
admin.site.register(transaction)
admin.site.register(account)