from django import forms


class PollForm(forms.Form):

    first_name = forms.CharField(required=True, max_length=100)
    last_name = forms.CharField(required=True, widget=forms.Textarea)
    specialization = forms.MultipleChoiceField(required=True)
    mail = forms.EmailField(required=False)
    side_nickname = forms.URLField(required=False)

    def save(self, *args, **kwargs):
        poll = super(PollForm, self).save(commit=False)
        if poll.validate_unique(exclude='id'):
            poll.save()
        else:
            return