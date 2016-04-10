"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from raghav import views
from threading import Thread
import datetime

urlpatterns = [
    url(r'^$',views.index,name="login"),
    url(r'^dashboard/',views.dashboard,name="dashboard"),
    url(r'^logout/',views.user_logout,name="userlogout"),
    url(r'^run/',views.run,name="run"),
    # url(r'^update/',views.check_updates,name="check_updates"),
    url(r'^emails/add/',views.add_emails,name="add_emails"),
    url(r'^emails/del/',views.del_emails,name="del_emails"),
    # url(r'^script/failed_nums.csv',views.download_output,name="download_output"),
    url(r'^script/(?P<filename>\w+)',views.download,name="download"),
    url(r'^admin/', admin.site.urls),
]


print "hello only once"


def update_background():
    update_on_time = datetime.time(2,0, 0, 0)
    while True:
        curr = datetime.datetime.time(datetime.datetime.now())
        if curr.hour == update_on_time.hour and curr.minute == update_on_time.minute and curr.second == update_on_time.second:
            views.check_updates()

thread = Thread(target=update_background)
thread.daemon = True
thread.start()
