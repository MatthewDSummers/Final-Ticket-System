from django.core.paginator import Paginator


# THIS IS USED FOR THE MESSAGES 
# Eventually refactor it for a broader scope

def paginate_it(request, the_list, context_title, page_number=10, elided=None):
    p = Paginator(the_list, page_number)
    page_number = request.GET.get("page", 1)

    # if supplied with a greater page number, just gives the last page 
    if int(page_number) > p.num_pages:
        page_number = int(page_number) # ?
        page_number = p.num_pages

    the_paginated_list = p.get_page(page_number)

    page_range =  p.get_elided_page_range(page_number, on_each_side=4, on_ends=1)

    context = {
        context_title: the_paginated_list,
    }

    context["page_range"] = p.get_elided_page_range(page_number, on_each_side=4, on_ends=1)
    context["page_range_length"] = len(list(page_range))
    context["page_number"] = page_number

    if context_title == "mail":
        if elided:
            title = request.GET.get("title") if request.method == "GET" else request.POST.get("title")
            context['elided_page_number'] = "/ticket-easy/mail/" + f"?title={title}&page="
    return context