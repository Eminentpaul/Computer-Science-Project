from django.db import models
from .utils import imageResize
from user_auth.models import User, Level
from django.utils.safestring import mark_safe
from datetime import datetime
from simple_history. models import HistoricalRecords

categories = (
    ('Campus', 'Campus'),
    ('Education', 'Education'),
    ('Social', 'Social'),
    ('Fellowship', 'Fellowship'),
    ('Research', 'Research')
)


Letcurer_status = (
    ('Full Time', 'Full Time'),
    ('Part Time', 'Part Time')
)


classes = (
    ('ND1', 'ND1'),
    ('ND2', 'ND2'),
    ('HND1_NCC', 'HND1 NCC'),
    ('HND1_SWD', 'HND1 SWD'),
    ('HND2_NCC', 'HND2 NCC'),
    ('HND2_SWD', 'HND2 SWD'),
)


semester = (
        ('First Semester', 'First Semester'), 
        ('Second Semester', 'Second Semester')
    )

# Updated choices to only include Monday to Friday
DAYS_OF_WEEK = (
    ('monday', 'Monday'),
    ('tuesday', 'Tuesday'),
    ('wednesday', 'Wednesday'),
    ('thursday', 'Thursday'),
    ('friday', 'Friday'),
)

CLASS_LEVEL = (
    ('nd1', 'ND1'),
    ('nd2', 'ND2'),
    ('hnd1_ncc', 'HND1 NCC'),
    ('hnd1_swd', 'HND1 SWD'),
    ('hnd2_ncc', 'HND2 NCC'),
    ('hnd2_swd', 'HND2 SWD'),

)

    

def get_year_choices():
    current_year = datetime.now().year
    return [(year, year) for year in range(2010, current_year + 20)]




# Create your models here.
class HomeSlide(models.Model):
    title = models.CharField(max_length=100)
    tag = models.CharField(max_length=300)
    image = models.ImageField(upload_to='home/')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.image:
            self.image = imageResize(self.image)
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
    
    @property
    def home_image(self):
        return self.image.url
    



class Blog(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=categories) 
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created']




class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    comment = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.author
    
    class Meta:
        ordering = ['-created']




class Images(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blogs')

    def save(self, *args, **kwargs):
        if self.image:
            self.image = imageResize(self.image)
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def blog_image(self):
        return self.image.url

    class Meta:
        verbose_name = "Images"








class Excos(models.Model):
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    year = models.IntegerField(choices=get_year_choices, default=datetime.now().year,)
    contact = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='Excos')

    def __str__(self):
        return self.name 
    
    def save(self, *args, **kwargs):
        if self.image:
            self.image = imageResize(self.image)
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)


    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 45px; height:auto;" />' % self.image.url)
        else:
            return 'No Image Found' 
    image_tag.short_description = 'Image'

    class Meta:
        verbose_name_plural = "Excos"
        ordering = ['-year']




class Staff(models.Model):
    full_name = models.CharField(max_length=200, verbose_name='Full Name')
    qualifications = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=500, choices=Letcurer_status, blank=True, null=True)
    citation = models.TextField(blank=True, null=True)
    phone_no = models.CharField(max_length=20, blank=True, null=True, verbose_name='Phone Number')
    email = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to='Lecturers', blank=True, null=True)
    is_teaching = models.BooleanField(default=True)



    def __str__(self):
        return self.full_name
    

    def avatar(self):
        if self.image:
            return self.image.url


    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 45px; height:auto;" />' % self.image.url)
        else:
            return 'No Image Found' 
    image_tag.short_description = 'Image'
    

    def save(self, *args, **kwargs):
        if self.image:
            self.image = imageResize(self.image)
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    
    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Staff List'



class Course(models.Model):
    course_code = models.CharField(max_length=50, verbose_name='Course Code')
    course_title = models.CharField(max_length=500, verbose_name='Course Title', null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True, blank=True)
    credit_load = models.CharField(max_length=20, null=True, blank=True)
    semester = models.CharField(max_length=200, choices=semester)
    lecturer = models.ForeignKey(Staff, on_delete=models.SET_NULL, 
                                 null=True, related_name='lecturer', 
                                 verbose_name='Assigned Lecturer', 
                                 blank=True)
    history = HistoricalRecords()


    def __str__(self):
        return self.course_code
    

    class Meta:
        ordering = ['semester', '-level']
        
    


class HOD(models.Model):
    lecturer = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    started = models.IntegerField(choices=get_year_choices)
    ended = models.CharField(max_length=20)

    def __str__(self):
        return self.lecturer.full_name
    

    class Meta:
        ordering = ['-started']
        verbose_name = 'HOD'
        verbose_name_plural = 'HODs' 



class Lab(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='Labs')


    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        if self.image:
            self.image = imageResize(self.image)
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)


    # class Meta:
    #     verbose_name = 'Lab'


class Class(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='Classes', blank=True, null=True, verbose_name='Class Image')
    timetable = models.ImageField(upload_to='Classes', blank=True, null=True)
    level = models.CharField(max_length=10, choices=CLASS_LEVEL, default='nd1')


    def __str__(self):
        return self.name
    
    def class_image(self):
        if self.image:
            return self.image.url


    def save(self, *args, **kwargs):
        if self.image:
            self.image = imageResize(self.image)
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
 

    class Meta:
        verbose_name_plural = 'Classes'




class Project_Team(models.Model):
    full_name = models.CharField(max_length=400)
    regno = models.CharField(max_length=50, verbose_name='Registration Number')
    designation = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=20, verbose_name='Phone Number')
    image = models.ImageField(upload_to='Team')


    def __str__(self):
        return self.full_name
    

    def avatar(self):
        if self.image:
            return self.image.url
    

    def save(self, *args, **kwargs):
        if self.image:
            self.image = imageResize(self.image)
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    
    class Meta:
        verbose_name = 'Project Team'
        verbose_name_plural = 'Project Teams'



class Semester(models.Model):
    semester = models.CharField(max_length=200, choices=semester)

    def __str__(self):
        return self.semester
    

    def clean(self):
        timetables = Timetable.objects.all()  #.filter(day_of_week='monday')
        timetables.delete()
        return None
        
 


class Timetable(models.Model):
    
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='timetable_level')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['day_of_week', 'start_time', 'level']

    def __str__(self):
        return f'{self.course} on {self.day_of_week}'