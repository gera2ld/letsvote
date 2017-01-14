from django import forms

class PollForm(forms.Form):
    title = forms.CharField()
    desc = forms.CharField(required=False)
    votes_lb = forms.IntegerField(required=False)
    votes_ub = forms.IntegerField(required=False)

class ChoiceForm(forms.Form):
    title = forms.CharField()
    desc = forms.CharField(required=False)

class AnswerForm(forms.Form):
    poll_values = forms.ModelMultipleChoiceField(queryset=None)

    def __init__(self, poll, *k, **kw):
        super().__init__(*k, **kw)
        self.poll = poll
        self.fields['poll_values'].queryset = poll.choice_set.all()

    def clean_poll_values(self):
        poll_values = self.cleaned_data['poll_values']
        if not self.poll.votes_lb <= len(poll_values) <= self.poll.votes_ub:
            raise forms.ValidationError('Invalid number of choices!')
        return poll_values
