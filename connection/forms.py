from django import forms
from .models import Client


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = [
            "db_name",
            "db_host",
            "db_user",
            "db_password",
            "port",
            "tables",
            "prompt",
            "queries",
            "db_type",
            "constraints",
        ]

        widgets = {
            "db_password": forms.PasswordInput(),
            "prompt": forms.Textarea(attrs={"rows": 4}),
            "tables": forms.Textarea(attrs={"rows": 5}),
            "queries": forms.Textarea(attrs={"rows": 5}),
        }