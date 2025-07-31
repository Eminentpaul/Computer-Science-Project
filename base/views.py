from django.shortcuts import render, redirect
from .models import HomeSlide, Blog, Images, Class_Timetable, Excos, Comment, Staff, Lab, Class
from .blogs import AllBlogs
from .forms import CommentForm 
import datetime
from django.contrib.auth.decorators import login_required


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

    context = {
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
    blog = Blog.objects.get(id=pk)
    comments = Comment.objects.all().filter(blog=blog)
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

@login_required(login_url='login')
def halls(request):
    halls = Class_Timetable.objects.all()

    context = {
        'halls': halls,
        'blogs': AllBlogs().blogs(),
        'images': AllBlogs().images(),
    }
    return render(request, 'base/halls.html', context)

def lecturer(request):
    lecturers = Staff.objects.all().filter(is_teaching=True)
    context = {
        'lecturers': lecturers,
        'blogs': AllBlogs().blogs(),
        'images': AllBlogs().images(),
    }
    return render(request, 'base/faculty.html', context)


def lecturer_details(request, pk):
    lecturer = Staff.objects.get(id=pk)

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
    lab = Lab.objects.get(id=pk)
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
    classroom = Class.objects.get(id=pk)
    context = {
        'lab': classroom,
        'blogs': AllBlogs().blogs(),
        'images': AllBlogs().images(),
    }
    return render (request, 'base/partial/lab.html', context)




def class_timetable(request):
    timetables = Class.objects.all()

    context = {
        'timetables': timetables,
        'blogs': AllBlogs().blogs(),
        'images': AllBlogs().images(),
        'timetable': True,
    }
    return render(request, 'base/class.html', context)


def class_timetable_pop(request, pk):
    timetable = Class.objects.get(id=pk)
    context = {
        'timetable': timetable,
        'blogs': AllBlogs().blogs(),
        'images': AllBlogs().images(),
        'time': True
    }
    return render (request, 'base/partial/class.html', context)



def excos(request):
    current_year = datetime.datetime.now().year
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
    exco = Excos.objects.get(id=pk)
    context = {
        'name': exco.name,
        'position': exco.position,
        'image': exco.image.url, 
        'year': exco.year
    }
    return render (request, 'base/partial/modal.html', context)


def _404(request, exception):
    return render(request, '404.html', {})