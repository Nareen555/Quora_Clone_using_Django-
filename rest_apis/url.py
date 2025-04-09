from django.urls import path
from .views import home,questions,votes,login_page,sign_page,followers,logout



urlpatterns = [
    path('log_in/',login_page),
    path('sign_up/',sign_page),
    path('log_in/home/',home,name="feed"),
    path('log_in/home/questions/',questions),
    path('log_in/home/votes/',votes),
    path('log_in/home/followers/',followers),
    path('log_in/home/logout/',logout),
    path('log_in/home/followers/update/',followers)
]



