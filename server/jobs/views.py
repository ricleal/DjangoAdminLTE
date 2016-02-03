from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, RedirectView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType

from .models import Job

import logging

logger = logging.getLogger('jobs.views')

class JobCreate(LoginRequiredMixin, CreateView):
    '''
    Create
    '''
    template_name = 'jobs/job_form.html'
    model = Job
    fields = ['script']
    
    #TODO
    # get session in the get and fill in the form?
    
    
    def form_valid(self, form):
        '''
        
        '''
        
        form.instance.user = self.request.user
        form.instance.instrument = self.request.user.profile.instrument
        
        form.instance.content_type = self.request.session['content_type']
        form.instance.object_id = self.request.session['object_id']
                
        logger.debug(self.request.POST.items());
        logger.debug(form.clean())
        
        
        return CreateView.form_valid(self, form)


class JobList(LoginRequiredMixin, ListView):
    '''
    List
    '''
    template_name = 'jobs/job_list.html'
    model = Job

class JobDetail(LoginRequiredMixin, DetailView):
    '''
    Detail 
    '''
    template_name = 'jobs/job_detail.html'
    model = Job



class JobUpdate(LoginRequiredMixin, UpdateView):
    '''
    Update
    '''
    template_name = 'jobs/job_form.html'
    #form_class = JobForm
    model = Job
