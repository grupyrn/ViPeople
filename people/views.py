from django.core.urlresolvers import reverse_lazy

from vanilla import CreateView, DeleteView, ListView, UpdateView

from .models import People
from .forms import People as PeopleForm


class BasePeopleView(object):
    model = People
    form_class = PeopleForm


class ListPeople(BasePeopleView, ListView):
    template_name = 'people_list.html'


class CreatePeople(BasePeopleView, CreateView):
    template_name = 'people_form.html'


class UpdatePeople(BasePeopleView, UpdateView):
    template_name = 'people_form.html'


class DeletePeople(BasePeopleView, DeleteView):
    template_name = 'people_confirm_delete.html'
    success_url = reverse_lazy('people_list')