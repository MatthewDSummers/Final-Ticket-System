from django.test import TestCase
from django.utils import timezone
from .models import Ticket, Category
from login_app.models import User
from django.db import models

class TicketIndexingTestCase(TestCase):

    def setUp(self):
        # create 1000 tickets
        self.category = Category.objects.create(name="Test Category", created_at = timezone.now())
        self.user = User.objects.create(full_name="Matthew Summers", level=9, created_at = timezone.now())
        for i in range(1000):
            Ticket.objects.create(
                category = self.category,
                priority = "Low",
                auto_priority = "Low",
                sender = self.user,
                desc = "Test ticket #" + str(i),
                created_at = timezone.now(),
                updated_at = timezone.now(),
            )

    def tearDown(self):
        Category.objects.filter(name="Test Category").delete()
        User.objects.filter(full_name="Matthew Summers").delete()

        # delete all tickets created in setUp
        Ticket.objects.all().delete()

    def test_indexing_performance(self):
        # calculate query time without index
        filters = {
            "created_at__lte": timezone.now(),
            "category": self.category,
            "priority": "Low",
            "sender": self.user,
            "status": "Unresolved",
        }
        start_time = timezone.now()
        # Ticket.objects.filter(created_at__lte=timezone.now(), category=category, priority="Low", sender=user, status="Unresolved", created_at__lte=timezone.now()).order_by("-created_at")
        Ticket.objects.filter(**filters).order_by("-created_at")
        query_time_without_index = timezone.now() - start_time
        print(query_time_without_index, "Query time without index")
        # add index to created_at field
        Ticket._meta.indexes = [models.Index(fields=['category', 'priority', 'sender', 'status', 'created_at']),]
        # Ticket.objects.refresh_from_db()
        Ticket.objects = Ticket.objects.all()

        # calculate query time with index
        start_time = timezone.now()
        Ticket.objects.filter(**filters).order_by("-created_at")
        query_time_with_index = timezone.now() - start_time
        print(query_time_with_index, "Query time with index")

        self.assertLess(query_time_with_index, query_time_without_index, "Query time with index is not less than query time without index")


