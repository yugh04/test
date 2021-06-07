from django.contrib import admin
from django.urls import path,  include
import quest.views #앱이름/뷰스
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
#홈페이지
    path('', quest.views.login, name='login'),  # views urls 패턴입력
    path('main_page', quest.views.main_page, name='main_page'),  # views urls 패턴입력
    path('logout_page', quest.views.logout_page, name='logout_page'),
    path('information_main', quest.views.information_main, name='information_main'),

#수리제작의뢰서
    path('work_list_main', quest.views.work_list_main, name='work_list_main'),
    path('work_job_main', quest.views.work_job_main, name='work_job_main'),
    path('work_job_view', quest.views.work_job_view, name='work_job_view'),
    path('work_job_write', quest.views.work_job_write, name='work_job_write'),
    path('work_job_app', quest.views.work_job_app, name='work_job_app'),
    path('work_job_accept', quest.views.work_job_accept, name='work_job_accept'),
    path('work_job_reject', quest.views.work_job_reject, name='work_job_reject'),
    path('work_job_submit', quest.views.work_job_submit, name='work_job_submit'),
    path('work_job_approval', quest.views.work_job_approval, name='work_job_approval'),
    path('work_job_app_reject', quest.views.work_job_app_reject, name='work_job_app_reject'),
    path('work_job_new', quest.views.work_job_new, name='work_job_new'),
    path('work_job_room', quest.views.work_job_room, name='work_job_room'),
    path('work_job_new_submit', quest.views.work_job_new_submit, name='work_job_new_submit'),
    path('work_job_new_accept', quest.views.work_job_new_accept, name='work_job_new_accept'),
    path('work_job_new_reject', quest.views.work_job_new_reject, name='work_job_new_reject'),
    path('work_job_new_upload', quest.views.work_job_new_upload, name='work_job_new_upload'),
    path('work_job_change', quest.views.work_job_change, name='work_job_change'),
    path('work_job_change_submit', quest.views.work_job_change_submit, name='work_job_change_submit'),
    path('work_job_delete_submit', quest.views.work_job_delete_submit, name='work_job_delete_submit'),

####admin####
    path('user_info_main', quest.views.user_info_main, name='user_info_main'),
    path('user_info_new', quest.views.user_info_new, name='user_info_new'),
    path('user_info_new_submit', quest.views.user_info_new_submit, name='user_info_new_submit'),
    path('user_info_change', quest.views.user_info_change, name='user_info_change'),
    path('user_info_change_submit', quest.views.user_info_change_submit, name='user_info_change_submit'),
    path('user_info_change_delete', quest.views.user_info_change_delete, name='user_info_change_delete'),
    path('roomlist_main', quest.views.roomlist_main, name='roomlist_main'),
    path('roomlist_new', quest.views.roomlist_new, name='roomlist_new'),
    path('roomlist_new_submit', quest.views.roomlist_new_submit, name='roomlist_new_submit'),
    path('roomlist_change', quest.views.roomlist_change, name='roomlist_change'),
    path('roomlist_delete', quest.views.roomlist_delete, name='roomlist_delete'),
    path('login_again', quest.views.login_again, name='login_again'),
    path('myinfo_change', quest.views.myinfo_change, name='myinfo_change'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





