from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse
from .models import Feature, Pelcon,Profile, Physics, SubjectFaculty, Upload_Subjects
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import File, Faculty,Semester,Subject
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse

def file_list(request):
    files = File.objects.all()
    return render(request, 'file_list.html', {'files': files})

def upvote_file(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    file.upvotes += 1
    file.save()
    return redirect('file_list')

def downvote_file(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    file.downvotes += 1
    file.save()
    return redirect('file_list')


# Create your views here.
def index(request):
    features =  Feature.objects.all()
 
    return render(request, 'index.html', {'features': features})


def login(request):
    if request.method == 'POST':
       username = request.POST['username']
       password = request.POST['password']

       user = auth.authenticate(username = username, password =password  )

       if user is not None:
        auth.login(request , user)
        return redirect('/login')    
       else:
        messages.info(request, 'invalid username or password')
        return redirect("/")
    else:
        return render(request, 'login.html')

def signup(request):
    if request.method =='POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username= request.POST['username']
        email= request.POST['email']
        password = request.POST['password']
        #repassword= request.POST['repassword']
               
       # if password == repassword:
        #if User.objects.filter(email=email).exists():
                #messages.info(request, 'email already exist!')
               # return redirect('signup/')
        #elif User.objects.filter(username==username).exists():
        #        messages.info(request, 'username already taken!')
                #return redirect('signup/')
        #else:
        user= User.objects.create_user(first_name=firstname, last_name=lastname, username=username,email=email, password=password)#, repassword=repassword)
        user.save()

                #user_model = User.objects.get(username=username)
                #new_user = Profile.objects.create(first_name=firstname, last_name=lastname, username=username)
                #new_user.save()
        return redirect('/login')
    else:
           #  messages.info(request, 'passwords donot match')
            # return redirect('/')
     return render(request,'signup.html')
    
class PelconView(generic.ListView):
	model = Pelcon
	template_name = 'pelcon.html'
	context_object_name = 'files'
	paginate_by = 4
	
def get_queryset(self):
		return Pelcon.objects.order_by('-id')

def Upload(request):
	if request.method == 'POST':
		name = request.POST['name']
		owner = request.POST['owner']
		pdf = request.FILES['pdf']
		faculty_name = request.POST['faculty']
		semester_name = request.POST['semester']
		subject_name = request.POST['subject']
		subject_faculty = SubjectFaculty.objects.get(
            faculty__name=faculty_name,
            semester__name=semester_name,
            subject__name=subject_name
        )
		upload = Upload_Subjects(name=name, owner=owner, pdf=pdf, subject_faculty=subject_faculty)
		upload.save()
	
		messages.success(request, 'Files was Submitted successfully')
		return redirect('pelcon')
	else:
		messages.error(request, 'Files was not Submitted successfully')
		return redirect('myupload')    



#subject
class PhysicsView(generic.ListView):
	model = Physics
	template_name = 'Physics1.html'
	context_object_name = 'files'
	paginate_by = 4


	def get_queryset(self):
		return Physics.objects.order_by('-id')


def PhysicsUpload(request):
    faculties = Faculty.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        owner = request.POST['owner']
        pdf = request.FILES['pdf']
        faculty_id = request.POST['faculty']
        faculty = Faculty.objects.get(id=faculty_id)

        b = Physics(name=name, owner=owner, pdf=pdf, faculty=faculty)
        b.save()

        messages.success(request, 'Files was Submitted successfully')
        return redirect('Physics1')
    else:
        messages.error(request, 'Files was not Submitted successfully')
    context = {'faculties': faculties}
    return render(request, 'myupload.html', context) 
#endsubject	  
       
def test(request):
    faculties = Faculty.objects.all()
    semesters = Semester.objects.filter(subjectfaculty__faculty=1).distinct()  # Initialize semesters to an empty queryset
    subjects = Subject.objects.all()  # Initialize subjects to an empty queryset
    
    selected_faculty_id = request.POST.get('faculty')
    selected_semester = request.POST.get('semester')
    selected_subject = request.POST.get('subject')
    selected_faculty_name = ''
    
    if selected_faculty_id:
        selected_faculty = Faculty.objects.get(id=selected_faculty_id)
        selected_faculty_name = selected_faculty.name
        semesters = Semester.objects.filter(subjectfaculty__faculty=selected_faculty).distinct()

    if selected_semester:
        selected_semester = Semester.objects.get(semester=selected_semester)
        subjects = Subject.objects.filter(subjectfaculty__faculty=selected_faculty, subjectfaculty__semester=selected_semester)
    
    if request.method == 'POST':
        name = request.POST['name']
        owner = request.POST['owner']
        pdf = request.FILES['pdf']
        subject_faculty_id = request.POST['subject']
        subject_faculty = SubjectFaculty.objects.get(id=subject_faculty_id)
        upload = Upload_Subjects(name=name, owner=owner, pdf=pdf, subject_faculty=subject_faculty)
        upload.save()
        messages.success(request, 'File was submitted successfully')
        if request.is_ajax():
            data = {'success': True}
            return JsonResponse(data)
        return redirect('Physics1')
    
    context = {
        'faculties': faculties,
        'semesters': semesters,
        'subjects': subjects,
        'selected_faculty_id': selected_faculty_id,
        'selected_semester': selected_semester,
        'selected_subject': selected_subject,
    }
    return render(request, 'test1.html', context)

def get_semesters(request):
    faculty_id = request.GET.get('faculty_id')
    if not faculty_id:
        return JsonResponse({'error': 'Faculty ID is required.'})

    faculty = get_object_or_404(Faculty, id=faculty_id)
    semesters = Semester.objects.filter(subjectfaculty__faculty=faculty).distinct()
  
    data = {
        'semesters': list(semesters.values('name','id')),
        
    }
    return JsonResponse(data)

def get_subjects(request):
    faculty_id = request.GET.get('faculty_id')
    if not faculty_id:
        return JsonResponse({'error': 'Faculty ID is required.'})

    faculty = get_object_or_404(Faculty, id=faculty_id)
    semesters = Semester.objects.filter(subjectfaculty__faculty=faculty).distinct()
  
    data = {
        'subjects': list(semesters.values('name','id')),
        
    }
    return JsonResponse(data)



def Physics1(request):
	return render(request, 'Physics1.html')

def Chemistry1(request):
	return render(request, 'Chemistry1.html')



def myupload(request):
    faculties = Faculty.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        owner = request.POST['owner']
        pdf = request.FILES['pdf']
        faculty_id = request.POST['faculty']
        faculty = Faculty.objects.get(id=faculty_id)

        b = Physics(name=name, owner=owner, pdf=pdf, faculty=faculty)
        b.save()

        messages.success(request, 'Files was Submitted successfully')
        return redirect('Physics1')
    else:
       messages.error(request, 'Files was not Submitted successfully')
       context = {'faculties': faculties}
       return render(request, 'myupload.html', context)   

def Physics_page(request):
	return render(request, 'Physics_page.html')

def Chemistry_page(request):
	return render(request, 'Chemistry_page.html')


def computercourses(request):
    return render(request, 'computercourses.html')

def mechanicalcourses(request):
    return render(request, 'mechanicalcourses.html')

def architecturecourses(request):
    return render(request, 'architecturecourses.html')

def electricalcourses(request):
    return render(request, 'electricalcourses.html')

def electronicscourses(request):
    return render(request, 'electronicscourses.html')

def civilcourses(request):
    return render(request, 'civilcourses.html')

def sidebar(request):
    return render(request, 'sidebar.html')

def view(request):
    return render(request, 'view.html')
 
 # Data to be inserted
faculties = ['Computer', 'Civil', 'Architecture', 'Mechanical', 'Electrical', 'Electronic']
semesters = ['First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh', 'Eighth', 'Ninth', 'Tenth']


# Insert faculties
for faculty in faculties:
    Faculty.objects.get_or_create(name=faculty)

# Insert semesters
for semester in semesters:
    Semester.objects.get_or_create(name=semester)

# Create a list of dictionaries, where each dictionary represents a Subject
subjects_data = [
    {'name': 'Physics', 'faculties': [{'faculty': 'Computer', 'semester': 'First'}, {'faculty': 'Electronic', 'semester': 'First'},{'faculty': 'Electrical', 'semester': 'First'}]},
    {'name': 'Mathematics1', 'faculties': [{'faculty': 'Computer', 'semester': 'First'}, {'faculty': 'Civil', 'semester': 'First'},{'faculty': 'Electronic', 'semester': 'First'},{'faculty': 'Electrical', 'semester': 'First'},{'faculty': 'Architecture', 'semester': 'First'},{'faculty': 'Mechanical', 'semester': 'First'},]},
    {'name': 'Computer_Programming', 'faculties': [{'faculty': 'Computer', 'semester': 'First'}, {'faculty': 'Civil', 'semester': 'First'},{'faculty': 'Electronic', 'semester': 'First'},{'faculty': 'Mechanical', 'semester': 'First'},]},
    {'name': 'Applied_Mechanics',  'faculties': [{'faculty': 'Computer', 'semester': 'First'},{'faculty': 'Electronic', 'semester': 'First'},{'faculty': 'Electrical', 'semester': 'First'},{'faculty': 'Architecture', 'semester': 'First'},]},
    {'name': 'Drawing1', 'faculties': [{'faculty': 'Computer', 'semester': 'First'}, {'faculty': 'Civil', 'semester': 'First'}]},
    {'name': 'Basic_Electrical _Engineering', 'faculties': [{'faculty': 'Computer', 'semester': 'First'},{'faculty': 'Electronic', 'semester': 'First'},{'faculty': 'Electrical', 'semester': 'First'}]},
]

# Loop through the list of subjects and create a Subject object for each one
for subject_data in subjects_data:
    # Create the Subject object
    subject, created = Subject.objects.get_or_create(name=subject_data['name'])
    
    # Loop through the faculties and semesters for this subject and create the SubjectFaculty objects
    for faculty_data in subject_data['faculties']:
        faculty_name = faculty_data['faculty']
        semester_name = faculty_data['semester']
        faculty = Faculty.objects.get(name=faculty_name)
        semester = Semester.objects.get(name=semester_name)
        SubjectFaculty.objects.get_or_create(subject=subject, faculty=faculty, semester=semester)
	
  