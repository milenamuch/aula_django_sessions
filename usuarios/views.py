from django.shortcuts import render,redirect
from django.contrib import messages, auth
from  django.contrib.messages import constants
from django.contrib.auth.models import User
from .models import EnderecoUsuario

def login (request):
    if request.user.is_authenticated:
        return redirect('/plataforma/home')
    status = request.GET.get('status') 
    return render(request,'login.html',{'status':status})

def cadastro (request):
    if request.user.is_authenticated:
        return redirect('/plataforma/home')
    
    status = request.GET.get('status')
    return render(request,'cadastro.html', {'status':status})

def valida_cadastro (request):
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    cep = request.POST.get('cep')
    rua = request.POST.get('rua')
    numero = request.POST.get('numero')

    
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
        print('salvou user')
        
        endereco_cadastro = EnderecoUsuario(cep=cep, rua=rua, numero=numero, usuario=usuario)
        endereco_cadastro.save()
        print('salvou endereço')
        messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso!')
        return redirect('/auth/cadastro/')
    
    except:
        messages.add_message(request, constants.ERROR, 'Erro no sistema.')
        return redirect('/auth/cadastro/')
    

def valida_login(request):
    nome = request.POST.get('nome')
    senha = request.POST.get('senha')
    usuario = auth.authenticate(request,username = nome, password = senha)
    if not usuario:
        messages.add_message(request, constants.WARNING, 'Nome ou senha inválido.')
        return redirect('/auth/login/')
    
    else:
        auth.login(request, usuario)
        request.session['logado'] = True
        return redirect('/plataforma/home')
       
    
def sair(request):
    auth.logout(request)
    return redirect('/auth/login/')