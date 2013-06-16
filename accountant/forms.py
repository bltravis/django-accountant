from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import Group
from django.utils.translation import ugettext as _

from .models import Account

class AccountForm(ModelForm):
    """ Convenience ModelForm for Account model to handle user/group assignment constraints """
    
    group = forms.ModelChoiceField(queryset=Group.objects.all(), help_text=_('Do not specify a user if assigning account to a group'))

    def clean(self):
        cleaned_data = super(AccountForm, self).clean()
        user = cleaned_data.get("user")
        group = cleaned_data.get("group")
        
        if not user and not group:
            raise forms.ValidationError(_("You must specify either a user or a group to associate with this account."))
        if user and group:
            raise forms.ValidationError(_("You may specify a user or a group to associate with this account, but not both."))
        return cleaned_data
    
    class Meta:
        model = Account