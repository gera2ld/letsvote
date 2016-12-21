from django import forms

class PollForm(forms.Form):
    poll_values = forms.ModelMultipleChoiceField(queryset=None, required=True)

    def __init__(self, choices, *k, **kw):
        super().__init__(*k, **kw)
        self.fields['poll_values'].queryset = choices