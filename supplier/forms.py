from django import forms

from . import models


class SuppliersForm(forms.ModelForm):
    class Meta:
        model = models.Supllier
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput({"class": "form-control"}),
            "description": forms.Textarea({"class": "form-control", "rows": 3}),
        }
        labels = {
            "name": "Nome",
            "description": "Descrição",
        }
