from django.shortcuts import render, redirect
from .models import HomeSlide, Blog, Images, Excos, Comment, Staff, Lab, Class, HOD, Project_Team, Course, Semester, Timetable, Level
from .blogs import AllBlogs
from .forms import CommentForm 
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from datetime import time, timedelta, datetime


# Create your views here.

def home(request):
    home_slide = HomeSlide.objects.all()
    blog = Blog.objects.all().first()
    post_images = Images.objects.filter(blog=blog)[0]

    context = {
        'home_slide': home_slide,
        'blogs': AllBlogs().blogs(),
        'images': AllBlogs().images(),
        'dd': 'norml', 
        'blog': blog, 
        'post_images': post_images,
    }
    return render(request, 'base/index.html', context)

def about(request):
    hods = HOD.objects.all()
    context = {
        'hods': hods,
        'blogs': AllBlogs().blogs(),
        'images': AllBlogs().images(),
    }
    return render(request, 'base/about.html', context)

def blog(request):
    blogs = Blog.objects.all()
    post_images = []
    for post in blogs:
        post_images.append(Images.objects.filter(blog=post)[0])

    context = {
        'all_blogs': blogs,
        'all_images': post_images,
        'blogs': AllBlogs().blogs(),
        'images': AllBlogs().images(),
    }
    return render(request, 'base/blog.html', context)

def blog_details(request, pk):
    form = CommentForm()

    blog = get_object_or_404(Blog, id=pk)
    comments = blog.comment_set.all()
    images = Images.objects.all().filter(blog=blog)
    others = images[1:]

    other_blogs = []
    post_images = []
    
    blogs = Blog.objects.all()[:5]
    for x in blogs:
        if x != blog:
            other_blogs.append(x)
            post_images.append(Images.objects.filter(blog=x)[0])

    # Submitting Comments 
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog 
            comment.save()

            return redirect('blog_details', blog.id)

    context = {
        'blog': blog,
        'images': others, 
        'main': images[0],
        'blogs': other_blogs,
        'comments': comments,
        'other_blog_images': post_images,
        
    }
    return render(request, 'base/blog-details.html', context)


def lecturer(request):
    lecturers = Staff.objects.all().filter(is_teaching=True)
    context = {
        'lecturers': lecturers,
        'blogs': AllBlogs().blogs(),
        'images': AllBlogs().images(),
    }
    return render(request, 'base/faculty.html', context)


def lecturer_details(request, pk):
    lecturer = get_object_or_404(Staff, id=pk)

    context = {
        'lecturer': lecturer
    }

    return render (request, 'base/partial/lecturer.html', context)


def non_lecturers(request):
    lecturers = Staff.objects.all().filter(is_teaching=False)
    non_teaching = True
    context = {
        'lecturers': lecturers,
        'blogs': AllBlogs().blogs(),
        'images': AllBlogs().images(),
        'non_teaching': non_teaching,
    }
    return render(request, 'base/faculty.html', context)


def labs(request):
    labs = Lab.objects.all()

    context = {
        'labs': labs,
        'blogs': AllBlogs().blogs(),
        'images': AllBlogs().images(),
    }
    return render(request, 'base/labs.html', context)


def lab_pop(request, pk):
    lab = get_object_or_404(Lab, id=pk)
    context = {
        'lab': lab
    }
    return render (request, 'base/partial/lab.html', context)


def class_room(request):
    classroom = Class.objects.all()

    context = {
        'labs': classroom,
        'blogs': AllBlogs().blogs(),
        'images': AllBlogs().images(),
    }
    return render(request, 'base/class.html', context)


def class_pop(request, pk):
    classroom = get_object_or_404(Class, id=pk)
    context = {
        'lab': classroom,
        'blogs': AllBlogs().blogs(),
        'images': AllBlogs().images(),
    }
    return render (request, 'base/partial/lab.html', context)




def class_timetable(request):
    semester = Semester.objects.all().first()
    timetables = Class.objects.all()
    courses = Course.objects.all().filter(semester=semester.semester)
    
    levels = []

    for timetable in Timetable.objects.all():
        if timetable.level not in levels:
            levels.append(timetable.level)

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
    all_levels = Level.objects.all().prefetch_related('timetable_level')
    

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

    context = {
        'timetables': timetables,
        'blogs': AllBlogs().blogs(),
        'images': AllBlogs().images(),
        'timetable': True,
        'courses': courses,
        'semester': semester,
        'days_of_week': days_of_week,
        'time_slots': time_slots,  # Now a list of tuples (start, end)
        'levels_with_timetables': levels_with_timetables,
        'levels': levels
    }
    return render(request, 'base/class.html', context)


def class_timetable_pop(request, pk):
    timetable = get_object_or_404(Class, id=pk)
    context = {
        'timetable': timetable,
        'blogs': AllBlogs().blogs(),
        'images': AllBlogs().images(),
        'time': True
    }
    return render (request, 'base/partial/class.html', context)



def excos(request):
    current_year = datetime.now().year
    excos = Excos.objects.all().filter(year=current_year)

    all_years = []

    for exco in Excos.objects.all(): 
        if exco.year not in all_years:
            all_years.append(exco.year)


    context = {
        'excos': excos,
        'all_years': all_years,
        'current_year': current_year,
        'blogs': AllBlogs().blogs(),
        'images': AllBlogs().images(),
    }
    return render(request, 'base/excos.html', context)


def excos_year(request, pk):
    current_year = pk
    excos = Excos.objects.all().filter(year=pk)

    all_years = []

    for exco in Excos.objects.all(): 
        if exco.year not in all_years:
            all_years.append(exco.year)


    context = {
        'excos': excos,
        'all_years': all_years,
        'current_year': current_year,
        'blogs': AllBlogs().blogs(),
        'images': AllBlogs().images(),
    }

    return render(request, 'base/partial/year.html', context)






def contact(request):
    context = {
        'excos': excos,
        'blogs': AllBlogs().blogs(),
        'images': AllBlogs().images(),
    }
    return render(request, 'base/contact.html', context)


def excos_pop(request, pk):
    exco = get_object_or_404(Excos, id=pk)
    context = {
        'name': exco.name,
        'position': exco.position,
        'image': exco.image.url, 
        'year': exco.year
    }
    return render (request, 'base/partial/modal.html', context)





def developer(request):
    team = Project_Team.objects.all()

    context = {
        'team': team,
        'blogs': AllBlogs().blogs(),
        'images': AllBlogs().images(),
    }
    return render(request, 'base/developer.html', context)


def developer_pop(request, pk):
    team = get_object_or_404(Project_Team, id=pk)
    context = {
        'team': team,
        'blogs': AllBlogs().blogs(),
        'images': AllBlogs().images(),
    }
    return render (request, 'base/partial/team.html', context)



def _404(request, exception):
    return render(request, '404.html', {})