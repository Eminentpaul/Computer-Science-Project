from django.shortcuts import render, redirect
from .models import HomeSlide, Blog, Images, Hall, Excos, Comment
from .blogs import AllBlogs
from .forms import CommentForm 
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    home_slide = HomeSlide.objects.all()

    context = {
        'home_slide': home_slide,
        'blogs': AllBlogs().blogs(),
        'images': AllBlogs().images(),
        'dd': 'norml'
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
    halls = Hall.objects.all()

    context = {
        'halls': halls,
        'blogs': AllBlogs().blogs(),
        'images': AllBlogs().images(),
    }
    return render(request, 'base/halls.html', context)

def lecturer(request):
    context = {
        'excos': excos,
        'blogs': AllBlogs().blogs(),
        'images': AllBlogs().images(),
    }
    return render(request, 'base/faculty.html', context)


def excos(request):
    excos = Excos.objects.all()

    context = {
        'excos': excos,
        'blogs': AllBlogs().blogs(),
        'images': AllBlogs().images(),
    }
    return render(request, 'base/excos.html', context)

def contact(request):
    context = {
        'excos': excos,
        'blogs': AllBlogs().blogs(),
        'images': AllBlogs().images(),
    }
    return render(request, 'base/contact.html', context)


def excos_pop(request, pk):
    exco = Excos.objects.get(id=pk)
    print(exco)
    return(request, 'base/partial/model.html', {'exco':exco})


def _404(request, exception):
    return render(request, '404.html', {})