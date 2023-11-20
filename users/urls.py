from users.apps import UsersConfig
from users.views import UsersListView, UsersDetailView, UsersUpdateView, UsersDeleteView, UsersRegistrationView
from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, )

app_name = UsersConfig.name

urlpatterns = [
    path("list/", UsersListView.as_view(), name='users_list'),
    path("view/<int:pk>/", UsersDetailView.as_view(), name='users_detail'),
    path("update/<int:pk>/", UsersUpdateView.as_view(), name='users_update'),
    path("delete/<int:pk>/", UsersDeleteView.as_view(), name='users_delete'),
    path("registration/", UsersRegistrationView.as_view(), name='users_registration'),
    path('token/', TokenObtainPairView.as_view(), name="take_token"),
    path('token/refresh/', TokenRefreshView.as_view(), name="refresh_token"),

]
