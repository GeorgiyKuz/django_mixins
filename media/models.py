from django.db import models

# Create your models here.

from django.db import models

from media.mixins import BorrowableMixin, DownloadableMixin


class MediaItem(models.Model):
    title = models.CharField(max_length=200)
    creator = models.CharField(max_length=100)
    publication_date = models.DateField()
    _internal_id = models.CharField(max_length=50, blank=True)  # инкапсуляция

    class Meta:
        abstract = True

    def get_description(self):
        raise NotImplementedError("Метод должен быть переопределен в дочерних классах")

    def _generate_internal_id(self):
        return f"MEDIA_{self.title[:5].upper()}"



class Book(BorrowableMixin, MediaItem):
    isbn = models.CharField(max_length=20)
    page_count = models.IntegerField()
    is_borrowed = models.BooleanField(default=False)
    borrowed_by = models.CharField(max_length=100, blank=True)

    def get_description(self):
        return f"Книга '{self.title}' автора {self.creator}, {self.page_count} стр."

    def read_sample(self):
        return f"Чтение отрывка из книги '{self.title}'"

    def get_media_type(self):
        return "book"

class Movie(DownloadableMixin, MediaItem):
    duration = models.IntegerField(help_text="Длительность в минутах")
    format = models.CharField(max_length=10)
    director = models.CharField(max_length=100)

    def get_description(self):  # полиморфизм
        return f"Фильм '{self.title}' режиссера {self.director}"

    def play_trailer(self):
        return f"Воспроизведение трейлера фильма '{self.title}'"

    def get_media_type(self):
        return "movie"

class AudioBook(DownloadableMixin, BorrowableMixin, MediaItem):
    duration = models.IntegerField()
    narrator = models.CharField(max_length=100)
    is_borrowed = models.BooleanField(default=False)
    borrowed_by = models.CharField(max_length=100, blank=True)

    def get_description(self):
        return f"Аудиокнига '{self.title}', читает {self.narrator}"

    def get_media_type(self):
        return "audiobook"
