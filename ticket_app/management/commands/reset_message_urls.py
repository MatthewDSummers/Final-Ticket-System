
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from ...models import Message


class Command(BaseCommand):
    help = 'Resets URLs for messages that are more than one week old'

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Print details about each message that has its URL reset',
        )

    def handle(self, *args, **options):
        one_week_ago = datetime.now() - timedelta(days=7)
        messages_to_reset = Message.objects.filter(created_at__lte=one_week_ago)
        for message in messages_to_reset:
            message.resetURL()
            # if options['verbose']:
            self.stdout.write(f'Successfully reset URL for message "{message.subject}"')



# WHY BASECOMMAND 
# Using the Django BaseCommand class provides a number of benefits over simply defining a standalone function. Here are a few reasons why you might want to use BaseCommand:

# 1. Standardization: BaseCommand provides a standardized way of defining custom management commands in Django. By using this class, you can follow the same conventions as other Django management commands, making it easier for other developers to understand and work with your code.

# 2. Integration: BaseCommand integrates with other parts of Django's management system, allowing you to easily run your command using the manage.py utility or include it as part of a larger batch job.

# 3. Flexibility: BaseCommand provides a flexible framework for defining custom command-line arguments and options, allowing you to create more complex and powerful commands as needed.

# 4. Testing: BaseCommand provides built-in support for testing your custom command, allowing you to easily verify that it behaves as expected under a variety of scenarios.

# In short, while it is possible to define a standalone function for resetting message URLs, using BaseCommand provides a standardized, integrated, and flexible way of defining the command that can be useful in a larger Django project.




# WHY `--verbose` VERBOSE WORKS

# You can run the command with the --verbose option to see details about each message that has its URL reset:
# python manage.py reset_message_urls --verbose


# The --verbose flag is picked up as an option argument rather than a positional argument because it is preceded by two hyphens --. In argparse, positional arguments are used without hyphens and options are used with one or two hyphens.

# When the handle method in the Command class is executed, the **options variable contains all of the command-line options and their values. The --verbose option is included in this dictionary as options['verbose'].

# So, when you run the command python manage.py reset_message_urls --verbose, the verbose option is set to True in the options dictionary, and the handle method can use this value to determine whether to print out the success messages.