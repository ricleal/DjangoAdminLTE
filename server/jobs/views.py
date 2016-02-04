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
    fields = '__all__'
    
    def get_initial(self):
        """
        Returns the initial data to populate the form
        """
        initial = super(JobCreate, self).get_initial()
        content_type = ContentType.objects.get(app_label=self.kwargs['app_name'], model=self.kwargs['model_name'])
        initial['content_type'] = content_type
        initial['object_id'] = self.kwargs['key']
        initial['user'] = self.request.user
        initial['instrument'] = self.request.user.profile.instrument
        # Let's make the script: get the Manager
        object_class = content_type.model_class()
        initial['script'] = object_class.objects.to_script(pk = self.kwargs['key'])
        return initial
    

class JobsMixin(object):

    def get_queryset(self):
        '''
        Make sure the user only accesses its Jobs
        '''
        return Job.objects.filter(user = self.request.user)

class JobList(LoginRequiredMixin, JobsMixin, ListView):
    '''
    List
    '''
    template_name = 'jobs/job_list.html'
    #model = Job
    def get_queryset(self):
        return super(JobList, self).get_queryset()

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
    model = Job
    fields = '__all__'
    
