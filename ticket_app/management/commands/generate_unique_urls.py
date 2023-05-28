# import random
# import string 
# from ...models import Message

# def generate_unique_url():
#     while True:
#         url = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
#         if not Message.objects.filter(url=url).exists():
#             return url