import datetime
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from datetime import date
from zoneinfo import ZoneInfo
from django.utils import timezone

# --- Валидаторы ---

phone_validator = RegexValidator(
    regex=r'^\+375 \((29|33|44|25)\) \d{3}-\d{2}-\d{2}$',
    message="Номер телефона должен быть в формате: +375 (29) XXX-XX-XX"
)

def validate_age_18(birthday):
    today = date.today()
    age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
    if age < 18:
        raise ValidationError("Возраст должен быть не менее 18 лет.")

def validate_not_future(value):
    if value > date.today():
        raise ValidationError("Дата не может быть в будущем.")


# --- 1. Предметная область (Зоопарк) ---

class AnimalClass(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название класса")

    class Meta:
        verbose_name = "Класс животных"
        verbose_name_plural = "Классы животных"

    def __str__(self):
        return self.name

class AnimalType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название вида")
    animal_class = models.ForeignKey(AnimalClass, on_delete=models.CASCADE, verbose_name="Класс")

    class Meta:
        verbose_name = "Вид животного"
        verbose_name_plural = "Виды животных"

    def __str__(self):
        return self.name

class Enclosure(models.Model):
    number = models.IntegerField(unique=True, verbose_name="Номер помещения")
    name = models.CharField(max_length=100, verbose_name="Название комплекса")
    has_pool = models.BooleanField(default=False, verbose_name="Наличие водоема")
    area = models.FloatField(verbose_name="Площадь (м2)")

    class Meta:
        verbose_name = "Вольер"
        verbose_name_plural = "Вольеры"

    def __str__(self):
        return f"Вольер №{self.number} ({self.name})"

class FeedType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Тип корма")
    daily_amount = models.FloatField(help_text="кг в сутки", verbose_name="Норма потребления")

    class Meta:
        verbose_name = "Вид корма"
        verbose_name_plural = "Виды корма"

    def __str__(self):
        return self.name

class Animal(models.Model):
    name = models.CharField(max_length=100, verbose_name="Кличка")
    species = models.ForeignKey(AnimalType, on_delete=models.PROTECT, verbose_name="Вид")
    room = models.ForeignKey(Enclosure, on_delete=models.SET_NULL, null=True, verbose_name="Помещение")
    birth_date = models.DateField(validators=[validate_not_future], verbose_name="Дата рождения")
    arrival_date = models.DateField(auto_now_add=True, verbose_name="Дата поступления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Ссылка на фото")
    feeds = models.ManyToManyField(FeedType, verbose_name="Рацион")

    class Meta:
        verbose_name = "Животное"
        verbose_name_plural = "Животные"

    def __str__(self):
        return f"{self.species} {self.name}"

# --- 2. Сотрудники и Контакты ---

class AccessCard(models.Model):
    card_number = models.CharField(max_length=50, unique=True, verbose_name="Номер карты")
    issued_at = models.DateField(auto_now_add=True, verbose_name="Выдана")

    class Meta:
        verbose_name = "Пропуск"
        verbose_name_plural = "Пропуски"

    def __str__(self):
        return self.card_number

class Employee(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="ФИО")
    photo_url = models.URLField(max_length=500, verbose_name="Ссылка на фото", null=True, blank=True)
    job_title = models.CharField(max_length=100, verbose_name="Должность")
    work_description = models.TextField(verbose_name="Описание выполняемых работ", blank=True)
    phone = models.CharField(validators=[phone_validator], max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Почта")
    birth_date = models.DateField(
        validators=[validate_age_18, validate_not_future],
        verbose_name="Дата рождения"
    )
    assigned_enclosure = models.ForeignKey(Enclosure, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Закрепленный вольер")
    access_card_id = models.OneToOneField(AccessCard, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Личный пропуск")

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return self.full_name

# --- 3. Служебные страницы (новости, отзывы, вакансии и др.) ---

class CompanyInfo(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    history = models.TextField(verbose_name="История")
    requisites = models.TextField(verbose_name="Реквизиты")
    logo = models.ImageField(upload_to='company/', blank=True, verbose_name="Логотип")

    class Meta:
        verbose_name = "О компании"
        verbose_name_plural = "О компании"

    def __str__(self):
        return self.title

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    short_content = models.CharField(max_length=255, verbose_name="Краткое содержание (1 предложение)")
    content = models.TextField(verbose_name="Полный текст")
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Ссылка на картинку")
    published_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    class Meta:
        ordering = ['-published_date']
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title

class FAQ(models.Model):
    question = models.CharField(max_length=255, verbose_name="Термин / Вопрос")
    answer = models.TextField(verbose_name="Определение / Ответ")
    added_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления на сайт")

    class Meta:
        verbose_name = "Словарь терминов"
        verbose_name_plural = "Словарь терминов и понятий" # Именно так, как в ТЗ

    def __str__(self):
        return self.question


class Review(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя автора")
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)],
                                         verbose_name="Оценка")

    # Это поле Django сохранит в БД как UTC, но покажет как Локальное
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def get_local_time(self):
        return self.created_at.astimezone(ZoneInfo("Europe/Minsk"))
    def get_utc_time(self):
        # Используем стандартный python-way для UTC
        return self.created_at.astimezone(datetime.timezone.utc)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

class Vacancy(models.Model):
    title = models.CharField(max_length=200, verbose_name="Должность")
    description = models.TextField(verbose_name="Описание")
    salary = models.CharField(max_length=100, verbose_name="Зарплата")
    posted_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="Активна")  # Добавь это!

    def __str__(self):
        return self.title

class PromoCode(models.Model):
    code = models.CharField(max_length=20, verbose_name="Промокод")
    description = models.CharField(max_length=200, verbose_name="Для чего")
    discount_percent = models.IntegerField(verbose_name="Скидка %")
    valid_until = models.DateField(verbose_name="Годен до")
    is_active = models.BooleanField(default=True, verbose_name="Активен") # Добавь это!

    def __str__(self):
        return self.code

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Сообщение")
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    class Meta:
        verbose_name = "Обратная связь"
        verbose_name_plural = "Сообщения обратной связи"

