from django.forms import ModelForm
from .models import Traveler

class TravelerForm(ModelForm):
	class Meta:
		model = Traveler;
		fields = ['employee_id', 'employee_name', 'sap_id', 'employee_email']
	# employee_id = forms.CharField(label='Employee ID:', max_length=100)
	# employee_name = forms.CharField(label='Employee Name:', max_length=100)
	# sap_id = forms.CharField(label='SAP ID:', max_length=100)
	# employee_email = forms.EmailField(label='Employee E-Mail:', max_length=100)s