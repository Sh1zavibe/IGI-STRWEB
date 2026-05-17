from django.contrib import admin
from .models import (
    AnimalClass, AnimalType, Enclosure, FeedType,
    Animal, Employee, AccessCard, News, FAQ, Review,
    PromoCode, ContactMessage, Vacancy, CompanyInfo
)

# --- 1. Вспомогательные классы (Inlines) ---

class AnimalInline(admin.TabularInline):
    """Позволяет добавлять животных прямо на странице вольера"""
    model = Animal
    extra = 1
    fields = ('name', 'species', 'birth_date')

# --- 2. Настройка основных моделей ---

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'room', 'birth_date')
    list_filter = ('species', 'room', 'species__animal_class') # Добавили фильтр по классу через связь
    search_fields = ('name', 'species__name')
    date_hierarchy = 'birth_date' # Удобная навигация по датам сверху

@admin.register(Enclosure)
class EnclosureAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'area', 'has_pool')
    list_editable = ('has_pool',) # Можно переключать наличие бассейна прямо в списке
    inlines = [AnimalInline]

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'job_title', 'phone', 'birth_date')
    search_fields = ('full_name', 'job_title')
    list_filter = ('job_title',)

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'salary', 'is_active') # Поля должны совпадать с моделями
    list_filter = ('is_active',)
    list_editable = ('is_active',)

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('is_active',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'short_content')
    search_fields = ('title', 'content')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'sent_at')
    readonly_fields = ('name', 'email', 'message', 'sent_at') # Сообщения обычно не редактируют

# --- 3. Простая регистрация оставшихся моделей ---

admin.site.register(AnimalClass)
admin.site.register(AnimalType)
admin.site.register(FeedType)
admin.site.register(AccessCard)
admin.site.register(FAQ)
admin.site.register(CompanyInfo)
