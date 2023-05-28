import bleach
import re

allowed_tags = ['div', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'span', 'strong', 'b', 'i', 'em', 'strike', 'u', 'ol', 'ul', 'li', 'br']

def bleachMessage(request):

    fields = {}
    if "the_message_body" in request.POST:
        body = bleach.clean(request.POST["the_message_body"], tags=allowed_tags, strip=True)
        fields["body"] = body
    if "the_message_subject" in request.POST:
        subject = bleach.clean(request.POST["the_message_subject"], tags=allowed_tags, strip=True)
        fields["subject"] = subject

    if "the_message_recipients" in request.POST:
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        recipient_emails = request.POST["the_message_recipients"]
        email_list = recipient_emails.split(",")
        email_list = [email.replace(",", "") for email in email_list]

        emails = []
        for email in email_list:
            if re.match(EMAIL_REGEX, email):
                emails.append(email)
        fields["emails"] = emails

    # CANNED RESPONSES 
    if "name" in request.POST:
        name = bleach.clean(request.POST["name"], tags=allowed_tags, strip=True)
        fields["name"] = name
    # if request.POST["body"]: # can throw key error 
    if request.POST.get("body"):
    # if "body" in request.POST: ## won't work; conflicts with the_message_body
        body = bleach.clean(request.POST["body"], tags=allowed_tags, strip=True)
        fields["body"] = body
    if "subject" in request.POST:
        subject = bleach.clean(request.POST["subject"], tags=allowed_tags, strip=True)
        fields["subject"] = subject

    return fields



def bleachTicket(request):

    fields = {}
    if "category" in request.POST:
        fields["category"] = bleach.clean(request.POST["category"], strip=True)
    if "priority" in request.POST:
        if request.POST["priority"] != "" and request.POST["priority"] != chr(32):
            fields["priority"] = bleach.clean(request.POST["priority"], strip=True)
    if "desc" in request.POST:
        fields["desc"] = bleach.clean(request.POST["desc"], tags=allowed_tags, strip=True)

    return fields


def bleachAutomator(post_data):
    fields = {}
    for field in post_data:
        fields[field] = bleach.clean(post_data[field], strip=True)
    return fields