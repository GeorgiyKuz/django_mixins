from django.test import TestCase
from datetime import date
from .models import Movie, Book, AudioBook
from .services import MediaFactory


class MovieModelTestCase(TestCase):
    """Тесты для класса Movie"""

    def setUp(self):
        """Подготовка данных для тестов"""
        self.movie = Movie.objects.create(
            title="Матрица",
            creator="Кино",
            publication_date=date(1999, 3, 31),
            duration=136,
            format="MP4",
            director="Вачовские сестры"
        )

    def test_movie_creation(self):
        """Тест создания объекта Movie"""
        self.assertEqual(self.movie.title, "Матрица")
        self.assertEqual(self.movie.duration, 136)
        self.assertEqual(self.movie.format, "MP4")
        self.assertEqual(self.movie.director, "Вачовские сестры")

    def test_movie_inheritance(self):
        """Тест наследования Movie от MediaItem"""
        self.assertTrue(hasattr(self.movie, 'title'))
        self.assertTrue(hasattr(self.movie, 'creator'))
        self.assertTrue(hasattr(self.movie, 'publication_date'))

    def test_movie_get_description(self):
        """Тест полиморфного переопределения метода get_description"""
        expected_description = "Фильм 'Матрица' режиссера Вачовские сестры"
        self.assertEqual(self.movie.get_description(), expected_description)

    def test_movie_play_trailer(self):
        """Тест уникального метода play_trailer"""
        expected_result = "Воспроизведение трейлера фильма 'Матрица'"
        self.assertEqual(self.movie.play_trailer(), expected_result)

    def test_movie_download_mixin(self):
        """Тест использования DownloadableMixin"""
        # Проверяем, что Movie имеет метод download от миксина
        self.assertTrue(hasattr(self.movie, 'download'))
        expected_result = "Скачивание Матрица началось..."
        self.assertEqual(self.movie.download(), expected_result)

    def test_movie_get_media_type(self):
        """Тест метода get_media_type"""
        self.assertEqual(self.movie.get_media_type(), "movie")

    def test_polymorphic_description_difference(self):
        """Тест полиморфного поведения - проверка различия описаний"""
        # Создаем объекты разных типов
        book = Book.objects.create(
            title="Война и мир",
            creator="Лев Толстой",
            publication_date=date(1869, 1, 1),
            isbn="978-5-17-980780-3",
            page_count=1200
        )
        
        # Проверяем, что описания отличаются
        movie_desc = self.movie.get_description()
        book_desc = book.get_description()
        
        self.assertNotEqual(movie_desc, book_desc)
        self.assertIn("режиссера", movie_desc)
        self.assertIn("автора", book_desc)

    def test_movie_duration_field(self):
        """Тест поля длительности"""
        self.assertIsInstance(self.movie.duration, int)
        self.assertGreater(self.movie.duration, 0)

    def test_movie_format_field(self):
        """Тест поля формата"""
        self.assertIsInstance(self.movie.format, str)
        self.assertTrue(len(self.movie.format) > 0)
        self.assertLessEqual(len(self.movie.format), 10)

    def test_movie_director_field(self):
        """Тест поля режиссера"""
        self.assertIsInstance(self.movie.director, str)
        self.assertTrue(len(self.movie.director) > 0)


class MediaFactoryTestCase(TestCase):
    """Тесты для фабрики MediaFactory"""

    def test_factory_create_movie(self):
        """Тест создания Movie через фабрику"""
        movie = MediaFactory.create_media(
            'movie',
            title="Интерстеллар",
            creator="Warner Bros",
            publication_date=date(2014, 11, 5),
            duration=169,
            format="MKV",
            director="Кристофер Нолан"
        )
        
        self.assertIsInstance(movie, Movie)
        self.assertEqual(movie.title, "Интерстеллар")
        self.assertEqual(movie.director, "Кристофер Нолан")

    def test_factory_get_media_class(self):
        """Тест получения класса по типу медиа"""
        movie_class = MediaFactory.get_media_class('movie')
        self.assertEqual(movie_class, Movie)

    def test_factory_get_all_media_types(self):
        """Тест получения всех типов медиа"""
        media_types = MediaFactory.get_all_media_types()
        self.assertIn('movie', media_types)
        self.assertIn('book', media_types)
        self.assertIn('audiobook', media_types)

    def test_factory_invalid_media_type(self):
        """Тест обработки неизвестного типа медиа"""
        with self.assertRaises(ValueError):
            MediaFactory.create_media(
                'invalid_type',
                title="Test",
                creator="Test",
                publication_date=date.today()
            )


class MovieMixinTestCase(TestCase):
    """Тесты для использования миксинов в Movie"""

    def setUp(self):
        self.movie = Movie.objects.create(
            title="Темный рыцарь",
            creator="DC Comics",
            publication_date=date(2008, 7, 18),
            duration=152,
            format="AVI",
            director="Кристофер Нолан"
        )

    def test_downloadable_mixin_presence(self):
        """Тест наличия методов из DownloadableMixin"""
        self.assertTrue(hasattr(self.movie, 'download'))
        self.assertTrue(callable(getattr(self.movie, 'download')))

    def test_download_method_return_value(self):
        """Тест возвращаемого значения метода download"""
        result = self.movie.download()
        self.assertIsInstance(result, str)
        self.assertIn(self.movie.title, result)
        self.assertIn("Скачивание", result)

    def test_movie_does_not_have_borrow(self):
        """Тест отсутствия метода borrow в Movie"""
        # Movie использует только DownloadableMixin, не BorrowableMixin
        self.assertFalse(hasattr(self.movie, 'is_borrowed'))
        self.assertFalse(hasattr(self.movie, 'borrow'))
