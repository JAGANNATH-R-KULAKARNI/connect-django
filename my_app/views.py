from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from my_app.models import Person
from my_app.models import Posts
from datetime import datetime
from dateutil import parser
from operator import itemgetter
import uuid
# Create your views here.

def home_page(request):

    if(request.method == 'POST'):
        pic=request.POST['profilepic']
        caption=request.POST['caption']
        print('bro here')
        print(pic)
        print(caption)
        print(request.user.username)
        now = datetime.now()
        print(now.strftime('%Y/%m/%d %I:%M:%S'))
        
        try:
            person=Person.objects.get(name=request.user.username)
            print(person)
            Posts.objects.create(post_id=uuid.uuid4(),person_name=person,text=caption,media_link=pic,time_posted=now,likes=0,liked_by={"liked_by" : []},comments={"comments" : []})
            messages.success(request,'Successfully Created the post')
        except:
            messages.info(request,'Post Creation unsuccessful')
            
        return redirect('/')        
    
    if not request.user.is_authenticated:
        return redirect('/login')
    
    posts=Posts.objects.all()
    temp=[]
    for i in posts:
        spec={}
        spec['person_name']=i.person_name
        spec['text']=i.text
        spec['media_link']=i.media_link
        spec['time_posted']=i.time_posted
        spec['likes']=len(i.liked_by['liked_by'])
        spec['comments']=i.comments['comments']
        spec['commentslen']=len(i.comments['comments'])
        spec['post_id']=i.post_id
        spec['likesfun']='homelikes/'+str(i.post_id)
  
        if(request.user.username in i.liked_by['liked_by']):
            spec['liked']=True
        else:
            spec['liked']=False
                
        temp.append(spec)
     
    for i in temp:
        print(i['person_name']) 
    
    temp.sort(key=itemgetter('time_posted'),reverse=True)

    
    for i in temp:
        refe=str(datetime.now()-parser.parse(i['time_posted']))
        print('---------------------')
        print(datetime.now())
        print(parser.parse(i['time_posted']))
        print(i['time_posted']+ '  '+i['text'])
        print(refe)
        print('---------------------')
        if(refe.find('day') != -1):
            jag=''
            for j in refe:
                if(j == ' '):
                    break
                jag=jag+j
                
            if(int(str(jag)) == 1):
                i['time_posted']=str(int(jag))+' day ago'    
            else:
                i['time_posted']=str(int(jag))+' days ago'
                    
        else:
            jag=''
            flag=0
            done=0
            for j in refe:
                
                if(j == ':'):
                    if(int(jag) != 0):
                        if(flag == 0):
                            if(int(jag) == 1):
                                i['time_posted']=str(int(jag))+' hour ago'
                            else:
                                i['time_posted']=str(int(jag))+' hours ago'   
                            done=1    
                            break
                        else:
                            if(int(jag) == 1):
                                i['time_posted']=str(int(jag))+ ' minute ago'
                            else:
                                i['time_posted']=str(int(jag))+ ' minutes ago'     
                            done=1    
                            break
                    jag=''     
                    flag=flag+1       
                    continue
                
                jag=jag+j
            
            if(done == 0):
                ben=jag[0:2]
                
                if(int(ben) == 1):
                    i['time_posted']=str(int(ben))+ ' second ago'
                else:
                    i['time_posted']=str(int(ben))+' seconds ago'    
            
    
    temp2=[]
    
    for index,i in enumerate(temp):
        
        if(index % 3 == 0):
            jag=[]
            jag.append(temp[index])
            if(index+1 < len(temp)):
                jag.append(temp[index+1])
  
            if(index+2 < len(temp)):
                jag.append(temp[index+2])
  
                
            temp2.append(jag)
    
    print(temp2)                
    return render(request,'my_app/home.html',{'posts' : temp2,'nop' : len(temp)})


def profileedit(request):
    if(request.method == 'POST'):
        print('here i am ')
        pic=request.POST['profilepicedit']
        bio=request.POST['editedtext']
        user=Person.objects.filter(name=request.user.username)[0]
        if(len(pic) != 0):
            user.pic=pic
        if(len(bio) != 0):    
            user.bio=bio
        user.save()
        if(len(pic) > 0 or len(bio) > 0):
            messages.success(request,'Edited Successfully')
        else:
            messages.info(request,'Edit Something')    
        
    return redirect('/profile')

def profilelikes(request,post_id):

    print('yo baby')    
    print(post_id)
    post=Posts.objects.filter(post_id=post_id)[0]
    print(post.liked_by['liked_by'])
    temp=post.liked_by['liked_by']
    if(request.user.username in temp):
        temp.remove(request.user.username)
    else:
        temp.append(request.user.username)
    post.liked_by['liked_by']=temp
    post.save()
    print(len(post.liked_by['liked_by']))
    
    return redirect('/profile')

def homelikes(request,post_id):
    
    print('yo baby')    
    print(post_id)
    post=Posts.objects.filter(post_id=post_id)[0]
    print(post.liked_by['liked_by'])
    temp=post.liked_by['liked_by']
    if(request.user.username in temp):
        temp.remove(request.user.username)
    else:
        temp.append(request.user.username)
    post.liked_by['liked_by']=temp
    post.save()
    print(len(post.liked_by['liked_by']))
    
    return redirect('/')

def comments_page(request):
     
    if(request.method == 'POST'):
        comment=request.POST['commentext']
        post_id=request.POST['post_id_of_modal']
        ctype=request.POST['which_page_comment']
        print('*********************')
        print(comment)
        print(post_id)
        print('*********************')
        person=Person.objects.filter(name=request.user.username)[0]
        post=Posts.objects.filter(post_id=post_id)[0]
        temp=post.comments['comments']
        temp.append({"by" : request.user.username, "c" : comment,"pic" : person.pic})
        post.comments['comments']=temp
        post.save()
        messages.success(request,'You commented on '+str(post.person_name)+ ' post')
        print(post)
        if(ctype == 'home'):
            return redirect('/')
        else:
            return redirect('/profile')
    return redirect('/profile')

def profile_page(request):
     
    if(request.method == 'POST'):
        pic=request.POST['profilepic']
        caption=request.POST['caption']
        print('bro here')
        print(pic)
        print(caption)
        print(request.user.username)
        now = datetime.now()
        print(now.strftime('%Y/%m/%d %I:%M:%S'))
        
        try:
            person=Person.objects.get(name=request.user.username)
            print(person)
            Posts.objects.create(post_id=uuid.uuid4(),person_name=person,text=caption,media_link=pic,time_posted=now,likes=0,liked_by={"liked_by" : []},comments={"comments" : []})
            messages.success(request,'Successfully Created the post')
        except:
            messages.info(request,'Post Creation unsuccessful')
            
        return redirect('/profile')    
    
    if not request.user.is_authenticated:
        return redirect('/login')
    
    person=Person.objects.get(name=request.user.username)
    posts=Posts.objects.filter(person_name=person)
    temp=[]
    for i in posts:
        spec={}
        spec['person_name']=i.person_name
        spec['text']=i.text
        spec['media_link']=i.media_link
        spec['time_posted']=i.time_posted
        spec['likes']=len(i.liked_by['liked_by'])
        spec['comments']=i.comments['comments']
        spec['commentslen']=len(i.comments['comments'])
        spec['post_id']=i.post_id
        spec['likesfun']='profilelikes/'+str(i.post_id)
  
        if(request.user.username in i.liked_by['liked_by']):
            spec['liked']=True
        else:
            spec['liked']=False
                
        temp.append(spec)
     
    for i in temp:
        print(i['person_name']) 
    
    temp.sort(key=itemgetter('time_posted'),reverse=True)

    
    for i in temp:
        refe=str(datetime.now()-parser.parse(i['time_posted']))
        print('---------------------')
        print(datetime.now())
        print(parser.parse(i['time_posted']))
        print(i['time_posted']+ '  '+i['text'])
        print(refe)
        print('---------------------')
        if(refe.find('day') != -1):
            jag=''
            for j in refe:
                if(j == ' '):
                    break
                jag=jag+j
                
            if(int(str(jag)) == 1):
                i['time_posted']=str(int(jag))+' day ago'    
            else:
                i['time_posted']=str(int(jag))+' days ago'
                    
        else:
            jag=''
            flag=0
            done=0
            for j in refe:
                
                if(j == ':'):
                    if(int(jag) != 0):
                        if(flag == 0):
                            if(int(jag) == 1):
                                i['time_posted']=str(int(jag))+' hour ago'
                            else:
                                i['time_posted']=str(int(jag))+' hours ago'   
                            done=1    
                            break
                        else:
                            if(int(jag) == 1):
                                i['time_posted']=str(int(jag))+ ' minute ago'
                            else:
                                i['time_posted']=str(int(jag))+ ' minutes ago'     
                            done=1    
                            break
                    jag=''     
                    flag=flag+1       
                    continue
                
                jag=jag+j
            
            if(done == 0):
                ben=jag[0:2]
                
                if(int(ben) == 1):
                    i['time_posted']=str(int(ben))+ ' second ago'
                else:
                    i['time_posted']=str(int(ben))+' seconds ago'    
            
    
    temp2=[]
    
    for index,i in enumerate(temp):
        
        if(index % 3 == 0):
            jag=[]
            jag.append(temp[index])
            if(index+1 < len(temp)):
                jag.append(temp[index+1])
  
            if(index+2 < len(temp)):
                jag.append(temp[index+2])
  
                
            temp2.append(jag)
    
    print(temp2)                
    return render(request,'my_app/profile.html',{'posts' : temp2,'person' : person,'nop' : len(temp)})


def login_page(request):
    
    if(request.method == 'POST'):
        username=request.POST['username']
        password=request.POST['password']
        
        user=authenticate(username=username,password=password)
        
        if user is not None:
            login(request,user)
            msg='Hello '+username+', You are successfully logged in'
            messages.success(request,msg)
            return redirect('/')
        else:
            messages.info(request,"Invalid Credentials")    
            return redirect('/login')
    
    return render(request,'my_app/login.html')

def signup_page(request):
    
    if(request.method == 'POST'):
        
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        bio=request.POST['bio']
        gender=request.POST['gender']
        age=request.POST['age']
        pic=request.POST['profilepic']
        
        if(int(age) <= 0):
            messages.info(request,'Invalid Age !')
            return redirect('/signup',name=username)
    
        if(User.objects.filter(username=username)):
            messages.info(request,username+' already exists !')
            return redirect('/signup')
        
        if(not username.isalnum()):
            messages.info(request,'Username must be Alpha-Numberic !')
            return redirect('/signup')
        
        if(User.objects.filter(email=email)):
            messages.info(request,email+' already exists !')
            return redirect('/signup')    
        
        myuser=User.objects.create_user(username,email,password)
        myuser.save()

        user=User.objects.get(username=myuser.username)
        person=Person.objects.create(added_by=user,name=username,bio=bio,age=age,gender=gender,pic=pic)
        person.save()
        
        print(person)
        messages.success(request,"Your Account has been successfully created")
        
        return redirect('/login')
    
    if request.user.is_authenticated:
        return redirect('/') 
       
    return render(request,'my_app/signup.html')



def log_out(request):
    logout(request)
    messages.success(request,"Succesfully logged out")
    
    return redirect('/login')