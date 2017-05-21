from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseServerError
from django.template import Template
from django.template.loader import get_template
from mainapi.models import Questions
import csv #to parse csv files
import io
import json #to parse json data


class CsvHandler: #This class handles csv data
    def __init__(self,file):
        file.seek(0)
        self.reader=csv.DictReader(io.StringIO(file.read().decode('utf-8')))

    def get_data(self):# This returns a reader object
        return self.reader


    


def upload_file(request):#This is the main view that handles upload through 
    if request.method!="POST":
        return HttpResponse('Only post here')
    try:
       a=CsvHandler(request.FILES['file'])
       handlePost(a.get_data())
       return HttpResponse('OK')
    except:
        return HttpResponse("Failure. Reasons can be\n1.'file' attribute must be there in the request.\n2. The file must be a .csv extension file.")


def getRequest(request ,offset): #This view function handles get request for getting details of questions
    if request.method!="GET":
        return HttpResponse('Only get request here')
    try:# check if offset is an integer
        a=int(offset)#This is the number that determines the number of questions requested, through the url
        return HttpResponse(handleGet("",number=a))
    except:
        if offset=="all":#check if it is the string 'all'
            return HttpResponse(handleGet("",all=True)) #in this case, return all the questions along with other details
        else :
            return HttpResponse("INVALID URL")

def delete(request):# this view function parses requests to delete questions in form of post and get requests
    if request.method=="GET":
        if 'delete' in request.GET:
            return HttpResponse(handleDelete(request.GET['delete']))#check and delete if it contains 'delete' keyword
        else:
            return HttpResponse("Invalid call.")
    elif request.method=="POST":#check if it is a post request 
        try:
            return HttpResponse(handleDelete(request.POST.get('delete',"")))#in this case the question to be deleted is spqcified in the value of the 'delete' parameter
        except:
            return HttpResponse("Either the query delete parameter is absent or the query is irrelevant")#in case the request is not sent with proper data
    elif request.method=="DELETE":#delete requests in the same way
        try:
            return HttpResponse(handleDelete(request.DELETE['delete']))
        except:
            return HttpResponse("Either the query delete parameter is absent or the query is irrelevant")
    elif request.method=="PUT":
        return HttpResponse("Put not allowed here")
    else:
        return HttpResponse("invalid call")


def handleDelete(question):#This function is called in the delete function since it actually interacts with database to delete a given question
    q=Questions.objects.filter(Question=question)
    if len(q)>0:
         for _ in q:
            _.delete()
         return "deleted"
    else:
        return "Question not found"
    

def getRequest2(request):  #This 
    print(request.method)
    if request.method=="GET":
        if 'q' in request.GET:
            return HttpResponse(handleGet(request.GET['q'],all=False))
        else:
            return HttpResponse("Invalid call.")
    elif request.method=="POST":
        print(request.POST)
        try:
            return HttpResponse(handleGet(request.POST.get('q',""),all=False))
        except:
            return HttpResponse("Either the query q parameter is absent or the query is irrelevant")        
    else:
        return HttpResponse("Get or post only at this url")


def put(request):# This function handles the new entries to the questions database, in form of a post request
    if not request.method=="POST":
        return HttpResponse("Only Post allowed instead of Put request")
    try:
        q=Questions(Question=request.POST.get('Question',""),      #This is the questions object which gets converted by django into an sql record automatically
                    Option_A=request.POST.get('Option_A',""),
                    Option_B=request.POST.get('Option_B',""),
                    Option_C=request.POST.get('Option_C',""),
                    Option_D=request.POST.get('Option_D',""),
                    Correct_Option=request.POST.get('Correct_Option',"")) 
        q.save()
        return HttpResponse("Question saved in the database")
    except:
        return HttpResponse("Error! Please check the data you have sent.")


      
def handlePost(data):
    for _ in data:
        q=Questions(Question=_['Question'],Option_A=_['Option_A'],Option_B=_['Option_B'], Option_C=_['Option_C'],Option_D=_['Option_D'],Correct_Option=_['Correct_Option'])
        q.save()


def handleGet(question,number=0,all=False): #THis function takes as parameters the question(if specified), number of questions(by default zero) and a boolean 'all' parameter
    response_main=[]                        #If the 'all' kwarg is set to True, it returns details of all the questions in the database
    if all:                                 #Otherwise it returns 'number' number of questions details or the details of a question specified by the 'question' arg if number is 0
        lst=Questions.objects.all()
        print(len(lst))
        for objct in lst:
            response={}
            response["Question"]=objct.Question
            response["Option_A"]=objct.Option_A
            response["Option_B"]=objct.Option_B
            response["Option_C"]=objct.Option_C
            response["Option_D"]=objct.Option_D
            response["Correct_Option"]=objct.Correct_Option
            response_main.append(response)
    elif number==0:
        lst=Questions.objects.filter(Question=question)
        for objct in lst:
            response={}
            response["Question"]=objct.Question
            response["Option_A"]=objct.Option_A
            response["Option_C"]=objct.Option_C
            response["Option_B"]=objct.Option_B
            response["Option_D"]=objct.Option_D
            response["Correct_Option"]=objct.Correct_Option
            response_main.append(response)
    elif number!=0:
        lst=Questions.objects.all()
        if number<len(lst):
            for _ in range(number):
               response={}
               response["Question"]=lst[_].Question
               response["Option_A"]=lst[_].Option_A
               response["Option_C"]=objct.Option_C
               response["Option_B"]=objct.Option_B
               response["Option_D"]=objct.Option_D
               response["Correct_Option"]=lst[_].Correct_Option
               response_main.append(response)
    return json.dumps(response_main) #convert it to json string




def testui(request): #The main web UI(web page) for testing
    t=get_template('testui.html')
    html=t.render()
    return HttpResponse(html)















    
