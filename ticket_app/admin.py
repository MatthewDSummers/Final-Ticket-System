from django.contrib import admin
from ticket_app.models import *


class TicketAdmin(admin.ModelAdmin):
    list_display = ["priority"]
    search_fields = ["category", "desc"]

class WebsiteAdmin(admin.ModelAdmin):
    list_display = ["name"]

class ImageAdmin(admin.ModelAdmin):
    list_display = ["ticket"]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]

class NoteAdmin(admin.ModelAdmin):
    list_display = ["name"]

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(Image, WebsiteAdmin)
admin.site.register(Category, WebsiteAdmin)
admin.site.register(Note, WebsiteAdmin)