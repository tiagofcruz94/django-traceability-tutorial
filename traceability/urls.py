from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "traceability"

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="traceability:lot_list"), name="home"),
    path("lotes/", views.lot_list, name="lot_list"),
    # By pk, not lot_number: real lot numbers contain "/".
    path("lotes/<int:pk>/", views.lot_detail, name="lot_detail"),
    path("carcacas/nova/", views.carcass_create, name="carcass_create"),
]


