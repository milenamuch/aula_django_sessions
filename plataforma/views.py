from django.shortcuts import render,redirect

def home(request):
    
    if request.session.get('logado'):
        return render(request, 'home.html')
    
    else:
        return redirect('/auth/login/')