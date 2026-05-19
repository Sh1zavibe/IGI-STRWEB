from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('animals/', views.animal_list, name='animal_list'),
    path('animals/<int:pk>/', views.animal_detail, name='animal_detail'),
    path('about/', views.about, name='about'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'), # Добавлено: Читать далее
    path('faq/', views.faq_list, name='faq_list'),
    path('contacts/', views.contact_view, name='contacts'),
    path('vacancies/', views.vacancy_view, name='vacancies'),
    path('promo/', views.promo_view, name='promo'),
    re_path(r'^privacy/$', views.privacy_view, name='privacy'),
    path('reviews/', views.reviews_page, name='reviews_page'),
    path('reviews/delete/<int:pk>/', views.review_delete, name='review_delete'),
    path('reviews/update/<int:pk>/', views.review_update, name='review_update'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
]
