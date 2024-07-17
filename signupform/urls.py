from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('form/', views.form, name='sgform'),
    path('table/', views.table, name='table'),
    path('edit/<int:id>', views.edit, name="edit"),
    path('delete/<int:id>', views.delete, name="delete"),
    path('otp-check/<int:f>', views.otpcheck, name='otpcheck'),
    path('dashboard/', views.dashboard, name="dashboard")

]
