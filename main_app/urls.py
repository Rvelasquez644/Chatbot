from django.urls import path , re_path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path('admin_ui', views.admin_ui , name='admin_ui'),

    path('patient_ui', views.patient_ui , name='patient_ui'),
    path('checkdisease', views.checkdisease, name="checkdisease"),
    path('checkall', views.checkall, name="checkall"),
    path('resultbc', views.resultbc, name="resultbc"),
    path('covid', views.covid, name="covid"),
    path('resultc', views.resultc, name="resultc"),
    path('pneumonia', views.pneumonia, name="pneumonia"),
    path('resultp', views.resultp, name="resultp"),
    path('resultd', views.resultd, name="resultd"),
    path('diabetes', views.diabetes, name="diabetes"),
    path('send_email', views.send_email, name="send_email"),
    path('chatbot', views.chatbot, name="chatbot"),
    path('get/', views.get_bot_response, name='get_bot_response'),

    # path('send_diagnosis', views.send_diagnosis, name="send_diagnosis"),
    path('pviewprofile/<str:patientusername>', views.pviewprofile , name='pviewprofile'),
    path('pconsultation_history', views.pconsultation_history , name='pconsultation_history'),
    path('consult_a_doctor', views.consult_a_doctor , name='consult_a_doctor'),
    path('make_consultation/<str:doctorusername>', views.make_consultation , name='make_consultation'),
    path('rate_review/<int:consultation_id>', views.rate_review , name='rate_review'),


    path('dconsultation_history', views.dconsultation_history , name='dconsultation_history'),
    path('dviewprofile/<str:doctorusername>', views.dviewprofile , name='dviewprofile'),
    path('doctor_ui', views.doctor_ui , name='doctor_ui'),
    
    
    
    path('consultationview/<int:consultation_id>', views.consultationview , name='consultationview'),
    path('close_consultation/<int:consultation_id>', views.close_consultation , name='close_consultation'),
    path('send_email/<int:consultation_id>', views.send_email , name='send_email'),  

    
    path('post', views.post, name='post'),
    path('chat_messages', views.chat_messages, name='chat_messages'),
    


]  
