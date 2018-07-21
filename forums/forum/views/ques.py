from django.views import *
from django.views.generic import *
from forum.models import *
from django.shortcuts import *
from forum.views import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import *
from django.utils.timezone import *
from forum.views.comments import *

class AddQuestion(forms.ModelForm):
    class Meta:
        model = Questions
        fields=['tag','question_title','question']

class CreateQuestionView(LoginRequiredMixin,CreateView):
    login_url = '/forum/login/'
    template_name = 'question_form.html'
    model = Questions
    form_class = AddQuestion

    def post(self, request, *args, **kwargs):
        user = request.user

        que_form=AddQuestion(request.POST)
        if que_form.is_valid():
            que=que_form.save(commit=False)
            import datetime
            que.created = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            que.last_modified = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            que.user=user
            que.username=user
            que.save()
        return redirect('questions_html')



class QuestionsListView(LoginRequiredMixin, ListView):
    login_url='/onlineapp/login/'

    model=Questions
    #context_object_name='col'
    #queryset = Questions.objects.all().values()
    template_name='questions.html'
    def get_context_data(self,**kwargs):
        # if not self.request.user.is_authenticated():
        #     redirect("onlineapp:login")

        context=super(QuestionsListView,self).get_context_data(**kwargs)
        context['heading'] = "All Questions"
        context['ques']=self.model.objects.all().values()
        context.update({'user_permissions':self.request.user.get_all_permissions()})
        return context

class QuestionDetailsView(LoginRequiredMixin,DetailView):
    login_url = '/forum/login/'
    model="Questions"
    template_name = 'questionDetails.html'
    def get_object(self, queryset=None):
        return get_object_or_404(Questions,**self.kwargs)

    def get_context_data(self,**kwargs):

        context=super(QuestionDetailsView,self).get_context_data(**kwargs)
        context['que']=Questions.objects.filter(id=self.kwargs['id']).get()
        context['comm']=Comments.objects.all().filter(comm_question=self.kwargs['id'])
        context['usrname']=str(self.request.user)
        context['form']=CreateCommentView.as_view()
        # import ipdb
        # ipdb.set_trace()
        return context


class UpdateQuestionView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    def has_permission(self):
        if self.request.user.id==Questions.objects.filter(id=self.kwargs['id']).values('user_id')[0]['user_id']:
            return True
        else:
            return False

    # def form_valid(self, form):
    #     que = form.save(commit=False)
    #     import datetime
    #     que.last_modified=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     return self.success_url
    # def has_permission(self):
    #     if self.request.user.id==self.kwargs['id']:
    #         return True
    #     else:
    #         return False
        # user=self.request.user
        # id=self.kwargs['userid']
    #if user.id==CreditCard.objects.filter(id=self.kwargs['id'].values('userid')[0]['userid'])
    login_url = '/login/'
    # permission_required = "creditcard:change_mytask"
    # permission_denied_message = "user doesnot have permission to change college"
    # raise_exception = True
    template_name = 'questions_form.html'
    #permission_required = 'onlineapp.add_college'
    #permission_denied_message='user doesnot have permission to create college'
    model=Questions
    form_class=AddQuestion

    # def get_context_data(self, **kwargs):
    #     que=form.save(commit=False)
    #     import datetime
    #     que.last_modified = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     que.save()
    #     return self.success_url



    def get_object(self, queryset=None):
        return get_object_or_404(Questions,**self.kwargs)

    success_url = reverse_lazy('questions_html')


class DeleteQuestionView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    def has_permission(self):
        if self.request.user.id==Questions.objects.filter(id=self.kwargs['id']).values('user_id')[0]['user_id']:
            return True
        else:
            return False
    login_url = 'login/'
    template_name = 'delete.html'
    #permission_required = 'onlineapp.add_college'
    #permission_denied_message='user doesnot have permission to create college'
    model=Questions

    success_url = reverse_lazy('questions_html')
    def get_object(self, queryset=None):
        return get_object_or_404(Questions,**self.kwargs)

class MyQuestionsListView(LoginRequiredMixin, ListView):
    login_url='/forum/login/'

    model=Questions
    #context_object_name='col'
    #queryset = Questions.objects.all().values()
    template_name='questions.html'
    def get_context_data(self,**kwargs):
        # if not self.request.user.is_authenticated():
        #     redirect("onlineapp:login")
        context=super(MyQuestionsListView,self).get_context_data(**kwargs)
        # import ipdb
        # ipdb.set_trace()
        context['heading'] = "My Questions"
        context['ques']=self.model.objects.all().filter(user_id=self.request.user.id).values()
        context.update({'user_permissions':self.request.user.get_all_permissions()})
        return context



class TagsListView(LoginRequiredMixin, ListView):
    login_url='/forum/login/'

    model=Questions
    #context_object_name='col'
    #queryset = Questions.objects.all().values()
    template_name='tags.html'
    def get_context_data(self,**kwargs):
        # if not self.request.user.is_authenticated():
        #     redirect("onlineapp:login")
        context=super(TagsListView,self).get_context_data(**kwargs)
        # import ipdb
        # ipdb.set_trace()
        context['tags']=self.model.objects.all().values('tag').distinct()
        context.update({'user_permissions':self.request.user.get_all_permissions()})
        return context

class TagsDetailListView(LoginRequiredMixin, ListView):
    login_url='/forum/login/'

    model=Questions
    #context_object_name='col'
    #queryset = Questions.objects.all().values()
    template_name='questions.html'
    def get_context_data(self,**kwargs):
        # if not self.request.user.is_authenticated():
        #     redirect("onlineapp:login")
        context=super(TagsDetailListView,self).get_context_data(**kwargs)
        # import ipdb
        # ipdb.set_trace()

        context['ques']=self.model.objects.all().filter(tag=self.kwargs['tag']).values()

        context.update({'user_permissions':self.request.user.get_all_permissions()})
        return context
