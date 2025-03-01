from django.views import generic
from django.utils.http import urlencode
from django.http import HttpResponseRedirect

from .services.llm import LLMPhonebookService
from .forms import PromptForm
from .models import Contact

class IndexView(generic.FormView):
    form_class = PromptForm
    template_name = "phonebook/index.html"

    llm = LLMPhonebookService()

    def form_valid(self, form):
        action = self.llm.process_prompt(form.cleaned_data["prompt"])
        response = self.llm.process_action(action)
        
        return HttpResponseRedirect(response['url'] + "?" + urlencode({'msg': response['msg']}))

class ListView(generic.ListView):
    model = Contact

class DetailView(generic.DetailView):
    model = Contact