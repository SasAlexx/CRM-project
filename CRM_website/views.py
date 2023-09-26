from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .forms import SignUpForm, RecordForm
from .models import Record
from .permissions import IsOwnerOrReadOnly
from .serializers import RecordSerializer


# View for using API`s based on model
class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = (IsOwnerOrReadOnly, )


def home(request):
    records = Record.objects.all()

    # Check if user has logged in
    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user1 = authenticate(request, username=username, password=password)
        if user1 is not None:
            login(request, user1)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.success(request, "There was an error logging in, please try again!")
            return redirect('home')
    else:
        context = {
            'records': records
        }
        return render(request, 'home.html', context)


def logout_user(request):
    logout(request)
    messages.success(request, "You've been logged out!")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered!")
            return redirect('home')
    else:
        form = SignUpForm()
        context = {
            'form': form
        }
        return render(request, 'register.html', context)

    return render(request, 'register.html', {'form': form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        context = {
            'customer_record': customer_record
        }
        return render(request, 'record.html', context)
    else:
        messages.success(request, "You must be logged in to visit this page!")
        return redirect('home')


def add_record(request):
    form = RecordForm()
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = RecordForm(request.POST)
            if form.is_valid():
                Record.objects.create(**form.cleaned_data)
                messages.success(request, "You have successfully added new record !")
                return redirect('home')

    else:

        context = {
            'form': form
        }
        return render(request, 'add_record.html', context)
    return render(request, 'add_record.html', {'form': form})


def delete_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        record.delete()
        messages.success(request, "Record deleted successfully!")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to do that!")
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        form = SignUpForm(request.POST)
        record.delete()
        messages.success(request, "Record deleted successfully!")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to do that!")
        return redirect('home')
