from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver, Signal
from .models import Ticket, Automator
from .automator_script import start_automator
ticket_status_changed = Signal()


# This script is how the Automators know when to act 

@receiver(post_save, sender=Ticket)
def upon_ticket_creation_automators(sender, instance, created, **kwargs):
    if created:
        ticket_id = instance.id
        bots = Automator.objects.filter(event="created").filter(enabled=True)

        for bot in bots:
            start_automator(bot, ticket_id)

@receiver(ticket_status_changed, sender=Ticket)
def handle_ticket_status_change(sender,  **kwargs):
    status = kwargs.get('status')
    ticket_id = kwargs.get('ticket')

    if status is None or ticket_id is None:
        return

    if status == "Resolved":
        bots = Automator.objects.filter(event="resolved").filter(enabled=True)
    elif status == "Reopened":
        bots = Automator.objects.filter(event="reopened").filter(enabled=True)
    elif status == "Hold":
        bots = Automator.objects.filter(event="hold").filter(enabled=True)
    else:
        return

    for bot in bots:
        start_automator(bot, ticket_id)
