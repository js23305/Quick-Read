from django.urls import path
from . import views

urlpatterns = [
    # path('book_summarizer/', views.book_summarizer, name='book_summarizer'),
    path('process-book/', views.book_summarizer, name='process_book'),
    path('generate-audio/', views.generate_audio, name='generate_audio'),
]