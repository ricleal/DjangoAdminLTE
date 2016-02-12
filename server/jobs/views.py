from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, RedirectView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy

from pprint import pformat
from .models import Job, Transaction
from .forms import JobForm
from .remote import communication as remote

import json 
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
        It creates an object from a generic relationship
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


class JobSubmission(LoginRequiredMixin, JobsMixin, DetailView):
    '''
    It assumes that there is a 1 job per transaction
    If the has been previously submitted, clones it and re-submit it
    The idea is to keep track of what is happening, even if it failed we keep an history.
    '''
    template_name = 'jobs/job_detail.html'
    model = Job
    
    def get_object(self, queryset=None):
        obj = super(JobSubmission, self).get_object(queryset)
        
        transaction = Transaction.objects.start_transaction(self.request, "Transaction for " + obj.title)
        if not transaction:
            raise Http404
        
        submitted_obj = Job.objects.submit_job(self.request, transaction, obj)
        if submitted_obj:
            self.kwargs['pk'] = submitted_obj.pk
            messages.success(self.request, "Job '%s' submitted to the cluster."%(submitted_obj))
        else:
            messages.error(self.request, "Job '%s' NOT submitted to the cluster."%(submitted_obj))
        return submitted_obj
    
    

class JobQuery(LoginRequiredMixin, JobsMixin, DetailView):
    '''
    Queries the remote to check the status of this job and populate
    the fields remote_*
    '''
    template_name = 'jobs/job_detail.html'
    model = Job
    
    def get_object(self, queryset=None):
        obj = super(JobQuery, self).get_object(queryset)
        obj = Job.objects.query_job(self.request, obj)
        if obj:
            messages.success(self.request, "Job '%s' successfully queried."%obj.title)
        else:
            messages.error(self.request, "Job '%s' NOT successfully queried."%(obj.title))
        return obj

    
class JobDelete(LoginRequiredMixin, JobsMixin, DeleteView):
    '''
    Deletes the job object and aborts the transaction remotely just in case
    '''
    success_url = reverse_lazy('jobs:job_list')
    model = Job
    
    def get_object(self, queryset=None):
        obj = super(JobDelete, self).get_object(queryset)
        success = Job.objects.delete_job(self.request, obj)
        if success:
            messages.success(self.request, "Remote Job '%s' successfully aborted."%obj)
        return obj

class JobResults(LoginRequiredMixin, JobsMixin, DetailView):
    
    template_name = 'jobs/job_results.html'
    model = Job
    
    def get_object(self, queryset=None):
        obj = super(JobResults, self).get_object(queryset)
        self.file_list = Transaction.objects.file_listing(self.request, obj.transaction)
        return obj
    
    def get_context_data(self, **kwargs):
        '''
        Set file list. It's called after get_object
        '''
        context = super(JobResults, self).get_context_data(**kwargs)
        if self.file_list:
            context["file_list"] = [[str(i)] for i in self.file_list] # remove unicode and make list of lists
        else:
            messages.error(self.request, "There was a problem getting the file list from the cluster.")
        return context


from .plotting.data import iq_string_to_plot_format
from .plotting.plot_1d import plot1d
from django.http import HttpResponse

def plot1d_multiple_ajax(request,job_id):
    
    logger.debug(pformat(request.POST.items()))
    plot_anchor  = ""
    job = get_object_or_404(Job, pk=job_id)
    try:
        files = request.POST['files']
        logger.debug(files)
        files = json.loads(files)
    except Exception, e:
        messages.error(request,"Error getting the files posted...")
    else:
        plot_data = []
        for filename in files:
            filename = filename[0] # it comes in an array
            logger.debug("Making plot for %s."%filename)
            file_content = Transaction.objects.download(request, job.transaction, filename)
            plot_data.append(iq_string_to_plot_format(file_content, filename))
        
        plot_anchor  = plot1d(plot_data)
                             
    
        

    return HttpResponse(plot_anchor)

