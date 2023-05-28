from django.template.loader import get_template
from ..models import User
from django import template
from ..user_functions import get_user

# Just so I know, the parent folder MUST be titled `templatetags` exactly or none of this works
# and there must be an empty __init__.py file at the same level as this file 

register = template.Library()

def user_form(request, target_user_id=None):
    context = {
        'user': get_user(request),
        'request': request,
    }
    if target_user_id is not None:
        try:
            target_user = User.objects.get(id=target_user_id)
            context["target_user"] = target_user
        except User.DoesNotExist:
            pass

    return context

user_form_template = get_template('ticket_easy_login_app_templates/tags/user-form.html')
register.inclusion_tag(user_form_template)(user_form)

