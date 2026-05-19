from django.contrib import admin
from .models import (
    AnimalClass, AnimalType, Enclosure, FeedType,
    Animal, Employee, AccessCard, News, FAQ, Review,
    PromoCode, ContactMessage, Vacancy, CompanyInfo
)

# Используем декораторы для моделей с настройками
@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'room', 'birth_date')
    list_filter = ('species', 'room')

@admin.register(Enclosure)
class EnclosureAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'area', 'has_pool')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'job_title', 'phone')

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'salary', 'is_active')

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'is_active')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'created_at')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'sent_at')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'short_content')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'added_date')

# Регистрируем оставшиеся простые модели ОДИН РАЗ
admin.site.register([AnimalClass, AnimalType, FeedType, AccessCard, CompanyInfo])
