from django.urls import path

from payment import views


urlpatterns = [path("ssl_payment", views.ssl_payment, name="ssl_payment")]
