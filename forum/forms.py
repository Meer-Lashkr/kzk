from django import forms
from .models import Question, Answer, QuestionTag


class QuestionForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=QuestionTag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Tags"
    )

    class Meta:
        model = Question
        fields = ('title', 'body', 'tags')
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'What is your Kurdish language question?',
                'class': 'form-input'
            }),
            'body': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Describe your question in detail...',
                'class': 'form-textarea'
            }),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Share your knowledge and answer this question...',
                'class': 'form-textarea'
            }),
        }
        labels = {
            'body': 'Your Answer',
        }
