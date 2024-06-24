from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Usuario
from django.contrib import messages, auth
from  django.contrib.messages import constants
from django.contrib.auth.models import User

def login (request):
    
    status = request.GET.get('status') 
    return render(request,'login.html',{'status':status})

def cadastro (request):
    status = request.GET.get('status')
    return render(request,'cadastro.html', {'status':status})

def valida_cadastro (request):
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    
    #nome ou email estão vazios?
    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha os campos corretamente.')
        return redirect('/auth/cadastro/')
    
    #A senha contém menos de 6 caracteres?
    if len(senha) < 6:
        messages.add_message(request, constants.WARNING, 'A senha precisa conter seis ou mais caracteres.')
        return redirect('/auth/cadastro')
    
    if User.objects.filter(email = email).exists():
        messages.add_message(request, constants.ERROR, 'Email já cadastrado.')
        return redirect('/auth/cadastro/')
    
    if User.objects.filter(username = nome).exists():
        messages.add_message(request, constants.ERROR, 'Nome de usuário já cadastrado.')
        return redirect('/auth/cadastro/')
    
    try:
        usuario = User.objects.create_user(username = nome, email = email, password = senha)
        usuario.save()
        messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso!')
        return redirect('/auth/cadastro/')
    
    except:
        messages.add_message(request, constants.ERROR, 'Erro no sistema.')
        return redirect('/auth/cadastro/')
    

def valida_login(request):
    print('passou aqui')
    nome = request.POST.get('nome')
    senha = request.POST.get('senha')
    print('passou aqui também')
    usuario = auth.authenticate(request,username = nome, password = senha)
    print('verificou se o usuaŕio pode ser autenticado')
    if not usuario:
        print('entrou no if, nao autenticou')
        messages.add_message(request, constants.WARNING, 'Nome ou senha inválido.')
        return redirect('/auth/login/')
    
    else:
        auth.login(request, usuario)
        request.session['logado'] = True
        print('entrou no else, autenticou')
        return redirect('/plataforma/home')
       
    
def sair(request):
    auth.logout(request)
    request.session.flush()
    messages.add_message(request, constants.WARNING, 'Faça login antes de acessar a plataforma.')
    return redirect('/auth/login/')