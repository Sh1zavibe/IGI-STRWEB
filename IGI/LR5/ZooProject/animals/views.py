import requests
import json
import logging
import calendar
import datetime
from statistics import median, mode, StatisticsError

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Count
from django.contrib.auth import login
from django.utils import timezone
from .models import News, Animal, Enclosure, FAQ, Vacancy, Review, Employee, PromoCode, CompanyInfo
from .forms import ContactForm, SignUpForm, ReviewForm

logger = logging.getLogger(__name__)

def index(request):
    last_news = News.objects.order_by('-published_date').first()
    weather = {'error': 'Данные недоступны'}
    try:
        res = requests.get('https://api.open-meteo.com/v1/forecast?latitude=53.9&longitude=27.56&current_weather=true', timeout=2)
        if res.status_code == 200:
            data = res.json()
            weather = {'temp': data['current_weather']['temperature'], 'wind': data['current_weather']['windspeed']}
    except: pass

    animal_fact = "Интересный факт скоро появится."
    try:
        fact_res = requests.get('https://catfact.ninja/fact', timeout=2)
        if fact_res.status_code == 200: animal_fact = fact_res.json().get('fact')
    except: pass

    avg_area = Enclosure.objects.aggregate(Avg('area'))['area__avg'] or 0
    employees = Employee.objects.all()
    ages = [(datetime.date.today().year - e.birth_date.year) for e in employees]
    med_age = median(ages) if ages else 0
    try: mod_age = mode(ages) if ages else 0
    except StatisticsError: mod_age = "Разнообразно"

    cal = calendar.HTMLCalendar().formatmonth(datetime.date.today().year, datetime.date.today().month)
    now_utc = datetime.datetime.now(datetime.timezone.utc)

    chart_data_qs = Animal.objects.values('species__animal_class__name').annotate(total=Count('id'))
    chart_labels = [item['species__animal_class__name'] for item in chart_data_qs if
                    item['species__animal_class__name']]
    chart_values = [item['total'] for item in chart_data_qs if item['species__animal_class__name']]

    return render(request, 'animals/index.html', {
        'last_news': News.objects.order_by('-published_date').first(),
        'weather': weather,
        'animal_fact': animal_fact,
        'stats': {'avg_area': round(avg_area, 2), 'med_age': med_age, 'mod_age': mod_age},
        'times': {
            'local': timezone.now(),
            'utc': datetime.datetime.now(datetime.timezone.utc),
            'calendar': cal,
            'tz_name': timezone.get_current_timezone_name()
        },
        # Важно: передаем как JSON-строки для JS
        'chart_labels': json.dumps(chart_labels),
        'chart_values': json.dumps(chart_values),
    })


def animal_list(request):
    search_query = request.GET.get('search', '')
    sort_param = request.GET.get('sort', 'name')  # По умолчанию сортировка по имени

    animals = Animal.objects.all().select_related('species', 'room')

    if search_query:
        animals = animals.filter(name__icontains=search_query)

    # Сортировка
    if sort_param:
        animals = animals.order_by(sort_param)

    return render(request, 'animals/animal_list.html', {
        'animals': animals,
        'search_query': search_query,
        'current_sort': sort_param
    })

def animal_detail(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    return render(request, 'animals/animal_detail.html', {'animal': animal})

def reviews_page(request):
    reviews = Review.objects.all().order_by('-created_at')
    form = ReviewForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            logger.warning("Анонимный пользователь пытался оставить отзыв")
            return redirect('login')  # Или выдай ошибку 403

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.name = request.user.username
            review.save()
            logger.info(f"Пользователь {request.user.username} оставил отзыв")
            return redirect('reviews_page')
    return render(request, 'animals/reviews.html', {'reviews': reviews, 'form': form})

# Функция удаления для полного CRUD
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user.username == review.name or request.user.is_superuser:
        review.delete()
    return redirect('reviews_page')

def vacancy_view(request):
    vacancies = Vacancy.objects.filter(is_active=True).order_by('-posted_date')
    return render(request, 'animals/vacancies.html', {'vacancies': vacancies})

def promo_view(request):
    promos = PromoCode.objects.filter(is_active=True)
    return render(request, 'animals/promo.html', {'promos': promos})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            logger.info(f"Новый пользователь зарегистрирован: {user.username}")  # Логирование
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def about(request):
    info = CompanyInfo.objects.first()
    form = ContactForm(request.POST or None)
    success = False
    if request.method == 'POST' and form.is_valid():
        form.save()
        logger.info(f"Получено новое сообщение обратной связи от {form.cleaned_data['email']}")
        success = True
        form = ContactForm()
    return render(request, 'animals/about.html', {'info': info, 'form': form, 'success': success})

def faq_list(request): return render(request, 'animals/faq.html', {'faqs': FAQ.objects.all()})
def news_list(request): return render(request, 'animals/news_list.html', {'news': News.objects.all()})
def contact_view(request):
    form = ContactForm() # Создаем пустую форму
    return render(request, 'animals/contacts.html', {
        'employees': Employee.objects.all(),
        'form': form  # Передаем форму в шаблон
    })
def privacy_view(request):
    try:
        return render(request, 'animals/privacy.html')
    except:
        from django.http import HttpResponse
        return HttpResponse("Политика конфиденциальности")


@login_required  # Защита удаления (Требование №6)
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user.username == review.name or request.user.is_superuser:
        review.delete()
        logger.info(f"Отзыв {pk} удален пользователем {request.user.username}")
    return redirect('reviews_page')

