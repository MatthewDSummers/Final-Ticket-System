from django.forms import ModelForm, TextInput, Textarea
from .models import CannedResponse, Reply

class MessageForm(ModelForm):
    class Meta:
        model = CannedResponse
        fields = ['name', 'subject', 'body']
        # fields = ['body'] 
        widgets = {

            'name': TextInput(attrs={'id': 'canned-response-name'}),
            'subject': TextInput(attrs={'id': 'canned-response-subject', 'name': 'the_message_subject'}),
            'body': Textarea(attrs={'id': 'canned-response-body', 'name': 'the_message_body'}),
        }
        error_messages = {
            'name': {'required': ''},
            'subject': {'required': ''},
            'body': {'required': ''},
        }
        error_css_class = ''
        required_css_class = ''



class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['body'] 
        widgets = {
            'body': Textarea(attrs={'class': 'editable'}),
        }
        labels = {
            'body': ''
        }
        error_messages = {
            'body': {'required': ''},
        }
        error_css_class = ''
        required_css_class = ''