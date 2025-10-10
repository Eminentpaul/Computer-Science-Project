from .models import Course, Level, Timetable, Semester
from django.shortcuts import get_object_or_404
from datetime import time, datetime, timedelta





def timetable_values(lev):
    current_level = get_object_or_404(Level, level=lev)


    semester = Semester.objects.all().first()
    # timetables = Class.objects.all()
    courses = Course.objects.all().filter(semester=semester.semester, level=str(current_level).upper())
    
    levels = Level.objects.all()

    days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    
    # Generate time slots from 8:00 to 16:00 (4:00 PM) in 1-hour intervals
    time_slots = []
    start_hour = 8
    end_hour = 14
    for i in range(start_hour, end_hour + 1, 2):
        start_time = time(i, 0)
        end_time = (datetime.combine(datetime.min, start_time) + timedelta(hours=2)).time()
        time_slots.append((start_time, end_time))

    # Retrieve all users and their events, then structure the data
    levels_with_timetables = []
    all_levels = Level.objects.all().filter(level=current_level).prefetch_related('timetable_level')
    

    for level in all_levels:
        events_matrix = {}
        for day in days_of_week:
            events_matrix[day] = {}
            day_events = level.timetable_level.filter(day_of_week=day).order_by('start_time')
            for event in day_events:
                event_start_hour = event.start_time.hour
                if start_hour <= event_start_hour <= end_hour:
                    events_matrix[day][time(event_start_hour, 0)] = event
        
        levels_with_timetables.append({
            'level': level,
            'events_matrix': events_matrix,
        })


    all_values = {
        'current_level': current_level,
        'semester': semester,
        'courses': courses,
        'levels': levels,
        'days_of_week': days_of_week,
        'time_slots': time_slots,
        'levels_with_timetables': levels_with_timetables,
    }

    return all_values