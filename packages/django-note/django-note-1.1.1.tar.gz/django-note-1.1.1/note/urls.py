from django.conf.urls import url, include
from .views import Index
from .views import NotesListCreateView, NotesListDetailView, NotesListUpdateView, NotesListDeleteView
from .views import NoteCreateView, NoteDetailView, NoteUpdateView, NoteDeleteView

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    url(r'^list/', include([
        url('^add/$', NotesListCreateView.as_view(), name='list-add'),
        url(r'^(?P<notes_list_id>\d+)/', include([
            url(r'^$', NotesListDetailView.as_view(), name='list-detail'),
            url(r'^update/$', NotesListUpdateView.as_view(), name='list-update'),
            url(r'^delete/$', NotesListDeleteView.as_view(), name='list-delete'),
            url(r'^item/', include([
                url(r'add/$', NoteCreateView.as_view(), name='list-item-add'),
                url(r'(?P<note_id>\d+)/', include([
                    url(r'^$', NoteDetailView.as_view(), name='list-item-detail'),
                    url(r'^update/$', NoteUpdateView.as_view(), name='list-item-update'),
                    url(r'^delete/$', NoteDeleteView.as_view(), name='list-item-delete'),
                ]))
            ]))
        ]))
    ])),
]
