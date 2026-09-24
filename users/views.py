import re
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse, JsonResponse
from django.db import connection, transaction
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from users.models import User, Game
from users.forms import UserForm
from users.csv_utils import sync_users_to_csv, get_csv_path


def home_view(request):
    """Home page with Assassin's Creed Valhalla background, navigation buttons and marquee."""
    return render(request, 'users/home.html')


def insert_user_view(request):
    """Insert User page with centered form, red Insert button, and status message."""
    success_message = None
    error_message = None
    form = UserForm()

    if request.method == 'POST':
        user_id_raw = request.POST.get('user_id', '').strip()
        user_name = request.POST.get('user_name', '').strip()
        country = request.POST.get('country', '').strip()
        u_age_raw = request.POST.get('u_age', '').strip()
        pincode = request.POST.get('pincode', '').strip()
        city = request.POST.get('city', '').strip()
        passwords = request.POST.get('passwords', '').strip()

        # Validation
        if not (user_id_raw and user_name and country and u_age_raw and pincode and city and passwords):
            error_message = "All fields are required!"
        else:
            try:
                user_id = int(user_id_raw)
                u_age = int(u_age_raw)

                if User.objects.filter(user_id=user_id).exists():
                    error_message = f"User ID {user_id} already exists!"
                else:
                    user = User.objects.create(
                        user_id=user_id,
                        user_name=user_name,
                        country=country,
                        u_age=u_age,
                        pincode=pincode,
                        city=city,
                        passwords=passwords
                    )
                    success_message = f"User {user_name} is insert successfully !"
                    form = UserForm()  # reset form
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'success': True,
                            'message': success_message,
                            'user': {
                                'user_id': user.user_id,
                                'user_name': user.user_name,
                            },
                        })
            except ValueError:
                error_message = "User ID and User age must be valid integers!"
            except Exception as e:
                error_message = f"Error inserting user: {e}"

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': error_message}, status=400)

    context = {
        'form': form,
        'success_message': success_message,
        'error_message': error_message,
    }
    return render(request, 'users/insert_user.html', context)


def show_user_view(request):
    """Show User Details page with users table, sorting controls, Run Query and Export CSV buttons."""
    users = User.objects.all().order_by('user_id')
    context = {
        'users': users,
        'title': 'Show User Details',
        'is_sorted': False,
        'selected_sort': 'User ID',
    }
    return render(request, 'users/show_user.html', context)


def sort_user_view(request):
    """Show User Data - Sorted page displaying users ordered by selected column."""
    sort_by = request.GET.get('sort_by') or request.POST.get('sort_by') or 'user_id'
    
    # Map UI dropdown labels to model fields
    sort_mapping = {
        'User ID': 'user_id',
        'user_id': 'user_id',
        'User Name': 'user_name',
        'user_name': 'user_name',
        'Country': 'country',
        'country': 'country',
        'User age': 'u_age',
        'user age': 'u_age',
        'u_age': 'u_age',
        'pincode': 'pincode',
        'City': 'city',
        'city': 'city',
        'password': 'passwords',
        'passwords': 'passwords',
    }

    field = sort_mapping.get(sort_by, 'user_id')
    users = User.objects.all().order_by(field)

    context = {
        'users': users,
        'title': 'Show User Data - Sorted',
        'is_sorted': True,
        'selected_sort': sort_by,
    }
    return render(request, 'users/sort_user.html', context)


def edit_user_view(request, user_id):
    """Edit User Records page displaying pre-populated form."""
    user = get_object_or_404(User, user_id=user_id)
    context = {
        'user': user,
        'success_message': None,
        'error_message': None,
    }
    return render(request, 'users/edit_user.html', context)


def update_user_view(request, user_id):
    """Handles updating a user record and auto-syncing to users.csv."""
    user = get_object_or_404(User, user_id=user_id)
    success_message = None
    error_message = None

    if request.method == 'POST':
        user_name = request.POST.get('user_name', '').strip()
        country = request.POST.get('country', '').strip()
        u_age_raw = request.POST.get('u_age', '').strip()
        pincode = request.POST.get('pincode', '').strip()
        city = request.POST.get('city', '').strip()
        passwords = request.POST.get('passwords', '').strip()

        if not (user_name and country and u_age_raw and pincode and city and passwords):
            error_message = "All fields are required!"
        else:
            try:
                user.user_name = user_name
                user.country = country
                user.u_age = int(u_age_raw)
                user.pincode = pincode
                user.city = city
                user.passwords = passwords
                user.save()

                success_message = "Record updated successfully!!"
            except ValueError:
                error_message = "Age must be an integer!"
            except Exception as e:
                error_message = f"Error updating user: {e}"

    context = {
        'user': user,
        'success_message': success_message,
        'error_message': error_message,
    }
    return render(request, 'users/edit_user.html', context)


def delete_user_view(request, user_id):
    """Deletes the specified user, auto-syncs CSV, and renders Deleted Successfully page."""
    try:
        user = User.objects.filter(user_id=user_id).first()
        if user:
            user.delete()
    except Exception as e:
        messages.error(request, f"Error deleting user {user_id}: {e}")
    
    return render(request, 'users/del_user.html', {'user_id': user_id})


def run_query_user_view(request):
    """Query page displaying SQL query input with cyan Execute button."""
    default_query = 'select * from "User" natural join "Game"'
    query_presets = [
        ('All users', 'SELECT * FROM "User"'),
        ('Users from India', 'SELECT * FROM "User" WHERE country = \'india\''),
        ('Users ordered by age', 'SELECT * FROM "User" ORDER BY u_age DESC'),
        ('Users with games', 'SELECT * FROM "User" NATURAL JOIN "Game"'),
        ('Game catalogue', 'SELECT * FROM "Game"'),
        ('Insert demo user (ID 999999)', 'INSERT INTO "User" (user_id, user_name, country, u_age, pincode, city, passwords) VALUES (999999, \'Query Demo\', \'India\', 25, \'000000\', \'Demo City\', \'demo\')'),
        ('Update demo user (run insert first)', 'UPDATE "User" SET city = \'Updated City\' WHERE user_id = 999999'),
        ('Delete demo user (run insert first)', 'DELETE FROM "User" WHERE user_id = 999999'),
    ]
    return render(request, 'users/query.html', {
        'default_query': default_query,
        'query_presets': query_presets,
    })


@require_http_methods(['GET', 'POST'])
def process_custom_query_view(request):
    """
    Executes one read or data-manipulation SQL statement and renders its result.
    DDL and multi-statement input remain blocked to protect the schema.
    """
    query = request.POST.get('query', '').strip()
    if not query:
        query = request.GET.get('query', '').strip()

    if not query:
        query = 'select * from "User" natural join "Game"'

    upper_query = query.upper()
    statement_match = re.match(r'^\s*(SELECT|INSERT|UPDATE|DELETE)\b', upper_query)
    forbidden_keywords = ['DROP', 'ALTER', 'CREATE', 'TRUNCATE', 'REPLACE', 'ATTACH', 'DETACH', 'PRAGMA']
    has_forbidden_keyword = any(re.search(r'\b' + kw + r'\b', upper_query) for kw in forbidden_keywords)
    has_multiple_statements = ';' in query.rstrip(';')
    if not statement_match or has_forbidden_keyword or has_multiple_statements:
        error_message = (
            "Security restriction: only one SELECT, INSERT, UPDATE, or DELETE statement is allowed. "
            "Schema-changing commands and multiple statements are blocked."
        )
        return render(request, 'users/query_results.html', {
            'query': query,
            'error_message': error_message,
            'columns': [],
            'rows': [],
            'result_message': None,
        })

    columns = []
    rows = []
    error_message = None
    result_message = None
    statement_type = statement_match.group(1)

    try:
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(query)
                if statement_type == 'SELECT' and cursor.description:
                    columns = [col[0] for col in cursor.description]
                    rows = cursor.fetchall()
                elif statement_type == 'INSERT':
                    result_message = f'INSERT completed successfully. {cursor.rowcount} row(s) added.'
                elif statement_type == 'UPDATE':
                    result_message = f'UPDATE completed successfully. {cursor.rowcount} row(s) changed.'
                elif statement_type == 'DELETE':
                    result_message = f'DELETE completed successfully. {cursor.rowcount} row(s) removed.'
            if statement_type in {'INSERT', 'UPDATE', 'DELETE'}:
                sync_users_to_csv()
                result_message += ' users.csv synchronized.'
    except Exception as e:
        error_message = f"SQL Execution Error: {e}"

    context = {
        'query': query,
        'columns': columns,
        'rows': rows,
        'error_message': error_message,
        'result_message': result_message,
    }
    return render(request, 'users/query_results.html', context)


def export_csv_view(request):
    """Regenerates users.csv and downloads it as an attachment."""
    try:
        csv_file = sync_users_to_csv()
        if os.path.exists(csv_file):
            response = FileResponse(open(csv_file, 'rb'), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="users.csv"'
            return response
        else:
            return HttpResponse("CSV file not found.", status=404)
    except Exception as e:
        return HttpResponse(f"Error generating CSV: {e}", status=500)
