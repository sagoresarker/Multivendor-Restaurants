from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
from django.contrib import messages
# Create your views here.



def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            '''
            # Method 1
            # Create the user using the form

            # get the password from form
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            # hash the password using set_password() method
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()
            '''

            # Method 2
            # Create the user using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Now pass the value in the models.py file and use create_user method

            user = User.objects.create_user(first_name=first_name, last_name=last_name,
                                    username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'Yor account has been registered successfully.')

            return redirect('registerUser')
        else:
            print('Invalid user')


    else:
        form = UserForm()
    context = {
        'form':form,
    }
    return render(request, 'accounts/registerUser.html', context)