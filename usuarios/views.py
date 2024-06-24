from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Usuario
from hashlib import sha256
from django.contrib import messages
from  django.contrib.messages import constants

def login (request):
    
    status = request.GET.get('status')
    return render(request,'login.html', {'status': status})

def cadastro (request):
    status = request.GET.get('status')
    return render(request,'cadastro.html', {'status': status})

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
    
    #já existe usuario com este email?
    usuario = Usuario.objects.filter(email = email) 
    
    if len(usuario) > 0:
        messages.add_message(request, constants.ERROR, 'Email já cadastrado.')
        return redirect('/auth/cadastro/')
    
    try:
        senha = sha256(senha.encode()).hexdigest() #criptografia de senha
        usuario = Usuario(nome = nome,
                        email = email,
                        senha = senha)
        
        usuario.save()
        messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso.')
        return redirect('/auth/cadastro/')
    
    except:
        messages.add_message(request, constants.ERROR, 'Erro no sistema.')
        return redirect('/auth/cadastro')
    

def valida_login (request):
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    senha = sha256(senha.encode()).hexdigest()
    
    usuario = Usuario.objects.filter(email = email).filter(senha = senha)
    
    if len(usuario) == 0:
        messages.add_message(request, constants.WARNING, 'Email ou senha inválido.')
        return redirect('/auth/login/')
    
    elif len(usuario) > 0:
        request.session['logado'] = True
        request.session['usuario_id'] = usuario[0].id
        return redirect('/plataforma/home')
    
def sair(request):
    request.session.flush()
    messages.add_message(request, constants.WARNING, 'Faça login antes de acessar a plataforma')
    return redirect('/auth/login/')