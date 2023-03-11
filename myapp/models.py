from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Feature(models.Model):
    name = models.CharField(max_length=100)
    details = models.CharField(max_length=500)

class Profile(models.Model):
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)

class Faculty(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Semester(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=50)
    semesters = models.ManyToManyField(Semester, through='SubjectSemester')
    faculties = models.ManyToManyField(Faculty, through='SubjectFaculty')
    def __str__(self):
        return self.name


    
class SubjectFaculty(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, default=1)

    class Meta:
        unique_together = ('subject', 'faculty', 'semester')
    

class SubjectSemester(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, default=1)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('subject', 'semester', 'faculty')


class Upload_Subjects(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='store/pdf/')
    subject_faculty = models.ForeignKey(SubjectFaculty, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    def __str__(self):
        return self.name


class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)    
    



class Pelcon(models.Model):
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='store/pdfs/')
   # cover = models.ImageField(upload_to='store/covers/')


    def __str__(self):
        return self.name
    
class Physics(models.Model):
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    pdf= models.FileField(upload_to='store/pdfs/Physics')


    def __str__(self):
        return self.name 
    



