# recursively sift through the body and subject 
# recursively sift through the body and subject 
# recursion
# recursion
def filter_email(email, ticket, full=False, repeat=False):
    message = email.subject if repeat == True else email.body

    if "{sender.full_name}" in message:
        message = message.replace("{sender.full_name}", email.sender.full_name)

    if "{recipient.first_name}" in message:
        message = message.replace("{recipient.first_name}", email.recipients.first().first_name)
    if "{recipient.last_name}" in message:
        message = message.replace("{recipient.last_name}", email.recipients.first().last_name)
    if "{recipient.full_name}" in message:
        message = message.replace("{recipient.full_name}", email.recipients.first().full_name)
    
    if "{ticket.id}" in message:
        message = message.replace("{ticket.id}", str(ticket.id))

    if "{ticket.category}" in message:
        message = message.replace("{ticket.category}", ticket.category.name)

    if "{ticket.priority}" in message:
        message = message.replace("{ticket.priority}", ticket.priority.lower())
    if "{ticket.priority.upper_case}" in message:
        message = message.replace("{ticket.priority.upper_case}", ticket.priority)

    if "{ticket.status}" in message:
        message = message.replace("{ticket.status}", ticket.status.lower())
    if "{ticket.status.upper_case}" in message:
        message = message.replace("{ticket.status.upper_case}", ticket.status)

    if full == False:
        email.subject = message 
    elif full == True:
        email.body = message 
    email.save()

    if full == True:
        filter_email(email, ticket, full=False, repeat=True)
    return email

# from .models import Ticket, Category
# from login_app.models import User

# def set_up_bot(bot, ticket_id):
#     ticket = Ticket.objects.all().get(id=ticket_id)
#     # ticket_category = ticket.category

# # NO CONDITIONS (Bot has no "IF", "OR", or "AND" statements)
#     if bot.condition == "":
#         bot.setupAction(ticket_id)

#     if bot.condition == "category":
#         try:
#             bot_condition = Category.objects.get(id=int(bot.condition_dependency))
#         except:
#             return
#         else:
#             ticket_aspect = ticket.category

#     elif bot.condition == "priority":
#         bot_condition = bot.condition_dependency
#         ticket_aspect = ticket.priority

#     elif bot.condition == "sender":
#         try:
#             bot_condition = User.objects.all().get(id=int(bot.condition_dependency))
#         except:
#             return
#         else:
#             ticket_aspect = ticket.sender
#     elif bot.condition == "no_admin":
#         bot_condition = None
#         ticket_aspect = ticket.assigned.all()
#         if not ticket_aspect:
#             ticket_aspect = None

#     elif bot.condition == "unresolved":
#         bot_condition = "Unresolved"
#         ticket_aspect = ticket.status

# # ONLY FIRST CONDITION 
#     elif bot.condition_or == "" and bot.condition_inclusive == "":
#         if ticket_aspect == bot_condition:
#             bot.setupAction(ticket_id)

# # "OR" CONDITION (no "and")
#     elif bot.condition_or != "" and bot.condition_inclusive == "": 

#         if bot.condition_or == "category":
#             try:
#                 category_of_or_condition = Category.objects.get(id=int(bot.condition_or_dependency))
#             except:
#                 return
#             else:
#                 if ticket_aspect == bot_condition or ticket.category == category_of_or_condition:
#                     bot.setupAction(ticket_id)

#         elif bot.condition_or == "priority":
#             if ticket_aspect == bot_condition or ticket.priority == bot.condition_or_dependency:
#                 bot.setupAction(ticket_id)

#         elif bot.condition_or == "sender":
#             try:
#                 sender = User.objects.all.get(id=int(bot.condition_or_dependency))
#             except:
#                 return
#             else:
#                 if ticket_aspect == bot_condition or ticket.sender == sender:
#                     bot.setupAction(ticket_id)

#         elif bot.condition_or == "no_admin":
#             if ticket_aspect == bot_condition or not ticket.assigned.all():
#                 bot.setupAction(ticket_id)

#         elif bot.condition_or == "unresolved":
#             if ticket_aspect == bot_condition or ticket.status == "Unresolved":
#                 bot.setupAction(ticket_id)

# # "AND" STATEMENT (no "or")
#     elif bot.condition_inclusive  != "" and bot.condition_or == "":

#         # THIS IS REDUNDANT .. DO VALIDATION TO ENSURE A BOT LIKE THIS WOULDN'T BE CREATED, 
#         # BUT SINCE I DON'T HAVE THE VALIDATION, HERE'S THIS 
#         if bot.condition_inclusive == "category":
#             try:
#                 category_of_and_condition = Category.objects.get(id=int(bot.condition_inclusive_dependency))
#             except:
#                 return
#             else:
#                 if ticket_aspect == bot_condition and ticket.category == category_of_and_condition:
#                     bot.setupAction(ticket_id)

#         if bot.condition_inclusive == "priority":
#             if ticket_aspect == bot_condition and ticket.priority == bot.condition_inclusive_dependency:
#                 bot.setupAction(ticket_id)

#         elif bot.condition_inclusive == "sender":
#             try:
#                 sender = User.objects.all().get(id=int(bot.condition_inclusive_dependency))
#             except:
#                 return
#             else:
#                 if ticket_aspect == bot_condition and ticket.sender == sender:
#                     bot.setupAction(ticket_id)

#         elif bot.condition_inclusive == "no_admin":
#             if ticket_aspect == bot_condition and not ticket.assigned.all():
#                 bot.setupAction(ticket_id)

#         elif bot.condition_inclusive == "unresolved":
#             if ticket_aspect == bot_condition and ticket.status == "Unresolved":
#                 bot.setupAction(ticket_id)
