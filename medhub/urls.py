from django.urls import path
from medhub.views import LoginApiView, PollApiView


urlpatterns = [
	path('login', LoginApiView.as_view(), name="user_login"),
	path('polls', PollApiView.as_view(), name="get_polls"),
]