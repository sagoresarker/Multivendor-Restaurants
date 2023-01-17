from django.shortcuts import render, redirect
from accounts.utils import detectUser, send_verification_email

from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied


# restrict the vendor from accessing from the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

# restrict the customer from accessing from the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already login")
        return redirect('dashboard')

    elif request.method == 'POST':
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

            # Send verification email
            send_verification_email(request, user)

            messages.success(request, 'Yor account has been registered successfully!')

            return redirect('registerUser')
        else:
            print('Invalid user')


    else:
        form = UserForm()
    context = {
        'form':form,
    }
    return render(request, 'accounts/registerUser.html', context)


def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already login")
        return redirect('dashboard')

    elif request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name,
                                    username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

            # Send verification email
            send_verification_email(request, user)

            messages.success(request, 'Yor account has been registered successfully! Please wait for the approval.')
            return redirect('registerVendor')
        else:
            print(form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form,
    }

    return render(request, 'accounts/registerVendor.html', context)



def activate(request, uidb64, token):
    # Activate the user by setting the _activate status to true
    return



def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already login")
        return redirect('myAccount')

    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now login.")
            return redirect('myAccount')
        else:
            messages.error(request, "Invalid login credentials.")
            return redirect('login')

    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, "You are logout.")
    return redirect('login')


@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):

    context = {

    }
    return render(request, 'accounts/custDashboard.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):

    context = {

    }
    return render(request, 'accounts/vendorDashboard.html', context)