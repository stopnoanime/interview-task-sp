from django import forms

class PromptForm(forms.Form):
    prompt = forms.CharField(label="LLM Prompt", widget=forms.Textarea)