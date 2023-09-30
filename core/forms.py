from django import forms

from core.models import Avowal, Comment

from hcaptcha.fields import hCaptchaField


class CreateAvowal(forms.ModelForm):
    hcaptcha = hCaptchaField()

    class Meta:
        model = Avowal
        fields = (
            "type_topic",
            "body",
        )
        widgets = {
            "type_topic": forms.Select(
                attrs={"class": "p-4 rounded-lg"},
            ),
            "body": forms.Textarea(
                attrs={
                    "class": "rounded-lg resize-none p-4",
                    "id": "body",
                    "rows": "4",
                },
            ),
        }


class CreateCommentForm(forms.ModelForm):
    hcaptcha = hCaptchaField()

    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "class": "w-full rounded-lg resize-none p-4 mt-2",
                    "id": "comment",
                    "rows": "4",
                },
            )
        }
