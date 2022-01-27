from django.forms import ModelForm
from .models import Choose


class Poll(ModelForm):
    class Meta:
        model = Choose
        fields = ['count_black', 'count_white', 'count_white']



