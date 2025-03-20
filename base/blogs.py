from .models import Blog, Images

class AllBlogs:
    def blogs(slef):
        blog = Blog.objects.all()[:2]
        return blog

    def images(self):
        post_images = []
        blog = Blog.objects.all()[:2]
        for post in blog:
            post_images.append(Images.objects.filter(blog=post)[0])

        return post_images
