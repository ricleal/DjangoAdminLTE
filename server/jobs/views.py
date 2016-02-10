from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, RedirectView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.http import Http404

from pprint import pformat
from .models import Job, Transaction
from .forms import JobForm


import logging

logger = logging.getLogger('jobs.views')

class JobCreate(LoginRequiredMixin, CreateView):
    '''
    Create
    '''
    template_name = 'jobs/job_form.html'
    form_class = JobForm

    def get_initial(self):
        """
        Returns the initial data to populate the form
        """
        initial = super(JobCreate, self).get_initial()
        content_type = ContentType.objects.get(app_label=self.kwargs['app_name'], model=self.kwargs['model_name'])
        initial['content_type'] = content_type
        initial['object_id'] = self.kwargs['key']
        # Let's make the script: get the Manager
        object_class = content_type.model_class()
        object_ = object_class.objects.get(pk = self.kwargs['key'])
        initial['script'] = object_class.objects.to_script(pk = self.kwargs['key'])
        initial['title'] = "Job for " + object_.title
        return initial

    def form_valid(self, form):
        """
        Sets initial values which are hidden in the form
        """
        #logger.debug(pformat(self.request.POST.items()))
        
        form.instance.user = self.request.user
        form.instance.instrument = self.request.user.profile.instrument
#         if 'button_reduce' in self.request.POST:
#             logger.debug("Reducing... create transaction:")
#             # create a transaction
#             transaction = Transaction.objects.start_transaction(self.request, form.instance.title)
#             if transaction:
#                 form.instance.transaction = transaction
#                 form.request = self.request
#             else:
#                 raise Http404
        return CreateView.form_valid(self, form)


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
    form_class = JobForm
    
    def get_object(self):
        return get_object_or_404(Job, pk=self.kwargs['pk'])
