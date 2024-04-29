from django import forms
from django.core.validators import ValidationError

from .models import Message


class ContactUsForm(forms.Form):
    text=forms.CharField(max_length=5,label="your message")
    name=forms.CharField(max_length=5,label="your name")
    def clean(self):
        text=self.cleaned_data.get("text")
        name=self.cleaned_data.get("name")
        if name==text:
            raise ValidationError("name and text are the same ",code="name_text_same")

    def clean_name(self):
        name=self.cleaned_data.get("name")
        if "a" in name:
            raise ValidationError("name cant have a ",code="a-in_name")
        return name



class MessageForm(forms.ModelForm):
    class Meta:
        model=Message
        fields="__all__"
        widgets={
            "title":forms.TextInput(attrs={
                "class":"form-control","placeholder":"enter your title",
                "style":"max-width:300px;"
            })
            ,"text":forms.TextInput(attrs={
                "class":"form-control"
            })
        }

