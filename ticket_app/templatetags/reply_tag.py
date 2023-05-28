from django.template.loader import get_template
from django import template
from ..models import Message
register = template.Library()
from ..forms import ReplyForm
# Just so I know, the parent folder MUST be titled `templatetags` exactly or none of this works
# and there must be an empty __init__.py file at the same level as this file 



# @register.simple_tag
# def reply_form(message_id):

#     return render_to_string('tags/inbox-reply-form.html')

# register.unregister('reply_form')

# register.simple_tag(name="reply_form")(None) 
# register.unregister_tag('reply_form')
# register.unregister_tag('reply_form')

def message_reply_form(message_id):
    # form = ReplyForm()
    single_message = Message.objects.get(id=message_id)

    context = {
        # "form" : form,
        'single_message': single_message
    }
    return context

reply_form_template = get_template('tags/inbox-reply-form.html')
register.inclusion_tag(reply_form_template)(message_reply_form)