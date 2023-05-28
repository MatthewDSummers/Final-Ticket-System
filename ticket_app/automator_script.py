from .models import User, Ticket, CannedResponse, Message, Inbox, Category
import random

def start_automator(bot, ticket_id):
    try:
        ticket = Ticket.objects.all().get(id=ticket_id)
        print(ticket, "THIS IS THE TICKET")
    except Ticket.DoesNotExist:
        return
    else:

    # NO CONDITIONS (Bot has no "IF", "OR", or "AND" statements)
        if bot.condition == "":
            print(ticket_id, "DID THE NON-CONDITIONAL BOT GET THE TICKET ID???")
            setup_action(bot, ticket_id)
        else:
            if bot.condition == "category":
                try:
                    bot_condition = Category.objects.get(id=int(bot.condition_dependency))
                except Category.DoesNotExist:
                    return
                else:
                    ticket_aspect = ticket.category

            elif bot.condition == "priority":
                bot_condition = bot.condition_dependency
                ticket_aspect = ticket.priority

            elif bot.condition == "sender":
                try:
                    bot_condition = User.objects.all().get(id=int(bot.condition_dependency))
                except User.DoesNotExist:
                    return
                else:
                    ticket_aspect = ticket.sender

            elif bot.condition == "no_admin":
                bot_condition = None
                ticket_aspect = ticket.assigned.all()
                if not ticket_aspect:
                    ticket_aspect = None

            elif bot.condition == "unresolved":
                bot_condition = "Unresolved"
                ticket_aspect = ticket.status

    # ONLY FIRST CONDITION 
            if bot.condition_or == "" and bot.condition_inclusive == "":
                if ticket_aspect == bot_condition:
                    setup_action(bot, ticket_id)

    # "OR" CONDITION (no "and")
            elif bot.condition_or != "" and bot.condition_inclusive == "": 

                if bot.condition_or == "category":
                    try:
                        category_of_or_condition = Category.objects.get(id=int(bot.condition_or_dependency))
                    except:
                        return
                    else:
                        if ticket_aspect == bot_condition or ticket.category == category_of_or_condition:
                            setup_action(bot, ticket_id)

                elif bot.condition_or == "priority":
                    if ticket_aspect == bot_condition or ticket.priority == bot.condition_or_dependency:
                        setup_action(bot, ticket_id)

                elif bot.condition_or == "sender":
                    try:
                        sender = User.objects.all.get(id=int(bot.condition_or_dependency))
                    except:
                        return
                    else:
                        if ticket_aspect == bot_condition or ticket.sender == sender:
                            setup_action(bot, ticket_id)

                elif bot.condition_or == "no_admin":
                    if ticket_aspect == bot_condition or not ticket.assigned.all():
                        setup_action(bot, ticket_id)

                elif bot.condition_or == "unresolved":
                    if ticket_aspect == bot_condition or ticket.status == "Unresolved":
                        setup_action(bot, ticket_id)

    # "AND" STATEMENT (no "or")
            elif bot.condition_inclusive  != "" and bot.condition_or == "":

                # THIS IS REDUNDANT .. DO VALIDATION TO ENSURE A BOT LIKE THIS WOULDN'T BE CREATED, 
                # BUT SINCE I DON'T HAVE THE VALIDATION, HERE'S THIS 
                if bot.condition_inclusive == "category":
                    try:
                        category_of_and_condition = Category.objects.get(id=int(bot.condition_inclusive_dependency))
                    except:
                        return
                    else:
                        if ticket_aspect == bot_condition and ticket.category == category_of_and_condition:
                            setup_action(bot, ticket_id)

                if bot.condition_inclusive == "priority":
                    if ticket_aspect == bot_condition and ticket.priority == bot.condition_inclusive_dependency:
                        setup_action(bot, ticket_id)

                elif bot.condition_inclusive == "sender":
                    try:
                        sender = User.objects.all().get(id=int(bot.condition_inclusive_dependency))
                    except:
                        return
                    else:
                        if ticket_aspect == bot_condition and ticket.sender == sender:
                            setup_action(bot, ticket_id)

                elif bot.condition_inclusive == "no_admin":
                    if ticket_aspect == bot_condition and not ticket.assigned.all():
                        setup_action(bot, ticket_id)

                elif bot.condition_inclusive == "unresolved":
                    if ticket_aspect == bot_condition and ticket.status == "Unresolved":
                        setup_action(bot, ticket_id)

# FILTER SETUP MORE 
def setup_action(bot, ticket_id):
    action = bot.then_action

    if bot.then_dependency != "":
        target = bot.then_dependency
    if action == "assign" or action == "priority" or action == "canned_response":
        take_action(bot, Ticket_ID = ticket_id, Target=target)
    elif action == "archive" or action == "hold":
        take_action(bot, Ticket_ID = ticket_id, Target="blank")


# FINALLY
def take_action(bot, *args, **kwargs):
    print("TAKE ACTION!")

    if kwargs['Target']:
        target = kwargs['Target']

    if kwargs['Ticket_ID']:
        ticket_id= kwargs['Ticket_ID']

    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return

    action = bot.then_action

    if action == "assign":
        try:
            person = User.objects.get(id=target)
        except User.DoesNotExist:
            return
        else:
            ticket.assigned.add(person)

    elif action == "priority":
        ticket.priority = target
        ticket.save()

    elif action == "archive":
        ticket.archived = True
        ticket.save()

    elif action == "hold":
        ticket.hold = "Hold"
        ticket.save()

    elif action == "canned_response":
        canned_id = target

        try:
            canned_response = CannedResponse.objects.get(id=canned_id)
        except CannedResponse.DoesNotExist:
            return
        else:
            person = None
            if bot.then_dependency_two == "to_sender":
                person = ticket.sender
                bot.send_canned_response(canned_response, person, ticket)
            else:
                if person is None:
                    try:
                        person = User.objects.get(id=bot.then_dependency_two)
                    except User.DoesNotExist:
                            return
                    else:
                        bot.send_canned_response(canned_response, person, ticket)
    return