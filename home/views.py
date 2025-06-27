from django.shortcuts import render
from django.views import View
from .forms import ContactForm


class HomeView(View):
    def get(self, request):
        template = 'home/index.html'
        return render(request, template_name=template)


class AboutView(View):
    def get(self, request):
        template = 'home/about.html'
        return render(request, template,)
    

class ProjectsView(View):
    def get(self, request):
        template = 'home/project.html'
        return render(request, template)
    

class ContactView(View):
    form_class = ContactForm

    def get(self, request):
        form = self.form_class()
        template = 'home/contact.html'
        return render(request, template, {'form': form})
        