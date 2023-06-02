from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .models import Profile
from django.http import HttpResponse

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')



@login_required
def onesignal_register(request):
  '''Receives the onesignal playerid of this user'''
  profile = Profile.objects.get(user=request.user) # The model where you will to save the profile.
  
  if request.POST.get('playerId'):
      profile.onesignal_playerId = request.POST.get('playerId')
      profile.save()
      return HttpResponse('Done')
  return HttpResponse('Something went wrong')