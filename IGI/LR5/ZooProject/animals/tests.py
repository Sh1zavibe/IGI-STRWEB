from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import (
    Animal, AnimalType, AnimalClass, Enclosure,
    Review, News, Vacancy, PromoCode, FAQ, Employee, CompanyInfo, ContactMessage
)
from .forms import ContactForm
import datetime


class ZooProjectTests(TestCase):
    def setUp(self):
        """Создание всех необходимых данных для тестов"""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')

        # Инфраструктура
        self.animal_class = AnimalClass.objects.create(name="Млекопитающие")
        self.animal_type = AnimalType.objects.create(name="Лев", animal_class=self.animal_class)
        self.enclosure = Enclosure.objects.create(number=101, name="Саванна", area=500.0)

        # Животное
        self.animal = Animal.objects.create(
            name="Симба",
            species=self.animal_type,
            room=self.enclosure,
            birth_date=datetime.date(2020, 1, 1)
        )

        # Сотрудник
        self.employee = Employee.objects.create(
            full_name="Иван Иванов",
            job_title="Кипер",
            phone="+375 (29) 123-45-67",
            email="ivan@zoo.com",
            birth_date=datetime.date(1990, 1, 1)
        )

        # Прочее
        News.objects.create(title="Новость", short_content="Кратко", content="Полный текст")
        FAQ.objects.create(question="?", answer="!")
        Vacancy.objects.create(title="Работник", description="Опис", salary="1000", is_active=True)
        PromoCode.objects.create(code="SALE", description="D", discount_percent=10,
                                 valid_until=datetime.date(2025, 1, 1), is_active=True)
        CompanyInfo.objects.create(title="О нас", history="Старая", requisites="Рекв")

    def test_all_pages_get(self):
        pages = ['index', 'animal_list', 'about', 'news_list', 'faq_list', 'contacts', 'vacancies', 'promo',
                 'reviews_page', 'signup', 'login']
        for page in pages:
            response = self.client.get(reverse(page))
            self.assertEqual(response.status_code, 200, f"Ошибка на {page}")

    def test_animal_detail_view(self):
        url = reverse('animal_detail', kwargs={'pk': self.animal.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_animal_search_and_sort(self):
        url = reverse('animal_list')
        res = self.client.get(url, {'search': 'Симба'})
        self.assertContains(res, "Симба")
        res = self.client.get(url, {'sort': 'name'})
        self.assertEqual(res.status_code, 200)

    def test_contact_form_submission(self):
        url = reverse('about')
        data = {'name': 'Дмитрий', 'email': 'dima@test.com', 'message': 'Привет'}
        response = self.client.post(url, data)
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_review_lifecycle(self):
        url = reverse('reviews_page')
        # Аноним
        res = self.client.post(url, {'text': 'Anon', 'rating': 5})
        self.assertEqual(res.status_code, 302)
        # Авторизованный
        self.client.login(username='testuser', password='password123')
        self.client.post(url, {'text': 'Классный зоопарк!', 'rating': 5})
        review = Review.objects.get(text='Классный зоопарк!')
        # Удаление
        del_url = reverse('review_delete', args=[review.pk])
        self.client.post(del_url)
        self.assertFalse(Review.objects.filter(pk=review.pk).exists())

    def test_index_statistics_logic(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('chart_labels', response.context)

    def test_model_methods(self):
        self.assertEqual(str(self.animal_class), "Млекопитающие")
        self.assertEqual(str(self.animal), "Лев Симба")

    def test_logout(self):
        """Тест выхода (поддержка Django 5.x POST)"""
        self.client.login(username='testuser', password='password123')
        # Используем POST для логаута
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_privacy_view_fallback(self):
        response = self.client.get(reverse('privacy'))
        self.assertEqual(response.status_code, 200)
