from ..models import Inbox, Message, Reply
from login_app.models import User
from django.contrib import messages
# import random
# import string
# from ..management.commands.reset_message_urls import generate_unique_url
from ..models import generate_unique_url
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .dependencies import user_level_required, get_user, CannedResponse, MessageForm, timedelta, date, re, JsonResponse
from ..forms import ReplyForm
from ..sanitize import bleachMessage
from django.urls import reverse
from ..utils import paginate_it


def theError(request, error_message):
    request.session['message_status'] = "error"
    messages.error(request, error_message)
    return

def get_page_name(request):
    name = request.POST.get("page_title")
    return JsonResponse({'success':name})


# MESSAGE FORM SUBMIT
def create_message(request):
    context = create_the_message(request, "create")
    return render(request, "inbox-single-message.html", context)

# REPLY FORM SUBMIT 
def reply(request, message_id):
    context = create_the_message(request, "reply", message_id=message_id)
    return render(request, "inbox-single-message.html", context)


# CREATES A MESSAGE; RETURNS CONTEXT ONLY
def create_the_message(request, message_type="create", message_id=None):
    sanitized = bleachMessage(request)
    user = get_user(request)
    context = {
        "user": user,
        "no_dark_mode": True,
        # "page_title" : "Single Message",
        "message_exists": True,
    }

    try:
        original_message = Message.objects.get(id=message_id)
    except:
        original_message = None

    email_list = sanitized["emails"]
    recipients = User.objects.filter(email__in=email_list)

    existing_emails = [user.email for user in recipients]
    non_existing_emails = [email for email in email_list if email not in existing_emails]

    if not non_existing_emails:
        url = generate_unique_url()
        if message_type == "reply":
            try:
                original_message = Message.objects.get(id=message_id)

            except Message.DoesNotExist:
                # handle case where original message does not exist
                return HttpResponse("Error: Original message not found")
            else:
                message = Reply.objects.create(
                    body = sanitized["body"],
                    sender = user,
                    parent_message = original_message,
                ) 
                print(message, "JAPOSDIJFPOASDJIFPOSIJ  HH9999")
                # If a user is added to a reply who was not a recipient of the original message
                for new_recipient in recipients.exclude(id__in=original_message.recipients.all()):
                    new_recipient.inbox.messages.add(original_message)

                print(message, "the reply")

                context["single_message"] = original_message
        else:
            message = Message.objects.create(
                body = sanitized["body"],
                sender = user,
            )
            for recipient in recipients:
                message.recipients.add(recipient)
                recipient.inbox.messages.add(message)

            message.subject = sanitized["subject"]
            message.url = url

            context["single_message"] = message


        for recipient in recipients:
            message.recipients.add(recipient)
        message.save()

    else:
        context["no_recipients_found"] = True

        for an_email_address in non_existing_emails:
            theError(request, f'No users have the email "{an_email_address}". Please add a valid recipient.')

        theError(request, "(You must send the email to a registered user of Ticket Easy using the email they registered with)")
        context["the_body"] = sanitized["body"]

        if original_message is not None:
            context["single_message"] = original_message
        else:
            context["new_message"] = True
            context["message_exists"] = False

    return context


# COMPOSE PAGE 
def new_message_page(request):
    user = User.objects.get(id=request.session["user_id"])
    context = {
        "no_dark_mode": True,
        "user":user,
        # "page_title" : "New Message",
        "new_message" : True,
        "inbox_count": user.inbox.messages.exclude(id__in=user.inbox.trashed.all().values_list('id', flat=True)).count(),

        # "reply": False,
    }
    return render(request, "inbox-single-message.html", context)


# PAGE OF AN EXISTENT MESSAGE
@user_level_required(1,8,9)
def mail_single(request, inbox_id, message_url):
    message = Message.objects.get(url=message_url)
    for x in message.replies.all():
        print(x)
    inbox = Inbox.objects.get(id=inbox_id)
    inbox.viewed.add(message)
    print(inbox.trashed.all().count(), "trashed")
    user = get_user(request)
    

    context = {
        "no_dark_mode": True,
        "user":user,
        "single_message": message,
        "message_exists": True,
        "page_title" : "Single Message",
        "reply": True,
        "inbox_count": user.inbox.messages.exclude(id__in=user.inbox.trashed.all().values_list('id', flat=True)).count(),
    }
    try:
        Message.objects.filter(recipients=user)
    except:
        return redirect(reverse('ticket-easy:dashboard'))
    else:
        return render(request, "inbox-single-message.html", context)


##### INBOX PAGE #####
def return_mail(title, user):
    title_to_messages = {
        "Mail": user.inbox.messages.exclude(id__in=user.inbox.trashed.all().values_list('id', flat=True)),
        "Bookmarked": user.inbox.starred.all(),
        "Sent": user.sent.all(),
        "Trash": user.inbox.trashed.all()
    }
    return title_to_messages.get(title, title_to_messages["Mail"])


@user_level_required(1,8,9)
def mail(request):
    user = get_user(request)
    title = request.GET.get("title") if request.method == "GET" else request.POST.get("title")
    the_mail = return_mail(title, user)
    context = paginate_it(request, the_mail, "mail", 20, elided=True)

    context["no_dark_mode"] = True
    context["user"] = user
    context["page_title"] = title or "Mail"

    if request.method == "POST":
        action = request.POST["action"]
        inbox_id = request.POST["inbox_id"]
        message_id = request.POST["message_id"]
        message = Message.objects.get(id=message_id)
        inbox = Inbox.objects.get(id=inbox_id)

        print(action, " <--- THE ACTION IS")
        if action == "delete":
            inbox.trashed.add(message)
            inbox.starred.remove(message)
        elif action == "favorite":
            inbox.starred.add(message)
        elif action == "unfavorite":
            inbox.starred.remove(message)
        elif action == "destroy":
            message.delete()
        elif action == "mark_as_unread":
            inbox.viewed.remove(message)
        elif action == "mark_as_read":
            inbox.viewed.add(message)
        elif action == "restore":
            inbox.trashed.remove(message)
        previous_url = request.META.get('HTTP_REFERER')
        print(previous_url)
        return redirect(previous_url)

    context['inbox_count'] = the_mail.count() if title == "Mail" else return_mail("Mail", user).count()
    return render(request, "inbox.html", context)


##### CANNED RESPONSES #####
@user_level_required(8,9)
def canned_response(request):
    context = {
        'user': get_user(request),
        'Cans': CannedResponse.objects.all(),
        'DistributedCans': Message.objects.all(),
        'Senders': User.objects.all().filter(level=9)
    }

    if request.method == "POST":
        if request.POST.get('option') == "single":
            message_id = request.POST.get('message')
            message = Message.objects.get(id=message_id)
            message.viewed = True 
            message.save()
            context['single_message'] = message
            context['form'] = MessageForm(request.POST)
            return render(request, "inbox.html", context)
        else:

            sanitized  = bleachMessage(request)
            x = CannedResponse.objects.create(
                name = sanitized["name"],
                subject = sanitized["subject"],
                body = sanitized["body"],
                sender = User.objects.get(id=request.POST['admin-select'])
            )
            print(x, "did i make a message?", x.name + " " + x.body + " " + x.subject )
            context['form'] = MessageForm(request.POST)
        return render(request, "new-canned-response.html", context)
    else:
        context['form'] = MessageForm(request.POST)

        return render(request, "new-canned-response.html", context)