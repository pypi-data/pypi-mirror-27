"""
note app models goes here.
"""
from django.db import models
from django.conf import settings
from django.urls import reverse


class NotesList(models.Model):
    """
    A class that represents a user's note list.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=120)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}, created: {}, modified: {}'.format(
            self.name,
            self.created,
            self.modified
        )

    @property
    def items(self):
        for note in Note.objects.filter(notes_list=self):
            yield note

    @property
    def completed(self):
        """
        Checks if all items for self are checked.

        :return: True if all are True, False otherwise.
        """
        return all((note.done for note in self.items))

    def get_absolute_url(self):
        return reverse('note:list-detail', kwargs={'notes_list_id': self.id})


class Note(models.Model):
    """
    A class which objects represent note list items.
    """
    notes_list = models.ForeignKey(NotesList)
    title = models.CharField(max_length=150)
    text = models.TextField(blank=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        return '{} from {} is {}'.format(self.title, self.notes_list.name, 'done' if self.done else 'undone')

    def get_absolute_url(self):
        return reverse(
            'note:list-item-detail',
            kwargs={'note_list_id': self.notes_list.id, 'note_list_item_id': self.id}
        )
