from django.urls import path, include
from .views import main_view as views
from .views import ticket_view as tickets
from .views import report_view as reports
from .views import inbox_view as inbox
from .views import automator_view as automators
app_name =  "ticket-easy"

urlpatterns = [
    # path('crontab/', include('django_crontab.urls')),

#LOGIN
    path('', views.login_app),

#HOME 
    path('dashboard', views.dashboard, name="dashboard"),

# NEW TICKET
    path('tickets/new', tickets.create_ticket, name="new-ticket-page"),
    path('create_ticket',tickets.create_ticket, name="create-ticket"),

## SINGLE TICKET
    path('ticket/<int:ticket_id>', tickets.ticket_page, name="single-ticket"),

#ALL TICKETS
    path('tickets/', tickets.all_tickets, name="tickets"),
    # path('users/<int:user_id>', tickets.all_tickets, name="user-tickets"),

# TICKET ACTIONS

    #change priority
    path('priority/<int:ticket_id>/<str:priority_option>', tickets.ticket_assignment_or_priority),

    #assignment
    path('assignment/<int:ticket_id>/<int:admin_id>', tickets.ticket_assignment_or_priority),
    # doesn't currently need name attribute. only used in JS

    # archives
    path('ticket/archive/<int:ticket_id>', tickets.archive, name="archive-ticket"),

    #status changed
    path('tickets/status/<int:ticket_id>', tickets.status_change, name="ticket-status"),

    # pin
    path('ticket/pin/<int:ticket_id>', tickets.pin, name="pin-ticket"),

    #edit ticket
    path('edit_ticket_page/<int:ticket_id>/<int:user_id>', tickets.edit_ticket_page, name="edit-ticket-page"),
    path('edit_ticket/<int:ticket_id>/<int:sender_id>', tickets.edit_ticket, name="edit-ticket"),

    # delete ticket 
    path('ticket/delete/<int:ticket_id>', tickets.delete, name="delete-ticket"),

# ADMIN STUFF
    #guide
    path('guide', views.guide, name="guide"),

    #categories
    path('category-page', views.category_page, name="category-page"),
    path('create-category', views.create_category, name="create-category"),
    path('delete-category', views.delete_category, name="delete-category"),

    # workflow websites
    path('create-site', views.create_site, name="create-site"),
    path('delete-site/<int:website_id>', views.delete_site, name="delete-site"),

    #images
    path('delete-images', views.delete_images),

## AUTOMATORS 
    path('automators/new', automators.automator, name="new-automator"),
    path('automators/all', automators.all_automators, name="all-automators"),
    path('automators/delete/<int:automator_id>', automators.automator_delete, name="delete-automator"),

    # get data for select menus
    path('get-info', automators.get_info),
    # used for JS 


## CANNED RESPONSES
    path('canned-response', inbox.canned_response, name="canned-response"),

## EMAILS
    path('mail/', inbox.mail, name="mail"),
    path('mail/<int:inbox_id>/<str:message_url>', inbox.mail_single),
    path("get_page_name", inbox.get_page_name),
    path("mail/new", inbox.new_message_page),
    path("mail/create", inbox.create_message, name="create-mail"),
    path("mail/reply/<int:message_id>", inbox.reply, name="create-reply"),

## REPORTS
    path('reports-page/', reports.reports_page, name="reports-page"),
    path('reports', reports.report, name="report-daterange"),
    path('reports/daily', reports.report_daily, name="report-singledate"),
    path('report-view', reports.report_view, name="report-view"),
    path('report-view-filter', reports.report_view_filter, name="report-view-filter"),
    path('my_chart/chof=validate', reports.g_chart, name="visual-chart"),
    path('report-delete-all', reports.delete_report),



# Y E T   U N U S E D 

# TEAMS
    # path('new-team-page', views.new_team),
    # path('new-team', views.new_team),
    # path('teams', views.teams),

# TASKS 
    # path('tasks', views.tasks),

# TICKET NOTES 
    # path('new_note/<int:ticket_id>', tickets.new_note),
    # path('delete_note/<int:note_id>/<int:ticket_id>', tickets.delete_note),
]
