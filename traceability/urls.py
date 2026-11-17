from django.urls import path

from . import views

app_name = "traceability"

urlpatterns = [
    path("lotes/", views.lot_list, name="lot_list"),
    # By pk, not lot_number: real lot numbers contain "/".
    path("lotes/<int:pk>/", views.lot_detail, name="lot_detail"),
    path("carcacas/nova/", views.carcass_create, name="carcass_create"),
]
