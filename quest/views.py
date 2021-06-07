from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from .models import worktable, room, users, manager
import datetime as date
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.db.models import Count, Sum
from django.db.models import Q, Max
import matplotlib.pyplot as plt
import re

# Create your views here.

##############################################################################################################
#################################################로그인페이지###################################################
##############################################################################################################

def login(request):
    return render(request, 'login.html') #templates 내 html연결

def logout_page(request):
    return render(request, 'logout_page.html') #templates 내 html연결

def information_main(request):
    return render(request, 'information_main.html') #templates 내 html연결

def login_again(request):
    return render(request, 'login_again.html') #templates 내 html연결

def login_password_submit(request):
    if request.method =='POST': #매소드값이 post인 값만 받는다
        loginid = request.POST.get('loginid')  # html에서 해당 값을 받는다
        now_password = request.POST.get('now_password')  # html에서 해당 값을 받는다
        new_password = request.POST.get('new_password')  # html에서 해당 값을 받는다
        new_password_again = request.POST.get('new_password_again')  # html에서 해당 값을 받는다
    ##이름 및 권한 끌고다니기##
        user = users.objects.get(userid=loginid)
        username = user.username
        userteam = user.userteam
        useremail = user.useremail
        usertel = user.usertel
        password = user.password
        auth = user.auth
        user = {"auth": auth, "password": password, "username": username, "userteam": userteam,"useremail":useremail,"usertel":usertel}
        if now_password != password:
            error_text = "기존 패스워드 입력이 잘못되었습니다."
            context={"error_text":error_text}
            return render(request, 'login_password.html',context)  # templates 내 html연결
        if new_password != new_password_again:
            error_text = "신규 패스워다가  일치하지 않습니다."
            context={"error_text":error_text}
            return render(request, 'login_password.html',context)  # templates 내 html연결
    # PASSWORD 복잡도 판단하기
        check = new_password
        if len(check) > 7:  # 8자 이상
            a = re.compile('[a-z]')  # 소문자 포함
            result_a = a.search(check)
            if result_a != None:
                b = re.compile(r'\d')  # 숫자 포함
                result_b = b.search(check)
                if result_b != None:
                    c = re.compile('[A-Z]')  # 대문자 포함
                    result_c = c.search(check)
                    if result_c != None:
                        d = re.compile('[~!@#$%^&*]')  # 특수문자자 포함
                        result_d = d.search(check)
                        if result_d != None:
                            today = date.datetime.today()
                            pass_date = "20" + today.strftime('%y') + "-" + today.strftime('%m') + "-" + today.strftime('%d')
                            user_info = users.objects.get(userid=loginid)
                            user_info.password = new_password
                            user_info.password_date = pass_date
                            user_info.fail_count = 0
                            user_info.login_lock = "Unlock"
                            user_info.save()
                            comp_signal ="Y"
                            context = {"comp_signal": comp_signal}
                            return render(request, 'login_password.html', context)  # templates 내 html연결
        error_text = "패스워드 정책에 위반됩니다."
        context = {"error_text": error_text}
        return render(request, 'login_password.html', context)  # templates 내 html연결

def myinfo_change(request):
    if request.method =='POST': #매소드값이 post인 값만 받는다
        loginid = request.POST.get('loginid')  # html에서 해당 값을 받는다
        user = users.objects.get(userid=loginid)
        username = user.username
        userteam = user.userteam
        useremail = user.useremail
        usertel = user.usertel
        password = user.password
        auth = user.auth
        user = {"auth": auth, "password": password, "username": username, "userteam": userteam,"useremail":useremail,"usertel":usertel}
        context = {"loginid": loginid}
        context.update(user)
    return render(request, 'myinfo_change.html', context) #templates 내 html연결

def main_page(request):
    if request.method =='POST': #매소드값이 post인 값만 받는다
        loginid = request.POST.get('loginid')  # html에서 해당 값을 받는다
        userpassword = request.POST.get('pw')  # html에서 해당 값을 받는다
    ##이름 및 권한 끌고다니기##
        try:
            user = users.objects.get(userid=loginid)
            username = user.username
            userteam = user.userteam
            password = user.password
            auth = user.auth
            user = {"auth":auth,"password":password,"username":username,"userteam":userteam}
        except:
            user={"loginid":loginid}
        login_infos = users.objects.filter(userid=loginid) #아이디 일치여부 확인
        login_infos = login_infos.values('userid')
        df_login_infos = pd.DataFrame.from_records(login_infos)
        login_infos_len = len(df_login_infos.index)
        if int(login_infos_len) == 1 :  ###아이디 확인
            login_info = users.objects.get(userid=loginid)  # 비밀번호 값 얻기
            if login_info.login_lock != "Lock":
                if login_info.password == userpassword: #비밀번호 일치여부
                    #####로그인실패 횟수 디폴트####
                    login_info.fail_count = 0
                    login_info.save()
            ######수리제작의뢰서 표 만들기######
                    today = date.datetime.today()
                    today_search = today.strftime('%y') + "." + today.strftime('%m') + "." + today.strftime('%d')
                    month_search = today.strftime('%y') + "." + today.strftime('%m')
                    try:
                        today_info = worktable.objects.filter(date=today_search).values('team').annotate(Count('team'))
                    except:
                        today_info = ""
                    try:
                        finish_info = worktable.objects.filter(finish_date=today_search).values('team').annotate(Count('team'))
                    except:
                        finish_info = ""
                    try:
                        t_e_1 = worktable.objects.filter(Q(status="신청", division__icontains="전기")|Q(status="신청완료", division__icontains="전기")).values('status')
                        df_t_e_1 = pd.DataFrame.from_records(t_e_1)
                        t_e_1_len = len(df_t_e_1.index)
                    except:
                        t_e_1_len = 0
                    try:
                        t_c_1 = worktable.objects.filter(Q(status="신청", division__icontains="건축")|Q(status="신청완료", division__icontains="건축")).values('status')
                        df_t_c_1 = pd.DataFrame.from_records(t_c_1)
                        t_c_1_len = len(df_t_c_1.index)
                    except:
                        t_c_1_len = 0
                    t_1_len = t_e_1_len + t_c_1_len
                    try:
                        t_e_2 = worktable.objects.filter(status="접수", division__icontains="전기").values('status')
                        df_t_e_2 = pd.DataFrame.from_records(t_e_2)
                        t_e_2_len = len(df_t_e_2.index)
                    except:
                        t_e_2_len = 0
                    try:
                        t_c_2 = worktable.objects.filter(status="접수", division__icontains="건축").values('status')
                        df_t_c_2 = pd.DataFrame.from_records(t_c_2)
                        t_c_2_len = len(df_t_c_2.index)
                    except:
                        t_c_2_len = 0
                    t_2_len = t_e_2_len + t_c_2_len
                    try:
                        t_e_3 = worktable.objects.filter(status="조치완료", division__icontains="전기").values('status')
                        df_t_e_3 = pd.DataFrame.from_records(t_e_3)
                        t_e_3_len = len(df_t_e_3.index)
                    except:
                        t_e_3_len = 0
                    try:
                        t_c_3 = worktable.objects.filter(status="조치완료", division__icontains="건축").values('status')
                        df_t_c_3 = pd.DataFrame.from_records(t_c_3)
                        t_c_3_len = len(df_t_c_3.index)
                    except:
                        t_c_3_len = 0
                    t_3_len = t_e_3_len + t_c_3_len
                    try:
                        t_e_4 = worktable.objects.filter(status="종결", division__icontains="전기").values('status')
                        df_t_e_4 = pd.DataFrame.from_records(t_e_4)
                        t_e_4_len = len(df_t_e_4.index)
                    except:
                        t_e_4_len = 0
                    try:
                        t_c_4 = worktable.objects.filter(status="종결", division__icontains="건축").values('status')
                        df_t_c_4 = pd.DataFrame.from_records(t_c_4)
                        t_c_4_len = len(df_t_c_4.index)
                    except:
                        t_c_4_len = 0
                    t_4_len = t_e_4_len + t_c_4_len
                    try:
                        t_e_6 = worktable.objects.filter(status="반려", division__icontains="전기").values('status')
                        df_t_e_6 = pd.DataFrame.from_records(t_e_6)
                        t_e_6_len = len(df_t_e_6.index)
                    except:
                        t_e_6_len = 0
                    try:
                        t_c_6 = worktable.objects.filter(status="반려", division__icontains="건축").values('status')
                        df_t_c_6 = pd.DataFrame.from_records(t_c_6)
                        t_c_6_len = len(df_t_c_6.index)
                    except:
                        t_c_6_len = 0
                    t_6_len = t_e_6_len + t_c_6_len
                    t_5_len = t_1_len + t_2_len + + t_3_len + t_4_len + t_6_len
                    t_c_5_len = t_c_1_len + t_c_2_len + + t_c_3_len + t_c_4_len + t_c_6_len
                    t_e_5_len = t_e_1_len + t_e_2_len + + t_e_3_len + t_e_4_len + t_e_6_len
                    if (auth == "Engineer") or (auth == "Eng. Manager") or (auth == "Eng. Supervisor"):
                        today_table = worktable.objects.filter(date=today_search).order_by('team')
                    else:
                        today_table = worktable.objects.filter(date=today_search, team=userteam).order_by('team')
        ######마이페이지 표 만들기######
                    wr_team_m = worktable.objects.filter(status="신청", team=userteam).values('status')
                    df_wr_team_m = pd.DataFrame.from_records(wr_team_m)
                    wr_team_m_len = len(df_wr_team_m.index)
                    staff_info = worktable.objects.filter(rep=username).values('status').annotate(Count('status')).order_by('status')
                    wr_so_m = worktable.objects.filter(status="조치완료").values('status')
                    df_wr_so_m = pd.DataFrame.from_records(wr_so_m)
                    wr_so_m_len = len(df_wr_so_m.index)
                    wr_eng = worktable.objects.filter(status="신청완료").values('status')
                    df_wr_eng = pd.DataFrame.from_records(wr_eng)
                    wr_eng_len = len(df_wr_eng.index)
        ######수리제작 표만들기####
                    try:
                        plt.figure(2)
                        plt.clf()
                        today = date.datetime.today()
                        this_year = today.strftime('%y')  # 올해 년도 구하기
                        month = [this_year + ".01", this_year + ".02", this_year + ".03", this_year + ".04", this_year + ".05",
                                 this_year + ".06",
                                 this_year + ".07", this_year + ".08", this_year + ".09", this_year + ".10", this_year + ".11",
                                 this_year + ".12"]
                        j = 0
                        total_bm = []
                        while j < 12:
                            date_team = month[j]
                            count = worktable.objects.filter(date__icontains=date_team)
                            count = count.values('team')
                            df_count = pd.DataFrame.from_records(count)
                            count_len = len(df_count.index)
                            total_bm.append(count_len)
                            j = j + 1
                        p20 = plt.bar(['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May.', 'Jun.', 'Jul.', 'Aug.', 'Sept.', 'Oct.', 'Nov.',
                                       'Dec.'],
                                      total_bm, color='coral', width=0.5, label='Request')
                        i = 0
                        comp_bm = []
                        while i < 12:
                            date_team = month[i]
                            count = worktable.objects.filter(finish_date__icontains=date_team, status='종결')
                            count = count.values('team')
                            df_count = pd.DataFrame.from_records(count)
                            count_len = len(df_count.index)
                            comp_bm.append(count_len)
                            i = i + 1
                        p21 = plt.plot(['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May.', 'Jun.', 'Jul.', 'Aug.', 'Sept.', 'Oct.', 'Nov.',
                                        'Dec.'],
                                       comp_bm, color='dodgerblue', marker='o', label='Complete')
                        plt.xlabel('[Date]')
                        plt.ylabel('[Count]')
                        plt.legend((p20[0], p21[0]), ('Request', 'Complete'))
                        plt.savefig('./static/bm_chart.png')
                    except:
                        pass
                    not_comp = worktable.objects.filter(Q(engrep__icontains=username) & ~Q(status='종결') &~Q(status='조치완료'))
                    not_comp = not_comp.values('team')
                    df_not_comp = pd.DataFrame.from_records(not_comp)
                    not_comp_len = len(df_not_comp.index)
        ######기본정보 보내기######
                    context = {"loginid": loginid,"today_info":today_info,"finish_info":finish_info,"today_table":today_table
                               ,"t_1_len":t_1_len,"t_2_len":t_2_len,"t_3_len":t_3_len,"t_4_len":t_4_len,"t_5_len":t_5_len
                               , "t_e_1_len": t_e_1_len, "t_e_2_len": t_e_2_len, "t_e_3_len": t_e_3_len, "t_e_4_len": t_e_4_len, "t_e_5_len": t_e_5_len
                               , "t_c_1_len":t_c_1_len, "t_c_2_len": t_c_2_len, "t_c_3_len": t_c_3_len, "t_c_4_len": t_c_4_len, "t_c_5_len": t_c_5_len
                                , "t_6_len": t_6_len, "t_c_6_len": t_c_6_len, "t_e_6_len": t_e_6_len,"wr_team_m_len":wr_team_m_len
                               ,"staff_info":staff_info,"wr_so_m_len":wr_so_m_len,"wr_eng_len":wr_eng_len,"not_comp_len":not_comp_len}
                    context.update(user)
                    return render(request, 'main_page.html', context)  # templates 내 html연결
                else:
                    password_fail = users.objects.get(userid=loginid)  # 아이디 일치여부 확인
                    password_fail.fail_count = int(password_fail.fail_count) + 1
                    password_fail.save()
                    login_error_text = "패스워드가 일치하지 않습니다. (" + str(password_fail.fail_count) + "times)"
                    messages.error(request, login_error_text)  # 경고
                    ###비밀번호 5회이상 틀리면 락킹###
                    if password_fail.fail_count == 5:
                        password_fail.login_lock = "Lock"
                        password_fail.save()
                    return render(request, 'login.html')  # templates 내 html연결
            else:
                messages.error(request, "패스워드 오류가 5회이상 발생하여 로그인이 불가합니다.")  # 경고
                return render(request, 'login.html')  # templates 내 html연결
        else:
            messages.error(request, "입력하신 아이디가 존재하지 않습니다.")  # 경고
            return render(request, 'login.html')  # templates 내 html연결

def work_list_main(request):
    if request.method =='POST': #매소드값이 post인 값만 받는다
        loginid = request.POST.get('loginid')  # html에서 해당 값을 받는다
        selecttext = request.POST.get('selecttext')  # html에서 해당 값을 받는다
        searchtext = request.POST.get('searchtext')  # html에서 해당 값을 받는다
        user = users.objects.get(userid=loginid)
        username = user.username
        userteam = user.userteam
        password = user.password
        auth = user.auth
        user = {"auth": auth, "password": password, "username": username, "userteam": userteam}
        if (auth == "Engineer") or (auth == "Eng. Manager") or (auth == "Eng. Supervisor"):
            if selecttext == "team":
                worklist = worktable.objects.filter(team__icontains=searchtext).order_by('team', '-job')
            elif selecttext == "division":
                worklist = worktable.objects.filter(division__icontains=searchtext).order_by('team', '-job')
            elif selecttext == "status":
                worklist = worktable.objects.filter(status__icontains=searchtext).order_by('team', '-job')
            elif selecttext == "engrep":
                worklist = worktable.objects.filter(engrep__icontains=searchtext).order_by('team', '-job')
            else:
                worklist = worktable.objects.all().order_by('team', '-job')
        else:
            if selecttext == "team":
                worklist = worktable.objects.filter(team__icontains=searchtext, team=userteam).order_by('team', '-job')
            elif selecttext == "division":
                worklist = worktable.objects.filter(division__icontains=searchtext, team=userteam).order_by('team', '-job')
            elif selecttext == "status":
                worklist = worktable.objects.filter(status__icontains=searchtext, team=userteam).order_by('team', '-job')
            elif selecttext == "engrep":
                worklist = worktable.objects.filter(engrep__icontains=searchtext, team=userteam).order_by('team', '-job')
            else:
                worklist = worktable.objects.filter(team=userteam).order_by('team', '-job')
        context = {"loginid": loginid, "worklist": worklist,"selecttext":selecttext,"searchtext":searchtext}
        context.update(user)
        return render(request, 'work_list_main.html', context)  # templates 내 html연결

def work_job_main(request):
    if request.method =='POST': #매소드값이 post인 값만 받는다
        loginid = request.POST.get('loginid')  # html에서 해당 값을 받는다
        user = users.objects.get(userid=loginid)
        username = user.username
        userteam = user.userteam
        password = user.password
        auth = user.auth
        user = {"auth": auth, "password": password, "username": username, "userteam": userteam}
        ####기본정보 보내기####
        signal = request.POST.get('signal')  # html에서 해당 값을 받는다
        if auth == "Engineer": ###엔지니어
            if signal == "yes":
                worklist = worktable.objects.filter(status="신청완료").order_by('status', '-job')
            else:
                worklist = worktable.objects.filter(Q(status="신청완료") | Q(status="접수")).order_by('status','team')
        elif (auth == "Eng. Manager") or (auth == "Eng. Supervisor"): ###엔지니어 팀장 슈퍼바이져
            worklist = worktable.objects.filter(status="조치완료").order_by('team', '-job')
        elif auth == "Team Manager": #### 일반 팀장
            if signal == "yes":
                worklist = worktable.objects.filter(team=userteam, status="신청").order_by('status', '-job')
            else:
                worklist = worktable.objects.filter(Q(team=userteam)&~Q(status="종결") & ~Q(status="반려")).order_by('status', '-job')
        else: ####팀원
            worklist = worktable.objects.filter(Q(rep=username)&~Q(status="종결")&~Q(status="반려")).order_by('status', '-job')
        context = {"loginid": loginid, "worklist": worklist,"signal":signal}
        context.update(user)
        return render(request, 'work_job_main.html', context)  # templates 내 html연결

def work_job_write(request):
    if request.method =='POST': #매소드값이 post인 값만 받는다
        loginid = request.POST.get('loginid')  # html에서 해당 값을 받는다
        jobno = request.POST.get('jobno')  # html에서 해당 값을 받는다
        user = users.objects.get(userid=loginid)
        username = user.username
        userteam = user.userteam
        password = user.password
        auth = user.auth
        user = {"auth": auth, "password": password, "username": username, "userteam": userteam}
        ####기본정보 보내기####
        signal = request.POST.get('signal')  # html에서 해당 값을 받는다
        if auth == "Engineer": ###엔지니어
            if signal == "yes":
                worklist = worktable.objects.filter(status="신청완료").order_by('status', '-job')
            else:
                worklist = worktable.objects.filter(Q(status="신청완료") | Q(status="접수")).order_by('status','team')
        elif (auth == "Eng. Manager") or (auth == "Eng. Supervisor"): ###엔지니어 팀장 슈퍼바이져
            worklist = worktable.objects.filter(status="조치완료").order_by('team', '-job')
        elif auth == "Team Manager": #### 일반 팀장
            if signal == "yes":
                worklist = worktable.objects.filter(team=userteam, status="신청").order_by('status', '-job')
            else:
                worklist = worktable.objects.filter(Q(team=userteam)&~Q(status="종결") & ~Q(status="반려")).order_by('status', '-job')
        else: ####팀원
            worklist = worktable.objects.filter(Q(rep=username)&~Q(status="종결")&~Q(status="반려")).order_by('status', '-job')
        signal_check = worktable.objects.get(job=jobno)
        if (signal_check.status == "신청완료") or (signal_check.status == "신청"):
            table_signal = "accept"
        else:
            table_signal = "write"
        if signal_check.attached_tag == "View":
            attach_view = "N"
        else:
            attach_view = "Y"
        telno = users.objects.get(userid=signal_check.userid)
        tel_no = telno.usertel
        view_table = worktable.objects.filter(job=jobno)
        context = {"loginid": loginid, "worklist": worklist,"table_signal":table_signal,"view_table":view_table,
                   "attach_view":attach_view,"signal":signal,"tel_no":tel_no}
        context.update(user)
        return render(request, 'work_job_main.html', context)  # templates 내 html연결

def work_job_view(request):
    if request.method =='POST': #매소드값이 post인 값만 받는다
        loginid = request.POST.get('loginid')  # html에서 해당 값을 받는다
        jobno = request.POST.get('jobno')  # html에서 해당 값을 받는다
        user = users.objects.get(userid=loginid)
        username = user.username
        userteam = user.userteam
        password = user.password
        auth = user.auth
        user = {"auth": auth, "password": password, "username": username, "userteam": userteam}
        ####기본정보 보내기####
        signal = request.POST.get('signal')  # html에서 해당 값을 받는다
        if auth == "Engineer": ###엔지니어
            if signal == "yes":
                worklist = worktable.objects.filter(status="신청완료").order_by('status', '-job')
            else:
                worklist = worktable.objects.filter(Q(status="신청완료") | Q(status="접수")).order_by('status','team')
        elif (auth == "Eng. Manager") or (auth == "Eng. Supervisor"): ###엔지니어 팀장 슈퍼바이져
            worklist = worktable.objects.filter(status="조치완료").order_by('team', '-job')
        elif auth == "Team Manager": #### 일반 팀장
            if signal == "yes":
                worklist = worktable.objects.filter(team=userteam, status="신청").order_by('status', '-job')
            else:
                worklist = worktable.objects.filter(Q(team=userteam)&~Q(status="종결") & ~Q(status="반려")).order_by('status', '-job')
        else: ####팀원
            worklist = worktable.objects.filter(Q(rep=username)&~Q(status="종결")&~Q(status="반려")).order_by('status', '-job')
        table_signal = "view"
        view_table = worktable.objects.filter(job=jobno)
        btn_check = worktable.objects.get(job=jobno)
        if (btn_check.rep == username) and (btn_check.status == "신청"):
            btn_view="Y"
        else:
            btn_view = "N"
        if btn_check.status == "신청":
            btn_view_2 = "Y"
        else:
            btn_view_2 = "N"
        if btn_check.attached_tag == "View":
            attach_view = "N"
        else:
            attach_view = "Y"
        context = {"loginid": loginid, "worklist": worklist,"table_signal":table_signal,"view_table":view_table,"btn_view":btn_view,
                   "btn_view_2":btn_view_2,"attach_view":attach_view,"signal":signal}
        context.update(user)
        return render(request, 'work_job_main.html', context)  # templates 내 html연결

def work_job_app(request):
    if request.method =='POST': #매소드값이 post인 값만 받는다
        loginid = request.POST.get('loginid')  # html에서 해당 값을 받는다
        jobno = request.POST.get('jobno')  # html에서 해당 값을 받는다
        user = users.objects.get(userid=loginid)
        username = user.username
        userteam = user.userteam
        password = user.password
        auth = user.auth
        user = {"auth": auth, "password": password, "username": username, "userteam": userteam}
        ####기본정보 보내기####
        signal = request.POST.get('signal')  # html에서 해당 값을 받는다
        if auth == "Engineer": ###엔지니어
            if signal == "yes":
                worklist = worktable.objects.filter(status="신청완료").order_by('status', '-job')
            else:
                worklist = worktable.objects.filter(Q(status="신청완료") | Q(status="접수")).order_by('status','team')
        elif (auth == "Eng. Manager") or (auth == "Eng. Supervisor"): ###엔지니어 팀장 슈퍼바이져
            worklist = worktable.objects.filter(status="조치완료").order_by('team', '-job')
        elif auth == "Team Manager": #### 일반 팀장
            if signal == "yes":
                worklist = worktable.objects.filter(team=userteam, status="신청").order_by('status', '-job')
            else:
                worklist = worktable.objects.filter(Q(team=userteam)&~Q(status="종결") & ~Q(status="반려")).order_by('status', '-job')
        else: ####팀원
            worklist = worktable.objects.filter(Q(rep=username)&~Q(status="종결")&~Q(status="반려")).order_by('status', '-job')
        table_signal = "approval"
        signal_check = worktable.objects.get(job=jobno)
        if signal_check.attached_tag == "View":
            attach_view = "N"
        else:
            attach_view = "Y"
        view_table = worktable.objects.filter(job=jobno)
        context = {"loginid": loginid, "worklist": worklist,"table_signal":table_signal,"view_table":view_table,
                   "signal":signal,"attach_view":attach_view}
        context.update(user)
        return render(request, 'work_job_main.html', context)  # templates 내 html연결

def work_job_accept(request):
    if request.method =='POST': #매소드값이 post인 값만 받는다
        loginid = request.POST.get('loginid')  # html에서 해당 값을 받는다
        jobno = request.POST.get('jobno')  # html에서 해당 값을 받는다
        user = users.objects.get(userid=loginid)
        username = user.username
        userteam = user.userteam
        password = user.password
        auth = user.auth
        user = {"auth": auth, "password": password, "username": username, "userteam": userteam}
    ####값저장하기####
        today = date.datetime.today()
        today_date = today.strftime('%y')+"."+today.strftime('%m')+"."+today.strftime('%d')
        save_data = worktable.objects.get(job=jobno)
        save_data.engrep = username
        save_data.get_date = today_date
        save_data.status = "접수"
        save_data.save()
    ###신청자에게 메일보내기###
        title_text = "(자동메일)수리제작의뢰서 접수의 건 [Job No.: " + save_data.job + "]"
        email_text = "Job No: " + save_data.job + "가 접수되었습니다." + \
                     "\n\nJob No: " + save_data.job + \
                     "\n팀: " + save_data.team + \
                     "\n요청자: " + save_data.rep + \
                     "\n요청일자: " + save_data.date + \
                     "\nRoom Name (Room No.): " + save_data.roomname + " (" + save_data.roomno + ")" \
                     "\n구분: " + save_data.division + \
                     "\n요청내용: " + save_data.description + \
                     "\n고장사유: " + save_data.reason + \
                     "\n담당자: " + save_data.engrep + \
                     "\n접수일자: " + save_data.get_date + \
                     "\n\n ※ 상기 메일 자동발신 메일이며 회신은 불가합니다." + \
                     "\n ※ Link: http://dmbio.synology.me:803"
    ##신청자 메일주소 불러오기##
        manager_get = users.objects.filter(userid=save_data.userid)
        manager_get = manager_get.values('no')
        df_manager_get = pd.DataFrame.from_records(manager_get)
        manager_get_len = len(df_manager_get.index)
        for i in range(manager_get_len):
            no_get = df_manager_get.iat[i, 0]
            try:
                email_get = users.objects.get(no=no_get)
                email_add = [email_get.useremail]
                email = EmailMessage(title_text, email_text, to=email_add)
                email.send()
            except:
                pass
    ####기본정보 보내기####
        signal = request.POST.get('signal')  # html에서 해당 값을 받는다
        if auth == "Engineer": ###엔지니어
            if signal == "yes":
                worklist = worktable.objects.filter(status="신청완료").order_by('status', '-job')
            else:
                worklist = worktable.objects.filter(Q(status="신청완료") | Q(status="접수")).order_by('status','team')
        elif (auth == "Eng. Manager") or (auth == "Eng. Supervisor"): ###엔지니어 팀장 슈퍼바이져
            worklist = worktable.objects.filter(status="조치완료").order_by('team', '-job')
        elif auth == "Team Manager": #### 일반 팀장
            if signal == "yes":
                worklist = worktable.objects.filter(team=userteam, status="신청").order_by('status', '-job')
            else:
                worklist = worktable.objects.filter(Q(team=userteam)&~Q(status="종결") & ~Q(status="반려")).order_by('status', '-job')
        else: ####팀원
            worklist = worktable.objects.filter(Q(rep=username)&~Q(status="종결")&~Q(status="반려")).order_by('status', '-job')
        table_signal = "accept"
        table_signal_div = "Job No.: " + save_data.job + "가 접수되었습니다."
        msg_signal = "Y"
        view_table = worktable.objects.filter(job=jobno)
        context = {"loginid": loginid, "worklist": worklist,"table_signal":table_signal,"view_table":view_table,
                   "table_signal_div":table_signal_div,"msg_signal":msg_signal,"signal":signal}
        context.update(user)
        return render(request, 'work_job_main.html', context)  # templates 내 html연결

def work_job_reject(request):
    if request.method =='POST': #매소드값이 post인 값만 받는다
        loginid = request.POST.get('loginid')  # html에서 해당 값을 받는다
        jobno = request.POST.get('jobno')  # html에서 해당 값을 받는다
        reject_reason = request.POST.get('reject_reason')  # html에서 해당 값을 받는다
        user = users.objects.get(userid=loginid)
        username = user.username
        userteam = user.userteam
        password = user.password
        auth = user.auth
        user = {"auth": auth, "password": password, "username": username, "userteam": userteam}
    ####값저장하기####
        today = date.datetime.today()
        today_date = today.strftime('%y')+"."+today.strftime('%m')+"."+today.strftime('%d')
        save_data = worktable.objects.get(job=jobno)
        save_data.engrep = username
        save_data.summary = "[반려사유] " + reject_reason
        save_data.status = "반려"
        save_data.save()
    ###신청자에게 메일보내기###
        title_text = "(자동메일)수리제작의뢰서 반려의 건 [Job No.: " + save_data.job + "]"
        email_text = "Job No: " + save_data.job + "가 반려되었습니다." + \
                     "\n\nJob No: " + save_data.job + \
                     "\n팀: " + save_data.team + \
                     "\n요청자: " + save_data.rep + \
                     "\n요청일자: " + save_data.date + \
                     "\nRoom Name (Room No.): " + save_data.roomname + " (" + save_data.roomno + ")" \
                     "\n구분: " + save_data.division + \
                     "\n요청내용: " + save_data.description + \
                     "\n반려사유: " + reject_reason + \
                     "\n담당자: " + save_data.engrep + \
                     "\n\n ※ 상기 메일 자동발신 메일이며 회신은 불가합니다." + \
                     "\n ※ Link: http://dmbio.synology.me:803"
    ##신청자 메일주소 불러오기##
        manager_get = users.objects.filter(userid=save_data.userid)
        manager_get = manager_get.values('no')
        df_manager_get = pd.DataFrame.from_records(manager_get)
        manager_get_len = len(df_manager_get.index)
        for i in range(manager_get_len):
            no_get = df_manager_get.iat[i, 0]
            try:
                email_get = users.objects.get(no=no_get)
                email_add = [email_get.useremail]
                email = EmailMessage(title_text, email_text, to=email_add)
                email.send()
            except:
                pass
    ####기본정보 보내기####
        signal = request.POST.get('signal')  # html에서 해당 값을 받는다
        if auth == "Engineer": ###엔지니어
            if signal == "yes":
                worklist = worktable.objects.filter(status="신청완료").order_by('status', '-job')
            else:
                worklist = worktable.objects.filter(Q(status="신청완료") | Q(status="접수")).order_by('status','team')
        elif (auth == "Eng. Manager") or (auth == "Eng. Supervisor"): ###엔지니어 팀장 슈퍼바이져
            worklist = worktable.objects.filter(status="조치완료").order_by('team', '-job')
        elif auth == "Team Manager": #### 일반 팀장
            if signal == "yes":
                worklist = worktable.objects.filter(team=userteam, status="신청").order_by('status', '-job')
            else:
                worklist = worktable.objects.filter(Q(team=userteam)&~Q(status="종결") & ~Q(status="반려")).order_by('status', '-job')
        else: ####팀원
            worklist = worktable.objects.filter(Q(rep=username)&~Q(status="종결")&~Q(status="반려")).order_by('status', '-job')
        table_signal = "accept"
        table_signal_div = "Job No.: " + save_data.job + "가 반려되었습니다."
        msg_signal = "Y"
        view_table = worktable.objects.filter(job=jobno)
        context = {"loginid": loginid, "worklist": worklist, "table_signal": table_signal, "view_table": view_table,
                   "table_signal_div": table_signal_div,"msg_signal":msg_signal,"signal":signal}
        context.update(user)
        return render(request, 'work_job_main.html', context)  # templates 내 html연결

def work_job_submit(request):
    if request.method =='POST': #매소드값이 post인 값만 받는다
        loginid = request.POST.get('loginid')  # html에서 해당 값을 받는다
        jobno = request.POST.get('jobno')  # html에서 해당 값을 받는다
        summary = request.POST.get('summary')  # html에서 해당 값을 받는다
        user = users.objects.get(userid=loginid)
        username = user.username
        userteam = user.userteam
        password = user.password
        auth = user.auth
        user = {"auth": auth, "password": password, "username": username, "userteam": userteam}
    ####값저장하기####
        today = date.datetime.today()
        today_date = today.strftime('%y')+"."+today.strftime('%m')+"."+today.strftime('%d')
        save_data = worktable.objects.get(job=jobno)
        save_data.summary = summary
        save_data.finish_date = today_date
        save_data.status = "조치완료"
        save_data.save()
    ###엔지니어에게 메일보내기###
        title_text = "(자동메일)수리제작의뢰서 조치완료의 건 [Job No.: " + save_data.job + "]"
        email_text = "Job No: " + save_data.job + "가 조치가 완료되었습니다." + \
                     "\n\nJob No: " + save_data.job + \
                     "\n팀: " + save_data.team + \
                     "\n요청자: " + save_data.rep + \
                     "\n요청일자: " + save_data.date + \
                     "\nRoom Name (Room No.): " + save_data.roomname + " (" + save_data.roomno + ")" \
                     "\n구분: " + save_data.division + \
                     "\n요청내용: " + save_data.description + \
                     "\n고장사유: " + save_data.reason + \
                     "\n담당자: " + save_data.engrep + \
                     "\n접수일자: " + save_data.get_date + \
                     "\n조치내용: " + save_data.summary + \
                     "\n조치완료일: " + save_data.finish_date + \
                     "\n\n ※ 상기 메일 자동발신 메일이며 회신은 불가합니다."+ \
                     "\n ※ Link: http://dmbio.synology.me:803"
    ##전체 메일주소 불러오기##
        manager_get = users.objects.filter(Q(userteam=userteam, auth__icontains="Manager")|Q(auth="Eng. Manager")|Q(userid=save_data.userid))
        manager_get = manager_get.values('no')
        df_manager_get = pd.DataFrame.from_records(manager_get)
        manager_get_len = len(df_manager_get.index)
        for i in range(manager_get_len):
            no_get = df_manager_get.iat[i, 0]
            try:
                email_get = users.objects.get(no=no_get)
                email_add = [email_get.useremail]
                email = EmailMessage(title_text, email_text, to=email_add)
                email.send()
            except:
                pass
    ####기본정보 보내기####
        signal = request.POST.get('signal')  # html에서 해당 값을 받는다
        if auth == "Engineer": ###엔지니어
            if signal == "yes":
                worklist = worktable.objects.filter(status="신청완료").order_by('status', '-job')
            else:
                worklist = worktable.objects.filter(Q(status="신청완료") | Q(status="접수")).order_by('status','team')
        elif (auth == "Eng. Manager") or (auth == "Eng. Supervisor"): ###엔지니어 팀장 슈퍼바이져
            worklist = worktable.objects.filter(status="조치완료").order_by('team', '-job')
        elif auth == "Team Manager": #### 일반 팀장
            if signal == "yes":
                worklist = worktable.objects.filter(team=userteam, status="신청").order_by('status', '-job')
            else:
                worklist = worktable.objects.filter(Q(team=userteam)&~Q(status="종결") & ~Q(status="반려")).order_by('status', '-job')
        else: ####팀원
            worklist = worktable.objects.filter(Q(rep=username)&~Q(status="종결")&~Q(status="반려")).order_by('status', '-job')
        table_signal = "write"
        table_signal_div = save_data.job + "가 조치완료 되었습니다."
        msg_signal = "Y"
        view_table = worktable.objects.filter(job=jobno)
        context = {"loginid": loginid, "worklist": worklist,"table_signal":table_signal,"view_table":view_table,
                   "table_signal_div":table_signal_div,"summary":summary,"msg_signal":msg_signal,"signal":signal}
        context.update(user)
        return render(request, 'work_job_main.html', context)  # templates 내 html연결

def work_job_approval(request):
    if request.method =='POST': #매소드값이 post인 값만 받는다
        loginid = request.POST.get('loginid')  # html에서 해당 값을 받는다
        jobno = request.POST.get('jobno')  # html에서 해당 값을 받는다
        user = users.objects.get(userid=loginid)
        username = user.username
        userteam = user.userteam
        password = user.password
        auth = user.auth
        user = {"auth": auth, "password": password, "username": username, "userteam": userteam}
    ####값저장하기####
        today = date.datetime.today()
        today_date = today.strftime('%y')+"."+today.strftime('%m')+"."+today.strftime('%d')
        save_data = worktable.objects.get(job=jobno)
        save_data.check = username +" / " + today_date
        save_data.status = "종결"
        save_data.save()
    ####기본정보 보내기####
        signal = request.POST.get('signal')  # html에서 해당 값을 받는다
        if auth == "Engineer": ###엔지니어
            if signal == "yes":
                worklist = worktable.objects.filter(status="신청완료").order_by('status', '-job')
            else:
                worklist = worktable.objects.filter(Q(status="신청완료") | Q(status="접수")).order_by('status','team')
        elif (auth == "Eng. Manager") or (auth == "Eng. Supervisor"): ###엔지니어 팀장 슈퍼바이져
            worklist = worktable.objects.filter(status="조치완료").order_by('team', '-job')
        elif auth == "Team Manager": #### 일반 팀장
            if signal == "yes":
                worklist = worktable.objects.filter(team=userteam, status="신청").order_by('status', '-job')
            else:
                worklist = worktable.objects.filter(Q(team=userteam)&~Q(status="종결") & ~Q(status="반려")).order_by('status', '-job')
        else: ####팀원
            worklist = worktable.objects.filter(Q(rep=username)&~Q(status="종결")&~Q(status="반려")).order_by('status', '-job')
        table_signal = ""
        view_table = worktable.objects.filter(job=jobno)
        context = {"loginid": loginid, "worklist": worklist,"table_signal":table_signal,"view_table":view_table,"signal":signal}
        context.update(user)
        return render(request, 'work_job_main.html', context)  # templates 내 html연결

def work_job_app_reject(request):
    if request.method =='POST': #매소드값이 post인 값만 받는다
        loginid = request.POST.get('loginid')  # html에서 해당 값을 받는다
        jobno = request.POST.get('jobno')  # html에서 해당 값을 받는다
        user = users.objects.get(userid=loginid)
        username = user.username
        userteam = user.userteam
        password = user.password
        auth = user.auth
        user = {"auth": auth, "password": password, "username": username, "userteam": userteam}
    ####값저장하기####
        save_data = worktable.objects.get(job=jobno)
        save_data.finish_date = ""
        save_data.status = "접수"
        save_data.save()
        ####기본정보 보내기####
        signal = request.POST.get('signal')  # html에서 해당 값을 받는다
        if auth == "Engineer": ###엔지니어
            if signal == "yes":
                worklist = worktable.objects.filter(status="신청완료").order_by('status', '-job')
            else:
                worklist = worktable.objects.filter(Q(status="신청완료") | Q(status="접수")).order_by('status','team')
        elif (auth == "Eng. Manager") or (auth == "Eng. Supervisor"): ###엔지니어 팀장 슈퍼바이져
            worklist = worktable.objects.filter(status="조치완료").order_by('team', '-job')
        elif auth == "Team Manager": #### 일반 팀장
            if signal == "yes":
                worklist = worktable.objects.filter(team=userteam, status="신청").order_by('status', '-job')
            else:
                worklist = worktable.objects.filter(Q(team=userteam)&~Q(status="종결") & ~Q(status="반려")).order_by('status', '-job')
        else: ####팀원
            worklist = worktable.objects.filter(Q(rep=username)&~Q(status="종결")&~Q(status="반려")).order_by('status', '-job')
        table_signal = ""
        view_table = worktable.objects.filter(job=jobno)
        context = {"loginid": loginid, "worklist": worklist,"table_signal":table_signal,"view_table":view_table,"signal":signal}
        context.update(user)
        return render(request, 'work_job_main.html', context)  # templates 내 html연결

def work_job_new(request):
    return render(request, 'work_job_new.html')  # templates 내 html연결

def work_job_change(request):
    return render(request, 'work_job_change.html')  # templates 내 html연결

def work_job_change_submit(request):
    if request.method == 'POST':  # 매소드값이 post인 값만 받는다
        roomno = request.POST.get('roomno')  # html newname의 값을 받는다.
        roomname = request.POST.get('roomname')  # html newname의 값을 받는다.
        job = request.POST.get('job')  # html newname의 값을 받는다.
        description = request.POST.get('description')  # html newname의 값을 받는다.
        loginid = request.POST.get('loginid')  # html newname의 값을 받는다.
        reason = request.POST.get('reason')  # html newname의 값을 받는다.
        user = users.objects.get(userid=loginid)
        username = user.username
        userteam = user.userteam
        password = user.password
        auth = user.auth
        user = {"auth": auth, "password": password, "username": username, "userteam": userteam}
    ###값변경하기
        value_change = worktable.objects.get(job=job)
        value_change.roomno = roomno
        value_change.roomname = roomname
        value_change.description = description
        value_change.reason = reason
        value_change.save()
    ###완료신호주기
        comp_signal ="Y"
        context={"comp_signal":comp_signal,"loginid":loginid}
        context.update(user)
        return render(request, 'work_job_change.html', context)  # templates 내 html연결

def work_job_delete_submit(request):
    if request.method == 'POST':  # 매소드값이 post인 값만 받는다
        job = request.POST.get('job_up')  # html newname의 값을 받는다.
        loginid = request.POST.get('loginid')  # html newname의 값을 받는다.
        user = users.objects.get(userid=loginid)
        username = user.username
        userteam = user.userteam
        password = user.password
        auth = user.auth
        user = {"auth": auth, "password": password, "username": username, "userteam": userteam}
    ###값변경하기
        value_change = worktable.objects.get(job=job)
        value_change.delete()
    ####기본정보 보내기####
        signal = request.POST.get('signal')  # html에서 해당 값을 받는다
        if auth == "Engineer":  ###엔지니어
            if signal == "yes":
                worklist = worktable.objects.filter(status="신청완료").order_by('status', '-job')
            else:
                worklist = worktable.objects.filter(Q(status="신청완료") | Q(status="접수")).order_by('status', 'team')
        elif (auth == "Eng. Manager") or (auth == "Eng. Supervisor"):  ###엔지니어 팀장 슈퍼바이져
            worklist = worktable.objects.filter(status="조치완료").order_by('team', '-job')
        elif auth == "Team Manager":  #### 일반 팀장
            if signal == "yes":
                worklist = worktable.objects.filter(team=userteam, status="신청").order_by('status', '-job')
            else:
                worklist = worktable.objects.filter(Q(team=userteam) & ~Q(status="종결") & ~Q(status="반려")).order_by(
                    'status', '-job')
        else:  ####팀원
            worklist = worktable.objects.filter(Q(rep=username) & ~Q(status="종결") & ~Q(status="반려")).order_by('status',
                                                                                                              '-job')
    ###완료신호주기
        delete_signal ="Y"
        context={"delete_signal":delete_signal,"loginid":loginid, "worklist": worklist, "signal": signal}
        context.update(user)
        return render(request, 'work_job_main.html', context)  # templates 내 html연결

def work_job_room(request):
    if request.method == 'POST':  # 매소드값이 post인 값만 받는다
        division = request.POST.get('division_give')  # html newname의 값을 받는다.
        roomno = request.POST.get('roomno_give')  # html newname의 값을 받는다.
        description = request.POST.get('description_give')  # html newname의 값을 받는다.
        loginid = request.POST.get('loginid')  # html newname의 값을 받는다.
        url = request.POST.get('url')  # html newname의 값을 받는다.
        reason = request.POST.get('reason_give')  # html newname의 값을 받는다.
        user = users.objects.get(userid=loginid)
        username = user.username
        userteam = user.userteam
        password = user.password
        auth = user.auth
        user = {"auth": auth, "password": password, "username": username, "userteam": userteam}
    ###ROOM No. 값 받기
        try:
            room_get = room.objects.get(roomno=roomno)
            roomname = room_get.roomname
            text_signal = "N"
        except:
            text_signal="Y"
            roomname=""
    ###선택 값 반환받기
        if division == "전기-콘센트":
            radio_1 = "checked"
            radio_2 = ""
            radio_3 = ""
            radio_4 = ""
            radio_5 = ""
            radio_6 = ""
            radio_7 = ""
        elif division == "전기-형광등":
            radio_1 = ""
            radio_2 = "checked"
            radio_3 = ""
            radio_4 = ""
            radio_5 = ""
            radio_6 = ""
            radio_7 = ""
        elif division == "전기-기타":
            radio_1 = ""
            radio_2 = ""
            radio_3 = "checked"
            radio_4 = ""
            radio_5 = ""
            radio_6 = ""
            radio_7 = ""
        elif division == "건축-도어":
            radio_1 = ""
            radio_2 = ""
            radio_3 = ""
            radio_4 = "checked"
            radio_5 = ""
            radio_6 = ""
            radio_7 = ""
        elif division == "건축-바닥보수":
            radio_1 = ""
            radio_2 = ""
            radio_3 = ""
            radio_4 = ""
            radio_5 = "checked"
            radio_6 = ""
            radio_7 = ""
        elif division == "건축-벽보수":
            radio_1 = ""
            radio_2 = ""
            radio_3 = ""
            radio_4 = ""
            radio_5 = ""
            radio_6 = "checked"
            radio_7 = ""
        elif division == "건축-기타":
            radio_1 = ""
            radio_2 = ""
            radio_3 = ""
            radio_4 = ""
            radio_5 = ""
            radio_6 = ""
            radio_7 = "checked"
        else:
            radio_1 = ""
            radio_2 = ""
            radio_3 = ""
            radio_4 = ""
            radio_5 = ""
            radio_6 = ""
            radio_7 = ""
        if url == "":
            url_comp = "N"
        else:
            url_comp = "Y"
        if reason == "N/A":
            na_check = "checked"
        else:
            na_check = ""
        context={"roomname":roomname,"roomno":roomno,"division":division,"radio_1":radio_1,"radio_2":radio_2,"radio_3":radio_3,
                    "radio_4":radio_4,"radio_5":radio_5,"radio_6":radio_6,"radio_7":radio_7,"text_signal":text_signal,
                    "description":description,"loginid":loginid,"reason":reason,"url":url,"url_comp":url_comp,"na_check":na_check}
        context.update(user)
        return render(request, 'work_job_new.html', context)  # templates 내 html연결

def work_job_new_submit(request):
    if request.method == 'POST':  # 매소드값이 post인 값만 받는다
        division = request.POST.get('division_give')  # html newname의 값을 받는다.
        roomno = request.POST.get('roomno')  # html newname의 값을 받는다.
        roomname = request.POST.get('roomname')  # html newname의 값을 받는다.
        roomname_2 = request.POST.get('roomname_2')  # html newname의 값을 받는다.
        loginid = request.POST.get('loginid')  # html newname의 값을 받는다.
        description = request.POST.get('description')  # html newname의 값을 받는다.
        reason = request.POST.get('reason')  # html newname의 값을 받는다.
        url = request.POST.get('url')  # html newname의 값을 받는다.
        user = users.objects.get(userid=loginid)
        username = user.username
        userteam = user.userteam
        password = user.password
        auth = user.auth
        user = {"auth": auth, "password": password, "username": username, "userteam": userteam}
    ###job No.생성하기
        today = date.datetime.today()
        job = today.strftime('%y')+today.strftime('%m')+today.strftime('%d')
        jobdate = today.strftime('%y')+"."+today.strftime('%m')+"."+today.strftime('%d')
        jobnocount = worktable.objects.filter(date = jobdate).values('date')
        df = pd.DataFrame.from_records(jobnocount)
        dflen = len(df.index)
        lens = str(dflen + 1)
        jobno = job +"/"+ userteam +"/"+ lens
    ###ROOM이름 값저장하기###
        if roomname =="":
            roomname_true = roomname_2
        else:
            roomname_true = roomname
    ###attached_tag 값저장하기###
        if url != "":
            attached_tag = "View"
        else:
            attached_tag = ""
    ###값저장하기###
        worktable(  # 워크테이블에 저장하기
            job=jobno,
            team=userteam,
            rep=username,
            roomno=roomno,
            description=description,
            userid=loginid,
            date=jobdate,
            division=division,
            roomname=roomname_true,
            reason=reason,
            attached_file=url,
            attached_tag=attached_tag,
        ).save()  # 저장
    ###해당팀장에게 메일보내기###
        title_text = "(자동메일)수리제작의뢰서 신청의 건 [Job No.: " + jobno + "]"
        email_text = "Job No: " + jobno + "가 신청되었습니다." + \
                     "\n\nJob No: " + jobno + \
                     "\n팀: " + userteam + \
                     "\n요청자: " + username + \
                     "\n요청일자: " + jobdate + \
                     "\nRoom Name (Room No.): " + roomname_true + " (" + roomno + ")" \
                     "\n구분: " + division + \
                     "\n요청내용: " + description + \
                     "\n고장사유: " + reason + \
                     "\n\n ※ 상기 메일 자동발신 메일이며 회신은 불가합니다." + \
                     "\n ※ Link: http://dmbio.synology.me:803"
    ##팀장 메일주소 불러오기##
        manager_get = users.objects.filter(userteam=userteam, auth__icontains="Manager")
        manager_get = manager_get.values('no')
        df_manager_get = pd.DataFrame.from_records(manager_get)
        manager_get_len = len(df_manager_get.index)
        for i in range(manager_get_len):
            no_get = df_manager_get.iat[i, 0]
            try:
                email_get = users.objects.get(no=no_get)
                email_add = [email_get.useremail]
                email = EmailMessage(title_text, email_text, to=email_add)
                email.send()
            except:
                pass
        comp_signal ="Y"
        context={"comp_signal":comp_signal,"loginid":loginid}
        context.update(user)
        return render(request, 'work_job_new.html', context)  # templates 내 html연결

def work_job_new_accept(request):
    if request.method == 'POST':  # 매소드값이 post인 값만 받는다
        loginid = request.POST.get('loginid')  # html에서 해당 값을 받는다
        jobno = request.POST.get('jobno')  # html에서 해당 값을 받는다
        user = users.objects.get(userid=loginid)
        username = user.username
        userteam = user.userteam
        password = user.password
        auth = user.auth
        user = {"auth": auth, "password": password, "username": username, "userteam": userteam}
    ####값저장하기####
        today = date.datetime.today()
        today_date = today.strftime('%y') + "." + today.strftime('%m') + "." + today.strftime('%d')
        save_data = worktable.objects.get(job=jobno)
        save_data.approval = username + " / " + today_date
        save_data.status = "신청완료"
        save_data.save()
    ###엔지니어에게 메일보내기###
        title_text = "(자동메일)수리제작의뢰서 신청의 건 [Job No.: " + save_data.job + "]"
        email_text = "Job No: " + save_data.job + "가 신청되었습니다." + \
                     "\n\nJob No: " + save_data.job + \
                     "\n팀: " + save_data.team + \
                     "\n요청자: " + save_data.rep + \
                     "\n요청일자: " + save_data.date + \
                     "\nRoom Name (Room No.): " + save_data.roomname + " (" + save_data.roomno + ")" \
                     "\n구분: " + save_data.division + \
                     "\n요청내용: " + save_data.description + \
                     "\n고장사유: " + save_data.reason + \
                     "\n\n ※ 상기 메일 자동발신 메일이며 회신은 불가합니다." + \
                     "\n ※ Link: http://dmbio.synology.me:803"
    #엔지니어 메일주소 불러오기##
        manager_get = users.objects.filter(Q(auth="Engineer")|Q(auth="Eng. Manager"))
        manager_get = manager_get.values('no')
        df_manager_get = pd.DataFrame.from_records(manager_get)
        manager_get_len = len(df_manager_get.index)
        for i in range(manager_get_len):
            no_get = df_manager_get.iat[i, 0]
            try:
                email_get = users.objects.get(no=no_get)
                email_add = [email_get.useremail]
                email = EmailMessage(title_text, email_text, to=email_add)
                email.send()
            except:
                pass
        ####기본정보 보내기####
        signal = request.POST.get('signal')  # html에서 해당 값을 받는다
        if auth == "Engineer": ###엔지니어
            if signal == "yes":
                worklist = worktable.objects.filter(status="신청완료").order_by('status', '-job')
            else:
                worklist = worktable.objects.filter(Q(status="신청완료") | Q(status="접수")).order_by('status','team')
        elif (auth == "Eng. Manager") or (auth == "Eng. Supervisor"): ###엔지니어 팀장 슈퍼바이져
            worklist = worktable.objects.filter(status="조치완료").order_by('team', '-job')
        elif auth == "Team Manager": #### 일반 팀장
            if signal == "yes":
                worklist = worktable.objects.filter(team=userteam, status="신청").order_by('status', '-job')
            else:
                worklist = worktable.objects.filter(Q(team=userteam)&~Q(status="종결") & ~Q(status="반려")).order_by('status', '-job')
        else: ####팀원
            worklist = worktable.objects.filter(Q(rep=username)&~Q(status="종결")&~Q(status="반려")).order_by('status', '-job')
        table_signal = ""
        view_table = worktable.objects.filter(job=jobno)
        context = {"loginid": loginid, "worklist": worklist, "table_signal": table_signal, "view_table": view_table,"signal":signal}
        context.update(user)
        return render(request, 'work_job_main.html', context)  # templates 내 html연결

def work_job_new_reject(request):
    if request.method == 'POST':  # 매소드값이 post인 값만 받는다
        loginid = request.POST.get('loginid')  # html에서 해당 값을 받는다
        jobno = request.POST.get('jobno')  # html에서 해당 값을 받는다
        reject_reason = request.POST.get('reject_reason')  # html에서 해당 값을 받는다
        user = users.objects.get(userid=loginid)
        username = user.username
        userteam = user.userteam
        password = user.password
        auth = user.auth
        user = {"auth": auth, "password": password, "username": username, "userteam": userteam}
    ####값저장하기####
        today = date.datetime.today()
        today_date = today.strftime('%y') + "." + today.strftime('%m') + "." + today.strftime('%d')
        save_data = worktable.objects.get(job=jobno)
        save_data.summary = "[반려사유] " + reject_reason
        save_data.status = "반려"
        save_data.save()
    ###신청자에게 메일보내기###
        title_text = "(자동메일)수리제작의뢰서 반려의 건 [Job No.: " + save_data.job + "]"
        email_text = "Job No: " + save_data.job + "가 반려되었습니다." + \
                     "\n\nJob No: " + save_data.job + \
                     "\n팀: " + save_data.team + \
                     "\n요청자: " + save_data.rep + \
                     "\n요청일자: " + save_data.date + \
                     "\nRoom Name (Room No.): " + save_data.roomname + " (" + save_data.roomno + ")" \
                      "\n구분: " + save_data.division + \
                     "\n요청내용: " + save_data.description + \
                     "\n반려사유: " + reject_reason + \
                     "\n\n ※ 상기 메일 자동발신 메일이며 회신은 불가합니다." + \
                     "\n ※ Link: http://dmbio.synology.me:803"
    #신청자 메일주소 불러오기##
        manager_get = users.objects.filter(userid=save_data.userid)
        manager_get = manager_get.values('no')
        df_manager_get = pd.DataFrame.from_records(manager_get)
        manager_get_len = len(df_manager_get.index)
        for i in range(manager_get_len):
            no_get = df_manager_get.iat[i, 0]
            try:
                email_get = users.objects.get(no=no_get)
                email_add = [email_get.useremail]
                email = EmailMessage(title_text, email_text, to=email_add)
                email.send()
            except:
                pass
        ####기본정보 보내기####
        signal = request.POST.get('signal')  # html에서 해당 값을 받는다
        if auth == "Engineer": ###엔지니어
            if signal == "yes":
                worklist = worktable.objects.filter(status="신청완료").order_by('status', '-job')
            else:
                worklist = worktable.objects.filter(Q(status="신청완료") | Q(status="접수")).order_by('status','team')
        elif (auth == "Eng. Manager") or (auth == "Eng. Supervisor"): ###엔지니어 팀장 슈퍼바이져
            worklist = worktable.objects.filter(status="조치완료").order_by('team', '-job')
        elif auth == "Team Manager": #### 일반 팀장
            if signal == "yes":
                worklist = worktable.objects.filter(team=userteam, status="신청").order_by('status', '-job')
            else:
                worklist = worktable.objects.filter(Q(team=userteam)&~Q(status="종결") & ~Q(status="반려")).order_by('status', '-job')
        else: ####팀원
            worklist = worktable.objects.filter(Q(rep=username)&~Q(status="종결")&~Q(status="반려")).order_by('status', '-job')
        table_signal = ""
        view_table = worktable.objects.filter(job=jobno)
        context = {"loginid": loginid, "worklist": worklist, "table_signal": table_signal, "view_table": view_table,"signal":signal}
        context.update(user)
        return render(request, 'work_job_main.html', context)  # templates 내 html연결

def work_job_new_upload(request):
    if request.method == 'POST':  # 매소드값이 post인 값만 받는다
        loginid = request.POST.get('loginid')  # html에서 해당 값을 받는다
        division = request.POST.get('division_give')  # html에서 해당 값을 받는다
        roomno = request.POST.get('roomno_give')  # html에서 해당 값을 받는다
        description = request.POST.get('description_give')  # html에서 해당 값을 받는다
        reason = request.POST.get('reason_give')  # html에서 해당 값을 받는다
        roomname_2 = request.POST.get('roomname_2_give')  # html에서 해당 값을 받는다
        roomname = request.POST.get('roomname')  # html에서 해당 값을 받는다
        user = users.objects.get(userid=loginid)
        username = user.username
        userteam = user.userteam
        password = user.password
        auth = user.auth
        user = {"auth": auth, "password": password, "username": username, "userteam": userteam}
    ###ROOM No. 값 받기
        try:
            room_get = room.objects.get(roomno=roomno)
            text_signal = "N"
        except:
            text_signal = "Y"
    ###선택 값 반환받기
        if division == "전기-콘센트":
            radio_1 = "checked"
            radio_2 = ""
            radio_3 = ""
            radio_4 = ""
            radio_5 = ""
            radio_6 = ""
            radio_7 = ""
        elif division == "전기-형광등":
            radio_1 = ""
            radio_2 = "checked"
            radio_3 = ""
            radio_4 = ""
            radio_5 = ""
            radio_6 = ""
            radio_7 = ""
        elif division == "전기-기타":
            radio_1 = ""
            radio_2 = ""
            radio_3 = "checked"
            radio_4 = ""
            radio_5 = ""
            radio_6 = ""
            radio_7 = ""
        elif division == "건축-도어":
            radio_1 = ""
            radio_2 = ""
            radio_3 = ""
            radio_4 = "checked"
            radio_5 = ""
            radio_6 = ""
            radio_7 = ""
        elif division == "건축-바닥보수":
            radio_1 = ""
            radio_2 = ""
            radio_3 = ""
            radio_4 = ""
            radio_5 = "checked"
            radio_6 = ""
            radio_7 = ""
        elif division == "건축-벽보수":
            radio_1 = ""
            radio_2 = ""
            radio_3 = ""
            radio_4 = ""
            radio_5 = ""
            radio_6 = "checked"
            radio_7 = ""
        elif division == "건축-기타":
            radio_1 = ""
            radio_2 = ""
            radio_3 = ""
            radio_4 = ""
            radio_5 = ""
            radio_6 = ""
            radio_7 = "checked"
        else:
            radio_1 = ""
            radio_2 = ""
            radio_3 = ""
            radio_4 = ""
            radio_5 = ""
            radio_6 = ""
            radio_7 = ""
    #################파일업로드하기##################
        if "upload_file" in request.FILES:
                # 파일 업로드 하기!!!
           upload_file = request.FILES["upload_file"]
           fs = FileSystemStorage()
           name = fs.save(upload_file.name, upload_file)  # 파일저장 // 이름저장
                    # 파일 읽어오기!!!
           url = fs.url(name)
        else:
            file_name = "-"
    #####첨부파일 시그널 주기#####
        url_comp = "Y"
        if reason == "N/A":
            na_check = "checked"
        else:
            na_check = ""
        context={"roomname":roomname,"roomno":roomno,"division":division,"radio_1":radio_1,"radio_2":radio_2,"radio_3":radio_3,
                    "radio_4":radio_4,"radio_5":radio_5,"radio_6":radio_6,"radio_7":radio_7,"text_signal":text_signal,
                    "description":description,"loginid":loginid,"reason":reason,"roomname_2":roomname_2,"url":url,
                    "url_comp":url_comp,"na_check":na_check}
        context.update(user)
        return render(request, 'work_job_new.html', context)  # templates 내 html연결




##############################################################################################################
#################################################Admin########################################################
##############################################################################################################

def user_info_main(request):
    if request.method =='POST': #매소드값이 post인 값만 받는다
        loginid = request.POST.get('loginid')  # html에서 해당 값을 받는다
    ##이름 및 권한 끌고다니기##
        user = users.objects.get(userid=loginid)
        username = user.username
        userteam = user.userteam
        password = user.password
        auth = user.auth
        user = {"auth": auth, "password": password, "username": username, "userteam": userteam}
        if auth == "Admin":
            user_info = users.objects.all() #db 동기화
        else:
            user_info = users.objects.filter(userteam=userteam) #db 동기화
        context = {"user_info": user_info, "loginid":loginid}
        context.update(user)
        return render(request, 'user_info_main.html', context) #templates 내 html연결

def user_info_new(request):
    return render(request, 'user_info_new.html')  # templates 내 html연결

def user_info_new_submit(request):
    if request.method =='POST': #매소드값이 post인 값만 받는다
        loginid = request.POST.get('loginid')  # html에서 해당 값을 받는다
    ##이름 및 권한 끌고다니기##
        user = users.objects.get(userid=loginid)
        username = user.username
        userteam = user.userteam
        password = user.password
        auth = user.auth
        user = {"auth": auth, "password": password, "username": username, "userteam": userteam}
    ##입력값 불러오기##
        userid_up = request.POST.get('userid')  # html Login id의 값을
        username_up = request.POST.get('username')  # html Login id의 값을
        userteam_up = request.POST.get('userteam')  # html Login id의 값을
        password_up = request.POST.get('password')  # html Login id의 값을
        password_again_up = request.POST.get('password_again')  # html Login id의 값을
        useremail_up = request.POST.get('useremail')  # html Login id의 값을
        auth_up = request.POST.get('auth')  # html Login id의 값을
        usertel_up = request.POST.get('usertel')  # html Login id의 값을
    # ID중복여부 판단하기
        try:
            id_check = users.objects.get(userid = userid_up)  # db 동기화
            messages.error(request, "아이디가 중복되었습니다.")  # 아이디 중복
            context = {"loginid":loginid}
            context.update(user)
            return render(request, 'user_info_new.html', context) #templates 내 html연결
        except:
    # PASSWORD 일치여부 판단하기
            if password_up != password_again_up:
                messages.error(request, "패스워드가 일치하지 않습니다.")  # 비번 불일치
                context = {"loginid": loginid}
                context.update(user)
                return render(request, 'user_info_new.html', context)  # templates 내 html연결
            else:
    ######################## 값 저장하기
                users(
                      userid=userid_up,
                      username=username_up,
                      userteam=userteam_up,
                      password=password_up,
                      useremail=useremail_up,
                      auth=auth_up,
                      usertel=usertel_up,
                      ).save()
                comp_signal="Y"
                context = {"loginid":loginid,"comp_signal":comp_signal}
                context.update(user)
                return render(request, 'user_info_new.html', context) #templates 내 html연결

def user_info_change(request):
    return render(request, 'user_info_change.html')  # templates 내 html연결

def user_info_change_submit(request):
    if request.method =='POST': #매소드값이 post인 값만 받는다
        userteam_get = request.POST.get('userteam')  # html에서 해당 값을 받는다
        password_get = request.POST.get('password')  # html에서 해당 값을 받는다
        useremail_get = request.POST.get('useremail')  # html에서 해당 값을 받는다
        auth_get = request.POST.get('auth')  # html에서 해당 값을 받는다
        usertel_get = request.POST.get('usertel')  # html에서 해당 값을 받는다
        userid_get = request.POST.get('userid')  # html에서 해당 값을 받는다
        loginid = request.POST.get('loginid')  # html에서 해당 값을 받는다
    ##이름 및 권한 끌고다니기##
        user = users.objects.get(userid=loginid)
        username = user.username
        userteam = user.userteam
        password = user.password
        auth = user.auth
        user = {"auth": auth, "password": password, "username": username, "userteam": userteam}
    ##변경값 저장하기##
        info_change = users.objects.get(userid=userid_get)
        info_change.userteam = userteam_get
        info_change.password = password_get
        info_change.useremail = useremail_get
        info_change.auth = auth_get
        info_change.usertel = usertel_get
        info_change.save()
    ##자동클로우즈##
        comp_signal = "Y"
        context = {"loginid":loginid,"comp_signal":comp_signal}
        context.update(user)
        return render(request, 'user_info_change.html', context) #templates 내 html연결

def user_info_change_delete(request):
    if request.method =='POST': #매소드값이 post인 값만 받는다
        loginid = request.POST.get('loginid')  # html에서 해당 값을 받는다
        userid_get = request.POST.get('userid')  # html에서 해당 값을 받는다
    ##이름 및 권한 끌고다니기##
        user = users.objects.get(userid=loginid)
        username = user.username
        userteam = user.userteam
        password = user.password
        auth = user.auth
        user = {"auth": auth, "password": password, "username": username, "userteam": userteam}
    ##내용삭제##
        delete_check = users.objects.get(userid=userid_get) #db 동기화
        delete_check.delete()
        user_info = users.objects.all() #db 동기화
        context = {"user_info": user_info, "loginid":loginid}
        context.update(user)
        return render(request, 'user_info_main.html', context) #templates 내 html연결


def roomlist_main(request):
    if request.method == 'POST':  # 매소드값이 post인 값만 받는다
        loginid = request.POST.get('loginid')  # html에서 해당 값을 받는다
    ##이름 및 권한 끌고다니기##
        user = users.objects.get(userid=loginid)
        username = user.username
        userteam = user.userteam
        password = user.password
        auth = user.auth
        user = {"auth": auth, "password": password, "username": username, "userteam": userteam}
    ###검색어 설정####
        selecttext = request.POST.get('selecttext')  # html 선택조건의 값을 받는다
        searchtext = request.POST.get('searchtext')  # html 입력 값을 받는다
        try:
            if selecttext == "roomname":
                room_list = room.objects.filter(roomname__icontains=searchtext).order_by("roomno")
            elif selecttext == "roomno":
                room_list = room.objects.filter(roomno__icontains=searchtext).order_by("roomno")
            else:
                room_list = room.objects.all().order_by("roomno")
        except:
            room_list = room.objects.all().order_by("roomno")
        if str(searchtext) == "None":
            searchtext = ""
        context = {"loginid": loginid,"room_list":room_list,"selecttext":selecttext,"searchtext":searchtext}
        context.update(user)
        return render(request, 'roomlist_main.html', context)  # templates 내 html연결

def roomlist_new(request):
    return render(request, 'roomlist_new.html')

def roomlist_new_submit(request):
    if request.method == 'POST':  # 매소드값이 post인 값만 받는다
        roomname = request.POST.get('roomname')  # html 선택조건의 값을 받는다
        roomno = request.POST.get('roomno')  # html 입력 값을 받는다
        loginid = request.POST.get('loginid')  # html에서 해당 값을 받는다
    ##이름 및 권한 끌고다니기##
        user = users.objects.get(userid=loginid)
        username = user.username
        userteam = user.userteam
        password = user.password
        auth = user.auth
        user = {"auth": auth, "password": password, "username": username, "userteam": userteam}
    ##중복여부 확인하기##
        dup_chk = room.objects.filter(roomno=roomno)
        dup_chk = dup_chk.values('no')
        df_dup_chk = pd.DataFrame.from_records(dup_chk)
        dup_chk_len = len(df_dup_chk.index)
        if int(dup_chk_len) > 0:
            messages.error(request, "Room No.가 중복되었습니다.")  # 경고
            comp_signal = "N"
        else:
    ##저장하기##
            room(
                roomname=roomname,
                roomno=roomno,
            ).save()
            comp_signal ="Y"
        context = {"loginid": loginid,"comp_signal":comp_signal,"roomname":roomname,"roomno":roomno}
        context.update(user)
        return render(request, 'roomlist_new.html', context)  # templates 내 html연결

def roomlist_delete(request):
    if request.method == 'POST':  # 매소드값이 post인 값만 받는다
        no = request.POST.get('no')  # html 입력 값을 받는다
        loginid = request.POST.get('loginid')  # html에서 해당 값을 받는다
    ##이름 및 권한 끌고다니기##
        user = users.objects.get(userid=loginid)
        username = user.username
        userteam = user.userteam
        password = user.password
        auth = user.auth
        user = {"auth": auth, "password": password, "username": username, "userteam": userteam}
    ##정보삭제하기
        room_del = room.objects.get(no=no)
        room_del.delete()
    ###검색어 설정####
        selecttext = request.POST.get('selecttext')  # html 선택조건의 값을 받는다
        searchtext = request.POST.get('searchtext')  # html 입력 값을 받는다
        try:
            if selecttext == "roomname":
                room_list = room.objects.filter(roomname__icontains=searchtext).order_by("roomno")
            elif selecttext == "roomno":
                room_list = room.objects.filter(roomno__icontains=searchtext).order_by("roomno")
            else:
                room_list = room.objects.all().order_by("roomno")
        except:
            room_list = room.objects.all().order_by("roomno")
        if str(searchtext) == "None":
            searchtext = ""
        context = {"loginid": loginid,"room_list":room_list,"selecttext":selecttext,"searchtext":searchtext}
        context.update(user)
        return render(request, 'roomlist_main.html', context)  # templates 내 html연결

def roomlist_change(request):
    if request.method == 'POST':  # 매소드값이 post인 값만 받는다
        new_name = request.POST.get('new_name')  # html 선택조건의 값을 받는다
        new_no = request.POST.get('new_no')  # html 입력 값을 받는다
        roomno = request.POST.get('roomno')  # html 입력 값을 받는다
        loginid = request.POST.get('loginid')  # html에서 해당 값을 받는다
        no = request.POST.get('no')  # html 입력 값을 받는다
    ##이름 및 권한 끌고다니기##
        user = users.objects.get(userid=loginid)
        username = user.username
        userteam = user.userteam
        password = user.password
        auth = user.auth
        user = {"auth": auth, "password": password, "username": username, "userteam": userteam}
    ##중복여부 확인하기##
        if roomno != new_no:
            dup_chk = room.objects.filter(roomno=new_no)
            dup_chk = dup_chk.values('no')
            df_dup_chk = pd.DataFrame.from_records(dup_chk)
            dup_chk_len = len(df_dup_chk.index)
            if int(dup_chk_len) > 0:
                messages.error(request, "Room No.가 중복되었습니다.")  # 경고
            ###검색어 설정####
                selecttext = request.POST.get('selecttext')  # html 선택조건의 값을 받는다
                searchtext = request.POST.get('searchtext')  # html 입력 값을 받는다
                try:
                    if selecttext == "roomname":
                        room_list = room.objects.filter(roomname__icontains=searchtext).order_by("roomno")
                    elif selecttext == "roomno":
                        room_list = room.objects.filter(roomno__icontains=searchtext).order_by("roomno")
                    else:
                        room_list = room.objects.all().order_by("roomno")
                except:
                    room_list = room.objects.all().order_by("roomno")
                if str(searchtext) == "None":
                    searchtext = ""
                context = {"loginid": loginid, "room_list": room_list,"selecttext":selecttext,"searchtext":searchtext}
                context.update(user)
                return render(request, 'roomlist_main.html', context)  # templates 내 html연결
    ##값 바꾸기##
        change_room = room.objects.get(no=no)
        if new_name !="":
            change_room.roomname = new_name
        if new_no !="":
            change_room.roomno = new_no
        change_room.save()
    ###검색어 설정####
        selecttext = request.POST.get('selecttext')  # html 선택조건의 값을 받는다
        searchtext = request.POST.get('searchtext')  # html 입력 값을 받는다
        try:
            if selecttext == "roomname":
                room_list = room.objects.filter(roomname__icontains=searchtext).order_by("roomno")
            elif selecttext == "roomno":
                room_list = room.objects.filter(roomno__icontains=searchtext).order_by("roomno")
            else:
                room_list = room.objects.all().order_by("roomno")
        except:
            room_list = room.objects.all().order_by("roomno")
        if str(searchtext) == "None":
            searchtext = ""
        context = {"loginid": loginid,"room_list":room_list,"selecttext":selecttext,"searchtext":searchtext}
        context.update(user)
        return render(request, 'roomlist_main.html', context)  # templates 내 html연결