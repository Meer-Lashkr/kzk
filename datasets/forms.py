from django import forms
from .models import CorrectionSubmission, ParallelTextSubmission, SentenceJudgmentSubmission, LANGUAGE_VARIANT_CHOICES


class CorrectThisForm(forms.ModelForm):
    integrity_swear = forms.BooleanField(
    required=True,
    label="I swear that this submission is my own work and that I have not plagiarized.",
    error_messages={
        'required': 'You must check this box to confirm this is your own original work.'
    }
)

    class Meta:
        model = CorrectionSubmission
        fields = ['incorrect_text', 'corrected_text', 'language_variant', 'topic', 'notes']
        widgets = {
            'incorrect_text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Paste or type the incorrect sentence here...',
                'class': 'form-textarea'
            }),
            'corrected_text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write the corrected version here...',
                'class': 'form-textarea'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Optional: explain the correction...',
                'class': 'form-textarea'
            }),
            'topic': forms.TextInput(attrs={
                'placeholder': 'e.g. Grammar, Spelling, Dialect...',
                'class': 'form-input'
            }),
        }
        labels = {
            'incorrect_text': 'Incorrect Sentence',
            'corrected_text': 'Corrected Sentence',
            'language_variant': 'Kurdish Dialect / Variant',
            'topic': 'Topic / Domain (optional)',
            'notes': 'Notes (optional)',
        }


class ParallelTextForm(forms.ModelForm):
    class Meta:
        model = ParallelTextSubmission
        fields = ['source_text', 'target_text', 'source_language', 'target_language', 'topic', 'notes']
        widgets = {
            'source_text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Enter the source text...',
                'class': 'form-textarea'
            }),
            'target_text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Enter the translation / parallel version...',
                'class': 'form-textarea'
            }),
            'source_language': forms.TextInput(attrs={
                'placeholder': 'e.g. Sorani Kurdish',
                'class': 'form-input'
            }),
            'target_language': forms.TextInput(attrs={
                'placeholder': 'e.g. English',
                'class': 'form-input'
            }),
            'topic': forms.TextInput(attrs={
                'placeholder': 'e.g. News, Literature, Daily Speech...',
                'class': 'form-input'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Optional notes...',
                'class': 'form-textarea'
            }),
        }
        labels = {
            'source_text': 'Source Text',
            'target_text': 'Target / Translation Text',
            'source_language': 'Source Language',
            'target_language': 'Target Language',
            'topic': 'Topic / Domain (optional)',
            'notes': 'Notes (optional)',
        }


class IsThisCorrectForm(forms.ModelForm):
    class Meta:
        model = SentenceJudgmentSubmission
        fields = ['sentence_text', 'binary_label', 'language_variant', 'topic', 'notes']
        widgets = {
            'sentence_text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Enter the Kurdish sentence to judge...',
                'class': 'form-textarea'
            }),
            'binary_label': forms.Select(attrs={'class': 'form-select'}),
            'language_variant': forms.Select(attrs={'class': 'form-select'}),
            'topic': forms.TextInput(attrs={
                'placeholder': 'e.g. Grammar, Colloquial...',
                'class': 'form-input'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Optional: explain your judgment...',
                'class': 'form-textarea'
            }),
        }
        labels = {
            'sentence_text': 'Kurdish Sentence',
            'binary_label': 'Is this sentence correct?',
            'language_variant': 'Kurdish Dialect / Variant',
            'topic': 'Topic / Domain (optional)',
            'notes': 'Notes (optional)',
        }
