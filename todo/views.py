from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

#### Только зарегистрированные пользователи имеют доступ
#### к конкретным страницам
#### from django.contrib.auth.decorators import login_required



def home(request):
    return render(request, 'todo/home.html')

def signupuser(request):
    if request.method == "GET":
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodo')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'That username has been taken. Please choose a new username.'})
        else:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
    if request.method == "GET":
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(), 'error':'Username and password did not match.'})
        else:
            login(request, user)
            return redirect('currenttodo')


#### Чтобы выполнить необходимо зайти под своим логином
@ login_required()
def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')

#### Чтобы выполнить необходимо зайти под своим логином
@ login_required()
def createtodo(request):
    if request.method == "GET":
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            ## Сохраняет форму в базе данных
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            ## Сохраняет информацию в базу данных
            newtodo.save()
            ## Переправляем пользователя на список записей
            return redirect('currenttodo')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'error':'Вы ввели неправильно. Попробуйте еще раз.'})

#### Чтобы выполнить необходимо зайти под своим логином
@ login_required()
def currenttodo(request):
    #### Вызов всех объектов Todo для определенного пользователя из базы данных
    #### Это команда user = request.user
    #### Команда datecompleted__isnull=True
    #### Если пользователь не завершил задачу, то она у него будет отображаться
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodo.html', {'todos':todos})

#### Чтобы выполнить необходимо зайти под своим логином
@ login_required()
def completedtodo(request):
    #### Вызов всех объектов Todo для определенного пользователя из базы данных
    #### Это команда user = request.user
    #### Команда datecompleted__isnull=False
    #### Если пользователь завершил задачу, то она не будет отображаться
    #### order.by - сортировка по критерию datecompleted
    #### - тире это обратный хронологический порядок
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/completedtodo.html', {'todos':todos})



#### Чтобы выполнить необходимо зайти под своим логином
@ login_required()
def viewtodo(request, todo_pk):
    # Система сверяет ключ записи и автора записи.
    # Если пользователь не будет match, то выйдет ошибка 404
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form})
    else:
        # Если пользователь делает изменения, во время существующей записи
        # И сохраняет запись, при помощи кнопки Save
        # То он запрос POST
        try:
            # Учтем ошибки пользователя при неправильности ввода
            # Так как, мы вносим изменения, а не создаем новые записи
            # То в скобках, указываем instance = todo
            # Чтобы запись изменилась, а не создалась новвая
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodo')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'error':'Bad Info'})


#### Чтобы выполнить необходимо зайти под своим логином
@ login_required()
def completetodo (request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        ## код будет заполнять текущей датой и временем
        ## в случаи выполнения задачи
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodo')

#### Чтобы выполнить необходимо зайти под своим логином
@ login_required()
def deletetodo (request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        ## код будет заполнять текущей датой и временем
        ## в случаи выполнения задачи
        todo.delete()
        return redirect('currenttodo')