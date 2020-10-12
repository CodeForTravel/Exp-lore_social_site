from django.shortcuts import render,redirect
from django.views.generic import ListView
from .models import ImagePost
from django.views import View
from . import forms

class ImagePostView(View):
    template_name = 'posts/timeline.html'
    def get(self,request):
        posts = ImagePost.objects.all()
        args = {'posts': posts}
        return render(request,self.template_name,args)


class ImageFormView(View):
    template_name = 'posts/image_form.html'

    def get(self,request):
        form = forms.ImageForm()
        variables = { 'form':form, }
        return render(request,self.template_name,variables)

    def post(self, request):
        form = forms.ImageForm(request.POST,request.FILES)
        if form.is_valid():
            form.deploy()
            return redirect('posts:timeline')
        variables = { 'form': form, }
        return render(request, self.template_name, variables)



