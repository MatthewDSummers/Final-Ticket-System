from django.db import models
from django.db import models
from django.db.models import Count, Value
from django.db.models.functions import Concat
from django.db.models.query import QuerySet

import json
from collections import Counter
from datetime import datetime, timedelta
import random
import string 

from login_app.models import User

from ckeditor.fields import RichTextField

from .automator_utils import filter_email

def generate_unique_url():
    while True:
        url = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        if not Message.objects.filter(url=url).exists():
            return url
# import urlGiver


class TicketManager(models.Manager):
    def validator(self, postData):
        errors={}

        print("hello?")
        if not postData['category']:
            errors['tick_category'] = "Please select a category"

        if postData['priority']:
            print("priority data?")
            print(postData['priority'])
            print("did we get any priority data?")
        # if not postData['priority']:
        #     print("no data?!")

        #     errors['tick_priority'] = "Please select a priority"

        if not postData['desc']:
            errors['tick_priority'] = "Please enter a description"
        elif len(postData['desc']) < 10:
            errors['tick_desc'] = "A description must be at least 10 characters"

        return errors

    def filter_by_date_range(self, start_date, end_date, filter_choice):
        queryset = Ticket.objects.filter(created_at__range=(start_date, end_date))

        if filter_choice == 'Category':
            queryset = queryset.values('category__name').annotate(count=Count('category__name')).order_by('category__name')
        elif filter_choice == 'Priority':
            queryset = queryset.values('priority').annotate(count=Count('priority')).order_by('priority')
        elif filter_choice == 'Status':
            queryset = queryset.values('status').annotate(count=Count('status')).order_by('status')
        elif filter_choice == 'Sender':
            queryset = queryset.values('sender__full_name').annotate(num_tickets=Count('id'))

        return queryset

class Category(models.Model):
    name = models.CharField(max_length=100)
    # ticket = models.ForeignKey(Ticket, related_name="category", on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Ticket(models.Model):
    category = models.ForeignKey(Category, related_name="ticket", on_delete=models.CASCADE)
    priority = models.CharField(max_length=12, default ="Not Set")
    auto_priority = models.CharField(max_length=12, default = "Low")
    # auto_priority = models.CharField(max_length=12)
    sender = models.ForeignKey(User, related_name="tickets", on_delete=models.CASCADE)
    desc = models.TextField()
    status = models.CharField(max_length=10, default='Unresolved')
    pinned = models.CharField(max_length=8, default='Unpinned', db_index=True)
    hold = models.CharField(max_length=10, blank=True, default='', db_index=True)
    reopened = models.BooleanField(blank=True, null=True, default=False)
    reopened_time = models.DateTimeField(null=True)
    archived = models.BooleanField(blank=True, null=True, default=False, db_index=True)
    assigned = models.ManyToManyField(User, related_name="assigned")
    first_resolved_at = models.DateTimeField(null=True)
    resolved_at = models.DateTimeField(null=True)
    resolved_by = models.ForeignKey(User, related_name="resolved_tickets", on_delete=models.SET_NULL, blank=True, null=True)
    first_resolved_by = models.ForeignKey(User, related_name="primary_resolved_tickets", on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TicketManager()

    def get_date(self):
        return self.created_at.date()

    def serialize(self):
        return {
            'id':self.id,
            'category':self.category,
            'priority':self.priority,
            'sender':self.sender.serialize(),
            'desc':self.desc,
            'status':self.status,
            'pinned':self.pinned,
            'hold':self.hold,
            'resolved_at':self.resolved_at,
            'resolved_by':self.resolved_by.serialize(),
            'created_at':self.created_at,
            'updated_at':self.updated_at
        }

    # this makes an object like this which I can make into JSON:
    # {
    #     'id': 1,
    #     'category': 'Example',
    #     'priority': 'High',
    #     'sender': {
    #         'id': 1,
    #         'first_name': 'John',
    #         'last_name': 'Doe',
    #         'level': 'Admin',
    #         'email': 'johndoe@example.com',
    #         'created_at': '2023-05-16 10:00:00',
    #         'updated_at': '2023-05-16 12:00:00'
    #     },
    #     'desc': 'Example ticket description',
    #     'status': 'Resolved',
    #     'pinned': 'Pinned',
    #     'hold': 'Hold',
    #     'resolved_at': None,
    #     'resolved_by': {
    #         'id': 2,
    #         'first_name': 'Jane',
    #         'last_name': 'Smith',
    #         'level': '1',
    #         'email': 'janesmith@example.com',
    #         'created_at': '2023-05-15 09:00:00',
    #         'updated_at': '2023-05-15 11:00:00'
    #     },
    #     'created_at': '2023-05-16 14:00:00',
    #     'updated_at': '2023-05-16 16:00:00'
    # }


    def google_chart(post_data, start, end):
        queryset = Ticket.objects.filter_by_date_range(start, end, post_data['cat'])
        data = []

        if post_data['cat'] == "Status":
            data.append(['Status', "Amount"])
            for status_level in queryset:
                data.append([status_level['status'], status_level['count']])

        if post_data['cat'] == "Priority":
            data.append(['Priority', "Amount"])
            for priority_level in queryset:
                data.append([priority_level['priority'], priority_level['count']])

        if post_data['cat'] == "Sender":
            data.append(['Person', "Amount"])
            for entry in queryset:
                data.append([entry['sender__full_name'], entry['num_tickets']])

        if post_data['cat'] == "Category":
            data.append(['Category', "Amount"])

            for entry in queryset:
                data.append([entry['category__name'], entry['count']])

        return json.dumps(data)

    class Meta:
        ordering = ['-created_at', '-status', 'priority']
        # ordering = ['auto_priority', '-created_at']


class Website(models.Model):
    name = models.CharField(max_length=100)
    content = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="websites", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Image(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    ticket = models.ForeignKey(Ticket, related_name="images", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CannedResponse(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    # body = models.TextField(default="")
    body = RichTextField(blank=True, null=True, default ="")
    sender = models.ForeignKey(User, related_name="canned_responses", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CustomQuerySet(QuerySet):
    def viewed_count(self):
        return self.filter(viewed=False).count()
    def starred_count(self):
        return self.filter(starred=True).count()

class CustomManager(models.Manager):
    _queryset_class = CustomQuerySet


class Message(models.Model):
    name = models.CharField(max_length=255, default="")
    subject = models.CharField(max_length=255, default="")
    body = models.TextField(default="")
    recipients = models.ManyToManyField(User, related_name="messages")
    sender = models.ForeignKey(User, related_name="sent", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url = models.TextField(max_length="32", default="")

    def resetURL(self):
        self.url = generate_unique_url()
        self.save(update_fields=["url"])

    def truncateBody(self):
        return f"{self.body[:75]}..."
    
    def truncateSubject(self):
        if len(self.subject) > 50:
            return f"{self.subject[:55]}..."
        else:
            return self.subject

    class Meta:
        ordering = ['-created_at']
    objects = CustomManager()

class Reply(models.Model):
    sender = models.ForeignKey(User, related_name="sent_replies", on_delete = models.CASCADE)
    body = models.TextField(default="")
    # body = RichTextField(blank=True, null=True, default ="")
    recipients = models.ManyToManyField(User, related_name="received_replies")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='replies')

class Inbox(models.Model):
    user = models.OneToOneField(User, related_name="inbox", on_delete=models.CASCADE)
    messages = models.ManyToManyField(Message, related_name="inbox")
    viewed = models.ManyToManyField(Message, related_name="inbox_viewed")
    starred = models.ManyToManyField(Message, related_name="inbox_starred")
    trashed = models.ManyToManyField(Message, related_name="inbox_trashed")


def bot_Error(field_name):
    field_name = 'Please provide a name' if field_name == "name" else field_name
    field_name =  'Please provide a value for the "WHEN" condition' if field_name == "when" else field_name

    field_name =  'If you want to assign an "IF" condition, it can\'t be empty' if field_name == "condition-one" else field_name
    field_name =   'Please provide supporting details for the "IF" condition' if field_name == "condition-one_supportive" else field_name

    field_name =   'If you want to assign an "OR" condition, it can\'t be empty' if field_name == "condition-or" else field_name
    field_name =   'Please provide supporting details for the "OR" condition' if field_name == "condition-or_supportive" else field_name

    field_name =   'If you want to assign an "AND" condition, it can\'t be empty' if field_name == "condition-inclusive" else field_name
    field_name =   'Please provide supporting details for the "AND" condition' if field_name == "condition-inclusive_supportive" else field_name

    field_name =   'Please provide a value for the "THEN" condition' if field_name == "then" else field_name
    field_name =   'Please provide supporting details for the "THEN" condition' if field_name == "then_supportive" else field_name
    field_name =   'Please select a user for the Canned Response' if field_name == "then_supportive_additional" else field_name

    return field_name

class MissingFieldError(Exception):
    pass


class AutomatorManager(models.Manager):
    def validator(self, sanitized_data):
        errors = {}

        invalid = {"", "Select an Option...", None}

        required_fields = {
            'name', 'when',
            'condition-one', 'condition-one_supportive',
            'condition-or', 'condition-or_supportive',
            'condition-inclusive', 'condition-inclusive_supportive',
            'then', 'then_supportive', 'then_supportive_additional'
        }

        ignored_fields = {"csrfmiddlewaretoken", "condition-one-checkbox", "condition-or-checkbox", "condition-inclusive-checkbox", "then-checkbox"}
        missing_fields = [field for field in sanitized_data if field not in required_fields and field not in ignored_fields]

        if missing_fields:
            raise MissingFieldError()

        # for sanitized in sanitized_data:
        #     if sanitized not in ignored_fields:
        #         for field in required_fields:
        #             if sanitized not in required_fields:
        #                 raise MissingFieldError()
        else:
            if sanitized_data["name"] == "":
                errors["name"] = bot_Error("name")
            if sanitized_data["when"] in invalid:
                errors["when"] = bot_Error("when")

            checkboxes = ["condition-one-checkbox", "condition-or-checkbox", "condition-inclusive-checkbox", "then-checkbox"]

            condition_fields = {
                "condition-one-checkbox": ["condition-one", "condition-one_supportive"],
                "condition-or-checkbox": ["condition-or", "condition-or_supportive"],
                "condition-inclusive-checkbox": ["condition-inclusive", "condition-inclusive_supportive"],
                "then-checkbox": ["then", "then_supportive", "then_supportive_additional"],
            }

            then_accepted_fields_without_conditionals = ["assign", "archive", "hold"]
            then_extra_fields = ["canned_messages"]

            other_accepted_fields_without_conditionals = ["no_admin", "unresolved", "withheld", "reopened"]

            for checkbox in checkboxes:
                if sanitized_data.get(checkbox):
                    fields = condition_fields.get(checkbox)
                    # print(fields[0], "THIS IS THE FIRST KEY")

                    if checkbox == "then-checkbox" and sanitized_data.get("then") not in then_accepted_fields_without_conditionals:
                        if sanitized_data.get("then") in invalid:
                            errors["then"] = bot_Error("then")
                        elif sanitized_data.get("then") in then_extra_fields:
                            for field in fields:
                                #Canned messages
                                print(sanitized_data.get(field), " THE CAN FIELDS")
                                if sanitized_data.get(field) in invalid:
                                    errors[field] = bot_Error(field)
                        elif sanitized_data.get("then") not in then_extra_fields:
                            if sanitized_data.get("then_supportive") in invalid:
                                errors["then_supportive"] = bot_Error("then_supportive")
                            # if sanitized_data.get("then_supportive_additional") in invalid:
                            #     errors["then_supportive_additional"] = bot_Error("then_supportive_additional")

                    parent_condition_passed = False
                    if checkbox != "then-checkbox":
                        data_keys = sanitized_data.keys()

                        # parent_condition_passed = []
                        for key in data_keys:
                            if key == fields[0] and sanitized_data.get(key) not in other_accepted_fields_without_conditionals:

                                if sanitized_data.get(key) in invalid:
                                    parent_condition_passed = False
                                    errors[key] = bot_Error(key)
                                else:
                                    parent_condition_passed = True
                                    

                            elif key == fields[1]:
                                if parent_condition_passed == True:
                                    if sanitized_data.get(key) in invalid:
                                        errors[key] = bot_Error(key)
            return errors

class Automator(models.Model):
    name = models.CharField(max_length=255)
    event = models.CharField(max_length=255)
    enabled = models.BooleanField(blank=True, null=True, default=True)
    condition = models.CharField(max_length=255)
    condition_dependency = models.CharField(max_length=255)

    condition_or = models.CharField(max_length=255)
    condition_or_dependency = models.CharField(max_length=255)

    condition_inclusive = models.CharField(max_length=255)
    condition_inclusive_dependency = models.CharField(max_length=255)

    then_action = models.CharField(max_length=255)
    then_dependency = models.CharField(max_length=255)
    then_dependency_two = models.CharField(max_length=255, default="")
    objects = AutomatorManager()

# SETUP ITS BEHAVIOR 
    def start(self, ticket_id):
        try:
            ticket = Ticket.objects.all().get(id=ticket_id)
        except Ticket.DoesNotExist:
            return
        else:

        # NO CONDITIONS (Bot has no "IF", "OR", or "AND" statements)
            if self.condition == "":
                self.setup_action(ticket_id)
            else:
                if self.condition == "category":
                    try:
                        bot_condition = Category.objects.get(id=int(self.condition_dependency))
                    except Category.DoesNotExist:
                        return
                    else:
                        ticket_aspect = ticket.category

                elif self.condition == "priority":
                    bot_condition = self.condition_dependency
                    ticket_aspect = ticket.priority

                elif self.condition == "sender":
                    try:
                        bot_condition = User.objects.all().get(id=int(self.condition_dependency))
                    except User.DoesNotExist:
                        return
                    else:
                        ticket_aspect = ticket.sender

                elif self.condition == "no_admin":
                    bot_condition = None
                    ticket_aspect = ticket.assigned.all()
                    if not ticket_aspect:
                        ticket_aspect = None

                elif self.condition == "unresolved":
                    bot_condition = "Unresolved"
                    ticket_aspect = ticket.status

        # ONLY FIRST CONDITION 
                if self.condition_or == "" and self.condition_inclusive == "":
                    if ticket_aspect == bot_condition:
                        self.setup_action(ticket_id)

        # "OR" CONDITION (no "and")
                elif self.condition_or != "" and self.condition_inclusive == "": 

                    if self.condition_or == "category":
                        try:
                            category_of_or_condition = Category.objects.get(id=int(self.condition_or_dependency))
                        except:
                            return
                        else:
                            if ticket_aspect == bot_condition or ticket.category == category_of_or_condition:
                                self.setup_action(ticket_id)

                    elif self.condition_or == "priority":
                        if ticket_aspect == bot_condition or ticket.priority == self.condition_or_dependency:
                            self.setup_action(ticket_id)

                    elif self.condition_or == "sender":
                        try:
                            sender = User.objects.all.get(id=int(self.condition_or_dependency))
                        except:
                            return
                        else:
                            if ticket_aspect == bot_condition or ticket.sender == sender:
                                self.setup_action(ticket_id)

                    elif self.condition_or == "no_admin":
                        if ticket_aspect == bot_condition or not ticket.assigned.all():
                            self.setup_action(ticket_id)

                    elif self.condition_or == "unresolved":
                        if ticket_aspect == bot_condition or ticket.status == "Unresolved":
                            self.setup_action(ticket_id)

        # "AND" STATEMENT (no "or")
                elif self.condition_inclusive  != "" and self.condition_or == "":

                    # THIS IS REDUNDANT .. DO VALIDATION TO ENSURE A BOT LIKE THIS WOULDN'T BE CREATED, 
                    # BUT SINCE I DON'T HAVE THE VALIDATION, HERE'S THIS 
                    if self.condition_inclusive == "category":
                        try:
                            category_of_and_condition = Category.objects.get(id=int(self.condition_inclusive_dependency))
                        except:
                            return
                        else:
                            if ticket_aspect == bot_condition and ticket.category == category_of_and_condition:
                                self.setup_action(ticket_id)

                    if self.condition_inclusive == "priority":
                        if ticket_aspect == bot_condition and ticket.priority == self.condition_inclusive_dependency:
                            self.setup_action(ticket_id)

                    elif self.condition_inclusive == "sender":
                        try:
                            sender = User.objects.all().get(id=int(self.condition_inclusive_dependency))
                        except:
                            return
                        else:
                            if ticket_aspect == bot_condition and ticket.sender == sender:
                                self.setup_action(ticket_id)

                    elif self.condition_inclusive == "no_admin":
                        if ticket_aspect == bot_condition and not ticket.assigned.all():
                            self.setup_action(ticket_id)

                    elif self.condition_inclusive == "unresolved":
                        if ticket_aspect == bot_condition and ticket.status == "Unresolved":
                            self.setup_action(ticket_id)

# FILTER SETUP MORE 
    def setup_action(self, ticket_id):
        action = self.then_action

        if self.then_dependency != "":
            target = self.then_dependency
        if action == "assign" or action == "priority" or action == "canned_response":
            self.take_action(Ticket_ID = ticket_id, Target=target)
        elif action == "archive" or action == "hold":
            self.take_action(Ticket_ID = ticket_id, Target="blank")


# FINALLY
    def take_action(self, *args, **kwargs):
        print("TAKE ACTION!")

        if kwargs['Target']:
            target = kwargs['Target']

        if kwargs['Ticket_ID']:
            ticket_id= kwargs['Ticket_ID']

        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return

        action = self.then_action

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
                if self.then_dependency_two == "to_sender":
                    person = ticket.sender
                    self.send_canned_response(canned_response, person, ticket)
                else:
                    if person is None:
                        try:
                            person = User.objects.get(id=self.then_dependency_two)
                        except User.DoesNotExist:
                                return
                        else:
                            self.send_canned_response(canned_response, person, ticket)
        return

# SEND CANNED RESPONSES 
    def send_canned_response(self, canned_response, person, ticket):
        url = generate_unique_url()

        email = Message.objects.create(
            name = canned_response.name,
            subject = canned_response.subject,
            body = canned_response.body,
            sender = canned_response.sender,
            url = url
        )
        email.recipients.add(person)
        email = filter_email(email, ticket, full=True)

        try:
            inbox = Inbox.objects.get(user=person)
        except Inbox.DoesNotExist:
            return
        else:
            inbox.messages.add(email)


        # IN VIEWS, FOR EACH RELEVANT FUNCTION, I CAN RUN A FOR LOOP FOR ALL RELEVANT BOTS:
        #     for automator in Automator.objects.all().filter(event=CURRENT_VIEW_KEYWORD):
        #         automator.event_check(event, ticket)

        # also, the signals file is pretty cool instead. don't need to run that bots in the functions. 
        # just delegate for when that something happens, then those bots will run 




# U N U S E D ( NEED TO BETTER DEVELOP )

class Task(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name="tasks")
    tickets = models.ManyToManyField(Ticket, related_name="tasks")
    status = models.CharField(max_length=10, default='Unresolved')
    priority = models.CharField(max_length=10, default='Low')

    start_date = models.DateField()
    end_date = models.DateField()

    archived = models.BooleanField(blank=True, null=True, default=False)
    hold = models.BooleanField(blank=True, null=True, default=False)
    complete = models.BooleanField(blank=True, null=True, default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Team(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="")
    tasks = models.ManyToManyField(Task, related_name="teams")
    members = models.ManyToManyField(User, related_name="teams")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Priority(models.Model):
    name = models.CharField(max_length=12)
    time = models.DurationField()
    toggle_auto_priorities = models.BooleanField(blank=True, null=True, default=False)
    toggle_on = models.DateTimeField(blank=True, null=True)
    toggle_off = models.DateTimeField(blank=True, null=True)
    cron_time = models.IntegerField(default="0")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
#     admin can make a new priority (set html options to fixed names for high , low, etc)
#     ----basically, he can just set the TIME.  the NAME will be set automatically.

class Note(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, related_name="notes", on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, related_name="notes", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)