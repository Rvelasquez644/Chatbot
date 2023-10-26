
from inspect import indentsize
import random
import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle

import json
from django.core.mail import EmailMessage
import cv2
import os
import io
from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import date
from werkzeug.utils import secure_filename
from django.contrib import messages
from django.contrib.auth.models import User , auth
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import numpy as np
from .models import patient , doctor , diseaseinfo , consultation ,rating_review
from chats.models import Chat, Feedback
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense
from PIL import Image
from django.utils.safestring import mark_safe
import sys

# Create your views here.


#loading model
import joblib as jb
model = jb.load('C:/Users/Rodrigo Velasquez/Desktop/Django__System-master/Django__System-master/ModelAI/model')
breastcancer_model = jb.load('C:/Users/Rodrigo Velasquez/Desktop/Django__System-master/Django__System-master/ModelAI/cancer_model.pkl')
diabetes_model = jb.load('C:/Users/Rodrigo Velasquez/Desktop/Django__System-master/Django__System-master/ModelAI/diabetes.sav')
# covid_model = jb.load('C:/Users/Erick/OneDrive/Escritorio/Hospital-Chatbot/Django__System-master/ModelAI/covid.h5')

covid_model = load_model('C:/Users/Rodrigo Velasquez/Desktop/Django__System-master/Django__System-master/ModelAI/covid.h5')
pneumonia_model = load_model('C:/Users/Rodrigo Velasquez/Desktop/Django__System-master/Django__System-master/ModelAI/pneumonia_model.h5')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = settings.APP_NAME

UPLOAD_FOLDER = 'media/'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def home(request):
  if request.method == 'GET':        
      if request.user.is_authenticated:
        return render(request,'index.html')
      else :
        return render(request,'index.html')       


def admin_ui(request):
    if request.method == 'GET':
      if request.user.is_authenticated:
        auser = request.user
        Feedbackobj = Feedback.objects.all()
        return render(request,'admin/admin_ui/admin_ui.html' , {"auser":auser,"Feedback":Feedbackobj})
      else :
        return redirect('home')
    if request.method == 'POST':
       return render(request,'patient/patient_ui/profile.html')


def patient_ui(request):
    if request.method == 'GET':
      if request.user.is_authenticated:
        patientusername = request.session['patientusername']
        puser = User.objects.get(username=patientusername)
        return render(request,'patient/patient_ui/profile.html' , {"puser":puser})
      else :
        return redirect('home')
    if request.method == 'POST':
       return render(request,'patient/patient_ui/profile.html')       


def pviewprofile(request, patientusername):
    if request.method == 'GET':
          puser = User.objects.get(username=patientusername)
          return render(request,'patient/view_profile/view_profile.html', {"puser":puser})
    

def checkall(request):
    if request.method == 'GET':
         #  puser = User.objects.get(username=patientusername)
          return render(request,'patient/checkdisease/checkall.html')
    

def resultbc(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        cpm = request.POST.get('concave_points_mean')
        am = request.POST.get('area_mean')
        rm = request.POST.get('radius_mean')
        pm = request.POST.get('perimeter_mean')
        cm = request.POST.get('concavity_mean')
        pred = breastcancer_model.predict(
            np.array([cpm, am, rm, pm, cm]).reshape(1, -1))
        # pb.push_sms(pb.devices[0],str(phone), 'Hello {},\nYour Breast Cancer test results are ready.\nRESULT: {}'.format(firstname,['NEGATIVE','POSITIVE'][pred]))
        context = {
            'firstname': firstname,
            'lastname': lastname,
            'age': age,
            'pred': pred,
            'gender': gender
        }
        return render(request, 'patient/checkdisease/resultbc.html', context=context)
    

def resultd(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        pregnancies = request.POST.get('pregnancies')
        glucose = request.POST.get('glucose')
        bloodpressure = request.POST.get('bloodpressure')
        insulin = request.POST.get('insulin')
        bmi = request.POST.get('bmi')
        diabetespedigree = request.POST.get('diabetespedigree')
        age = request.POST.get('age')
        skinthickness = request.POST.get('skin')
        pred = diabetes_model.predict(
            [[pregnancies, glucose, bloodpressure, skinthickness, insulin, bmi, diabetespedigree, age]])
        # pb.push_sms(pb.devices[0],str(phone), 'Hello {},\nYour Diabetes test results are ready.\nRESULT: {}'.format(firstname,['NEGATIVE','POSITIVE'][pred]))
        context = {
            'firstname': firstname,
            'lastname': lastname,
            'age': age,
            'pred': pred,
            'gender': gender
        }
        return render(request, 'patient/checkdisease/resultd.html', context=context)
    


def diabetes(request):
    if request.method == 'GET':
         #  puser = User.objects.get(username=patientusername)
          return render(request,'patient/checkdisease/diabetes.html')

    

def covid(request):
    if request.method == 'GET':
         #  puser = User.objects.get(username=patientusername)
          return render(request,'patient/checkdisease/covid.html')
    

def resultc(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        file = request.FILES.get('file')
        if file and allowed_file(file.name):
            img_data = file.read()
            img = Image.open(io.BytesIO(img_data)).convert('RGB')
            filename = secure_filename(file.name)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            img.save(file_path)
            messages.success(request, 'Image successfully uploaded and displayed below')
            img = cv2.imread('static/uploads/'+filename)
            img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
            img = img.reshape(1, 224, 224, 3)
            img = img/255.0
            pred = covid_model.predict(img)
            if pred < 0.5:
                pred = 0
            else:
                pred = 1            
            context = {
                'firstname': firstname,
                'lastname': lastname,
                'age': age,
                'pred': pred,
                'gender': gender,
                'filename': filename
            }
            return render(request, 'patient/checkdisease/resultc.html', context=context)
        


def pneumonia(request):
    if request.method == 'GET':
         #  puser = User.objects.get(username=patientusername)
          return render(request,'patient/checkdisease/pneumonia.html')


def resultp(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        file = request.FILES.get('file')
        if file and allowed_file(file.name):
            img_data = file.read()
            img = Image.open(io.BytesIO(img_data)).convert('RGB')
            filename = secure_filename(file.name)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            img.save(file_path)
            messages.success(request, 'Image successfully uploaded and displayed below')
            img = cv2.imread('static/uploads/'+filename)
            img = cv2.resize(img, (150, 150))
            img = img.reshape(1, 150, 150, 3)
            img = img/255.0
            pred = pneumonia_model.predict(img)
            if pred < 0.5:
                pred = 0
            else:
                pred = 1
            context = {
                'firstname': firstname,
                'lastname': lastname,
                'age': age,
                'pred': pred,
                'gender': gender,
                'filename': filename
            }
            # pb.push_sms(pb.devices[0],str(phone), 'Hello {},\nYour COVID-19 test results are ready.\nRESULT: {}'.format(firstname,['POSITIVE','NEGATIVE'][pred]))
            return render(request, 'patient/checkdisease/resultp.html', context=context)

        else:
            messages.success(request, 'Allowed image types are - png, jpg, jpeg')
            return redirect(request.url)


def checkdisease(request):

  diseaselist=['Fungal infection','Allergy','GERD','Chronic cholestasis','Drug Reaction','Peptic ulcer diseae','AIDS','Diabetes ',
  'Gastroenteritis','Bronchial Asthma','Hypertension ','Migraine','Cervical spondylosis','Paralysis (brain hemorrhage)',
  'Jaundice','Malaria','Chicken pox','Dengue','Typhoid','hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D',
  'Hepatitis E', 'Alcoholic hepatitis','Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemmorhoids(piles)',
  'Heart attack', 'Varicose veins','Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthristis',
  'Arthritis', '(vertigo) Paroymsal  Positional Vertigo','Acne', 'Urinary tract infection', 'Psoriasis', 'Impetigo']

  diseases_dict = {
    'Fungal infection': 'Infección fúngica',
    'Allergy': 'Alergia',
    'GERD': 'ERGE',
    'Chronic cholestasis': 'Colestasis crónica',
    'Drug Reaction': 'Reacción a medicamentos',
    'Peptic ulcer disease': 'Úlcera péptica',
    'AIDS': 'SIDA',
    'Diabetes ': 'Diabetes',
    'Gastroenteritis': 'Gastroenteritis',
    'Bronchial Asthma': 'Asma bronquial',
    'Hypertension ': 'Hipertensión',
    'Migraine': 'Migraña',
    'Cervical spondylosis': 'Espondilosis cervical',
    'Paralysis (brain hemorrhage)': 'Parálisis (hemorragia cerebral)',
    'Jaundice': 'Ictericia',
    'Malaria': 'Malaria',
    'Chicken pox': 'Varicela',
    'Dengue': 'Dengue',
    'Typhoid': 'Fiebre tifoidea',
    'hepatitis A': 'Hepatitis A',
    'Hepatitis B': 'Hepatitis B',
    'Hepatitis C': 'Hepatitis C',
    'Hepatitis D': 'Hepatitis D',
    'Hepatitis E': 'Hepatitis E',
    'Alcoholic hepatitis': 'Hepatitis alcohólica',
    'Tuberculosis': 'Tuberculosis',
    'Common Cold': 'Resfriado común',
    'Pneumonia': 'Neumonía',
    'Dimorphic hemmorhoids(piles)': 'Hemorroides dimórficas (almorranas)',
    'Heart attack': 'Ataque cardíaco',
    'Varicose veins': 'Venas varicosas',
    'Hypothyroidism': 'Hipotiroidismo',
    'Hyperthyroidism': 'Hipertiroidismo',
    'Hypoglycemia': 'Hipoglucemia',
    'Osteoarthristis': 'Osteoartritis',
    'Arthritis': 'Artritis',
    '(vertigo) Paroymsal  Positional Vertigo': 'Vértigo posicional paroxístico (vértigo posicional)',
    'Acne': 'Acné',
    'Urinary tract infection': 'Infección del tracto urinario',
    'Psoriasis': 'Psoriasis',
    'Impetigo': 'Impétigo'
}


  symptomslist=['itching','skin_rash','nodal_skin_eruptions','continuous_sneezing','shivering','chills','joint_pain',
  'stomach_pain','acidity','ulcers_on_tongue','muscle_wasting','vomiting','burning_micturition','spotting_urination',
  'fatigue','weight_gain','anxiety','cold_hands_and_feets','mood_swings','weight_loss','restlessness','lethargy',
  'patches_in_throat','irregular_sugar_level','cough','high_fever','sunken_eyes','breathlessness','sweating',
  'dehydration','indigestion','headache','yellowish_skin','dark_urine','nausea','loss_of_appetite','pain_behind_the_eyes',
  'back_pain','constipation','abdominal_pain','diarrhoea','mild_fever','yellow_urine',
  'yellowing_of_eyes','acute_liver_failure','fluid_overload','swelling_of_stomach',
  'swelled_lymph_nodes','malaise','blurred_and_distorted_vision','phlegm','throat_irritation',
  'redness_of_eyes','sinus_pressure','runny_nose','congestion','chest_pain','weakness_in_limbs',
  'fast_heart_rate','pain_during_bowel_movements','pain_in_anal_region','bloody_stool',
  'irritation_in_anus','neck_pain','dizziness','cramps','bruising','obesity','swollen_legs',
  'swollen_blood_vessels','puffy_face_and_eyes','enlarged_thyroid','brittle_nails',
  'swollen_extremeties','excessive_hunger','extra_marital_contacts','drying_and_tingling_lips',
  'slurred_speech','knee_pain','hip_joint_pain','muscle_weakness','stiff_neck','swelling_joints',
  'movement_stiffness','spinning_movements','loss_of_balance','unsteadiness',
  'weakness_of_one_body_side','loss_of_smell','bladder_discomfort','foul_smell_of urine',
  'continuous_feel_of_urine','passage_of_gases','internal_itching','toxic_look_(typhos)',
  'depression','irritability','muscle_pain','altered_sensorium','red_spots_over_body','belly_pain',
  'abnormal_menstruation','dischromic _patches','watering_from_eyes','increased_appetite','polyuria','family_history','mucoid_sputum',
  'rusty_sputum','lack_of_concentration','visual_disturbances','receiving_blood_transfusion',
  'receiving_unsterile_injections','coma','stomach_bleeding','distention_of_abdomen',
  'history_of_alcohol_consumption','fluid_overload','blood_in_sputum','prominent_veins_on_calf',
  'palpitations','painful_walking','pus_filled_pimples','blackheads','scurring','skin_peeling',
  'silver_like_dusting','small_dents_in_nails','inflammatory_nails','blister','red_sore_around_nose',
  'yellow_crust_ooze']

  symptom_dict = {'picazón':'itching',
                'erupciones_en_la_piel':'skin_rash',
                'erupciones_nodulares_en_la_piel':'nodal_skin_eruptions',
                'estornudos_continuos':'continuous_sneezing',
                'escalofríos':'shivering',
                'escalofríos':'chills',
                'dolor_articular':'joint_pain',
                'dolor_de_estómago':'stomach_pain',
                'acidez':'acidity',
                'úlceras_en_la_lengua':'ulcers_on_tongue',
                'pérdida_de_músculo':'muscle_wasting',
                'vómitos':'vomiting',
                'quemazón_al_orinar':'burning_micturition',
                'manchas_en_la_orina':'spotting_ urination',
                'fatiga':'fatigue',
                'aumento_de_peso':'weight_gain',
                'ansiedad':'anxiety',
                'manos_y_pies_fríos':'cold_hands_and_feets',
                'cambios_de_humor':'mood_swings',
                'pérdida_de_peso':'weight_loss',
                'inquietud':'restlessness',
                'letargo':'lethargy',
                'manchas_en_la_garganta':'patches_in_throat',
                'niveles_irregulares_de_azúcar':'irregular_sugar_level',
                'tos':'cough',
                'fiebre_alta':'high_fever',
                'ojos_hundidos':'sunken_eyes',
                'falta_de_aire':'breathlessness',
                'sudoración':'sweating',
                'deshidratación':'dehydration',
                'indigestión':'indigestion',
                'dolor_de_cabeza':'headache',
                'piel_amarillenta':'yellowish_skin',
                'orina_oscura':'dark_urine',
                'náuseas':'nausea',
                'pérdida_de_apetito':'loss_of_appetite',
                'dolor_detrás_de_los_ojos':'pain_behind_the_eyes',
                'dolor_de_espalda':'back_pain',
                'estreñimiento':'constipation',
                'dolor_abdominal':'abdominal_pain',
                'diarrea':'diarrhoea',
                'fiebre_moderada':'mild_fever',
                'orina_amarilla':'yellow_urine',
                'ojos_amarillentos':'yellowing_of_eyes',
                'fracaso_agudo_del_hígado':'acute_liver_failure',
                'sobrecarga_de_líquidos':'fluid_overload',
                'hinchazón_del_estómago':'swelling_of_stomach',
                'nódulos_linfáticos_hinchados':'swelled_lymph_nodes',
                'malestar_general':'malaise',
                'visión_borrosa_y_distorsionada':'blurred_and_distorted_vision',
                'flema':'phlegm',
                'irritación_de_garganta':'throat_irritation',
                'ojos_rojos':'redness_of_eyes',
                'presión sinusal': 'sinus_pressure',
                'nariz que moquea': 'runny_nose',
                'congestión': 'congestion',
                'dolor en el pecho': 'chest_pain',
                'debilidad en las extremidades': 'weakness_in_limbs',
                'ritmo cardíaco rápido': 'fast_heart_rate',
                'dolor durante las evacuaciones intestinales': 'pain_during_bowel_movements',
                'dolor en la región anal': 'pain_in_anal_region',
                'heces con sangre': 'bloody_stool',
                'irritación en el ano': 'irritation_in_anus',
                'dolor de cuello': 'neck_pain',
                'mareo': 'dizziness',
                'calambres': 'cramps',
                'moretones': 'bruising',
                'obesidad': 'obesity',
                'piernas hinchadas': 'swollen_legs',
                'vasos sanguíneos hinchados': 'swollen_blood_vessels',
                'cara y ojos hinchados': 'puffy_face_and_eyes',
                'tiroides agrandada': 'enlarged_thyroid',
                'uñas quebradizas': 'brittle_nails',
                'extremidades hinchadas': 'swollen_extremeties',
                'hambre excesiva': 'excessive_hunger',
                'contactos extramatrimoniales': 'extra_marital_contacts',
                'labios secos y hormigueantes': 'drying_and_tingling_lips',
                'habla arrastrada': 'slurred_speech',
                'dolor de rodilla': 'knee_pain',
                'dolor de cadera': 'hip_joint_pain',
                'debilidad muscular': 'muscle_weakness',
                'cuello rígido': 'stiff_neck',
                'articulaciones hinchadas': 'swelling_joints',
                'rigidez de movimiento': 'movement_stiffness',
                'movimientos giratorios': 'spinning_movements',
                'pérdida de equilibrio': 'loss_of_balance',
                'inestabilidad': 'unsteadiness',
                'debilidad de un lado del cuerpo': 'weakness_of_one_body_side',
                'pérdida del olfato': 'loss_of_smell',
                'molestia en la vejiga': 'bladder_discomfort',
                'olor fétido de la orina': 'foul_smell_of urine',
                'sensación continua de orinar': 'continuous_feel_of_urine',
                'paso de gases': 'passage_of_gases',
                'picazón interna': 'internal_itching',
                'aspecto tóxico (tifus)': 'toxic_look_(typhos)',
                'depresión': 'depression',
                'irritabilidad': 'irritability',
                'dolor muscular': 'muscle_pain',
                'sensorio alterado': 'altered_sensorium',
                'manchas rojas en el cuerpo': 'red_spots_over_body',
                'dolor abdominal': 'belly_pain',
                'menstruación anormal': 'abnormal_menstruation',
                'manchas descoloridas': 'dischromic _patches',
                'lagrimeo de los ojos': 'watering_from_eyes',
                'aumento del apetito': 'increased_appetite',
                'poliuria': 'polyuria',
                'historia familiar': 'family_history',
                'esputo mucoso': 'mucoid_sputum',
                'esputo oxidado': 'rusty_sputum',
                'falta de concentración': 'lack_of_concentration',
                'trastornos visuales': 'visual_disturbances',
                'recepción de transfusión de sangre': 'receiving_blood_transfusion',
                'recepción de inyecciones no estériles': 'receiving_unsterile_injections',
                'coma': 'coma',
                'sangrado estomacal': 'stomach_bleeding',
                'distensión del abdomen': 'distention_of_abdomen',
                'historial de consumo de alcohol': 'history_of_alcohol_consumption',
                'sobrecarga de líquidos': 'fluid_overload',
                'sangre en el esputo': 'blood_in_sputum',
                'venas prominentes en la pantorrilla': 'prominent_veins_on_calf',
                'palpitaciones': 'palpitations',
                'dolor al caminar': 'painful_walking',
                'espinillas llenas de pus': 'pus_filled_pimples',
                'puntos negros': 'blackheads',
                'descamación': 'scurring',
                'descamación de la piel': 'skin_peeling',
                'polvo plateado': 'silver_like_dusting',
                'pequeñas abolladuras en las uñas': 'small_dents_in_nails',
                'uñas inflamadas': 'inflammatory_nails',
                'ampolla': 'blister',
                'herida roja alrededor de la nariz': 'red_sore_around_nose',
                'costra amarilla que supura': 'yellow_crust_ooze'}

  alphabaticsymptomslist = sorted(symptom_dict.keys())

  if request.method == 'GET':    
     return render(request,'patient/checkdisease/checkdisease.html', {"list2":alphabaticsymptomslist})
  elif request.method == 'POST':       
      ## access you data by playing around with the request.POST object      
      inputno = int(request.POST["noofsym"])
      print(inputno)
      if (inputno == 0 ) :
          return JsonResponse({'predicteddisease': "none",'confidencescore': 0 })  
      else :
        psymptoms = []
        psymptoms = request.POST.getlist("symptoms[]")       
        print(psymptoms)
      
        # Traducción de síntomas
        psymptoms_en = []
        for symptom in psymptoms:
            if symptom in symptom_dict:
                psymptoms_en.append(symptom_dict[symptom])
      
        testingsymptoms = []
        #append zero in all coloumn fields...
        for x in range(0, len(symptomslist)):
          testingsymptoms.append(0)

        #update 1 where symptoms gets matched...
        for k in range(0, len(symptomslist)):
          for z in psymptoms_en:
              if (z == symptomslist[k]):
                  testingsymptoms[k] = 1
        inputtest = [testingsymptoms]
        print(inputtest)
        predicted = model.predict(inputtest)
        print("La enfermedad predicha es : ")
        print(predicted)
        y_pred_2 = model.predict_proba(inputtest)
        confidencescore=y_pred_2.max() * 100
        print("puntuación de confianza : = {0} ".format(confidencescore))
        confidencescore = format(confidencescore, '.0f')
        predicted_disease = predicted[0]        

        diseases_dict
        #consult_doctor codes----------

        #   doctor_specialization = ["Rheumatologist","Cardiologist","ENT specialist","Orthopedist","Neurologist",
        #                             "Allergist/Immunologist","Urologist","Dermatologist","Gastroenterologist"]        

        Reumatólogo = [  'Osteoarthristis','Arthritis']       
        Cardiólogo = [ 'Heart attack','Bronchial Asthma','Hypertension ']       
        Otorrinolaringólogo = ['(vertigo) Paroymsal  Positional Vertigo','Hypothyroidism' ]
        Ortopedista = []
        Neurólogo = ['Varicose veins','Paralysis (brain hemorrhage)','Migraine','Cervical spondylosis']
        Alergólogo_Inmunólogo = ['Allergy','Pneumonia',
        'AIDS','Common Cold','Tuberculosis','Malaria','Dengue','Typhoid']
        Urólogo = [ 'Urinary tract infection',
         'Dimorphic hemmorhoids(piles)']
        Dermatólogo = [  'Acne','Chicken pox','Fungal infection','Psoriasis','Impetigo']
        Gastroenterólogo = ['Peptic ulcer diseae', 'GERD','Chronic cholestasis','Drug Reaction','Gastroenteritis','Hepatitis E',
        'Alcoholic hepatitis','Jaundice','hepatitis A',
         'Hepatitis B', 'Hepatitis C', 'Hepatitis D','Diabetes ','Hypoglycemia']
         
        if predicted_disease in Reumatólogo :
           consultdoctor = "Reumatólogo"           
        if predicted_disease in Cardiólogo :
           consultdoctor = "Cardiólogo"
        elif predicted_disease in Otorrinolaringólogo :
           consultdoctor = "Otorrinolaringólogo"     
        elif predicted_disease in Ortopedista :
           consultdoctor = "Ortopedista"     
        elif predicted_disease in Neurólogo :
           consultdoctor = "Neurólogo"     
        elif predicted_disease in Alergólogo_Inmunólogo :
           consultdoctor = "Alergólogo/Inmunólogo"     
        elif predicted_disease in Urólogo :
           consultdoctor = "Urólogo"     
        elif predicted_disease in Dermatólogo :
           consultdoctor = "Dermatólogo"     
        elif predicted_disease in Gastroenterólogo :
           consultdoctor = "Gastroenterólogo"     
        else :
           consultdoctor = "other"
        request.session['doctortype'] = consultdoctor
        patientusername = request.session['patientusername']
        puser = User.objects.get(username=patientusername)

        predicted_disease = predicted[0]
        predicted_disease_es = diseases_dict.get(predicted_disease, "Desconocido")     

        #saving to database.....................
        patient = puser.patient
        diseasename = predicted_disease_es
        no_of_symp = inputno
        symptomsname = psymptoms
        confidence = confidencescore
        diseaseinfo_new = diseaseinfo(patient=patient,diseasename=diseasename,no_of_symp=no_of_symp,symptomsname=symptomsname,confidence=confidence,consultdoctor=consultdoctor)
        diseaseinfo_new.save()
        request.session['diseaseinfo_id'] = diseaseinfo_new.id
        print("disease record saved sucessfully.............................")
        
        return JsonResponse({'predicteddisease': predicted_disease_es ,'confidencescore':confidencescore , "consultdoctor": consultdoctor})

def pconsultation_history(request):
    if request.method == 'GET':
      patientusername = request.session['patientusername']
      puser = User.objects.get(username=patientusername)
      patient_obj = puser.patient        
      consultationnew = consultation.objects.filter(patient = patient_obj)    
      return render(request,'patient/consultation_history/consultation_history.html',{"consultation":consultationnew})


def dconsultation_history(request):
    if request.method == 'GET':
      doctorusername = request.session['doctorusername']
      duser = User.objects.get(username=doctorusername)
      doctor_obj = duser.doctor        
      consultationnew = consultation.objects.filter(doctor = doctor_obj)    
      return render(request,'doctor/consultation_history/consultation_history.html',{"consultation":consultationnew})


def doctor_ui(request):
    if request.method == 'GET':
      doctorid = request.session['doctorusername']
      duser = User.objects.get(username=doctorid)    
      return render(request,'doctor/doctor_ui/profile.html',{"duser":duser})
    
def dviewprofile(request, doctorusername):
    if request.method == 'GET':         
         duser = User.objects.get(username=doctorusername)
         r = rating_review.objects.filter(doctor=duser.doctor)       
         return render(request,'doctor/view_profile/view_profile.html', {"duser":duser, "rate":r} )    
       
def  consult_a_doctor(request):
    if request.method == 'GET':        
        doctortype = request.session['doctortype']
        print(doctortype)
        dobj = doctor.objects.all()
        #dobj = doctor.objects.filter(specialization=doctortype)
        return render(request,'patient/consult_a_doctor/consult_a_doctor.html',{"dobj":dobj})

def  make_consultation(request, doctorusername):
    if request.method == 'POST':
        patientusername = request.session['patientusername']
        puser = User.objects.get(username=patientusername)
        patient_obj = puser.patient        
        #doctorusername = request.session['doctorusername']
        duser = User.objects.get(username=doctorusername)
        doctor_obj = duser.doctor
        request.session['doctorusername'] = doctorusername
        diseaseinfo_id = request.session['diseaseinfo_id']
        diseaseinfo_obj = diseaseinfo.objects.get(id=diseaseinfo_id)
        consultation_date = date.today()
        status = "activo"        
        consultation_new = consultation( patient=patient_obj, doctor=doctor_obj, diseaseinfo=diseaseinfo_obj, consultation_date=consultation_date,status=status)
        consultation_new.save()
        request.session['consultation_id'] = consultation_new.id
        print("consultation record is saved sucessfully.............................")         
        return redirect('consultationview',consultation_new.id)

def  consultationview(request,consultation_id):   
    if request.method == 'GET':   
      request.session['consultation_id'] = consultation_id
      consultation_obj = consultation.objects.get(id=consultation_id)
      return render(request,'consultation/consultation.html', {"consultation":consultation_obj })
   #  if request.method == 'POST':
   #    return render(request,'consultation/consultation.html' )

def rate_review(request,consultation_id):
   if request.method == "POST":         
         consultation_obj = consultation.objects.get(id=consultation_id)
         patient = consultation_obj.patient
         doctor1 = consultation_obj.doctor
         rating = request.POST.get('rating')
         review = request.POST.get('review')
         rating_obj = rating_review(patient=patient,doctor=doctor1,rating=rating,review=review)
         rating_obj.save()
         rate = int(rating_obj.rating_is)
         doctor.objects.filter(pk=doctor1).update(rating=rate)
         return redirect('consultationview',consultation_id)

def close_consultation(request,consultation_id):
   if request.method == "POST":         
         consultation.objects.filter(pk=consultation_id).update(status="cerrado")         
         return redirect('home')
   

def send_email(request, consultation_id):
    if request.method == 'POST':
        consultation_id = request.POST.get('consultation_id')
        email = request.POST.get('email')
        comentario = request.POST.get('mensaje')
        consultation_obj  = consultation.objects.get(pk=consultation_id)
        symptoms = "\n".join(consultation_obj.diseaseinfo.symptomsname)

        if email:
            subject = 'Diagnóstico de su consulta médica'
            body = f'Su diagnóstico es: {consultation_obj.diseaseinfo.diseasename}\n\nLista de síntomas:\n{symptoms}\n\nComentario personal: {comentario}\n\nEdad del paciente: {consultation_obj.patient.age}\nNombre del paciente: {consultation_obj.patient.name}\nCorreo del paciente: {consultation_obj.patient.user.email}\nTeléfono del paciente: {consultation_obj.patient.mobile_no}'
            sender_email = 'medical@gmail.com'
            sender_password = 'tupassword'
            receiver_email = email

            try:
                email = EmailMessage(
                    subject,
                    body,
                    sender_email,
                    [receiver_email],
                    reply_to=[sender_email]
                )
                email.send()

                messages.success(request, 'El diagnóstico se ha enviado correctamente.')
                return redirect('dconsultation_history')
            except Exception as e:
                messages.error(request, f'Error al enviar el correo electrónico: {str(e)}')
        else:
            messages.error(request, 'Por favor ingrese la dirección de correo electrónico del paciente.')
    return redirect('dconsultation_history')




#-----------------------------chatting system ---------------------------------------------------

def post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        consultation_id = request.session['consultation_id']

        if 'clear' in request.POST:
            # Borrar todos los mensajes del chat
            Chat.objects.filter(consultation_id=str(consultation_id)).delete()
            return HttpResponse('Mensajes del chat borrados.')

        c = Chat(consultation_id=str(consultation_id), sender=request.user.username, message=msg)
        if msg != '':
            c.save()
            response_msg = get_chatbot_response(msg, c)
            chatbot_response = Chat(consultation_id=str(consultation_id), sender='Chatbot', message=response_msg)
            chatbot_response.save()
            if response_msg:
                return JsonResponse({'msg': response_msg})
    else:
        return HttpResponse('La solicitud debe ser POST.')

def get_chatbot_response(message, consultation_obj):
    consultation_id = consultation_obj.consultation_id

    try:
        consultation_obj = Chat.objects.filter(consultation_id=consultation_id).latest('id')
    except Chat.DoesNotExist:
        consultation_obj = Chat(consultation_id=consultation_id)

    current_state = consultation_obj.current_state if hasattr(consultation_obj, 'current_state') else 'start'

    response = ''

    case = {
        'start': {
            '1': ('predict', '¿Tienes fiebre? (1.Sí 2.No)'),
            '2': ('end', 'Gracias por usar el sistema de predicción de enfermedades. ¡Hasta luego!'),
            'default': ('start', '¿Quieres predecir alguna enfermedad? (1.Resfriado común 2.No)')
        },
        'predict': {
            '1': ('symptom_1', '¿Tienes congestión nasal? (1.Sí 2.No)'),
            '2': ('end', 'No tienes la enfermedad.'),
            'default': ('predict', '¿Tienes fiebre? (1.Sí 2.No)')
        },
        'symptom_1': {
            '1': ('symptom_2', '¿Tienes estornudos? (1.Sí 2.No)'),
            '2': ('end', 'No tienes la enfermedad.'),
            'default': ('symptom_1', '¿Tienes congestión nasal? (1.Sí 2.No)')
        },
        'symptom_2': {
            '1': ('symptom_3', '¿Tienes dolor de garganta? (1.Sí 2.No)'),
            '2': ('end', 'No tienes la enfermedad.'),
            'default': ('symptom_2', '¿Tienes estornudos? (1.Sí 2.No)')
        },
        'symptom_3': {
            '1': ('end', 'Tienes la enfermedad.'),
            '2': ('end', 'No tienes la enfermedad.'),
            'default': ('symptom_3', '¿Tienes dolor de garganta? (1.Sí 2.No)')
        },
        'end': {
            '1': ('end', 'Tienes la enfermedad.'),
            '2': ('end', 'No tienes la enfermedad.'),
            'default': ('end', 'Has completado la evaluación de síntomas. ¿Tienes la enfermedad? (1.Sí 2.No)')
        }
    }

    if current_state.startswith('symptom_'):
        symptom_number = int(current_state.split('_')[1])
        if message.lower() == '1' or message.lower() == 'sí' or message.lower() == 'no':
            next_symptom = symptom_number + 1
            if next_symptom <= 3:
                next_state = f'symptom_{next_symptom}'
                response = case[next_state]['default'][1]
                current_state = next_state
            else:
                response = case['end']['default'][1]
                current_state = 'end'
        else:
            response = 'Lo siento, no entendí tu respuesta. Por favor, responde con "1" o "2".'
    else:
        if message.lower() in case[current_state]:
            next_state, response = case[current_state][message.lower()]
            current_state = next_state
        else:
            _, response = case[current_state]['default']

    consultation_obj.current_state = current_state
    consultation_obj.save()

    return response


def chat_messages(request):
    if request.method == "GET":
        consultation_id = request.session['consultation_id']
        c = Chat.objects.filter(consultation_id=str(consultation_id))
        return render(request, 'consultation/chat_body.html', {'chat': c})
    

#-----------------------------chatting system 2 ---------------------------------------------------

model2 = load_model('C:/Users/Rodrigo Velasquez/Desktop/Django__System-master/Django__System-master/ModelAI/model2.h5')
intents = json.loads(open('C:/Users/Rodrigo Velasquez/Desktop/Django__System-master/Django__System-master/ModelAI/data.json').read())
words = pickle.load(open('C:/Users/Rodrigo Velasquez/Desktop/Django__System-master/Django__System-master/ModelAI/texts.pkl', 'rb'))
classes = pickle.load(open('C:/Users/Rodrigo Velasquez/Desktop/Django__System-master/Django__System-master/ModelAI/labels.pkl', 'rb'))
lemmatizer = WordNetLemmatizer()
print(sys.getdefaultencoding())

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model2):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model2.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    intents = intents_json['intents']

    for intent in intents:
        if intent['tag'] == tag:
            result = random.choice(intent['responses'])
            result = result.encode('utf-8').decode('utf-8')
            return result

    return "No se encontró una respuesta adecuada para esa consulta."

def chatbot_response(msg):
    ints = predict_class(msg, model2)
    with open('C:/Users/Rodrigo Velasquez/Desktop/Django__System-master/Django__System-master/ModelAI/data.json', 'r', encoding='utf-8') as file:
        intents_json = json.load(file)
    res = getResponse(ints, intents_json)
    return res.encode('utf-8').decode('utf-8')

def chatbot(request):
    return render(request, 'patient/checkdisease/chatbot.html')

def get_bot_response(request):
    userText = request.GET.get('msg', '')
    response = chatbot_response(userText)
    return JsonResponse({'response': response}, json_dumps_params={'ensure_ascii': False})

