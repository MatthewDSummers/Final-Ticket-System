from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator

import bcrypt

from .models import User
from ticket_app.models import Inbox

from .user_functions import get_user, if_not_logged_in, user_level_required
from .sanitize import bleachUser


def theInfo(request, info_message):
    request.session['message_status'] = "success"
    messages.info(request, info_message)
    return

def theError(request, error_message):
    request.session['message_status'] = "error"
    messages.error(request, error_message)
    return

def user_or_error(request, error_message=None):
    try:
        user = User.objects.get(id=request.session["user_id"])
    except:
        theError(request, error_message)
        return redirect(reverse('login-app:login-page'))
    return user

def kickedOut(request,message_type=None, message=None,):
    request.session.flush()
    if message_type == "error":
        theError(request, message)
    elif message_type == "info":
        theInfo(request, message)

    return redirect('/ticket-easy/users')

@if_not_logged_in
def index(request):
    return render(request, 'ticket_easy_login_app_templates/index.html')

def update_tabs(request):
    option = request.GET.get("option")
    # print(option[], "the otpion")
    if option == "tab-one":
        print(option)
        return render(request, "ticket_easy_login_app_templates/tab-one.html")
    if option == "tab-two":
        print(option)
        return render(request, "ticket_easy_login_app_templates/tab-two.html")
    if option == "tab-three":
        print(option)
        return render(request, "ticket_easy_login_app_templates/tab-three.html")

@if_not_logged_in
def register_user(request):
    errors = User.objects.validator(request.POST)

    if errors:
        for k, v in errors.items():
            messages.error(request, v)
        request.session['message_status'] = "error"
        return redirect(reverse('login-app:register-page'))
        
    elif len(User.objects.all()) < 1:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            level=9,
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash
        )
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            level = 1,
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash
        )
    inbox = Inbox.objects.create(user=user)
    print(inbox.user, "the user ")
    messages.info(request, "Welcome to the ticket app!  Please login! ")
    request.session['message_status'] = "success"
    return redirect(reverse('login-app:login-page'))

@if_not_logged_in 
def login(request):
    try:
        user = User.objects.get(email = request.POST['email'])
    except:
        request.session['message_status'] = "error"
        messages.error(request, "Incorrect email address or password")
        return redirect(reverse('login-app:login-page'))

    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session['user_id'] = user.id
        user.reset_failed_authorizations()

        if user.level == 1:
            return redirect(reverse('ticket-easy:new-ticket-page'))
        elif user.level == 9 or user.level == 8:
            return redirect(reverse('ticket-easy:dashboard'))
    else:
        request.session['message_status'] = "error"
        messages.error(request, "Incorrect email address or password")
        return redirect(reverse('login-app:login-page'))


def logout(request):
    request.session.flush()

    # if 'user_id' in request.session:
    #     del request.session['user_id']

    return redirect('/ticket-easy/users')

@if_not_logged_in
def reg_page(request):
    return render(request, 'ticket_easy_login_app_templates/register_page.html')

@if_not_logged_in
def signin_page(request):
    return render(request, 'ticket_easy_login_app_templates/signin_page.html')

@user_level_required(8,9)
def all(request):
    current_user=User.objects.get(id=request.session['user_id'])
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    the_users = User.objects.all()

    p = Paginator(the_users, 12)

    page_number = request.GET.get("page", 1)

    if int(page_number) > p.num_pages:
        page_number = int(page_number) # ?
        page_number = p.num_pages

    users = p.get_page(page_number)

    page_range =  p.get_elided_page_range(page_number, on_each_side=4, on_ends=1)

    context = {
        'user': user,
        'users': users,
        'current_user':current_user
    }

    context["page_range"] = p.get_elided_page_range(page_number, on_each_side=4, on_ends=1)
    context["page_range_length"] = len(list(page_range))
    context["page_number"] = page_number
    return render(request, 'users.html', context)

@user_level_required(8,9)
def change_user_permission_level(request, user_id):
    target_user = User.objects.get(id=user_id)
    decision = request.POST["decision"]
    previous_url = request.META.get('HTTP_REFERER')


    if decision == "Make Administrator":
        target_user.level = 8
        theInfo(request, f"{target_user.full_name} is now an Basic Administrator")
    elif decision == "Make Super-Administrator":
        target_user.level = 9
        theInfo(request, f"{target_user.full_name} is now a Super Administrator")
    elif decision == "Revoke Administrator":
        target_user.level = 1
        theInfo(request, f"{target_user.full_name} is now a Standard User")
        for ticket in target_user.assigned.all():
            ticket.assigned.remove(target_user)

    elif decision == "Revoke Super-Administrator":
    
        if User.objects.filter(level=9).count() != 1:
            theInfo(request, f"{target_user.full_name} is now an Basic Administrator")
            target_user.level = 8
        else:
            theError(request, f"This is the only Super-Admin account. There must remain at least one Super-Admin.")

    target_user.save()
    # print(target_user.level, "the level AFTER")

    return redirect(previous_url)


# @user_level_required(9)
# def delete_note(request, note_id, ticket_id):
#     # ticket_id = request.POST['ticket_id']
#     ticket = Ticket.objects.get(id=ticket_id)
#     note = Note.objects.get(id=note_id)
#     note.delete()
#     return redirect(f'home/ticket/{ticket.id}')


@user_level_required(1,8,9)
def delete_user(request, target_id):
    previous_url = request.META.get('HTTP_REFERER')
    user = user_or_error(request, error_message="You must be logged in to delete an account")

    try:
        target_user = User.objects.get(id=target_id)
    except:
        return kickedOut(request, message_type="error", message="Deletions must be done through the site's form. Please login to continue.")

    if bcrypt.checkpw(request.POST["password"].encode(), user.password.encode()):
        user.reset_failed_authorizations()

        if target_user.level == 9:
            if user.level == 9:
                if User.objects.filter(level=9).count() == 1:
                    theError(request, f"This is the only Super-Admin account.  There must remain at least one Super-Admin.")
                    return redirect(previous_url)
                else:
                    request.session['message_status'] = "success"
                    
                    target_user.delete()
                    if request.POST["which_account"] == "own_account":
                        return kickedOut(request, message_type="info", message="You have deleted your account")

                    elif request.POST["which_account"] == "not_own_account":
                        theInfo(request, "The user account has been deleted")
                        # return redirect(f'/ticket-easy/users/{user.id}')
                        return redirect(reverse('login-app:user-tickets', kwargs={'user_id': user.id}))

        else:
            if user.level == 1 and target_user != user:
                theError(request, f"This is not your account.")
                return redirect(previous_url)
            else:
                request.session['message_status'] = "success"
                target_user.delete()
                if request.POST["which_account"] == "own_account":
                    return kickedOut(request, message_type="info", message="You have deleted your account")

                elif request.POST["which_account"] == "not_own_account":
                    theInfo(request, "The user account has been deleted")
                    # return redirect(f'/ticket-easy/users/{user.id}')
                    return redirect(reverse('login-app:user-tickets', kwargs={'user_id': user.id}))
    else:
        if user.failed_authorization() == True:
            return kickedOut(request, message_type="error", message="Too many authorization attempts. Login again to continue.")
        else:
            request.session['message_status'] = "error"
            messages.error(request, "Incorrect password")

            return redirect(previous_url)

## new user ##
@user_level_required(8,9)
def new_user(request):
    context = {
        'user' : get_user(request)
    }
    if request.method == "POST":
        errors = User.objects.validator(request.POST)
        if errors:
            for k, v in errors.items():
                messages.error(request, v)
            request.session['message_status'] = "error"
            return render(request, 'ticket_easy_login_app_templates/user-edit-or-new.html', context)
        else:
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            new_user = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                level = 1,
                full_name = request.POST['first_name'] + " " + request.POST['last_name'],
                email = request.POST['email'],
                password = pw_hash
            )
            if 'admin-check' in request.POST:
                new_user.level = 8
                messages.info(request, f"New Admin {new_user.full_name} successfully created")
                request.session['message_status'] = "success"
            elif 'super-admin-check' in request.POST:
                new_user.level = 9
                messages.info(request, f"New Super Admin {new_user.full_name} successfully created")
                request.session['message_status'] = "success"
            else:
                new_user.level = 1
                messages.info(request, f"New user {new_user.full_name} successfully created")
                request.session['message_status'] = "success"
            new_user.save()

            Inbox.objects.create(user=new_user)

    return render(request, 'ticket_easy_login_app_templates/user-edit-or-new.html', context)


def edit_user(request, user_id):
    user = get_user(request)

    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        pass 
    else:
        context = {
            'user' : user,
            'target_user': target_user,
        }

        if request.method == "POST":
            errors = User.objects.validator(request.POST, form_type="Edit", authorizer=user, target_user=target_user)

            if errors:
                request.session['message_status'] = "error"
                for k, v in errors.items():
                    if k == 'too_many_attempts':
                        return kickedOut(request, message_type="error", message=v)
                    else:
                        messages.error(request, v)
                return redirect(f'/ticket-easy/users/edit/{target_user.id}')

            else:
                sanitized = bleachUser(request.POST)

                target_user.first_name = sanitized["first_name"]
                target_user.last_name = sanitized["last_name"]
                target_user.email = sanitized["email"]

                pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
                target_user.password = pw_hash

                if 'admin-check' in request.POST:
                    target_user.level = 8
                    theInfo(request, info_message=f"{target_user.full_name} is now a Staff member")
                elif 'super-admin-check' in request.POST:
                    target_user.level = 9
                    theInfo(request, info_message=f"{target_user.full_name} is now a Super-Admin")
                
                theInfo(request, info_message=f"{target_user.full_name} successfully edited")

                target_user.save()
                return redirect(reverse('login-app:edit-user', kwargs={'user_id': target_user.id}))

    return render(request, 'ticket_easy_login_app_templates/user-edit-or-new.html', context)