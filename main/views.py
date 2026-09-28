from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.cache import cache  # Импортируем кэш для ускорения
from django.views.decorators.cache import cache_page

from .models import Section, Block
from .forms import SectionForm, BlockForm


@cache_page(900, key_prefix='index_page')
def index_page(request):
    """Главная страница сайта (Мгновенная отдача готового HTML из Redis)"""
    sections = Section.objects.prefetch_related('blocks').all()
    return render(request, 'index.html', {'sections': sections})

    if not sections_html:
        # Если в кэше пусто, делаем ОПТИМИЗИРОВАННЫЙ запрос к БД (prefetch_related)
        sections = Section.objects.prefetch_related('blocks').all()
        # Сохраняем в кэш на 15 минут (900 секунд)
        cache.set('index_sections_cache', sections, 900)
    else:
        sections = sections_html

    return render(request, 'index.html', {'sections': sections})


def login_view(request):
    """Вход на сайт"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.username == 'admin_super' or user.is_superuser:
                return redirect('custom_dashboard')
            return redirect('index_page')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """Выход"""
    logout(request)
    return redirect('index_page')


@login_required(login_url='login')
def custom_dashboard(request):
    """Кастомная админка"""
    if request.user.username != 'admin_super' and not request.user.is_superuser:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    sections = Section.objects.prefetch_related('blocks').all()
    return render(request, 'dashboard/main.html', {'sections': sections})


# --- ДОБАВЛЕНИЕ ---
@login_required(login_url='login')
def add_section(request):
    if request.user.username != 'admin_super' and not request.user.is_superuser:
        return redirect('index_page')
    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            form.save()
            cache.delete('index_sections_cache')  # Сбрасываем кэш при изменениях!
            return redirect('custom_dashboard')
    else:
        form = SectionForm()
    return render(request, 'dashboard/add_form.html', {'form': form, 'title': 'Добавить раздел'})


@login_required(login_url='login')
def add_block(request):
    if request.user.username != 'admin_super' and not request.user.is_superuser:
        return redirect('index_page')
    if request.method == 'POST':
        form = BlockForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            cache.delete('index_sections_cache')  # Сбрасываем кэш при изменениях!
            return redirect('custom_dashboard')
    else:
        form = BlockForm()
    return render(request, 'dashboard/add_form.html', {'form': form, 'title': 'Добавить блок'})


# --- РЕДАКТИРОВАНИЕ (NEW) ---
@login_required(login_url='login')
def edit_block(request, pk):
    """Редактирование существующего блока"""
    if request.user.username != 'admin_super' and not request.user.is_superuser:
        return redirect('index_page')
    block = get_object_or_404(Block, pk=pk)
    if request.method == 'POST':
        form = BlockForm(request.POST, request.FILES, instance=block)
        if form.is_valid():
            form.save()
            cache.delete('index_sections_cache')  # Обновляем кэш сайта
            return redirect('custom_dashboard')
    else:
        form = BlockForm(instance=block)
    return render(request, 'dashboard/add_form.html', {'form': form, 'title': f'Редактировать блок #{block.id}'})


# --- УДАЛЕНИЕ (NEW) ---
@login_required(login_url='login')
def delete_block(request, pk):
    """Удаление блока"""
    if request.user.username != 'admin_super' and not request.user.is_superuser:
        return redirect('index_page')
    block = get_object_or_404(Block, pk=pk)
    if request.method == 'POST':  # Удаление подтверждено методом POST
        block.delete()
        cache.delete('index_sections_cache')  # Сбрасываем кэш сайта
        return redirect('custom_dashboard')
    return render(request, 'dashboard/confirm_delete.html', {'object': block, 'type': 'блока'})
