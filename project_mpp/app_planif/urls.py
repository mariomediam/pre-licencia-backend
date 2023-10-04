from django.urls import path
from .views import (InsertPlan_estrategicoController,
UpdatePlan_estrategicoController,
DeletePlan_estrategicoController,
SelectPlan_estrategicoController,
)

urlpatterns= [
    path("SelectPlan_estrategico/", SelectPlan_estrategicoController.as_view()),
    path("insertPlan_estrategico/", InsertPlan_estrategicoController.as_view()),
    path("updatePlan_estrategico/", UpdatePlan_estrategicoController.as_view()),
    path("DeletePlan_estrategico/", DeletePlan_estrategicoController.as_view()),
]
