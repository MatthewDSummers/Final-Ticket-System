from .dependencies import *
from django.urls import reverse
##### TABLE OF CONTENTS 
from django.db.models import Q
from ..sanitize import bleachAutomator
from ..models import MissingFieldError

def theError(request, error_message):
    request.session['message_status'] = "error"
    messages.error(request, error_message)
    return


##### INFO FOR SELECTS #####
@user_level_required(9)
def get_info(request):
    # for bot in Automator.objects.all():
    #     bot.delete()

    if request.method == "GET":
        option = request.GET.get("option")
        categories = {"options": {}}
        empty_set = None

        if option == "category":
            cats = Category.objects.all()
            if cats.count() > 1:
                for item in cats:
                    categories["options"][item.name] = item.id
            else:
                empty_set = "No Categories"

        elif option == "priority":
            for item in ['Low', 'Intermediate', 'High', 'Crucial']:
                categories['options'][item] = item

        elif option == "sender":
            for item in User.objects.all():
                categories["options"][item.full_name] = item.id

        elif option == "send_can":
            for item in User.objects.all():
                categories["options"]["To Sender"] = "to_sender"
                categories["options"][f"To {item.full_name}"] = item.id

        elif option == "assign":
            admins = User.objects.filter(Q(level=8) | Q(level=9))
            for item in admins:
                categories["options"][item.full_name] = item.id

        elif option == "canned_response":
            if CannedResponse.objects.all().count() > 0:
                for item in CannedResponse.objects.all():
                    categories["options"][item.name] = item.id
                    categories["options"]["send_can"] = "send_can"
            else:
                empty_set = "No Canned Responses"

        if empty_set:
            categories["options"]["empty_set"] = empty_set

        return JsonResponse(categories)
    else:
        return JsonResponse({})


##### BOTS #####
def bots_context(request):
    context = {
        'user': get_user(request),
        'Then_Options': {'Assign':'assign', 'Change Priority To...':'priority', 'Archive Ticket':'archive', 'Put On Hold':'hold', 'Send Canned Response': 'canned_response'},
        'If_Options': {'Category is...':'category', 'Priority is...':'priority', 'Sender is...':'sender', 'Ticket is unassigned':'no_admin', 'Ticket is unresolved':'unresolved'},
        'When_Options': {'Ticket is created':'created', 'Ticket is put on Hold':'hold', 'Ticket is re-opened':'reopened', 'Ticket is Resolved':'resolved'},
    }
    return context

@user_level_required(9)
def automator(request):
    context = bots_context(request)
    sanitized = bleachAutomator(request.POST)

    # IF NO CONDITION-ONE supportive but have condition-one, IT'S THROWING AN ERROR 
    if request.method == "POST":
        try:
            errors = Automator.objects.validator(sanitized)
            if errors:
                for k, v in errors.items():
                    messages.error(request, v)
                request.session['message_status'] = "error"
                # return redirect(reverse('ticket-easy:new-automator'))
                return render(request, 'new-automator.html', context)

            else:
                bot = Automator.objects.create(
                    name = sanitized["name"],
                    event = sanitized["when"],
                    condition = sanitized["condition-one"],
                    condition_dependency = sanitized["condition-one_supportive"],
                    condition_or = sanitized["condition-or"],
                    condition_or_dependency = sanitized["condition-or_supportive"],
                    condition_inclusive = sanitized["condition-inclusive"],
                    condition_inclusive_dependency = sanitized["condition-inclusive_supportive"],
                    then_action = sanitized["then"],
                    then_dependency = sanitized["then_supportive"],
                    then_dependency_two = sanitized["then_supportive_additional"]
                )
                request.session['message_status'] = "success"
                messages.info(request, f'Automator "{bot.name}" created successfully')
        except MissingFieldError:
            return render(request, 'error.html', {'error_message': 'Invalid request'}, status=400)

    return render(request, 'new-automator.html', context)

@user_level_required(9)
def automator_delete(request, automator_id):
    bot = Automator.objects.get(id=automator_id)
    bot.delete()
    messages.info(request, "The automation has been deleted")
    request.session['message_status'] = "success"
    return redirect('/ticket-easy/automators/all')

@user_level_required(9)
def all_automators(request):
    admin_levels = [8, 9]
    context = {
    # 'please': x,
        'user': get_user(request),
        'all_bots': Automator.objects.all(),
        'Users': User.objects.all(),
        'Admins': User.objects.filter(level__in=admin_levels),
        'Then_Options' : {'Assign':'assign', 'Change Priority To...':'priority', 'Archive Ticket':'archive', 'Put On Hold':'hold', 'Send Canned Response': 'canned_response'},
        'If_Options' : {'Category is...':'category', 'Priority is...':'priority', 'Sender is...':'sender', 'Ticket is unassigned':'no_admin', 'Ticket is unresolved':'unresolved'},
        'When_Options' : {'Ticket is created':'created', 'Ticket is put on Hold':'hold', 'Ticket is re-opened':'reopened', 'Ticket is Resolved':'resolved'}
    }
    context['all_bots'] = Automator.objects.all()
    context['categories'] = Category.objects.all()


    # exclusions = [None, False, '']
    # can_bots = Automator.objects.exclude(then_dependency_two__in=exclusions)



    # MAKE A DICTIONARY `canned_responses` FOR THE CUSTOM FILTER `get_item` IN THE TEMPLATE 
        # get_item function is located in utility_tags.py in the templatetags in ticket_app

    can_bots = Automator.objects.filter(then_action="canned_response")

    canned_responses = {}

    for bot in can_bots:
        the_can = CannedResponse.objects.get(id=int(bot.then_dependency))
        canned_responses[bot.then_dependency] = {"name": the_can.name, "id": the_can.id}

        # {% with canned_message=canned_responses|get_item:bot.then_dependency  %}
        # <!-- Display the name and ID of the canned message -->
        #     <select id="then" class="bot-{{bot.id}}" data-select data-border="radius">
        #                 <option selected value={{canned_message.id}}>Send canned response "{{ canned_message.name }}" to 
        #                     {% for person in users_in_can %}
        #                         {{person.full_name}}{{forloop.counter|lengthify:users_in_can}}
        #                     {% endfor %}
        #                 </option>

        #         {% for key, value in Then_Options.items %}
        #             {% if key != "Notify" %}
        #                 <option value="{{value}}">{{key}}</option>
        #             {% endif %}
        #         {% endfor %}
        #     </select>
        # {% endwith %}


    #List of all the CannedResponse ID's from the can_bots
    can_user_ids = can_bots.values_list('then_dependency_two', flat=True)
    # All users who are associated to receiving Canned Responses 
    can_bot_users = User.objects.filter(id__in=can_user_ids)


# this is cool too. it's located at the top of the all_bots page and utilizes a function from utility_tags called listify 
    # context["test_list_one"] = ["Jim"]
    # context["test_list_two"] = ["Jim", "Sally"]
    # context["test_list_three"] = ["Jim", "Sally", "John"]
    # context["test_list_four"] = ["Jim", "Sally", "John", "Martha"]
    # context["test_list_five"] = ["Jim", "Sally", "John", "Martha", "Dave"]
    # context["test_list_six"] = [1]
    # context["test_list_seven"] = [1, 2]
    # context["test_list_eight"] = [1, 2, 3]
    # context["test_list_nine"] = [1, 2, 3, 4]
    # context["test_list_ten"] = [1, 2, 3, 4, 5]

    # ^ it returns commas and ampersand where relevant 

    context["canned_responses"] = canned_responses
    context["all_bots"] = Automator.objects.all()
    context["users_in_can"] = can_bot_users

    if request.GET.get('ajax'):
        if request.GET.get('option') == "created":
            context['all_bots'] = Automator.objects.filter(event="created")
        elif request.GET.get('option') == "pending":
            context['all_bots'] = Automator.objects.filter(event="pending")
        elif request.GET.get('option') == "hold":
            context['all_bots'] = Automator.objects.filter(event="hold")
        elif request.GET.get('option') == "reopened":
            context['all_bots'] = Automator.objects.filter(event="reopened")
        elif request.GET.get('option') == "resolved":
            context['all_bots'] = Automator.objects.filter(event="resolved")

        if request.GET.get('option') == "assign":
            context['all_bots'] = Automator.objects.filter(event="created")
        elif request.GET.get('option') == "notify":
            context['all_bots'] = Automator.objects.filter(event="pending")
        elif request.GET.get('option') == "priority":
            context['all_bots'] = Automator.objects.filter(event="hold")
        elif request.GET.get('option') == "reopened":
            context['all_bots'] = Automator.objects.filter(event="reopened")
        elif request.GET.get('option') == "resolved":
            context['all_bots'] = Automator.objects.filter(event="resolved")
        return render(request, 'all-bots.html', context)

    else:
        return render(request, 'all-bots.html', context)