from django import forms
from .models import customer, transaction, bank

class add_customer_to_bank(forms.ModelForm):
    class Meta:
        model = customer
        exclude = ('act_id',)


class do_transactions(forms.ModelForm):
    class Meta:
        model = transaction
        fields="__all__"

class add_new_bank(forms.ModelForm):
    class Meta:
        model = bank
        fields="__all__"
