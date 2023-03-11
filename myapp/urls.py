from django.contrib import admin
from django.urls import path
from . import views
from .views import file_list, get_semesters, upvote_file, downvote_file



urlpatterns = [
     path('', views.index, name='index'),
     path('login/',views.login, name='login'),
     path('login/signup/',views.signup, name='signup'),
     path('computercourses/', views.computercourses, name='computercourses'),
     path('mechanicalcourses/', views.mechanicalcourses, name='mechanicalcourses'),
     path('electricalcourses/', views.electricalcourses, name='electricalcourses'),
     path('electronicscourses/', views.electronicscourses, name='electronicscourses'),
     path('civilcourses/', views.civilcourses, name='civilcourses'),
     path('architecturecourses/', views.architecturecourses, name='architecturecourses'),
     path('computercourses/Physics1/Chemistry1', views.Chemistry1, name='Chemistry1'),
   
     path('', file_list, name='file_list'),
    path('upvote/<int:file_id>/', upvote_file, name='upvote_file'),
    path('downvote/<int:file_id>/', downvote_file, name='downvote_file'),

     path('file_list/', views.file_list, name='file_list'),
     path('test1/', views.test, name='test1'),

      #path('pelcon/', views.PelconView.as_view(), name='pelcon')
     #path('pelconUpload/', views.pelconUpload, name='pelconUpload'),
     path('myupload/', views.myupload, name='myupload'),
     
     path('Physics1/', views.PhysicsView.as_view(), name='Physics1'),
     path('PhysicsUpload/', views.PhysicsUpload, name='PhysicsUpload'),
     path('Physics_page/', views.Physics_page, name='Physics_page'),
     path('computercourses/Physics1/', views.PhysicsView.as_view(), name='Physics1'),
     

     path('get_semesters/', views.get_semesters, name='get_semesters'),
     path('get_subjects/', views.get_subjects, name='get_subjects'), 
     path('test1/', views.test, name='test1'),  
     path('view/', views.view, name='view')  
      
      ]
