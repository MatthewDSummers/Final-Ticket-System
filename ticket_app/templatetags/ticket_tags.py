from django.template.loader import get_template
from ..models import Category
from django import template
from login_app.models import User
from django.core.paginator import Paginator
from ..views.ticket_view import ticketFilter, getTicketContext
register = template.Library()
# Just so I know, the parent folder MUST be titled `templatetags` exactly or none of this works
# and there must be an empty __init__.py file at the same level as this file 

def tickets_table(request, page_type, table_variant=None):
# def tickets_table(request, page_type, page_number, table_variant=None):
    # print( "HELLLLLLO")
    profile_page_user_id = request.resolver_match.kwargs.get('user_id') if request.resolver_match.kwargs.get('user_id') else None
    print(profile_page_user_id, " profile iD??")
    context = getTicketContext(request, page_type, table_variant=table_variant, profile_page_user_id=profile_page_user_id)
    context["request"] = request
    # context = getTicketContext(request, page_type, table_variant=table_variant, profile_page_user_id=profile_page_user_id, page_number=page_number)
    return context
tickets_table_template = get_template('tags/tickets-table-tag.html')
register.inclusion_tag(tickets_table_template)(tickets_table)
