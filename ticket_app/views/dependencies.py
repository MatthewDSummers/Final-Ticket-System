from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from ..models import Ticket, Task, Team, Category, Priority, Website, Image, Note, CannedResponse, Inbox, Message, Automator

# from .report_view import aware_date_range
from login_app.user_functions import User, user_level_required, get_user, if_not_logged_in
from ..calendar_module import get_formatted_dates, get_aware_date
from datetime import datetime, date, timedelta

from django.contrib import messages
import pytz
from collections import Counter
from django.db.models import Count, Q
import json
import bcrypt 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time
import re
from ticket_app.forms import MessageForm
# from .report_view import get_aware_date
# from .ticket_view import isUser

# from django.core import serializers
# from django.conf import settings
# from django.core.files.storage import FileSystemStorage
# import itertools
# import datetime
# from nis import cat

# def user_is_staff_or_superuser(view_func):
#     def wrapper(request, *args, **kwargs):
#         user = User.objects.get(id=request.session['user_id'])
#         if user:
#             if user.level == 8 or user.level == 9:
#                 return view_func(request, *args, **kwargs)
#             else:
#                 return redirect('/')
#         else:
#             return redirect('/')
#     return wrapper

