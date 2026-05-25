import requests
import logging
import calendar
import datetime
import io
import base64
from statistics import median, mode, StatisticsError
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Count
from django.contrib.auth import login
from django.utils import timezone

from .models import News, Animal, Enclosure, FAQ, Vacancy, Review, Employee, PromoCode, CompanyInfo
from .forms import ContactForm, SignUpForm, ReviewForm

logger = logging.getLogger(__name__)

def generate_animal_chart():
    """Генерирует круговую диаграмму классов животных"""
    data_qs = Animal.objects.values('species__animal_class__name').annotate(total=Count('id'))
    labels = [item['species__animal_class__name'] or 'Другие' for item in data_qs]
    values = [item['total'] for item in data_qs]

    if not values:
        return None

    plt.figure(figsize=(6, 4))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140,
            colors=['#ffc107', '#17a2b8', '#28a745', '#dc3545'])
    plt.title("Распределение животных по классам")
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()
    return image_base64

# --- ГЛАВНАЯ СТРАНИЦА ---
def index(request):
    last_news = News.objects.order_by('-published_date').first()
    latest_faqs = FAQ.objects.order_by('-added_date')[:3] # 3 вопроса для главной
    now = timezone.now()

    # Погода API
    weather = {'error': 'Данные недоступны'}
    try:
        res = requests.get('https://api.open-meteo.com/v1/forecast?latitude=53.9&longitude=27.56&current_weather=true', timeout=2)
        if res.status_code == 200:
            data = res.json()
            weather = {'temp': data['current_weather']['temperature'], 'wind': data['current_weather']['windspeed']}
    except Exception:
        pass

    # Факт о животных API
    animal_fact = "Интересный факт скоро появится."
    try:
        fact_res = requests.get('https://catfact.ninja/fact', timeout=2)
        if fact_res.status_code == 200:
            animal_fact = fact_res.json().get('fact')
    except Exception:
        pass

    # Статистика
    avg_area = Enclosure.objects.aggregate(Avg('area'))['area__avg'] or 0
    employees = Employee.objects.all()
    ages = [(datetime.date.today().year - e.birth_date.year) for e in employees]
    try:
        med_age = median(ages) if ages else 0
        mod_age = mode(ages) if ages else 0
    except StatisticsError:
        mod_age = "Разнообразно"

    cal = calendar.HTMLCalendar().formatmonth(datetime.date.today().year, datetime.date.today().month)
    chart_img = generate_animal_chart()

    return render(request, 'animals/index.html', {
        'last_news': last_news,
        'latest_faqs': latest_faqs,
        'weather': weather,
        'animal_fact': animal_fact,
        'stats': {'avg_area': round(avg_area, 2), 'med_age': med_age, 'mod_age': mod_age},
        'times': {
            'local': timezone.localtime(now), # Переводим в Минск
            'utc': now,                      # Оставляем как есть (UTC)
            'calendar': cal,
        },
        'chart_image': chart_img,
    })

# --- НОВОСТИ ---
def news_list(request):
    news = News.objects.all().order_by('-published_date')
    return render(request, 'animals/news_list.html', {'news': news})

def news_detail(request, pk):
    article = get_object_or_404(News, pk=pk)
    return render(request, 'animals/news_detail.html', {'article': article})

# --- ОТЗЫВЫ ---
def reviews_page(request):
    reviews = Review.objects.all().order_by('-created_at')
    form = ReviewForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.name = request.user.username
            review.save()
            return redirect('reviews_page')
    return render(request, 'animals/reviews.html', {'reviews': reviews, 'form': form})

@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user.username == review.name or request.user.is_superuser:
        review.delete()
    return redirect('reviews_page')

# --- ПРОМОКОДЫ ---
def promo_view(request):
    # Разделяем на действующие и архивные
    active_promos = PromoCode.objects.filter(is_active=True).order_by('valid_until')
    archive_promos = PromoCode.objects.filter(is_active=False).order_by('-valid_until')
    return render(request, 'animals/promo.html', {
        'active_promos': active_promos,
        'archive_promos': archive_promos
    })

# --- ОСТАЛЬНОЕ ---
def about(request):
    info = CompanyInfo.objects.first()
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return render(request, 'animals/about.html', {'info': info, 'form': ContactForm(), 'success': True})
    return render(request, 'animals/about.html', {'info': info, 'form': form})

def contact_view(request):
    employees = Employee.objects.all()
    return render(request, 'animals/contacts.html', {'employees': employees})

def faq_list(request):
    faqs = FAQ.objects.all().order_by('-added_date')
    return render(request, 'animals/faq.html', {'faqs': faqs})


def vacancy_view(request):
    vacancies = Vacancy.objects.filter(is_active=True).order_by('-posted_date')
    return render(request, 'animals/vacancies.html', {'vacancies': vacancies})

def privacy_view(request):
    return render(request, 'animals/privacy.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def animal_list(request):
    animals = Animal.objects.all().select_related('species', 'room')

    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        animals = animals.filter(name__icontains=search_query)

    # Сортировка
    sort_by = request.GET.get('sort', 'name_asc')
    if sort_by == 'name_asc':
        animals = animals.order_by('name')
    elif sort_by == 'name_desc':
        animals = animals.order_by('-name')
    elif sort_by == 'date_asc':
        animals = animals.order_by('birth_date')
    elif sort_by == 'date_desc':
        animals = animals.order_by('-birth_date')
    else:
        animals = animals.order_by('name')

    return render(request, 'animals/animal_list.html', {
        'animals': animals,
        'search_query': search_query,
        'current_sort': sort_by,
    })

def animal_detail(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    return render(request, 'animals/animal_detail.html', {'animal': animal})


@login_required
def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user.username != review.name and not request.user.is_superuser:
        return redirect('reviews_page')

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('reviews_page')
    else:
        form = ReviewForm(instance=review)
    return render(request, 'animals/review_form.html', {'form': form})

