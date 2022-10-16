# Django admin multi-select filter

Django admin multi-select filter is a Django app that allows you to add a multi-select filter to the Django admin.

## Installation
1. Install using pip:
    ```bash
    pip install django-admin-multi-select-filter
    ```
2. Use the `MultiSelectFilter` in your admin classes (you do **not** need to add the app to `INSTALLED_APPS`):
    ```python
    from django.contrib import admin
    from django_admin_multi_select_filter.filters import MultiSelectFieldListFilter

    class MyModelAdmin(admin.ModelAdmin):
        list_filter = (
            ...
            ('my_field', MultiSelectFieldListFilter),
            ...
        )
    ```