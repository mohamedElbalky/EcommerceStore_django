from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'first_name',
            'last_name',
            'email',
            'telephone',
            'address',
            'postal_code',
            'city',
            'country',
            'note',
            'transport',
        )
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'inp', "onkeyup": "fillField(id)"}
            ),
            'last_name': forms.TextInput(
                attrs={'class': 'inp', "onkeyup": "fillField(id)"}
            ),
            'email': forms.TextInput(
                attrs={'class': 'inp', "onkeyup": "fillField(id)"}
            ),
            'telephone': forms.TextInput(
                attrs={'class': 'inp', "onkeyup": "fillField(id)"}
            ),
            'address': forms.TextInput(
                attrs={'class': 'inp', "onkeyup": "fillField(id)"}
            ),
            'postal_code': forms.TextInput(
                attrs={'class': 'inp', "onkeyup": "fillField(id)"}
            ),
            'city': forms.TextInput(
                attrs={'class': 'inp', "onkeyup": "fillField(id)"}
            ),
            'country': forms.Select(attrs={'class': 'inp country', "onkeyup": "fillField(id)"}),
            'note': forms.Textarea(
                attrs={'class': 'inp', 'rows': 1, "onkeyup": "fillField(id)"}
            ),
            'transport': forms.RadioSelect
        }

    # def clean(self):
    #     cd = self.cleaned_data
        
