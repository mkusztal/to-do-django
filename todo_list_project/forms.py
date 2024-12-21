from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter the note title",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter the note content",
                    "rows": 5,
                }
            ),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) > 255:
            raise forms.ValidationError("The title cannot exceed 255 characters.")
        return title

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if not content.strip():
            raise forms.ValidationError("Content cannot be empty.")
        return content
