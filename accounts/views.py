from django.shortcuts import render,redirect
from django.views import View
from . import forms
from django.contrib.auth import views as auth_views
from django.contrib.auth import update_session_auth_hash

class HomeView(View):
    template_name = 'accounts/home.html'
    def get(self,request):
        variables = {}
        return render(request, self.template_name, variables)

class ProfileView(View):
    template_name = 'accounts/profile.html'
    def get(self,request):
        args = {'user': request.user }
        return render(request,self.template_name,args)


class ProfileCreateView(View):
    template_name = 'accounts/profile_form.html'

    def get(self,request):
        form = forms.ProfileForm()
        variables = {
            'form':form,
        }
        return render(request,self.template_name,variables)

    def post(self, request):
        form = forms.ProfileForm(request.POST or None)

        if form.is_valid():
            form.deploy()
            return redirect('accounts:profile')

        variables = {
            'form': form,
        }
        return render(request, self.template_name, variables)

class EditProfileView(View):
    template_name = 'accounts/edit_profile.html'

    def get(self,request):
        form = forms.EditProfileForm()
        variables = {
            'form':form,
        }
        return render(request,self.template_name,variables)

    def post(self, request):
        form = forms.EditProfileForm(request.POST or None)

        if form.is_valid():
            form.save()
            return redirect('accounts:profile')

        variables = {
            'form': form,
        }
        return render(request, self.template_name, variables)


class SignUpView(View):
    template_name = 'accounts/signup.html'

    def get(self,request):
        form = forms.UserRegistrationForm()
        variables = {
            'form':form,
        }
        return render(request,self.template_name,variables)

    def post(self, request):
        form = forms.UserRegistrationForm(request.POST or None)

        if form.is_valid():
            form.deploy()
            return redirect('accounts:login')

        variables = {
            'form': form,
        }
        return render(request, self.template_name, variables)

#View for Change password
class PasswordChangeView(View):
    template_name = 'accounts/password_change_form.html'

    def get(self,request):
        form = forms.PasswordChangeForm(user = request.user)
        args = {
            'form':form
        }
        return render(request,self.template_name,args)

    def post(self,request):
        form = forms.PasswordChangeForm(data = request.POST or None, user = request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('accounts:passwoerd_change_complete')

        args = {
            'form':form
        }
        return render(request,self.template_name,args)


class PasswordChangeCompleteView(View):
    template_name = 'accounts/password_change_complete.html'

    def get(self,request):
        return render(request,self.template_name)



# View for Reset Password

class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = '/accounts/password-reset/done/'


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
        template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
        template_name = 'accounts/password_reset_confirm.html'
        success_url = '/accounts/password-reset-complete/'

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
        template_name = 'accounts/password_reset_complete.html'