from django.urls import path

from .views import store_clean, store_group, store_one, store_xlsx

urlpatterns = [
    path("<str:store_id>", store_one),
    path("<str:store_id>/group_op", store_group),
    path("<str:store_id>/clean", store_clean),
    path("<str:store_id>/xlsx_report", store_xlsx),
]
