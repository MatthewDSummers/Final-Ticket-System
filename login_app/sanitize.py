import bleach

def bleachUser(post_data):
    fields = {}
    desired_fields = ["first_name", "last_name", "email"]

    for field in post_data:
        if field in desired_fields:
            fields[field] = bleach.clean(post_data[field], strip=True)
    return fields
