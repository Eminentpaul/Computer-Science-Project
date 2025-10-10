from django.shortcuts import render, redirect
from base.models import Timetable
from django.contrib.auth.decorators import login_required
from django.contrib import messages as mg
from base.models import Course, Timetable, Semester, Level
from .forms import TimetableForm
from datetime import datetime, time
from django.shortcuts import get_object_or_404

# Create your views here.

@login_required(login_url='login')
def timetable_dash(request):

    if not request.user.level:
        mg.warning(request, 'Please Update your Level to Continue')
        return redirect('edit_profile', request.user.profile.id)
    

    level_query = get_object_or_404(Level, level=str(request.user.level))
    
    courses = Timetable.objects.all().filter(level=level_query)
    
    context = {
        'courses': courses,
        
    }
    
    return render(request, 'timetable/dashboard/index.html', context)




@login_required(login_url='login')
def delete_course(request, pk):
    course = get_object_or_404(Timetable, id=pk)
    course.delete()


    mg.success(request, 'Course deleted Successfully!')
    return redirect('timetable_dash')



@login_required(login_url='login')
def edit_course(request, pk):
    course = get_object_or_404(Timetable, id=pk)
    form = TimetableForm(instance=course)
    

    if request.method == 'POST':
        
        form = TimetableForm(request.POST, instance=course)

        if form.is_valid():
            form.save()

            mg.success(request, 'Course Updated Successfully!')
            return redirect('timetable_dash')


    context = {
        'form': form,
        'edit': True
    }
    return render(request, 'timetable/dashboard/add-lecture.html', context)




@login_required(login_url='login')
def create_timetable(request):
    level = request.user.level.upper()
    semester = Semester.objects.all().first()
    all_courses = Course.objects.all().filter(level=level, semester=semester)

    level_query = get_object_or_404(Level, level=str(request.user.level))
    

    if request.method == 'POST':
        start = request.POST.get('start_time')
        end = request.POST.get('end_time')
        day_of_week = request.POST.get('day_of_week')
        course = get_object_or_404(Course, id=request.POST.get('course'))
        s = datetime.strptime(start, '%H:%M')
        e = datetime.strptime(end, '%H:%M')
        if s == e:
            mg.error(request, f'The Starting time and ending time of {course} cannot be the same')
        else:
            colliding = Timetable.objects.all().filter(day_of_week=day_of_week, \
                                            level=level_query, \
                                                start_time=s).last()
        
            if colliding:
                mg.warning(request, f'{course} cannot be starting at the same time({start}) with {colliding.course} on {day_of_week.title()}')
            else:
                form = TimetableForm(request.POST)

                if form.is_valid():
                    timetable = form.save(commit=False)
                    timetable.level = level_query
                    timetable.save()

                    mg.success(request, f'{course} created sucessfully')
                    return redirect('add_lecture')
                
                else: mg.error(request, 'Invalid Input')
        

    
    context = {
        'all_courses': all_courses,
        'form': TimetableForm()
    }
    return render(request, 'timetable/dashboard/add-lecture.html', context)
    