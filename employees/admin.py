
from django.contrib import admin
from .models import Department, Employee


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'email',
        'department',
        'designation',
        'salary',
        'status',
    )

    list_filter = ('status', 'department')
    search_fields = ('first_name', 'last_name', 'email')
    list_per_page = 10

