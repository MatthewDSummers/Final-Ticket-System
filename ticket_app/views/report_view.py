
from .dependencies import *
# from ..calendar_module import get_formatted_dates
# from .ticket_view import get_user
##### REPORTS #####
from django.urls import reverse

@user_level_required(8,9)
def reports_page(request):
    context = {
        'user': get_user(request),
    }
    return render(request, 'reports.html', context)

@user_level_required(8,9)
def report(request):
    user = get_user(request)

    if request.method == "POST":
        if request.POST['start'] != '':
            if request.POST['end'] != '':
                start = request.POST['start']
                end = request.POST['end']
                python_start = datetime.strptime(start, "%Y-%m-%d")
                python_end = datetime.strptime(end, "%Y-%m-%d")

                timezone = pytz.timezone('Europe/London')
                aware_start = timezone.localize(python_start) 
                aware_end = timezone.localize(python_end)

                test = Ticket.objects.filter(created_at__range=(aware_start, aware_end))
                # django_results = json.dumps(list(Ticket.objects.filter(created_at__range=(aware_start, aware_end))))
                the_ids = []
                for ticket in test:
                    the_ids.append(ticket.id)

                django_results = json.dumps(the_ids)
                test_len = test[:10]
                # END DATE FILTER
                if len(test) < 1:
                    no_results = True
                else:
                    no_results = False

                res = aware_start.strftime("%b-%d-%G")
                res2 = aware_end.strftime("%b-%d-%G")
                context = {
                    'no_results':no_results,
                    'categories' : Category.objects.all(),
                    'res' : res,
                    'res2' : res2,
                    'django_results':django_results,
                    'test':test,
                    'test_len':test_len,
                    'start':start,
                    'end':end,
                    'user':user,
                    'users':User.objects.all(),
                }
                calendar_results = get_formatted_dates([start, end])
                first_date = calendar_results[0]
                second_date = calendar_results[1]
                context["no_date"] = f"between {first_date} and {second_date}"
                context["the_date"] = f"Results for {first_date} — {second_date}"

                # test = User.objects.filter(Q(created_at__gt=aware_start) & Q(created_at__lt=aware_end))
                return render(request, "reports.html", context)
            else:
                return redirect(reverse('ticket-easy:reports-page'))
        else:
            return redirect(reverse('ticket-easy:reports-page'))
    else:
        return redirect(reverse('ticket-easy:reports-page'))

@user_level_required(8,9)
def report_daily(request):
    if 'date' in request.POST:
        date = request.POST['date']
        # print(date)
        python_date = datetime.strptime(date, "%Y-%m-%d")
        timezone = pytz.timezone('Europe/London')
        aware_date = timezone.localize(python_date)
        # print(aware_date)
        # result = Ticket.objects.filter(created_at__date=aware_date)
        result = Ticket.objects.filter(created_at__date=python_date)
        user = get_user(request)
        categories = Category.objects.all()

        if len(result) < 1:
            no_results = True
        else:
            no_results = False
        print(result)
        start = request.POST['date']


        the_ids = []
        for r in result:
            the_ids.append(r.id)
        django_results = json.dumps(the_ids)
        context = {
            'django_results':django_results,
            'start':start,
            'no_results':no_results,
            'categories':categories,
            'daily':date,
            'user':user,
            'per_day':result,
        }
        calendar_dates = get_formatted_dates([start])
        calendar_date = calendar_dates[0]
        context["no_date"] = f"for {calendar_date}"
        context["the_date"] = f"Results for {calendar_date}"
        return render(request, 'reports.html', context)
    else:
        return redirect(reverse('ticket-easy:reports-page'))

@user_level_required(8,9)
def report_view(request):
    context = {}
    start = request.POST['res1']
    end = request.POST['res2']
    print(start, type(start), "startasdoifjpsadijfoisdjfoisdjofijoisdjfdoisjsoi")
    # res = f"Results for {start} to {end}"
    if end:
        calendar_results = get_formatted_dates([start, end])
        first_date = calendar_results[0]
        second_date = calendar_results[1]
        context["the_date"] = f"Results for {first_date} — {second_date}"
    else:
        calendar_results = get_formatted_dates([start])
        date = calendar_results[0]
        context["the_date"] = f"Results for {date}"

    results = request.POST.getlist("result_items")
    if len(results) < 1:
        results = request.POST["res1"]
    id_list = []

    for item in results:
        id_list += item.split(',')

    user = get_user(request)

    finale = []
    for idn in id_list:
        ticket = Ticket.objects.get(id=idn)
        finale.append(ticket)
    context["users"] = User.objects.all()
    context["finale"] = finale
    context["user"] = user
        # 'res':res,
        # 'test':test,
        # 'users':User.objects.all(),
        # 'res':res,
        # 'finale':finale,
        # 'user':user,
        # }
    return render(request, 'report-view.html', context)

@user_level_required(8,9)
def report_view_filter(request):
    user = get_user(request)
    R = request.POST
    fc = 'filter_cat'
    fp = 'filter_prio'
    fst = 'filter_status'
    # fs = 'filter_sender'
    start = request.POST['res1']
    end = request.POST['res2']
    if start != '' and end != '':

        python_start = datetime.strptime(start, "%Y-%m-%d")
        python_end = datetime.strptime(end, "%Y-%m-%d")

        timezone = pytz.timezone('Europe/London')
        aware_start = timezone.localize(python_start) 
        aware_end = timezone.localize(python_end)

        test = Ticket.objects.filter(created_at__range=(aware_start, aware_end))
        # END getCorrectDates

        start = aware_start.strftime("%b-%d-%G")
        end = aware_end.strftime("%b-%d-%G")
        res = f"Results for {start} to {end}"
        context ={'user':user, 'res':res}
    else:
        daily = request.POST['res3']
        print(daily)
        # python_start = datetime.strptime(daily, "%Y-%m-%d")
        # timezone = pytz.timezone('Europe/London')
        # aware_start = timezone.localize(daily)
        test = Ticket.objects.filter(created_at__date=(daily))
        # END getCorrectDates
        user = get_user(request)
        R = request.POST
        fc = 'filter_cat'
        fp = 'filter_prio'
        fst = 'filter_status'
        fs = 'filter_sender'

        # day = daily.strftime("%b-%d-%G")
        res = f"Results for {daily}"
        context ={'user':user, 'res':res}

    if fc in R:
        category = Category.objects.get(id=request.POST['filter_cat'])
        if fp in R and fst not in R:
            cat = test.filter(category=category)
            p2 = cat.filter(priority=R['filter_prio'])
            if p2.exists():
                context['p2'] = p2
            else:
                context['nothing'] = "No results"

        elif fp not in R and fst in R:
            cat = test.filter(category=category)
            st2 = cat.filter(status=R['filter_status'])
            # context['st2'] = st2
            if st2.exists():
                context['st2'] = st2
            else:
                context['nothing'] = "No results"

        elif fp and fst in R:
            cat = test.filter(category=category)
            st = cat.filter(status=R['filter_status'])
            pst2 = st.filter(priority=R['filter_prio'])
            # context['pst2'] = pst2
            if pst2.exists():
                context['pst2'] = pst2
            else:
                context['nothing'] = "No results"

        elif fp not in R and fst not in R:
            cat = test.filter(category=category)
            # context['cat'] = cat
            if cat.exists():
                context['cat'] = cat
            else:
                context['nothing'] = "No results"

    if fc not in R:
        if fp in R and fst not in R:
            p1 = test.filter(priority=R['filter_prio'])
            # context['p1'] = p1
            if p1.exists():
                context['p1'] = p1
            else:
                context['nothing'] = "No results"

        elif fp not in R and fst in R:
            st1 = test.filter(status=R['filter_status'])
            # context['st1'] = st1
            if st1.exists():
                context['st1'] = st1
            else:
                context['nothing'] = "No results"

        elif fp and fst in R:
            st = test.filter(status=R['filter_status'])
            pst1 = st.filter(priority=R['filter_prio'])
            # context['pst1'] = pst1
            if pst1.exists():
                context['pst1'] = pst1
            else:
                context['nothing'] = "No results"

    return render(request, 'report-view.html', context)

@user_level_required(8,9)
def delete_report(request):
    r = Ticket.objects.all()
    r.delete()
    return redirect('/ticket-easy')



## charts ##
@user_level_required(8,9)
def g_chart(request): 
    start = request.POST['res1']
    end = request.POST['res2']

    dates = get_aware_date(start, end)
    data = Ticket.google_chart(request.POST, dates[0], dates[1])

    formatted_dates = get_formatted_dates([start, end])

    start = formatted_dates[0]
    end = formatted_dates[1]
    dates_string = f"Results for {start} to {end}"
    # dates_string = f"Results for {start} to {end}"

    chart_type = request.POST['chart-type']

    if chart_type == "pie":
        type = "pie" 
    elif chart_type == "bar":
        type = "bar"

    context = {
        # 'tickets_query': tickets,
        'values':data,
        'user':get_user(request),
        'type': type,
        'title':dates_string
        } 
    return render(request, 'report-charts.html', context)

# @user_level_required(8,9)
# def lines(request):
#     start = request.POST['bar1']
#     end = request.POST['bar2']

#     dates = get_aware_date(start, end)

#     formatted_dates = get_formatted_dates([start, end], "charts")

#     start = formatted_dates[0]
#     end = formatted_dates[1]
#     dates_string = f"Results for {start} to {end}"

#     test = Ticket.objects.filter(created_at__range=(dates[0], dates[1])).values('created_at__date', 'status').annotate(count=Count('id'))

#     data = []
#     for date in test.values_list('created_at__date', flat=True).distinct():
#         date_data = [date.strftime('%Y-%m-%d')]
#         for status in ['Unresolved', 'Resolved']:
#             count = test.filter(created_at__date=date, status=status).values_list('count', flat=True).first() or 0
#             date_data.append(count)
#         data.append(date_data)
#     # print(type(data), data, "data")

#     json_data = json.dumps(data)
#     print(len(data))

#     context = {
#         'user': get_user(request),
#         'values':json_data,
#         # 'vaxis': ['Date', 'Unresolved', 'Resolved'],
#         'type': "line",
#         'title':dates_string
#     }
#     return render(request, 'report-charts.html', context)
