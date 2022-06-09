import imp
from os import stat
from django.http import HttpResponse
from django.shortcuts import render
from  .models import *
import socket
import json
import base64
from pathlib import Path
from django.core.files import File
import cv2
import face_recognition
from django.template import context
from mail_code import mail_code


# Create your views here
def home(request):
      data = {}
      toggle_obj = toggle.objects.all()
      ids = toggle_obj[0].intrudersys
      led = toggle_obj[1].led
      #print("ids-",ids,"led-",led)
      data['ids'] = ids
      data['led'] = led
      #alarm
      x = 0
      time = None
      a = alarm.objects.all()
      for i in a:
        time = i.atime
        x = 1
      data['atime']=time

      if x == 1:
        print("alarm on")
        data['alarm']= '1'
        print(data)
        return render(request,"home.html",data)
      else:
        print("alarm off")
        data['alarm']= '0'
        print(data)
        return render(request,"home.html",data)
    
def alarmon(request):
    if request.method == "POST":
      alarm_time = request.POST.get("time")
      print(alarm_time)
      if alarm_time == 'off':
        a = alarm.objects.get(pkey = 1)
        a.delete()
        print("deleted")
      else:
        entry = alarm(pkey=1,atime=alarm_time)
        entry.save()  
        print("entered")
    return HttpResponse(request,None)
  
def toggleIDS(request):
    if request.method == "POST":
      ids = request.POST.get("ids")
      if ids == 'false':
        a = toggle.objects.get(pkey = 1)
        a.intrudersys = False
        a.save()
        print("Off")
      else:
        a = toggle.objects.get(pkey = 1)
        a.intrudersys = True
        a.save()
        print("On")
    return HttpResponse(request,None)

def toggleLED(request):
    if request.method == "POST":
      led = request.POST.get("led")
      if led == 'false':
        #storing switch state
        a = toggle.objects.get(pkey = 2)
        a.led = False
        a.save()
        print("Off")
      else:
        #storing switch state
        a = toggle.objects.get(pkey = 2)
        a.led = True
        a.save()
        print("On")
    return HttpResponse(request,None)


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def rpi(request):
    if request.method == "POST":
      ittime = request.POST.get("ittime")
      itdate = request.POST.get("itdate")
      pic = request.POST.get("media")

      #image processing
      with open("image.png", "wb") as new_file:
          new_file.write(base64.decodebytes(bytes(pic,encoding='utf-8'))) 
      images = owner.objects.all()
      images = list(images)
      arr = []
      img_totest = face_recognition.load_image_file('image.png')
      img_totested = cv2.cvtColor(img_totest,cv2.COLOR_BGR2RGB)
      for i in images:
          img = i.own_picture
          print(img)
          img_given = face_recognition.load_image_file(img)
          img_given = cv2.cvtColor(img_given,cv2.COLOR_BGR2RGB)
          faceLoc = face_recognition.face_locations(img_given)[0]
          encode_img = face_recognition.face_encodings(img_given)[0]
          faceLoctest = face_recognition.face_locations(img_totest)[0]
          encodeTestresult = face_recognition.face_encodings(img_totest)[0]
          arr.append(encode_img)
      result = []
      for i in range(0,len(arr)):
        results = face_recognition.compare_faces([arr[i]],encodeTestresult)
        result.append(results[0])
      print(result)
      flag = 0
      for i in result:
        if i == True:
          flag = 1
      print(flag)
      if flag == 0:
          print(ittime,"-",itdate)
          a = intruder_stat.objects.get(pkey = 1)
          a.intr_state = True
          a.save()

          entry = intruder(intr_time = ittime,intr_date = itdate)
          entry.save()
          picurl = intruder.objects.get(intr_time = ittime,intr_date = itdate)
          imgpath = Path('image.png')
          with imgpath.open(mode='rb') as f:
            picurl.picture = File(f,name=imgpath.name)
            picurl.save()
          data = {"Msg": "Intruder"}
          mail_code()

      elif flag == 1:
          data = {"Msg": "Owner"}
      return HttpResponse(json.dumps(data),content_type='application/json')

def history(request):
    data = {}
    intrutions = intruder.objects.all()
    data["content"] = list(intrutions)[::-1]
    print(intrutions[0].picture.url)
    return render(request,"history.html",context = data)

def client(request):
    data = {}
    toggle_obj = toggle.objects.all()
    led = toggle_obj[1].led
    #print("ids-",ids,"led-",led)
    if led == True:
      data['led'] = 1
    else:
      data['led'] = 0
    #intruder
    stat_obj = intruder_stat.objects.all()
    stat = stat_obj[0].intr_state
    if stat == True:
      data['stat'] = 1
    elif stat == False:
      data['stat'] = 0
    a = intruder_stat.objects.get(pkey = 1)
    a.intr_state = False
    a.save()
    return HttpResponse(json.dumps(data),content_type='application/json')

def ids(request):
    toggle_obj = toggle.objects.all()
    ids = toggle_obj[0].intrudersys
    stream = toggle_obj[2].stream
    data = {}
    data['ids'] = ids
    data['stream'] = stream
    return HttpResponse(json.dumps(data),content_type='application/json')
  
def stream(request):
    if request.method == "POST":
      state = request.POST.get("stream")
      if state == '0':
        a = toggle.objects.get(pkey = 3)
        a.stream = False
        a.save()
        print("Stream - Off")
      else:
        a = toggle.objects.get(pkey = 3)
        a.stream = True
        a.save()
        print("Stream - On")
    return HttpResponse(request,None)
