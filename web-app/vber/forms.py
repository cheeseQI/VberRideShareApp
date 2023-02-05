from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="username", max_length=128)
    password = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput)

class DriverForm(forms.Form):
    driver_name = forms.CharField(label="diver_name", max_length=128)
    type = forms.CharField(label="type", max_length=128)
    plate_number = forms.CharField(label="plate_number", max_length=128)
    max_capacity = forms.CharField(label="max_capacity", max_length=128)
    spec_info = forms.CharField(label="spec_info", max_length=128)