# class TicketContext:
#     @staticmethod
#     def add_to_context(the_context, request, *args):
#         if 'key1' in request.GET:
#             the_context[request.GET['key1']] = args[0]
#         if 'key2' in request.GET:
#             the_context[request.GET['key2']] = args[1]

#     @staticmethod
#     def modify_context(the_context, request, *args):
#         if 'key3' in request.GET and len(args[0]) < 10:
#             the_context[request.GET['key3']] = args[0]
#         if 'key4' in request.GET and len(args[1]) < 5:
#             the_context[request.GET['key4']] = args[1]

#     @staticmethod
#     def process_context(request, *args):
#         the_context = {}
#         the_context.add_to_context(the_context, request, *args)
#         the_context.modify_context(the_context, request, *args)
#         return the_context

