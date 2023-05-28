from .dependencies import *
# from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest
from ..signals import ticket_status_changed
from ..sanitize import bleachTicket
# from ..calendar_module import get_formatted_dates
from django.urls import reverse

from urllib.parse import urlparse
from django.http import QueryDict
# import sys

# from ..templatetags.ticket_tags import *
##### TICKETS #####

## create ticket ##

def create_ticket(request):
    user = get_user(request)
    context = { 
        'user': user,
        'categories': Category.objects.all()
    }


    if request.method == "POST":
        errors = Ticket.objects.validator(request.POST)

        if errors:
            for k, v in errors.items():
                messages.error(request, v)
            request.session['message_status'] = "error"
            return redirect(reverse('ticket-easy:new-ticket-page'))

        else:
            request.session['message_status'] = "success"
            messages.info(request, "Ticket submitted successfully")

            sanitized = bleachTicket(request)
            category = Category.objects.get(name=sanitized["category"])

            tick = Ticket.objects.create(
                sender = user,
                category = category,
                desc = sanitized['desc'],
            )

            if sanitized.get("priority"):
                tick.priority = sanitized["priority"]
                tick.save()

            # for bots in Automator.objects.all().filter(event="created"):
            #     if bots.enabled == True:
            #         bots.start(tick.id)


            if "image" in request.FILES:
                print(request.FILES['image'])
                Image.objects.create(
                        image=request.FILES['image'],
                        name=request.FILES['image'].name,
                        ticket=tick
                    )
    return render(request, "new_ticket.html", context)

## edit ticket page ##
@user_level_required(1,8,9)
def edit_ticket_page(request, ticket_id, user_id):
    ticket = Ticket.objects.get(id=ticket_id)
    sender = ticket.sender
    user = get_user(request)
    categories = Category.objects.values_list('name', flat=True)
    priorities = ["Not Set", "Low", "Intermediate", "High", "Crucial"]
    # one_hour_from_creation = ticket.created_at + timedelta(hours=1)
    if user.level == 1 and user != sender:
        print("ok")
        return redirect(reverse('ticket-easy:new-ticket-page'))
    context = {
        'categories':categories,
        'user': user,
        'ticket': ticket,
        'sender': sender,
        'priorities': priorities, 
    }

    return render(request, 'edit-ticket.html', context)

## edit ticket ##
# http://localhost:8000/edit_ticket_page/229/2
@user_level_required(1,8,9)
def edit_ticket(request, ticket_id, sender_id):
    ticket = Ticket.objects.get(id=ticket_id)
    sender = ticket.sender
    print(ticket.created_at)
    one_hour_from_creation = ticket.created_at + timedelta(hours=1)
    print(one_hour_from_creation)
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")
    time_limit = one_hour_from_creation.strftime("%d/%m/%Y %H:%M:%S")
    user = get_user(request)
    if user.level == 1:
        print("user level 1")

    if dt < time_limit:
        if 'cat' not in request.POST:
            ticket.priority = request.POST['prio']
            ticket.desc = request.POST['desc']
            ticket.save()
            return redirect(f'/profile/{sender.id}')

        cat = Category.objects.get(name=request.POST['cat'])
        if 'cat' in request.POST:
            ticket.priority = request.POST['prio']
            ticket.category = cat
            ticket.desc = request.POST['desc']
            ticket.save()
            return redirect(f'/profile')
    else:
        return redirect('ticket-easy:new-ticket-page')

## delete ticket ##
@user_level_required(1, 8,9)
def delete(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    user = get_user(request)
    if user.level == 1:
        if ticket.sender == user:
            ticket.delete()
    else:
        ticket.delete()

    url = request.POST.get('ticket_context_url', '/')
    print(url, " and of course this is the ticket context url")

    return redirect(url+"&ajax=ajax")


## assignment ##
@user_level_required(9)
def ticket_assignment_or_priority(request, ticket_id, admin_id=None, priority_option=None):

    ticket = Ticket.objects.get(id=ticket_id)
    type = request.POST["action-type"]
    previous_url = request.META.get('HTTP_REFERER')

    if type == "assign":
        admin = User.objects.get(id=admin_id)
        ticket.assigned.add(admin)
    elif type == "unassign":
        admin = User.objects.get(id=admin_id)
        ticket.assigned.remove(admin)
    elif type == "priority":
        ticket.priority = priority_option
    ticket.save()

    return redirect(previous_url)

## single ticket page ##
@user_level_required(1,8,9)
def ticket_page(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    # print(ticket.serialize)
    # if user.level == 9:
    ticket = Ticket.objects.get(id=ticket_id)
    sender = ticket.sender
    # sender = User.objects.filter(tickets=ticket_id)

    ticket_notes = Note.objects.filter(ticket=ticket_id)
    # 'time_limit' : one_hour_from_creation,
    context = {
        'notes': Note.objects.all(),
        'ticket':ticket,
        'images':Image.objects.filter(ticket=ticket.id),
        'sender':sender,
        'user':get_user(request),
        'admins':User.objects.filter(level=9),
        'tick_notes' : ticket_notes
    }
    return render(request, 'ticket.html', context)

# @user_level_required(1,8,9)
def profileTicketFilter(request, profile_page_user_id=None, table_variant=None):
    profile_page_user = User.objects.get(id=profile_page_user_id)
    print(profile_page_user.id, "HIS ID IS THIS ")

    tickets = Ticket.objects.all().filter(sender=profile_page_user)
    tickets = tickets.filter(hold="Hold") if table_variant == "Hold" else tickets
    tickets = tickets.filter(status="Resolved") if table_variant == "Resolved" else tickets
    tickets = tickets.filter(status="Unresolved") if table_variant == "Unresolved" else tickets
    return tickets

# @user_level_required(8,9)
def ticketFilter(request, page_type, table_variant=None, profile_page_user_id=None):
    print(page_type, "table type")
    print(table_variant, "table variant")
    print(profile_page_user_id, "profile page user id")
    # user = User.objects.get(full_name="Matthew Summers")
    # # for ticket in Ticket.objects.all():
    # #     ticket.assigned.remove(user)

    # user = User.objects.get(full_name="Matthew Summers")

    # for ticket in Ticket.objects.all():
    #     if ticket.id % 2 != 0:
    #         ticket.assigned.remove(user)
    #         # ticket.assigned.add(user)
    # assigned_tickets = Ticket.objects.filter(assigned=user)
    # # for i, ticket in enumerate(assigned_tickets):
    # for ticket in Ticket.objects.all():
    #     # if i % 2 != 0:
    #         ticket.status = "Unresolved"
    #         ticket.resolved_at = None 
    #         ticket.resolved_by = None
    #         ticket.save()
    user = get_user(request) 
    if user and user.level == 9 or user.level == 8:
        if profile_page_user_id is not None:
            print("we're filtering tickets for PROFILE from ticketFilter function")
            tickets = Ticket.objects.all().filter(assigned=User.objects.get(id=profile_page_user_id))
            tickets = tickets.filter(hold="Hold") if table_variant == "Hold" else tickets
            tickets = tickets.filter(status="Resolved") if table_variant == "Resolved" else tickets
            tickets = tickets.filter(status="Unresolved") if table_variant == "Unresolved" else tickets
            # print(tickets)
        elif page_type == "Active":
            tickets = Ticket.objects.exclude(archived=True).exclude(hold="Hold").exclude(status="Resolved")
        elif page_type == "Pinned":
            tickets = Ticket.objects.exclude(archived=True).filter(pinned="Pinned")
        elif page_type == "Archived":
            tickets = Ticket.objects.filter(archived=True)
        elif page_type == "Withheld":
            tickets = Ticket.objects.filter(hold="Hold")
        elif page_type == "Resolved":
            tickets = Ticket.objects.exclude(archived=True).filter(status="Resolved")
            print("holding")
        return tickets
    else:
        return False





def getTicketContext(request, the_type, table_variant=None, profile_page_user_id=None):

    user = get_user(request)

    context = {
        'pinned': Ticket.objects.filter(pinned="Pinned"),
        'categories': Category.objects.all(),
        'Admins': User.objects.filter(level=9),
        'user': user,
    }

    page_number = request.GET.get('page', 1)
    which_page = "" if profile_page_user_id is None else f"users/{profile_page_user_id}"
    context['which_type'] = the_type


    # GET THE TICKETS 
    if the_type == "Assigned":
        tickets = ticketFilter(request, the_type, table_variant=table_variant, profile_page_user_id=profile_page_user_id)
        context['tag_filter'] = table_variant
        context['profile_page'] = True
    elif the_type == "Sent":
        tickets = profileTicketFilter(request, table_variant=table_variant, profile_page_user_id=profile_page_user_id)
        context['tag_filter'] = table_variant
        context['profile_page'] = True

    else:
        tickets = ticketFilter(request, the_type, table_variant=table_variant, profile_page_user_id=None)
        context['tag_filter'] = the_type


    if request.GET.get('not_main_page'):
        context['not_main_page'] = True

    if tickets != False:
        print("authorized")
###  FILTER THE TICKETS 
    # < FILTERED RESULTS >
        if 'filter' in request.GET:
            the_filter = request.GET.get('filter')
            the_value = request.GET.get('value')

        ## BY ID

            if the_filter == "ID":
                option = the_value
                context["not_main_page"] = True
                if option.isnumeric():
                    print("numeric")
                    option = int(option)
                    tickets = tickets.filter(id=option)
                    context['title'] = f"Ticket number {option}"
                    context['searched'] = f"with an ID of {option}"
                    page_number = 1

        ### DATES
            if the_filter == "Date":
                if "to" in the_value:
                    date_list = the_value.split("to")
                    aware_dates = get_aware_date(date_list[0], date_list[1])
                    tickets = tickets.filter(created_at__range=aware_dates)
                    # i could also use relativedelta or arrow, i suppose.
                    formatted_date = get_formatted_dates(date_list)
                    context["title"] = f"Results for {formatted_date[0]} - {formatted_date[1]}" if tickets.count() > 1 else f"Result for {formatted_date[0]} - {formatted_date[1]}"
                    context["searched"] = f"between {formatted_date[0]} and {formatted_date[1]}"

                else:
                    tickets = tickets.filter(created_at__date=the_value)

                    formatted_date = get_formatted_dates(the_value)
                    context["searched"] = f"for {formatted_date[0]}"
                    context["title"] = f"Results for {formatted_date[0]}" if tickets.count() > 1 else f"Result for {formatted_date[0]}"

        ### PRIORITIES
            elif the_filter == "Priority":
                tickets = tickets.filter(priority=the_value)
                # context['title'] = f"{the_value} Priority"
                # context['searched'] = f"{the_value} Priority"

        ### ASSIGNMENT
            elif the_filter == "Assignment":
                if the_value == "Unassigned":
                    tickets = tickets.filter(assigned=None)

                elif the_value == "Assigned":
                    tickets = tickets.exclude(assigned=None)

                else:
                    tickets = tickets.filter(assigned__full_name__icontains=the_value)
                    # case insensitive search 
                context['title'] = f"{the_value} Tickets" if the_value == "Unassigned" or the_value == "Assigned" else f"Tickets for {the_value}"
        ### STATUS
            elif the_filter == "Status":
                if the_value == "Withheld":
                    context['title'] = f"{the_value} Status"
                    context['searched'] = "are withheld"

                elif the_value == "Archived":
                    context['title'] = f"{the_value} Tickets"
                    context['searched'] = "have been archived"

                else:
                    tickets = tickets.filter(status=the_value)
                    context['title'] = f"{the_value} Status"

        ### CATEGORIES
            elif the_filter == "Category":
                tickets = tickets.filter(category__name=the_value)
                # for t in tickets:
                #     print (t.status)
                #     print (t.category.name)
                #     user = t.assigned.first().full_name
                #     print (user)
                context['title'] = f"Tickets for {the_value}"

        ### DESCRIPTION
            elif the_filter == "Desc":
                tickets = tickets.filter(desc__contains=the_value)
                context['title'] = f'Tickets containing "{the_value}"'
                page = 1

        ### BY ID
            elif the_filter == "OrderID":
                tickets = tickets.order_by("id") if the_value == "Ascending" else tickets.order_by("-id")
                context['title'] = f'Tickets in {the_value} Order'

            p = Paginator(tickets, 12)

            if int(page_number) > p.num_pages:
                page_number = int(page_number)
                page_number = p.num_pages
            all_tickets = p.get_page(page_number)
            page_number_next = int(page_number) + 1
            page_number_previous = int(page_number) - 1
            page_range =  p.get_elided_page_range(page_number, on_each_side=4, on_ends=1)
            context["page_range"] = p.get_elided_page_range(page_number, on_each_side=4, on_ends=1)
            context["page_range_length"] = len(list(page_range))


            if profile_page_user_id is None:
                context['elided_page_number'] = reverse('ticket-easy:tickets') + f"?type={the_type}&filter={the_filter}&value={the_value}&page="
                context['next_url'] = reverse('ticket-easy:tickets') + f"?type={the_type}&filter={the_filter}&value={the_value}&page={page_number_next}"
                context['previous_url'] = reverse('ticket-easy:tickets') + f"?type={the_type}&filter={the_filter}&value={the_value}&page={page_number_previous}"
            else:
                context['elided_page_number'] = reverse('login-app:user-tickets', kwargs={'user_id': profile_page_user_id}) + f"?type={the_type}&filter={the_filter}&value={the_value}&table_variant={table_variant}&page="
                print(context['elided_page_number'])
                print("DID THE LINK PRINT?????????")
                context['next_url'] = reverse('login-app:user-tickets', kwargs={'user_id': profile_page_user_id}) + f"?type={the_type}&filter={the_filter}&value={the_value}&table_variant={table_variant}&page={page_number_next}"
                context['previous_url'] = reverse('login-app:user-tickets', kwargs={'user_id': profile_page_user_id}) + f"?type={the_type}&filter={the_filter}&value={the_value}&table_variant={table_variant}&page={page_number_previous}"
            context["ticket_context_url"] = context['elided_page_number'] + str(page_number)
            # if profile_page_user_id is None:
            #     context['elided_page_number'] = reverse('ticket-easy:tickets') + f"{which_page}?type={the_type}&filter={the_filter}&value={the_value}&page="
            #     context['next_url'] = reverse('ticket-easy:tickets') + f"{which_page}?type={the_type}&filter={the_filter}&value={the_value}&page={page_number_next}"
            #     context['previous_url'] = reverse('ticket-easy:tickets') + f"{which_page}?type={the_type}&filter={the_filter}&value={the_value}&page={page_number_previous}"
            # else:
            #     context['elided_page_number'] = reverse('ticket-easy:tickets') + f"{which_page}?type={the_type}&filter={the_filter}&value={the_value}&table_variant={table_variant}&page="
            #     context['next_url'] = reverse('ticket-easy:tickets') + f"{which_page}?type={the_type}&filter={the_filter}&value={the_value}&table_variant={table_variant}&page={page_number_next}"
            #     context['previous_url'] = reverse('ticket-easy:tickets') + f"{which_page}?type={the_type}&filter={the_filter}&value={the_value}&table_variant={table_variant}&page={page_number_previous}"
            # context["ticket_context_url"] = context['elided_page_number'] + str(page_number)

        else:

            # for t in Ticket.objects.all():
            #     if t.id % 2 == 0:
            #         t.status = "Resolved"
            #         t.save()
            p = Paginator(tickets, 12)

            if int(page_number) > p.num_pages:
                page_number = int(page_number)
                page_number = p.num_pages
            all_tickets = p.get_page(page_number)
            page_number_next = int(page_number) + 1
            page_number_previous = int(page_number) - 1
            page_range =  p.get_elided_page_range(page_number, on_each_side=4, on_ends=1)
            context["page_range"] = p.get_elided_page_range(page_number, on_each_side=4, on_ends=1)
            context["page_range_length"] = len(list(page_range))

            # if not page_number_next:
            #     print("no page number next")
            #     page_number_next = 1
            # if not page_number_previous:
            #     page_number_previous = 1

            # if profile_page_user_id is None:
            #     context['elided_page_number'] = reverse('ticket-easy:tickets') + f"{which_page}?type={the_type}&page="
            #     context['next_url'] = reverse('ticket-easy:tickets') + f"{which_page}?type={the_type}&page={page_number_next}"
            #     context['previous_url'] = reverse('ticket-easy:tickets') + f"{which_page}?type={the_type}&page={page_number_previous}"
            # else:
            #     context['elided_page_number'] = reverse('ticket-easy:tickets') + f"{which_page}?type={the_type}&table_variant={table_variant}&page="
            #     context['next_url'] = reverse('ticket-easy:tickets') + f"{which_page}?type={the_type}&table_variant={table_variant}&page={page_number_next}"
            #     context['previous_url'] = reverse('ticket-easy:tickets') + f"{which_page}?type={the_type}&table_variant={table_variant}&page={page_number_previous}"
            if profile_page_user_id is None:
                context['elided_page_number'] = reverse('ticket-easy:tickets') + f"?type={the_type}&page="
                context['next_url'] = reverse('ticket-easy:tickets') + f"?type={the_type}&page={page_number_next}"
                context['previous_url'] = reverse('ticket-easy:tickets') + f"?type={the_type}&page={page_number_previous}"
            else:
                context['elided_page_number'] = reverse('login-app:user-tickets', kwargs={'user_id': profile_page_user_id}) + f"?type={the_type}&table_variant={table_variant}&page="
                context['next_url'] = reverse('login-app:user-tickets', kwargs={'user_id': profile_page_user_id}) + f"?type={the_type}&table_variant={table_variant}&page={page_number_next}"
                context['previous_url'] = reverse('login-app:user-tickets', kwargs={'user_id': profile_page_user_id}) + f"?type={the_type}&table_variant={table_variant}&page={page_number_previous}"
        context['tickets'] = all_tickets

        context["ticket_context_url"] = context['elided_page_number'] + str(page_number)
        print(context["ticket_context_url"], "i have you now")

        if tickets.count() < 1:
            context["title"] = ""
        return context
    else:
        return None


@user_level_required(1,8,9)
def all_tickets(request, user_id = None):
    # user = User.objects.get(id=1)
    # user.level = 9
    # user.save()


    the_type = request.GET.get('type')
    table_variant = request.GET.get('table_variant', None)
    profile_page_user_id = request.resolver_match.kwargs.get('user_id') if request.resolver_match.kwargs.get('user_id') else None

    if the_type not in ['Active', 'Sent', 'Assigned', 'Pinned', 'Archived', 'Withheld', 'Profile', 'Resolved']:
        context = {"user": get_user(request)}
        return render(request, 'error.html', {'error_message': 'Invalid request'}, status=400)

    if 'ajax' in request.GET:

        context = getTicketContext(request, the_type, table_variant=table_variant, profile_page_user_id=user_id)

        return render(request, 'tags/tickets-table-tag.html', context)
    else:

        context = {
            'user': get_user(request)
        } 
        context['tag_filter'] = the_type

        if the_type == "Active":
            context['grand_title'] = "Active Tickets"
        elif the_type == "Withheld":
            context['grand_title'] = "Withheld Tickets"
        elif the_type == "Archived":
            context['grand_title'] = "Archived Tickets"
        elif the_type == "Pinned":
            context['grand_title'] = "Pinned Tickets"
        elif the_type == "Resolved":
            context['grand_title'] = "Resolved Tickets"

        if the_type in ['Active', 'Pinned', 'Archived', 'Withheld', 'Resolved']:
            return render(request, "all-tickets.html", context)
        elif the_type in ['Sent', 'Assigned', 'Profile']:
            context['profile_page'] = True
            profile_page_user_id = request.resolver_match.kwargs.get('user_id') if request.resolver_match.kwargs.get('user_id') else None
            print(profile_page_user_id, "this is the profile page user id that is initally being returned and returning the html userpage.html")
            context["sender"] = User.objects.get(id=profile_page_user_id)
            return render(request, "user_page.html", context)


## notes for tickets ##
@user_level_required(8,9)
def new_note(request, ticket_id):
    user = User.objects.get(id=request.session['user_id'])
    ticket = Ticket.objects.get(id=ticket_id)
    sender = User.objects.filter(tickets=ticket_id)
    notes = Note.objects.all()


    Note.objects.create(
    name = request.POST['note_name'],
    creator = user,
    ticket = ticket,
    content = request.POST['note'],
    )

    context = {
        'notes':notes,
        'ticket':ticket,
        'sender':sender,
        'user':user
    }
    return redirect(reverse('ticket-easy:single-ticket', kwargs={'ticket_id': ticket.id}), context)

@user_level_required(8,9)
def delete_note(request, note_id, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    note = Note.objects.get(id=note_id)
    user = get_user(request)
    # check that other admins cant delete other admins notes unless super admin 
    note.delete()
    return redirect(reverse('ticket-easy:single-ticket', kwargs={'ticket_id': ticket.id}))

    # return render(request, 'ticket.html')
    

@user_level_required(8,9)
def archive(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if "archive" == request.POST.get("method"):
        ticket.archived = True
        ticket.hold = ""
    elif "unarchive" == request.POST.get("method"):
        ticket.archived = False
    ticket.save()

    url = request.POST.get('ticket_context_url', '/')
    print(url, " and of course this is the ticket context url")

    return redirect(url+"&ajax=ajax")

## resolve ##
# @user_level_required(8,9)
# def resolve(request, ticket_id):
#     ticket = Ticket.objects.get(id=ticket_id)
#     user = get_user(request)

#     if ticket.first_resolved_at == None:
#         ticket.first_resolved_at = datetime.now()
#     if ticket.first_resolved_by == None:
#         ticket.first_resolved_by = user

#     ticket.hold = ""
#     ticket.status = "Resolved"
#     ticket.resolved_at = datetime.now()
#     ticket.resolved_by = user
#     ticket.save()
#     ticket_status_changed.send(Ticket, ticket=ticket.id, status="Resolved")

#     return redirect(reverse('ticket-easy:single-ticket', kwargs={'ticket_id': ticket.id}))


## unresolve ##
# @user_level_required(8,9)
# def unresolve(request, ticket_id):
#     ticket = Ticket.objects.get(id=ticket_id)
#     ticket.status = "Unresolved"
#     ticket.resolved_by = None
#     ticket.resolved_at = None
#     ticket.save()
#     # ticket_status_changed.send(Ticket, ticket=ticket.id, status="Reopened")

#     return redirect(reverse('ticket-easy:single-ticket', kwargs={'ticket_id': ticket.id}))


## pin ##
@user_level_required(8,9)
def pin(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if "pin" == request.POST.get("method"):
        ticket.pinned = "Pinned"
    elif "unpin" == request.POST.get("method"):
        ticket.pinned = "Unpinned"
    ticket.save()

    url = request.POST.get('ticket_context_url', '/')

    return redirect(url+"&ajax=ajax")
    # return render(request, "tags/tickets-table-tag.html")

## hold ##
@user_level_required(8,9)
# def hold(request, ticket_id):
def status_change(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    action = request.POST.get("method") 

    # ticket.reopened = False if request.POST.get("method") == "hold" else True
    # ticket.hold = "Hold" if request.POST.get("method") == "hold" else ""

    if action == "hold":
        status = "Hold"

        ticket.hold = "Hold"
        ticket.status = "Unresolved"
        ticket.archived = False

    elif action == "reopened":
        status = "Reopened"

        ticket.hold = ""

    elif action == "unresolve":
        status = "Reopened"

        ticket.status = "Unresolved"
        ticket.resolved_by = None
        ticket.resolved_at = None

    elif action == "resolve":
        status = "Resolved"
        user = get_user(request)

        if ticket.first_resolved_at == None:
            ticket.first_resolved_at = datetime.now()
        if ticket.first_resolved_by == None:
            ticket.first_resolved_by = user
        # ticket.assigned.clear() # don't do this. 

        ticket.hold = ""
        ticket.status = "Resolved"
        ticket.resolved_at = datetime.now()
        ticket.resolved_by = user
    ticket.save()

    ticket_status_changed.send(Ticket, ticket=ticket.id, status=status)

    if action == "hold" or action == "reopened":
        url = request.POST.get('ticket_context_url', '/')
        return redirect(url+"&ajax=ajax")
    else:
        return redirect(reverse('ticket-easy:single-ticket', kwargs={'ticket_id': ticket.id}))

    # for bot in Automator.objects.filter(event="hold"):
    #     bot.start(ticket_id)
    # return redirect(request.POST.get('url', '/'))
