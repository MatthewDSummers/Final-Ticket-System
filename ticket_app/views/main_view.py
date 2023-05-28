from .dependencies import *
from django.urls import reverse
##### TABLE OF CONTENTS 
# 1. Base URL
# 2. Homepage
# 3. Guide
# 4. Tickets
# 5. User stuff 
# 6. Category Stuff
# 7. Imagery 
# 8. Reports
# 9. Charts
# 10. General Info API
# 11. Bots 
# 12. Canned Responses 
# 13. Inbox Stuff
# 14. Teams
# 15. Tasks
from ..sanitize import bleachTicket


##### See if viewer is a user #####
# def get_user(request):
#     if 'user_id' in request.session:
#         user = User.objects.get(id=request.session['user_id'])
#         return user
#     else:
#         return False

def theError(request, error_message):
    request.session['message_status'] = "error"
    messages.error(request, error_message)
    return

##### BASE URL #####
def login_app(request): 
    return redirect('/users')

##### HOMEPAGE #####
@user_level_required(8,9)
def dashboard(request):

    user = get_user(request)

    user_websites = Website.objects.filter(user=user)
    web_len = len(user_websites)

    withheld = Ticket.objects.filter(hold="Hold").count()

    assigned = Ticket.objects.filter(assigned=user).filter(status="Unresolved").count()
    unassigned = Ticket.objects.filter(assigned=None).count()
    unset = Ticket.objects.filter(priority="Not Set").count()

    unresolved = Ticket.objects.filter(status="Unresolved").count()

    context = {
            "unassigned": unassigned,
            "unset": unset,
            "unresolved":unresolved,
            "assigned":assigned,
            "withheld":withheld,
            
            'user': get_user(request),
            "user_websites" : user_websites,
            "web_len" : web_len
    }
    return render(request, 'home.html', context)

## dashboard controls ##
@user_level_required(8,9)
def create_site(request):
    user = User.objects.get(id=request.session['user_id'])
    Website.objects.create(
        name = request.POST['name'],
        content = request.POST['website'],
        user = user
    )
    return redirect(reverse('ticket-easy:dashboard'))

@user_level_required(8,9)
def delete_site(request, website_id):
    website = Website.objects.get(id=website_id)
    website.delete()
    return redirect(reverse('ticket-easy:dashboard'))

##### GUIDE #####
@user_level_required(8,9)
def guide(request):
    return render(request, 'guide.html', context={'user':get_user(request)})


##### USER STUFF #####

## profile ##
@user_level_required(1,8,9)
def profile(request):
    # if get_user(request):
    user = get_user(request)
    my_tickets = Ticket.objects.filter(sender=user)
    withheld = my_tickets.filter(hold="Hold")
    unresolved = my_tickets.filter(status="Unresolved")
    resolved = my_tickets.filter(status="Resolved")

    context = {
            # 'now':now,
            # 'one_hour': one_hour,
            "withheld":withheld,
            "unresolved":unresolved,
            "resolved":resolved,
            "user":user,
            "my_tickets":my_tickets,
            # "MyMessages": my_messages,
            "page_title": "My Profile",
            # "unviewed": my_messages.filter(viewed=False).count()
    }
    # return render(request, 'user-profile.html', context)
    return render(request, 'profile.html', context)
    #     else:
    #         return redirect('/new_ticket')
    # else:
    #     return redirect('/users/signin')




##### CATEGORY STUFF #####

## category page ##
@user_level_required(8,9)
def category_page(request):
    context = {
        'user' : get_user(request),
        'categories': Category.objects.all()
    }
    return render(request, 'new-category.html', context)


## add category ##
@user_level_required(8,9)
def create_category(request):
    sanitized = bleachTicket(request)

    # Check if a category with the same name already exists
    existing_categories = Category.objects.filter(name=sanitized['category'])

    if not existing_categories.exists():
        # Create the category if it does not exist
        if sanitized["category"] != "":
            name = sanitized["category"]

            category = Category.objects.create(
                name=name
            )
            messages.info(request, f"Category {category.name} added")
            request.session['message_status'] = "success"
        return redirect(reverse('ticket-easy:category-page'))
    else:
        # Return an error message if the category already exists
        theError(request, "A category with that name already exists")
        return redirect(reverse('ticket-easy:category-page'))


## remove category ##
@user_level_required(8,9)
def delete_category(request):

    if request.POST['category_id'] != "":
        the_id = request.POST['category_id']

        category = Category.objects.get(id=the_id)
        messages.info(request, f"Category {category.name} removed")
        request.session['message_status'] = "success"
        category.delete()

    return redirect(reverse('ticket-easy:category-page'))




##### IMAGERY #####
# def upload(request):
# if request.method == "POST":
    # image = request.FILES['image']
    # print(pic.name)
    # fs = FileSystemStorage()
    # fs.save(image.name, image)

@user_level_required(9)
def delete_images(request):
    Image.objects.all().delete()
    return redirect('/')


##### GENERAL INFO #####
@user_level_required(8,9)
def get_info(request):
    if request.method == "POST":
        categories = {}

        if request.POST.get('option') == "category":
            cats = Category.objects.all()
            for index, item in enumerate(cats):
                categories[index] = f"{item.name}|{item.id}"
            categories['category'] = "category"


        elif request.POST.get('option') == "priority":
            for index, item in enumerate(['Low|Low', 'Intermediate|Intermediate', 'High|High', 'Crucial|Crucial']):
                categories[index] = item
            categories['priority'] = "priority"

        elif request.POST.get('option') == "sender":
            for index, item in enumerate(User.objects.all()):
                x = item.full_name
                categories[index] = f"{x}|{item.id}"
            categories['person'] = "person"

        elif request.POST.get('option') == "no_admin" or request.POST.get('option') == "archive" or request.POST.get('option') == "hold":
            return JsonResponse(categories)
        elif request.POST.get('option') == "assign":
            for index, item in enumerate(User.objects.filter(level=9)):
                x = item.full_name
                categories[index] = f"{x}|{item.id}"
            categories['person'] = "person"
        elif request.POST.get('option') == "notify" or "send_can" in request.POST.get('option'):
            for index, item in enumerate(User.objects.all()):
                x = item.full_name
                categories[index] = f"{x}|{item.id}"
            categories['person'] = "person"
        elif request.POST.get('option') == "canned_response":
                categories['person'] = "person"

                if len(CannedResponse.objects.all()) > 0:
                    for index, item in enumerate(CannedResponse.objects.all()):
                        x = item.name
                        categories[index] = f"{x}|send_can|{item.id}"
                else:
                    categories[0] = "No canned responses"
        return JsonResponse(categories)
    else:
        print("Can't get here")



##### BOTS #####
@user_level_required(8,9)
def automator(request):
    context = {
        'user': get_user(request),
    }

    if request.method == "POST":
        if 'name' in request.POST:
            name = request.POST['name']
        if 'when' in request.POST:
            when = request.POST['when']

        if when:
            bot = Automator.objects.create(
                name = name,
                event = when,
            )

            if 'condition-1' not in request.POST:
                # bot.save()
                print("non-conditional")
            else:
                bot.condition = request.POST['condition-one']
                if 'condition-one_supportive' in request.POST:
                    print("condition-one_supportive: ", request.POST["condition-one_supportive"])
                    bot.condition_dependency = request.POST['condition-one_supportive']
    # OR condition 
                if 'condition-or' in request.POST:
                    bot.condition_or = request.POST['condition-or']
                    if request.POST['condition-or_supportive']:
                        bot.condition_or_dependency= request.POST['condition-or_supportive']
    # AND condition 
                if 'condition-inclusive' in request.POST:
                    bot.condition_inclusive = request.POST['condition-inclusive']
                    if 'condition-inclusive_supportive' in request.POST:
                        bot.condition_inclusive_dependency = request.POST['condition-inclusive_supportive']
            if 'then' in request.POST:
                bot.then_action = request.POST['then']
                print(request.POST['then'], "this is canned?")
                if 'then_supportive' in request.POST:
                    bot.then_dependency = request.POST['then_supportive']
                    print(request.POST['then_supportive'], "this is then dep")

                    if 'then_supportive_supportive' in request.POST:
                        print(request.POST['then_supportive_supportive'], "this is then then then dep")

                        bot.then_dependency_two = request.POST['then_supportive_supportive']
                bot.save()

                print(bot.then_action)
                print("THE ACTION!!!!!!!!!!!!!!!!!!!!!!!!!")
            else:
                print("no action taken")
                # context['finished'] = "success"
            bot.save()
        else:
            print("no name")
    else:
        print("no")

        context['Then_Options'] = {'Assign':'assign', 'Notify':'notify', 'Change Priority To...':'priority', 'Archive Ticket':'archive', 'Put On Hold':'hold', 'Send Canned Response': 'canned_response'}
        context['If_Options'] = {'Category is...':'category', 'Priority is...':'priority', 'Sender is...':'sender', 'Ticket is unassigned':'no_admin', 'Ticket is unresolved':'unresolved'}
        context['When_Options'] = {'Ticket is created':'created', 'Ticket is put on Hold':'hold', 'Ticket is re-opened':'reopened', 'Ticket is Resolved':'resolved'}
            # 'Ticket exists for...':'pending'
    return render(request, 'new-automator.html', context)

@user_level_required(9)
def automator_delete(request, automator_id):
    bot = Automator.objects.get(id=automator_id)
    bot.delete()
    messages.info(request, "The automation has been deleted")
    request.session['message_status'] = "success"
    return redirect('/ticket-easy/automators/all')

@user_level_required(8,9)
def all_automators(request):
    context = {
    # 'please': x,
        'user': get_user(request),
        'all_bots': Automator.objects.all(),
        'Users': User.objects.all(),
        'Then_Options' : {'Assign':'assign', 'Notify':'notify', 'Change Priority To...':'priority', 'Archive Ticket':'archive', 'Put On Hold':'hold', 'Send Canned Response': 'canned_response'},
        'If_Options' : {'Category is...':'category', 'Priority is...':'priority', 'Sender is...':'sender', 'Ticket is unassigned':'no_admin', 'Ticket is unresolved':'unresolved'},
        'When_Options' : {'Ticket is created':'created', 'Ticket is put on Hold':'hold', 'Ticket is re-opened':'reopened', 'Ticket is Resolved':'resolved'}
    }
    context['all_bots'] = Automator.objects.all()
    context['categories'] = Category.objects.all()


    exclusions = [None, False, '']
    cans_and_notification_bots = Automator.objects.exclude(then_dependency_two__in=exclusions)
    for can in cans_and_notification_bots:
        print(can)
    cans_and_notification_user_ids = cans_and_notification_bots.values_list('then_dependency_two', flat=True)
    cans_and_notification_bot_users = User.objects.filter(id__in=cans_and_notification_user_ids)

    for user in cans_and_notification_bot_users:
        print(user)

    context["user_in_can_or_notification"] = cans_and_notification_bot_users

    if request.POST.get('ajax'):
        if request.POST.get('option') == "created":
            context['all_bots'] = Automator.objects.filter(event="created")
        elif request.POST.get('option') == "pending":
            context['all_bots'] = Automator.objects.filter(event="pending")
        elif request.POST.get('option') == "hold":
            context['all_bots'] = Automator.objects.filter(event="hold")
        elif request.POST.get('option') == "reopened":
            context['all_bots'] = Automator.objects.filter(event="reopened")
        elif request.POST.get('option') == "resolved":
            context['all_bots'] = Automator.objects.filter(event="resolved")

        if request.POST.get('option') == "assign":
            context['all_bots'] = Automator.objects.filter(event="created")
        elif request.POST.get('option') == "notify":
            context['all_bots'] = Automator.objects.filter(event="pending")
        elif request.POST.get('option') == "priority":
            context['all_bots'] = Automator.objects.filter(event="hold")
        elif request.POST.get('option') == "reopened":
            context['all_bots'] = Automator.objects.filter(event="reopened")
        elif request.POST.get('option') == "resolved":
            context['all_bots'] = Automator.objects.filter(event="resolved")
        return render(request, 'all-bots.html', context)

    else:


        return render(request, 'all-bots.html', context)




##### TEAMS #####
@user_level_required(8,9)
def teams(request):
    user = get_user(request)

    if request.GET.get('filter') == "add-member":
        team = Team.objects.all()

        context= {
            'user':user,
            'Teams': team,
            'team_members':User.objects.filter(level=9),
            'add_member':True,

            }
        return render(request, "teams.html", context)

    elif request.GET.get('filter') == "all":
        context= {
            'user':user,
            'team_members':User.objects.filter(level=9),
            'all_teams': Team.objects.all()
            }
        for team in Team.objects.all():
            print(team.name)
        return render(request, "teams.html", context)

    elif request.GET.get('filter') == "specific":
        team = Team.objects.get(name=request.GET.get('value'))
        context= {
            'user':user,
            'team_members':User.objects.filter(level=9),
            # 'all_teams': Team.objects.all(),
            'team': team,
            }
        if not request.GET.get('category'):
            context['tasks'] = True
        elif request.GET.get('category'):
            category = request.GET.get('category')
            if category == "Tasks":
                context['tasks'] = True
            elif category == "Members":
                context['members'] = True
            
        return render(request, "teams-ajax.html", context)

@user_level_required(8,9)
def new_team(request):
    user = get_user(request)
    context= {
        'user':user,
        'team_members':User.objects.filter(level=9),
        'new_team':True
        }

    if request.method == "POST":
        if not request.POST.get("adding-members"):
            team = Team.objects.create(
                name = request.POST['name'],
                description = request.POST['description']
            )
            messages.info(request, f"New team {team.name} added.")
            request.session['message_status'] = "success"
        else:
            team_name = request.POST.get("team")
            team = Team.objects.get(name=team_name)
            print(team)
            raw_members = json.loads(request.POST.get("members"))
            for x in raw_members:
                for member in User.objects.filter(level=9):
                    if member.id == int(x):
                        print(member.full_name)
                        team.members.add(member)
            team.save()

    return render(request, "teams.html", context)

##### TASKS #####
@user_level_required(8,9)
def tasks(request):
    context = {
        'user': get_user(request),
        'tickets': Ticket.objects.all()
    }

    if request.GET.get('filter') == "new":
        context['new_task'] = True
    return render(request, "tasks.html", context)


