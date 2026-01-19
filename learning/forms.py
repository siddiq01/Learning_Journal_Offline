from django import forms
from .models import Topic
from django_ckeditor_5.widgets import CKEditor5Widget

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        # 🟢 Added difficulty back as it is in your model
        fields = ['title', 'subject', 'content', 'status', 'difficulty']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter a catchy title...'}),
            # 🟢 Use CKEditor5Widget for the content field
            'content': CKEditor5Widget(attrs={"class": "django_ckeditor_5"}, config_name="default"),
            'subject': forms.Select(),
            'status': forms.Select(),
            'difficulty': forms.Select(),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply form-control to all fields EXCEPT content (CKEditor manages its own styling)
        for name, field in self.fields.items():
            if name != 'content':
                field.widget.attrs.update({'class': 'form-control'})