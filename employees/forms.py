from django import forms
from .models import Employee, Department

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'department',
            'designation',
            'salary',
            'joining_date',
            'status',
        ]

        widgets = {
            'joining_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']

