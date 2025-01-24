from datetime import datetime

from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author', 'is_published', 'created_at',)
        widgets = {
            'pub_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            )
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['pub_date'].initial = datetime.now()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
