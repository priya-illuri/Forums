from django.views import *
from django.views.generic import *
from forum.models import *
from django.shortcuts import *
from forum.views import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import *
from django.utils.timezone import *



class AddComment(forms.ModelForm):
    class Meta:
        model = Comments
        fields=['comment']


class CreateCommentView(LoginRequiredMixin,CreateView):
    login_url = '/forum/login/'
    template_name = 'questionDetails.html'
    model = Comments
    form_class = AddComment


    def get_object(self, queryset=None):
        return get_object_or_404(Questions,**self.kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateCommentView, self).get_context_data(**kwargs)
        context['que'] = Questions.objects.filter(id=self.kwargs['id']).get()
        context['comm'] = Comments.objects.all().filter(comm_question=self.kwargs['id'])
        context['usrname'] = str(self.request.user)
        # context['form'] = CreateCommentView.as_view()
        # import ipdb
        # ipdb.set_trace()
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        question = get_object_or_404(Questions, **kwargs)
        com_form=AddComment(request.POST)
        if com_form.is_valid():
            comm=com_form.save(commit=False)
            import datetime
            comm.commented_on = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            comm.username=user
            #question=Questions.objects.filter(id=self.kwargs['id']).get()
            comm.comm_question=question
            question.no_of_comments+=1
            question.save()
            comm.save()
        return redirect('questions_html')


class DeleteCommentView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    def has_permission(self):

        if str(self.request.user)==Comments.objects.filter(id=self.kwargs['id']).values('username')[0]['username']:

            return True
        else:
            return False
    login_url = 'login/'
    template_name = 'delete.html'
    #permission_required = 'onlineapp.add_college'
    #permission_denied_message='user doesnot have permission to create college'
    model=Comments

    success_url = reverse_lazy('questions_html')

    def get_object(self, queryset=None):
        return get_object_or_404(Comments,**self.kwargs)

    def post(self, request, *args, **kwargs):
        com=Comments.objects.all().filter(id=self.kwargs['id']).values('comm_question_id')[0]['comm_question_id']
        que=Questions.objects.get(pk=com)
        que.no_of_comments-=1

        # import ipdb
        # ipdb.set_trace()
        # que.no_of_comments += 1
        import datetime
        que.last_modified = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        que.save()

        return self.delete(request, *args, **kwargs)