from django.contrib import admin
from django.urls import path,  include
import quest.views #앱이름/뷰스
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
#홈페이지
    path('', quest.views.login, name='login'),  # views urls 패턴입력
    path('home', quest.views.home, name='home'), #views urls 패턴입력
    path('list/home2', quest.views.home2, name='home2'),  # views urls 패턴입력
    path('list/list', quest.views.list, name='list'),  # views urls 패턴입력
#로그인페이지
    path('adminurl/', quest.views.adminurl, name='adminurl'),  # views urls 패턴입력
    path('adminurl/plus', quest.views.plus),  # views urls 패턴입력
    path('adminurl/minus', quest.views.minus),  # views urls 패턴입력
    path('adminroom/', quest.views.adminroom, name='adminroom'),  # views urls 패턴입력
    path('adminroom/roominsert', quest.views.roominsert, name='roominsert'),  # views urls 패턴입력
    path('teammanager/', quest.views.teammanager, name='teammanager'),  # views urls 패턴입력
    path('teammanager/managerinsert', quest.views.managerinsert, name='managerinsert'),  # views urls 패턴입력
    path('adminmenu/', quest.views.adminmenu, name='adminmenu'),  # views urls 패턴입력
    path('register/', quest.views.register, name='register'),  # views urls 패턴입력
    path('register/registeok', quest.views.registeok, name='registeok'),  # views urls 패턴입력
    path('adminroom/changerm', quest.views.changerm, name='changerm'),  # views urls 패턴입력
    path('teammanager/changeteam', quest.views.changeteam, name='changeteam'),  # views urls 패턴입력
    path('changeinfo/', quest.views.changeinfo, name='changeinfo'),  # views urls 패턴입력
    path('changeinfo/changeinfocomp', quest.views.changeinfocomp, name='changeinfocomp'),  # views urls 패턴입력
    path('changeinfo/changeinfook', quest.views.changeinfook, name='changeinfook'),  # views urls 패턴입력
#리스트페이지
    path('list/', quest.views.list, name='list'),  # views urls 패턴입력
    path('list/search', quest.views.search, name='search'),  # views urls 패턴입력
    path('list/check', quest.views.check, name='check'),  # views urls 패턴입력
#신규등록
    path('list/enroll/', quest.views.enroll, name='enroll'), #신규등록
    path('list/enroll/insertok', quest.views.insertok, name='insertok'),  # insertok 클릭이랑 insertok views랑 링크하기
    path('enrollcomp/', quest.views.enrollcomp, name='enrollcomp'),  # views urls 패턴입력
    path('list/enroll/roomnamecall', quest.views.roomnamecall, name='roomnamecall'),  # views urls 패턴입력
#접수
    path('list/popup', quest.views.popup, name='popup'),  # 신규등록 팝업
    path('list/popupalarm', quest.views.popupalarm, name='popupalarm'),  # 신규등록 팝업
    path('list/accept', quest.views.accept, name='accept'), #승인
    path('list/reject', quest.views.reject, name='reject'),  #반려
    path('list/popupclose', quest.views.popupclose, name='popupclose'),
    path('list/delete', quest.views.delete, name='delete'),
    path('list/approval', quest.views.approval, name='approval'),
    path('list/teamreject', quest.views.teamreject, name='teamreject'),
    path('list/popup/update', quest.views.update, name='update'),  # 업데이트 팝업
    path('list/popup/changecomp', quest.views.changecomp, name='changecomp'),  # views urls 패턴입력
#완료
    path('list/complete', quest.views.complete, name='complete'),  # 완료
    path('list/completeapproval', quest.views.completeapproval, name='completeapproval'),
    path('list/completereject', quest.views.completereject, name='completereject'),
    path('list/completecheck', quest.views.completecheck, name='completecheck'),  # 완료
    path('list/completealarm', quest.views.completealarm, name='completealarm'),  # 완료
    path('list/completebtn', quest.views.completebtn, name='completebtn'),  #완료
#사무용품신청
    path('supply/', quest.views.supply, name='supply'),  # views urls 패턴입력
    path('listsidebar/', quest.views.listsidebar, name='listsidebar'),  # views urls 패턴입력
#미사용버튼
    path('supply/upload', quest.views.upload, name='upload'),  # views urls 패턴입력
    path('home/mysqltest', quest.views.mysqltest, name='mysqltest'),  # views urls 패턴입력
    path('home/mysqltable', quest.views.mysqltable, name='mysqltable'),  # views urls 패턴입력

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





