from django.template.loader import get_template
from django import template
from ..models import Message
from login_app.user_functions import get_user
from ..views.inbox_view import return_mail
import re
from django.utils.html import strip_tags

register = template.Library()
# Just so I know, the parent folder MUST be titled `templatetags` exactly or none of this works
# and there must be an empty __init__.py file at the same level as this file 

def inbox_count(request, user):
    return return_mail("Mail", user).count()

def message_template(request):
    user = get_user(request)
    context={
        "no_dark_mode": True,
        "page_title" : "New Message",
        # "inbox_count": inbox_count(request, user)
    }

    print(inbox_count(request, user))
    print("did it print?")
    return context

message_page = get_template('tags/inbox-message-template.html')
register.inclusion_tag(message_page)(message_template)


def reply_template(request, message_id):
    message = Message.objects.get(id=message_id)
    user = get_user(request)
    context={
        "no_dark_mode": True,
        "page_title" : message.subject[:54]+ "...",
        "full_title": message.subject,
        "single_message": message,
        "user": user,
        # "inbox_count": inbox_count(request, user)
    }

    return context

reply_page = get_template('tags/inbox-reply-template.html')
register.inclusion_tag(reply_page)(reply_template)









@register.filter
def strip_html(value):
    """Removes all HTML tags from the given string."""
    return strip_tags(value)











# @register.simple_tag
# def reply_form(request):
#     return render_to_string('tags/inbox-reply-form.html')

# register.unregister('reply_form')


# def message_reply_form(request):
#     return {"use": True}

# reply_form_template  = get_template('tags/inbox-reply-form.html')
# register.inclusion_tag(reply_form_template )(message_reply_form)