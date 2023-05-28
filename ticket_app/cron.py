# from sqlalchemy import over
from .models import Ticket, Priority
# from datetime import datetime, timedelta
import pytz


# A L L    U N U S E D
def update_priority():
    target = Priority.objects.get(name="Intermediate")
    if target.toggle_auto_priorities == True:
        current = datetime.now()
        timezone = pytz.timezone('UTC')
        now = timezone.localize(current)

        # low = Priority.objects.get(name="Low")
        medium = Priority.objects.get(name="Intermediate")
        high = Priority.objects.get(name="High")
        crucial = Priority.objects.get(name="Crucial")
        overdue = Priority.objects.get(name="Overdue")



        # l = low.time
        m = medium.time
        h = high.time
        c = crucial.time
        o = overdue.time
        unresolved = Ticket.objects.filter(status="Unresolved")
        not_withheld = unresolved.filter(hold="")

        for ticket in not_withheld:
            if ticket.reopened == True:
                if target.toggle_off:
                    previously_exhausted_time = target.withheld_time - ticket.created_at
                    previously_exhausted_toggle_time = target.toggle_off - ticket.created_at
                    limit = previously_exhausted_time + previously_exhausted_toggle_time

                    if limit < m:
                        medium = m - limit

                    if limit > m and limit < h:
                        high = h - limit

                    if limit > h and limit < c:
                        crucial = c - limit

                    if limit > c and limit < o:
                        overdue = o - limit


                    if ticket.auto_priority == "Crucial":
                        if now > ticket.reopened_time + overdue:
                            ticket.auto_priority = "Overdue"
                            ticket.save(update_fields=['auto_priority'])

                    if ticket.auto_priority == "High":
                        if now > ticket.reopened_time + crucial:
                            ticket.auto_priority = "Crucial"
                            ticket.save(update_fields=['auto_priority'])

                    if ticket.auto_priority == "Intermediate":
                        if now > ticket.reopened_time + high :
                            ticket.auto_priority = "High"
                            ticket.save(update_fields=['auto_priority'])

                    if ticket.auto_priority == "Low":
                        if now > ticket.reopened_time + medium:
                            ticket.auto_priority = "Intermediate"
                            ticket.save(update_fields=['auto_priority'])

                elif not target.toggle_off:
                    # low = ticket.reopened_time + l
                    medium = ticket.reopened_time  + m
                    high = ticket.reopened_time  + h
                    crucial = ticket.reopened_time  + c
                    # overdue = crucial + o
                    overdue = ticket.reopened_time + o

                    if ticket.auto_priority == "Crucial":
                        limit = overdue - c
                        if now > limit:
                            ticket.auto_priority = "Overdue"
                            ticket.save(update_fields=['auto_priority'])
                    if ticket.auto_priority == "High":
                        limit = crucial - h
                        if now > limit:
                            ticket.auto_priority = "Crucial"
                            ticket.save(update_fields=['auto_priority'])

                    if ticket.auto_priority == "Intermediate":
                        limit = high - m
                        if now > limit:
                            ticket.auto_priority = "High"
                            ticket.save(update_fields=['auto_priority'])

                    if ticket.auto_priority == "Low":
                        # limit = medium - l
                        if now > medium:
                            ticket.auto_priority = "Intermediate"
                            ticket.save(update_fields=['auto_priority'])




            elif target.toggle_off and ticket.reopened != True:
                previously_exhausted_time = target.toggle_off - ticket.created_at

                if previously_exhausted_time < m:
                    medium = m - previously_exhausted_time

                if previously_exhausted_time > m and previously_exhausted_time < h:
                    high = h - previously_exhausted_time

                if previously_exhausted_time > h and previously_exhausted_time < c:
                    crucial = c - previously_exhausted_time

                if previously_exhausted_time > c and previously_exhausted_time < o:
                    overdue = o - previously_exhausted_time

                if ticket.auto_priority == "Crucial":
                    limit = overdue
                    if now > target.toggle_on + limit:
                        ticket.auto_priority = "Overdue"
                        ticket.save(update_fields=['auto_priority'])

                if ticket.auto_priority == "High":
                    limit = crucial
                    if now > target.toggle_on + limit:
                        ticket.auto_priority = "Crucial"
                        ticket.save(update_fields=['auto_priority'])

                if ticket.auto_priority == "Intermediate":
                    limit = high
                    if now > target.toggle_on + limit:
                        ticket.auto_priority = "High"
                        ticket.save(update_fields=['auto_priority'])

                if ticket.auto_priority == "Low":
                    limit = medium
                    if now > target.toggle_on + limit:
                        ticket.auto_priority = "Intermediate"
                        ticket.save(update_fields=['auto_priority'])
            else:
                # low = ticket.created_at + l
                medium = ticket.created_at  + m
                high = ticket.created_at  + h
                crucial = ticket.created_at + c
                # overdue = crucial + o
                overdue = ticket.created_at + o

                if ticket.auto_priority == "Crucial":
                    limit = o - c
                    if now > ticket.created_at + limit:
                        ticket.auto_priority = "Overdue"
                        ticket.save(update_fields=['auto_priority'])

                if ticket.auto_priority == "High":
                    limit = c - h
                    if now > ticket.created_at + limit:
                        ticket.auto_priority = "Crucial"
                        ticket.save(update_fields=['auto_priority'])

                        # return True
                if ticket.auto_priority == "Intermediate":
                    limit = h - m
                    if now > ticket.created_at + limit:
                        ticket.auto_priority = "High"
                        ticket.save(update_fields=['auto_priority'])

                if ticket.auto_priority == "Low":
                    # limit = m - l
                    if now > medium:
                        ticket.auto_priority = "Intermediate"
                        ticket.save(update_fields=['auto_priority'])


                # if now > medium:
                #     ticket.auto_priority = "Intermediate"
                #     ticket.save(update_fields=['auto_priority'])
                # # if ticket.auto_priority == "Intermediate":
                # #     limit = high - m
                # if now > high:
                #     ticket.auto_priority = "High"
                #     ticket.save(update_fields=['auto_priority'])
                # # if ticket.auto_priority == "High":
                #     # limit = crucial - h
                # if now > crucial:
                #     ticket.auto_priority = "Crucial"
                #     ticket.save(update_fields=['auto_priority'])
                # # if ticket.auto_priority == "Crucial":
                #     # limit = overdue - c
                # if now > overdue:
                #     ticket.auto_priority = "Overdue"
                #     ticket.save(update_fields=['auto_priority'])

        return True
    else:
        pass
# def update_priority():
#     now = datetime.now()
#     timezone = pytz.timezone('UTC')
#     aware = timezone.localize(now)
#     for ticket in Ticket.objects.all():
#         medium = ticket.created_at  + timedelta(minutes=1)
#         high = ticket.created_at  + timedelta(minutes=2)
#         crucial = ticket.created_at  + timedelta(minutes=3)
#         if aware < medium:
#             ticket.auto_priority = "Low"
#             ticket.save(update_fields=['auto_priority'])
#         if aware > medium:
#             ticket.auto_priority = "Intermediate"
#             ticket.save(update_fields=['auto_priority'])
#         if aware > high:
#             ticket.auto_priority = "High"
#             ticket.save(update_fields=['auto_priority'])
#         if aware > crucial:
#             ticket.auto_priority = "Crucial"
#             ticket.save(update_fields=['auto_priority'])
#     return True







# OLD

# from .models import Ticket, Priority
# from datetime import datetime, timedelta
# import pytz

# def update_priority():
#     current = datetime.now()
#     timezone = pytz.timezone('UTC')
#     now = timezone.localize(current)

#     low = Priority.objects.get(name="Low")
#     medium = Priority.objects.get(name="Intermediate")
#     high = Priority.objects.get(name="High")
#     crucial = Priority.objects.get(name="Crucial")
#     overdue = Priority.objects.get(name="Overdue")

#     l = low.time
#     m = medium.time
#     h = high.time
#     c = crucial.time
#     o = overdue.time
#     unresolved = Ticket.objects.filter(status="Unresolved")
#     not_withheld = unresolved.filter(hold="")

#     for ticket in not_withheld:
#         if ticket.reopened == True:
#             # low = ticket.reopened_time + l
#             medium = ticket.reopened_time  + m
#             high = ticket.reopened_time  + h
#             crucial = ticket.reopened_time  + c
#             # overdue = crucial + o
#             overdue = ticket.reopened_time + o

#             if ticket.auto_priority == "Crucial":
#                 limit = overdue - c
#                 if now > limit:
#                     ticket.auto_priority = "Overdue"
#                     ticket.save(update_fields=['auto_priority'])
#             if ticket.auto_priority == "High":
#                 limit = crucial - h
#                 if now > limit:
#                     ticket.auto_priority = "Crucial"
#                     ticket.save(update_fields=['auto_priority'])

#             if ticket.auto_priority == "Intermediate":
#                 limit = high - m
#                 if now > limit:
#                     ticket.auto_priority = "High"
#                     ticket.save(update_fields=['auto_priority'])

#             if ticket.auto_priority == "Low":
#                 limit = medium - l
#                 if now > low:
#                     ticket.auto_priority = "Intermediate"
#                     ticket.save(update_fields=['auto_priority'])


#         else:
#             low = ticket.created_at + l
#             medium = ticket.created_at  + m
#             high = ticket.created_at  + h
#             crucial = ticket.created_at + c
#             # overdue = crucial + o
#             overdue = ticket.created_at + o

#             if ticket.auto_priority == "Crucial":
#                 limit = o - c
#                 if now > ticket.created_at + limit:
#                     ticket.auto_priority = "Overdue"
#                     ticket.save(update_fields=['auto_priority'])

#             if ticket.auto_priority == "High":
#                 limit = c - h
#                 if now > ticket.created_at + limit:
#                     ticket.auto_priority = "Crucial"
#                     ticket.save(update_fields=['auto_priority'])

#                     # return True
#             if ticket.auto_priority == "Intermediate":
#                 limit = h - m
#                 if now > ticket.created_at + limit:
#                     ticket.auto_priority = "High"
#                     ticket.save(update_fields=['auto_priority'])

#             if ticket.auto_priority == "Low":
#                 limit = m - l
#                 if now > low:
#                     ticket.auto_priority = "Intermediate"
#                     ticket.save(update_fields=['auto_priority'])









#             # if now > medium:
#             #     ticket.auto_priority = "Intermediate"
#             #     ticket.save(update_fields=['auto_priority'])
#             # # if ticket.auto_priority == "Intermediate":
#             # #     limit = high - m
#             # if now > high:
#             #     ticket.auto_priority = "High"
#             #     ticket.save(update_fields=['auto_priority'])
#             # # if ticket.auto_priority == "High":
#             #     # limit = crucial - h
#             # if now > crucial:
#             #     ticket.auto_priority = "Crucial"
#             #     ticket.save(update_fields=['auto_priority'])
#             # # if ticket.auto_priority == "Crucial":
#             #     # limit = overdue - c
#             # if now > overdue:
#             #     ticket.auto_priority = "Overdue"
#             #     ticket.save(update_fields=['auto_priority'])

#     return True

# # def update_priority():
# #     now = datetime.now()
# #     timezone = pytz.timezone('UTC')
# #     aware = timezone.localize(now)
# #     for ticket in Ticket.objects.all():
# #         medium = ticket.created_at  + timedelta(minutes=1)
# #         high = ticket.created_at  + timedelta(minutes=2)
# #         crucial = ticket.created_at  + timedelta(minutes=3)
# #         if aware < medium:
# #             ticket.auto_priority = "Low"
# #             ticket.save(update_fields=['auto_priority'])
# #         if aware > medium:
# #             ticket.auto_priority = "Intermediate"
# #             ticket.save(update_fields=['auto_priority'])
# #         if aware > high:
# #             ticket.auto_priority = "High"
# #             ticket.save(update_fields=['auto_priority'])
# #         if aware > crucial:
# #             ticket.auto_priority = "Crucial"
# #             ticket.save(update_fields=['auto_priority'])
# #     return True









