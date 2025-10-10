from django.forms import ModelForm
from base.models import Timetable

class TimetableForm(ModelForm):
    class Meta:
        model = Timetable
        fields = ['course', 'day_of_week', 'start_time', 'end_time']