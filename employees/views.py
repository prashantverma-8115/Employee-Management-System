from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.deletion import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404

from .models import Employee, Department
from .forms import EmployeeForm, DepartmentForm


# Dashboard
@login_required
def dashboard(request):
    context = {
        'total_employees': Employee.objects.count(),
        'total_departments': Department.objects.count(),
        'active_employees': Employee.objects.filter(
            status='Active'
        ).count(),
        'recent_employees': Employee.objects.select_related(
            'department'
        ).order_by('-created_at')[:5],
    }

    return render(request, 'employees/dashboard.html', context)


# Employee: List, Search, Filters and Pagination
@login_required
def employee_list(request):
    employees = Employee.objects.select_related(
        'department'
    ).all().order_by('id')

    # Search by first name, last name or email
    search = request.GET.get('search', '').strip()

    if search:
        employees = employees.filter(
            Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(email__icontains=search)
        )

    # Filter by status
    status = request.GET.get('status', '').strip()
    valid_statuses = dict(Employee.STATUS_CHOICES)

    if status in valid_statuses:
        employees = employees.filter(status=status)
    else:
        status = ''

    # Filter by department
    department_id = request.GET.get('department', '').strip()

    if department_id.isdigit():
        if Department.objects.filter(pk=int(department_id)).exists():
            employees = employees.filter(
                department_id=int(department_id)
            )
        else:
            department_id = ''
    else:
        department_id = ''

    # Pagination: 10 employees per page
    paginator = Paginator(employees, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'employees': page_obj.object_list,
        'page_obj': page_obj,
        'search': search,
        'selected_status': status,
        'selected_department': department_id,
        'departments': Department.objects.all().order_by('name'),
        'status_choices': Employee.STATUS_CHOICES,
    }

    return render(
        request,
        'employees/employee_list.html',
        context
    )


# Employee: Create
@login_required
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('employees:employee_list')
    else:
        form = EmployeeForm()

    return render(
        request,
        'employees/employee_form.html',
        {
            'form': form,
            'page_title': 'Add Employee',
        }
    )


# Employee: Update
@login_required
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)

        if form.is_valid():
            form.save()
            return redirect('employees:employee_list')
    else:
        form = EmployeeForm(instance=employee)

    return render(
        request,
        'employees/employee_form.html',
        {
            'form': form,
            'page_title': 'Edit Employee',
        }
    )


# Employee: Delete
@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        employee.delete()
        return redirect('employees:employee_list')

    return render(
        request,
        'employees/employee_confirm_delete.html',
        {'employee': employee}
    )


# Department: List
@login_required
def department_list(request):
    departments = Department.objects.all().order_by('name')

    return render(
        request,
        'employees/department_list.html',
        {'departments': departments}
    )


# Department: Create
@login_required
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('employees:department_list')
    else:
        form = DepartmentForm()

    return render(
        request,
        'employees/department_form.html',
        {
            'form': form,
            'page_title': 'Add Department',
        }
    )


# Department: Update
@login_required
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)

    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)

        if form.is_valid():
            form.save()
            return redirect('employees:department_list')
    else:
        form = DepartmentForm(instance=department)

    return render(
        request,
        'employees/department_form.html',
        {
            'form': form,
            'page_title': 'Edit Department',
        }
    )


# Department: Delete
@login_required
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)

    if request.method == 'POST':
        try:
            department.delete()
        except ProtectedError:
            return render(
                request,
                'employees/department_confirm_delete.html',
                {
                    'department': department,
                    'error': (
                        'This department has employees assigned to it. '
                        'Reassign or remove those employees first.'
                    ),
                }
            )

        return redirect('employees:department_list')

    return render(
        request,
        'employees/department_confirm_delete.html',
        {'department': department}
    )


