# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import NotesList, Note


class Index(LoginRequiredMixin, ListView):
    model = NotesList
    context_object_name = 'notes_lists'
    template_name = 'note/index.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class CRUDViewCommonMixin:
    model = None
    pk_url_kwarg = ''
    context_object_name = ''


class NotesListCRUDViewCommonMixin(CRUDViewCommonMixin):
    model = NotesList
    pk_url_kwarg = 'notes_list_id'
    context_object_name = 'notes_list'


class NotesListCreateView(LoginRequiredMixin, NotesListCRUDViewCommonMixin, CreateView):
    fields = ['name']
    template_name = 'note/list/create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class NotesListDetailView(LoginRequiredMixin, NotesListCRUDViewCommonMixin, DetailView):
    template_name = 'note/list/detail.html'


class NotesListUpdateView(LoginRequiredMixin, NotesListCRUDViewCommonMixin, UpdateView):
    fields = ['name']
    template_name = 'note/list/update.html'


class NotesListDeleteView(LoginRequiredMixin, NotesListCRUDViewCommonMixin, DeleteView):
    template_name = 'note/list/delete.html'
    success_url = reverse_lazy('note:index')


class NoteCRUDViewCommonMixin(CRUDViewCommonMixin):
    model = Note
    pk_url_kwarg = 'note_id'
    context_object_name = 'note'


class NoteCreateView(LoginRequiredMixin, NoteCRUDViewCommonMixin, CreateView):
    fields = ['title', 'text']
    template_name = 'note/list/item/create.html'

    def form_valid(self, form):
        form.instance.notes_list = NotesList.objects.get(id=self.kwargs['notes_list_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('note:list-detail', kwargs=self.kwargs)


class NoteDetailView(LoginRequiredMixin, NoteCRUDViewCommonMixin, DetailView):
    template_name = 'note/list/item/detail.html'


class NoteUpdateView(LoginRequiredMixin, NoteCRUDViewCommonMixin, UpdateView):
    fields = ['title', 'text', 'done']
    template_name = 'note/list/update.html'

    def get_success_url(self):
        return reverse('note:list-detail', kwargs={'notes_list_id': self.kwargs['notes_list_id']})


class NoteDeleteView(LoginRequiredMixin, NoteCRUDViewCommonMixin, DeleteView):
    template_name = 'note/list/item/delete.html'

    def get_success_url(self):
        return reverse('note:list-detail', kwargs={'notes_list_id': self.kwargs['notes_list_id']})
