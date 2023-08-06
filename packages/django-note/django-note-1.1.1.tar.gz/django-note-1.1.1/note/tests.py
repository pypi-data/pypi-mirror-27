from django.test import TestCase, RequestFactory
from django.conf import settings
from django.apps import apps
from django.contrib.auth.models import AnonymousUser

from .models import NotesList, Note
from .views import Index
from .views import NotesListCreateView
from .views import NoteCreateView, NoteUpdateView, NoteDeleteView


AUTH_USER_MODEL = apps.get_model(settings.AUTH_USER_MODEL)


class NotesListModelTestCase(TestCase):
    def setUp(self):
        self.notes_list = NotesList.objects.create(name='Test list', user=AUTH_USER_MODEL.objects.create())

    def test_datetime_logic(self):
        self.assertLessEqual(self.notes_list.created, self.notes_list.modified)

    def test_completed(self):
        self.assertTrue(self.notes_list.completed)


class NoteModelTestCase(TestCase):
    def setUp(self):
        self.note_list_item = Note.objects.create(
            title='Test item',
            notes_list=NotesList.objects.create(name='Test list', user=AUTH_USER_MODEL.objects.create()),
            text='Lorem ipsum dolor ... sit amet'
        )

    def test_done(self):
        self.assertFalse(self.note_list_item.done)


class ViewTestCase(TestCase):
    def setUp(self):
        self._view = None
        self._request_factory = RequestFactory()
        self._user = AnonymousUser()


class ConcreteUserViewTestCase(ViewTestCase):
    def setUp(self):
        super().setUp()
        self._user = AUTH_USER_MODEL.objects.create()


class IndexViewTestCase(ConcreteUserViewTestCase):
    def setUp(self):
        super().setUp()
        self._view = Index()
        self._view.request = self._request_factory.get('/')
        self._view.request.user = self._user

    def test_get_queryset(self):
        for notes_list in self._view.get_queryset():
            self.assertEqual(notes_list.user, self._user)

    def test_as_view(self):
        response = Index.as_view()(self._view.request)
        self.assertEqual(response.status_code, 200)


class CRUDViewCommonMixinTestCase(TestCase):
    pass


class NotesListCRUDViewCommonMixinTestCase(TestCase):
    pass


class NotesListCreateViewTestCase(ConcreteUserViewTestCase):
    def setUp(self):
        super().setUp()
        self._view = NotesListCreateView()
        self._view.request = self._request_factory.get('/list/add/')
        self._view.request.user = self._user

    def test_form_valid(self):
        form = self._view.get_form_class()({'name': 'test_list'})
        self.assertEqual(self._view.form_valid(form).status_code, 302)

    def test_as_view(self):
        response = NotesListCreateView.as_view()(self._view.request)
        self.assertEqual(response.status_code, 200)


class NotesListDetailViewTestCase(ConcreteUserViewTestCase):
    pass


class NotesListUpdateViewTestCase(ConcreteUserViewTestCase):
    pass


class NotesListDeleteViewTestCase(ConcreteUserViewTestCase):
    pass


class NoteCRUDViewCommonMixinTestCase(ConcreteUserViewTestCase):
    pass


class NoteCreateViewTestCase(ConcreteUserViewTestCase):
    def setUp(self):
        super().setUp()
        self._view = NoteCreateView()
        self._view.request = self._request_factory.get('/list/item/add/')
        self._view.request.user = self._user
        test_notes_list = NotesList.objects.create(name='test note list', user=self._user)
        setattr(self._view, 'kwargs', {'notes_list_id': test_notes_list.id})

    def test_form_valid(self):
        form = self._view.get_form_class()({'title': 'test_list item', 'text': 'test_list item text'})
        self.assertEqual(self._view.form_valid(form).status_code, 302)

    def test_get_success_url(self):
        self.assertNotEqual(self._view.get_success_url(), '')

    def test_as_view(self):
        response = NoteCreateView.as_view()(self._view.request)
        self.assertEqual(response.status_code, 200)


class NoteDetailViewTestCase(ConcreteUserViewTestCase):
    pass


class NoteUpdateViewTestCase(ConcreteUserViewTestCase):
    def setUp(self):
        super().setUp()
        self._view = NoteUpdateView()
        test_notes_list = NotesList.objects.create(name='test note list', user=self._user)
        setattr(self._view, 'kwargs', {'notes_list_id': test_notes_list.id})

    def test_get_success_url(self):
        self.assertNotEqual(self._view.get_success_url(), '')


class NoteDeleteViewTestCase(ConcreteUserViewTestCase):
    def setUp(self):
        super().setUp()
        self._view = NoteDeleteView()
        test_notes_list = NotesList.objects.create(name='test note list', user=self._user)
        setattr(self._view, 'kwargs', {'notes_list_id': test_notes_list.id})

    def test_get_success_url(self):
        self.assertNotEqual(self._view.get_success_url(), '')
