from django.urls import path, include
from . import views
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view()),
    path("clients/", include([
           path("", views.ClientCreate.as_view()),
           path("<int:pk>", views.ClientUpdateDestroy.as_view())
       ]
    )),
    path("mailings/", include(
        [
            path("", views.MailingCreate.as_view()),
            path("<int:pk>", views.MailingUpdateDestroy.as_view())
        ]
    )),
    path("statistics/", include(
        [
            path("general/", views.MailingGeneralStatisticsView.as_view()),
            path("detailed/<int:pk>", views.MailingDetailedStatisticsView.as_view()),
        ]
    ))
]

