from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from .models import worktable, room, users, manager
import datetime as date
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
import pandas as pd
from django.core.files.storage import FileSystemStorage

# Create your views here.

##############################################################################################################
#################################################로그인페이지###################################################
##############################################################################################################

def adminmenu(request): #어드민홈 // 완료
    return render(request, 'adminmenu.html') #templates 내 html연결

def changeinfo(request): #가입정보변경 // 완료
    return render(request, 'changeinfo.html') #templates 내 html연결

def changerm(request): #룸정보변경 // 완료
    if request.method == 'POST':  # 매소드값이 post인 값만 받는다
    #기존 값들 정보 불러오기
        newname1 = request.POST.get('newname')  # html newname의 값을 받는다.
        oldno1 = request.POST.get('oldno')  # html old no의 값을 받는다.
        newno1 = request.POST.get('newno')  # html new no의 값을 받는다.
        roominfo = room.objects.get(roomno=oldno1)  # team명과 search값이 같은 항목을 필터링한다.
        if newname1 != "":
            roominfo.roomname = newname1
            roominfo.save()
        if  newno1 != "":
            roominfo.roomno = newno1
            roominfo.save()
    rooms = room.objects.all().order_by('no') #db 동기화
    context={'room':rooms}
    return render(request, 'adminroom.html', context) #templates 내 html연결

def changeteam(request): #팀장변경 // 완료
    if request.method == 'POST':  # 매소드값이 post인 값만 받는다
    #신규 값들 정보 불러오기
        newname1 = request.POST.get('newname')  # html newname의 값을 받는다.
        newteamname1 = request.POST.get('newteamname')  # html jobno의 값을 받는다.
        newid1 = request.POST.get('newid')  # html jobno의 값을 받는다.
    #기존 값들 정보 불러오기
        oldid1 = request.POST.get('oldid')  # html jobno의 값을 받는다.
        managerinfo = manager.objects.get(id=oldid1)  # team명과 search값이 같은 항목을 필터링한다.
    #정보 업데이트
        if newname1 != "":
            managerinfo.name = newname1
            managerinfo.save()
        if newteamname1 != "":
            managerinfo.teamname = newteamname1
            managerinfo.save()
        if newid1 != "":
            managerinfo.id = newid1
            managerinfo.save()
    teamm = manager.objects.all() #db 동기화
    context={'teammanager':teamm}
    return render(request, 'teammanager.html', context) #templates 내 html연결

def adminroom(request): #메인홈 // 완료
    rooms = room.objects.all().order_by('no') #db 동기화
    context={'room':rooms}
    return render(request, 'adminroom.html', context) #templates 내 html연결

def teammanager(request): #메인홈 // 완료
    teamm = manager.objects.all() #db 동기화
    context={'teammanager':teamm}
    return render(request, 'teammanager.html', context) #templates 내 html연결

def login(request): #메인홈 // 완료
    return render(request, 'login.html') #templates 내 html연결

def home2(request): #메인홈 // 완료
    idd2 = request.POST.get('idd2')  # html id의 값을 받는다.
    return render(request, 'home.html', {"idd2":idd2}) #templates 내 html연결

def register(request): #가입
    return render(request, 'register.html') #templates 내 html연결

def registeok(request): #가입완료
    if request.method =='POST': #매소드값이 post인 값만 받는다
        idcheck=request.POST.get("userid")
        pw1check=request.POST.get("pw1")
        pw2check=request.POST.get("pw2")
        if pw1check == pw2check: #패스워드 일치여부 확인
            try:
                #아이디 중복확인
                users.objects.get(userid = idcheck)
                messages.error(request, "WARNING: ID가 중복되었습니다.") #경고
                return render(request, 'register.html')  # templates 내 html연결
        #입력값 저장
            except:
                users( #워크테이블에 get하기
                    userid = request.POST.get("userid"),
                    password = request.POST.get("pw1"),
                    username = request.POST.get("username"),
                    userteam = request.POST.get("userteam"),
                    useremail = request.POST.get("useremail"),
                    usertel=request.POST.get("usertel"),
                ).save() #저장
                messages.error(request, "가입이 완료되었습니다.") #경고
                return render(request, 'register.html')  # templates 내 html연결
        else:
            messages.error(request, "WARNING: Password가 일치하지 않습니다.")  # 경고
            return render(request, 'register.html')  # templates 내 html연결

def adminurl(request): #어드민창 접속 // 완료
    user = users.objects.all()
    context={"user":user}
    return render(request, 'adminurl.html', context) #templates 내 html연결

def plus(request): #수리제작의뢰서 리스트 // 완료
#유저 아이디, 권한 값불러오기
    userid2 = request.POST.get('userid1')
    user = users.objects.get(userid = userid2)
    idd2 = request.POST.get('auth1')
#권한값 +1
    authno = int(idd2)
    if authno < 7:
        authno = authno + 1
    user.auth = authno
    user.save()
#데이터 다시 렌더링
    user = users.objects.all()
    context={"user":user}
    return render(request, 'adminurl.html', context) #templates 내 html연결

def minus(request): #수리제작의뢰서 리스트 // 완료
    # 유저 아이디, 권한 값불러오기
    userid2 = request.POST.get('userid2')
    user = users.objects.get(userid=userid2)
    idd2 = request.POST.get('auth2')
    # 권한값 +1
    authno = int(idd2)
    if authno > 0:
        authno = authno - 1
    user.auth = authno
    user.save()
# 데이터 다시 렌더링
    user = users.objects.all()
    context = {"user": user}
    return render(request, 'adminurl.html', context)  # templates 내 html연결

def home(request):
    if request.method =='POST': #매소드값이 post인 값만 받는다
    # 로그인 정보 비교
        worktables = worktable.objects.all().order_by('-no')  # db 동기화
        search1 = request.POST.get('idd2') #html idd의 값을 받는다.
        search2 = request.POST.get('pww') #html pww의 값을 받는다.
    #신규등록시 정보값 자동전송
        try:
            idd2 = request.POST.get('idd2')  # html idd의 값을 받는다.
            userinfo = users.objects.get(userid=idd2)
            userinfo1 = [userinfo.username]  # username str
            username = userinfo1[0]
            userinfo2 = [userinfo.userteam]  # team명 str
            userteam = userinfo2[0]
            idcheck = users.objects.get(userid = search1) #id값 일치하는지 확인
            checkid = [idcheck.userid] # id값 불러오기
            checkpw = [idcheck.password] # id값에 맞는 pw값 불러오기
            checkpw2 = checkpw[0] #pw값 듀플값에서 str로 변환
            checkid2 = checkid[0] #id값 듀플값에서 str로 변환
            if checkpw2 == search2: #pw값 일치하는지 확인
                return render(request, 'list.html', {'idd2':checkid2, 'worktables':worktables, "username": username, "userteam": userteam})  # templates 내 html연결
            else:
                messages.error(request, "WARNING: 비밀번호가 일치하지 않습니다.") #경고창
                return render(request, 'login.html')  # templates 내 html연결
        except:
            messages.error(request, "WARNING: ID가 일치하지 않습니다.") #경고
            return render(request, 'login.html')  # templates 내 html연결

def changeinfocomp(request):
    if request.method =='POST': #매소드값이 post인 값만 받는다
        search1 = request.POST.get('idd2') #html idd의 값을 받는다.
        search2 = request.POST.get('pww') #html pww의 값을 받는다.
        try:
            idcheck = users.objects.get(userid = search1) #id값 일치하는지 확인
            checkid = [idcheck.userid] # id값 불러오기
            checkpw = [idcheck.password] # id값에 맞는 pw값 불러오기
            checkpw2 = checkpw[0] #pw값 듀플값에서 str로 변환
            checkid2 = checkid[0] #id값 듀플값에서 str로 변환
            if checkpw2 == search2: #pw값 일치하는지 확인
                transferinfo = users.objects.filter(userid=search1)  # id값 일치하는지 확인
                return render(request, 'changeinfocomp.html', {'idd2':checkid2, 'transferinfo':transferinfo})  # templates 내 html연결
            else:
                messages.error(request, "비밀번호가 일치하지 않습니다.") #경고창
                return render(request, 'changeinfo.html')  # templates 내 html연결
        except:
            messages.error(request, "ID가 일치하지 않습니다.") #경고
            return render(request, 'changeinfo.html')  # templates 내 html연결

def changeinfook(request):
    if request.method == 'POST':  # 매소드값이 post인 값만 받는다
        userid1 = request.POST.get('userid') #html userid의 값을 받는다.
        password1 = request.POST.get('password') #html password의 값을 받는다.
        username1 = request.POST.get('username') #html username의 값을 받는다.
        userteam1 = request.POST.get('userteam') #html userteam의 값을 받는다.
        email1 = request.POST.get('useremail') #html useremail의 값을 받는다.
        tel1 = request.POST.get('usertel') #html usertel의 값을 받는다.
    #입력값 저장하기
        changeinfo = users.objects.get(userid=userid1)  # id값 일치하는지 확인
        changeinfo.userid = userid1
        changeinfo.password = password1
        changeinfo.username = username1
        changeinfo.userteam = userteam1
        changeinfo.useremail = email1
        changeinfo.usertel = tel1
        changeinfo.save() # 저장
        return render(request, 'changefinish.html')

def roominsert(request):  # 검색창
    if request.method == 'POST':  # 매소드값이 post인 값만 받는다
        room( #워크테이블에 저장하기
            roomname = request.POST.get("roomname"),
            roomno = request.POST.get("roomno"),
        ).save() #저장
    rooms = room.objects.all().order_by('no') #db 동기화
    context={'room':rooms}
    return render(request, 'adminroom.html', context) #templates 내 html연결

def managerinsert(request):  # 검색창
    if request.method == 'POST':  # 매소드값이 post인 값만 받는다
        try:
            searchid = request.POST.get("id")
            managermail1 = users.objects.get(userid = searchid)
            useremail1 = [managermail1.useremail]  # 팀장메일주소 불러오기
            manageremail = useremail1[0]
            manager(  # 워크테이블에 저장하기
                teamname=request.POST.get("teamname"),
                name=request.POST.get("name"),
                id=request.POST.get("id"),
                email=manageremail,
            ).save()  # 저장
        except:
            print("에러")
        teamm = manager.objects.all() #db 동기화
        context={'teammanager':teamm}
        return render(request, 'teammanager.html', context) #templates 내 html연결

##############################################################################################################
################################################수리제작의뢰서###################################################
##############################################################################################################

##########list 메인창########

def search(request): #검색창
    if request.method == 'POST':  # 매소드값이 post인 값만 받는다
        searchtext = request.POST.get('searchtext')
        selecttext = request.POST.get('selecttext')
    #select값에 따른 검색조건 입력
        if selecttext == "job":
            worktables = worktable.objects.filter(job=searchtext).order_by('-no')
        elif selecttext == "status":
            worktables = worktable.objects.filter(status=searchtext).order_by('-no')
        elif selecttext == "team":
            worktables = worktable.objects.filter(team=searchtext).order_by('-no')
        else:
            worktables = worktable.objects.filter(rep=searchtext).order_by('-no')
        idd2 = request.POST.get('idd2')  # html idd의 값을 받는다.
        userinfo = users.objects.get(userid=idd2)
        userinfo1 = [userinfo.username]  # username str
        username = userinfo1[0]
        userinfo2 = [userinfo.userteam]  # team명 str
        userteam = userinfo2[0]
        return render(request, 'list.html', {'worktables': worktables, "idd2": idd2, "username": username,
                                                 "userteam": userteam})  # templates 내 html연결

def listsidebar(request): #사이드바 // 완료
    worktables = worktable.objects.all().order_by('-no') #db 동기화
    idd2 = request.POST.get('idd2')  # html idd의 값을 받는다.
    return render(request, 'listsidebar.html', {'worktables': worktables, "idd2": idd2}) #templates 내 html연결

def list(request): #수리제작의뢰서 리스트 // 완료
    worktables = worktable.objects.all().order_by('-no') #db 동기화
    idd2 = request.POST.get('idd2')  # html idd의 값을 받는다.
    userinfo = users.objects.get(userid=idd2)
    userinfo1 = [userinfo.username]  # username str
    username = userinfo1[0]
    userinfo2 = [userinfo.userteam]  # team명 str
    userteam = userinfo2[0]
    return render(request, 'list.html', {'worktables': worktables, "idd2": idd2, "username":username, "userteam":userteam }) #templates 내 html연결

##########확인버튼########

def check(request): #확인창 // 완료
    if request.method == 'POST':  # 매소드값이 post인 값만 받는다
    #기존 값들 정보 불러오기
        search2 = request.POST.get('jobno#')  # html jobno의 값을 받는다.
        roomno2 = request.POST.get('roomno#')  # html rmno의 값을 받는다.
        userid1 = request.POST.get('userid#')  # html userid#의 값을 받는다.
        idd2 = request.POST.get('idd2')  # html loginid의 값을 받는다.
        worktables = worktable.objects.all().order_by('-no')  # db 동기화
        work2 = worktable.objects.filter(job=search2) # team명과 search값이 같은 항목을 필터링한다.
        roomname = room.objects.filter(roomno=roomno2)
        user = users.objects.filter(userid=userid1)
        idd3 = users.objects.filter(userid=idd2)
        userinfo = users.objects.get(userid=idd2)
        userinfo1 = [userinfo.username]  # username str
        username = userinfo1[0]
        userinfo2 = [userinfo.userteam]  # team명 str
        userteam = userinfo2[0]
        return render(request, 'check.html', {'worktables': worktables, 'work2': work2,'roomname': roomname,'user':user,'idd2':idd2,'idd3':idd3,
                                              "username": username, "userteam": userteam})

##########신규등록########

def enrollcomp(request): #메인홈 // 완료
    worktables = worktable.objects.all().order_by('-no')[:1] #db 동기화
    context={'worktables':worktables}
    return render(request, 'enrollcomp.html', context) #templates 내 html연결

def enroll(request): #수리제작 등록창 // 완료
    return render(request, 'enroll.html') #templates 내 html연결

def roomnamecall(request): #수리제작 등록창 // 완료\
    if request.method =='POST': #매소드값이 post인 값만 받는다
        try:
            roomno1 = request.POST.get('roomno')  # html idd의 값을 받는다.
            rooms = room.objects.get(roomno = roomno1)
            userinfo1 = [rooms.roomno]  # username str
            roomno = userinfo1[0]
            userinfo2 = [rooms.roomname]  # username str
            roomname = userinfo2[0]
        except:
            roomno = request.POST.get('roomno')  # html idd의 값을 받는다
            roomname = ""
        return render(request, 'enroll.html', {'roomno': roomno, 'roomname': roomname})  # templates 내 html연결

def insertok(request): #insertok 클릭시 동작 // 완료
    if request.method =='POST': #매소드값이 post인 값만 받는다
    # job No.인식
        today = date.datetime.today()
        job = today.strftime('%y')+today.strftime('%m')+today.strftime('%d')
        jobdate = today.strftime('%y')+"."+today.strftime('%m')+"."+today.strftime('%d')
        jobnocount1 = worktable.objects.filter(date = jobdate)  #
        jobnocount = jobnocount1.values('date')  #
        df = pd.DataFrame.from_records(jobnocount)
        dflen = len(df.index)
        lens = dflen + 1
        lens = str(lens)
        userid1 = request.POST.get("idd2")
        jobno1 = users.objects.get(userid=userid1)
        userteam2 = [jobno1.userteam]  # team명 str
        userteam2 = userteam2[0]
        username2 = [jobno1.username]  # 이름 str
        username2 = username2[0]
        userid2 = [jobno1.userid]  # id str
        userid2 = userid2[0]
        jobno = job +"/"+ userteam2 +"/"+ lens

    # 이메일 내용 작성
        titletext = "수리제작의뢰서 요청메일 // Job No:" + jobno
        team1 = userteam2 #team명
        rep1 = username2 #신청자명
        id1 = userid2 #id
        roomno1 = request.POST.get("roomno") #room no
        roomname1 = request.POST.get("roomname") #room name
        description1 = request.POST.get("desc")
        emailtext = "수리제작의뢰서 Job No:" + jobno + "가 신청되었습니다." + \
                        "\n\n팀:" + team1 + "\n신청자: " + rep1 + "(" + id1 + ")" + "\n위치: " + roomname1 + " (" + roomno1 +")" +\
                        "\n요청내용: " + description1 + \
                        "\n Link : http://dmbio.synology.me:803"

    # 팀장에게 메일보내기
        manageremail2 = manager.objects.filter(teamname=team1)  # 레벨4권한담당자한테 메일보내기
        repemail = manageremail2.values('email')  # sql문 dataframe으로 변경
        df = pd.DataFrame.from_records(repemail)
        dflen = len(df.index) #담당자 인원수 확인
        for k in range(dflen):
            managermail = df.iat[k, 0]
            email2 = EmailMessage(titletext, emailtext, to=[managermail])
            email2.send()

    #입력값 저장
        worktable( #워크테이블에 저장하기
            job = jobno,
            team = request.POST.get("userteam"),
            rep = request.POST.get("username"),
            roomno = request.POST.get("roomno"),
            description = request.POST.get("desc"),
            userid = request.POST.get("idd2"),
            date = jobdate,
            roomname = request.POST.get("roomname"),
        ).save() #저장

    else:
        print('error')
    worktables = worktable.objects.all().order_by('-no')[:1]  # db 동기화
    context = {'worktables': worktables}
    return render(request, 'enrollcomp.html', context)  # templates 내 html연결

##########완료버튼########

def completebtn(request): #조치완료버튼 //
    if request.method =='POST': #매소드값이 post인 값만 받는다
    #상태값/조치내용 업데이트
        search2 = request.POST.get('complete1')  # html accept1의 값을 받는다.
        work2 = worktable.objects.get(job=search2)  # team명과 search값이 같은 항목을 필터링한다.
        resultmail = request.POST.get('result1')  # html accept1의 값을 받는다.
    #로그인id값 받기
        idd1 = request.POST.get('idd2')  # html loginid 값을 받는다.
        idd = users.objects.get(userid=idd1)
        acceptid = [idd.username]
        userid = acceptid[0]  # 접수원 ID
        acceptauth2 = [idd.auth]
        acceptauth = acceptauth2[0]  # 접수원 권한
        if acceptauth == 4 or acceptauth == 5:
        #완료내용 이메일 보내기(타이틀)
                summary3 = [work2.job] #jobno내용불러오기
                summary4 = summary3[0] #str변환
                titletext = "수리제작의뢰서 완료메일 // Job No:" + summary4

        #완료내용 이메일 보내기(내용)
                summary1 = [work2.summary] #완료내용불러오기
                summary2 = summary1[0] #str변환
                summary5 = [work2.description]  #요청내용불러오기
                summary6 = summary5[0] #str변환
                summary7 = [work2.rep] # 담당자불러오기
                summary8 = summary7[0] #str변환
                summary9 = [work2.roomname]  # room name불러오기
                summary10 = summary9[0] #str변환
                summary11 = [work2.roomno]  # room no불러오기
                summary12 = summary11[0] #str변환
                emailtext = "수리제작의뢰서 Job No:" + summary4 +"가 조치완료되었습니다. \n\n" + \
                        "신청자: " + summary8 + \
                        "\n위치: " + summary10 + " (" + summary12 +")" +\
                        "\n요청내용: " + summary6 +\
                        "\n담당자: " + userid + \
                        "\n작업내용: " + resultmail + \
                        "\n Link : http://dmbio.synology.me:803"

        # 신청자 이메일 주소 불러오기
                email1 = [work2.userid] # 이메일 아이디 받아오기
                email2 = email1[0] #str변환
                useremail2 = users.objects.get(userid=email2)
                useremail = [useremail2.useremail] #이메일 주소 불러오기
                email1 = EmailMessage(titletext, emailtext, to=useremail)
                email1.send()

        # 신청팀장 이메일 주소 불러오기
                team11 = [work2.team]  # team불러오기
                team1 = team11[0]  # str변환
                manageremail2 = manager.objects.filter(teamname=team1)  # 레벨4권한담당자한테 메일보내기
                repemail = manageremail2.values('email')  # sql문 dataframe으로 변경
                df = pd.DataFrame.from_records(repemail)
                dflen = len(df.index)  # 담당자 인원수 확인
                for k in range(dflen):
                    managermail = df.iat[k, 0]
                    email2 = EmailMessage(titletext, emailtext, to=[managermail])
                    email2.send()

        # SO팀장 이메일 주소 불러오기
                repemail3 = users.objects.filter(auth="5")  # 레벨4권한담당자한테 메일보내기
                repemail1 = repemail3.values('useremail')  # sql문 dataframe으로 변경
                df1 = pd.DataFrame.from_records(repemail1)
                dflen1 = len(df1.index)  # 담당자 인원수 확인
                for j in range(dflen1):
                    managermail1 = df.iat[j, 0]
                    email3 = EmailMessage(titletext, emailtext, to=[managermail1])
                    email3.send()

        #스테이터스 값 업데이트 /조치완료내용 업로드
                work2.status = "조치완료"
                work2.summary = request.POST.get('result1')
                work2.save()
        #화면반환
                search4 = request.POST.get('complete1')  # html job no의 값을 받는다.
                search1 = request.POST.get('roomno')  # html roomno의 값을 받는다.
                idd2 = request.POST.get('idd2')  # html loginid의 값을 받는다.
                worktables = worktable.objects.all().order_by('-no')  # db 동기화
                comp2 = worktable.objects.filter(job=search4)  # team명과 search1값이 같은 항목을 필터링한다.
                room2 = room.objects.filter(roomno=search1)  # team명과 search2값이 같은 항목을 필터링한다.
                idd3 = users.objects.filter(userid=idd2)
                userinfo = users.objects.get(userid=idd2)
                userinfo1 = [userinfo.username]  # username str
                username = userinfo1[0]
                userinfo2 = [userinfo.userteam]  # team명 str
                userteam = userinfo2[0]
                return render(request, 'completecheck.html',
                            {'worktables': worktables, 'comp2': comp2, 'room2': room2, "idd2": idd2, "idd3": idd3,
                            "username": username, "userteam": userteam})

        else:
                search4 = request.POST.get('complete1')  # html job no의 값을 받는다.
                search1 = request.POST.get('roomno')  # html roomno의 값을 받는다.
                idd2 = request.POST.get('idd2')  # html loginid의 값을 받는다.
                worktables = worktable.objects.all().order_by('-no')  # db 동기화
                comp2 = worktable.objects.filter(job=search4)  # team명과 search1값이 같은 항목을 필터링한다.
                room2 = room.objects.filter(roomno=search1)  # team명과 search2값이 같은 항목을 필터링한다.
                idd3 = users.objects.filter(userid=idd2)
                userinfo = users.objects.get(userid=idd2)
                userinfo1 = [userinfo.username]  # username str
                username = userinfo1[0]
                userinfo2 = [userinfo.userteam]  # team명 str
                userteam = userinfo2[0]
                messages.error(request, "WARNING: 수리제작의뢰서 [조치완료]는 수리제작담당자만 가능합니다.")  # 경고
                return render(request, 'completealarm.html',
                            {'worktables': worktables, 'comp2': comp2, 'room2': room2, "idd2": idd2, "idd3": idd3,
                            "username": username, "userteam": userteam})

def complete(request): #삭제 // 완료
    if request.method =='POST': #매소드값이 post인 값만 받는다
    # 기존 값들 정보 불러오기
        status1 = request.POST.get('job3')  # html job3의 값을 받는다.
        search4 = request.POST.get('job2') #html job2의 값을 받는다.
        search1 = request.POST.get('job1') #html job1의 값을 받는다.
        idd2 = request.POST.get('idd2')  # html loginid의 값을 받는다.
        if status1 == "접수":  # pw값 일치하는지 확인
            worktables = worktable.objects.all().order_by('-no')  # db 동기화
            comp2 = worktable.objects.filter(job = search1) #team명과 search1값이 같은 항목을 필터링한다.
            room2 = room.objects.filter(roomno=search4)  # team명과 search2값이 같은 항목을 필터링한다.
            idd3 = users.objects.filter(userid=idd2)
            userinfo = users.objects.get(userid=idd2)
            userinfo1 = [userinfo.username]  # username str
            username = userinfo1[0]
            userinfo2 = [userinfo.userteam]  # team명 str
            userteam = userinfo2[0]
            return render(request, 'complete.html', {'worktables': worktables,'comp2':comp2,'room2':room2, "idd2": idd2, "idd3": idd3, #templates 내 html연결
                                                     "username": username, "userteam": userteam})
        elif status1 == "조치완료":  # pw값 일치하는지 확인
            worktables = worktable.objects.all().order_by('-no')  # db 동기화
            comp2 = worktable.objects.filter(job = search1) #team명과 search1값이 같은 항목을 필터링한다.
            room2 = room.objects.filter(roomno=search4)  # team명과 search2값이 같은 항목을 필터링한다.
            idd3 = users.objects.filter(userid=idd2)
            userinfo = users.objects.get(userid=idd2)
            userinfo1 = [userinfo.username]  # username str
            username = userinfo1[0]
            userinfo2 = [userinfo.userteam]  # team명 str
            userteam = userinfo2[0]
            return render(request, 'completecheck.html', {'worktables': worktables,'comp2':comp2,'room2':room2, "idd2": idd2, "idd3": idd3, #templates 내 html연결
                                                     "username": username, "userteam": userteam})
        else:
            worktables = worktable.objects.all().order_by('-no')  # db 동기화
            comp2 = worktable.objects.filter(job=search1)  # team명과 search1값이 같은 항목을 필터링한다.
            room2 = room.objects.filter(roomno=search4)  # team명과 search2값이 같은 항목을 필터링한다.
            idd3 = users.objects.filter(userid=idd2)
            userinfo = users.objects.get(userid=idd2)
            userinfo1 = [userinfo.username]  # username str
            username = userinfo1[0]
            userinfo2 = [userinfo.userteam]  # team명 str
            userteam = userinfo2[0]
            messages.error(request, "WARNING: [상태]값이 [접수or조치완료]일 경우에만 진행됩니다.")  # 경고
            return render(request, 'completealarm.html', {'worktables': worktables, 'comp2': comp2, 'room2': room2,
                                                     "idd2": idd2, "idd3": idd3, "username": username, "userteam": userteam})  # templates 내 html연결

def completealarm(request): #삭제 // 완료
    if request.method =='POST': #매소드값이 post인 값만 받는다
    # 기존 값들 정보 불러오기
        status1 = request.POST.get('job3')  # html job3의 값을 받는다.
        search4 = request.POST.get('job2') #html job2의 값을 받는다.
        search1 = request.POST.get('job1') #html job1의 값을 받는다.
        idd2 = request.POST.get('idd2')  # html loginid의 값을 받는다.
        if status1 == "접수":  # pw값 일치하는지 확인
            worktables = worktable.objects.all().order_by('-no')  # db 동기화
            comp2 = worktable.objects.filter(job = search1) #team명과 search1값이 같은 항목을 필터링한다.
            room2 = room.objects.filter(roomno=search4)  # team명과 search2값이 같은 항목을 필터링한다.
            idd3 = users.objects.filter(userid=idd2)
            userinfo = users.objects.get(userid=idd2)
            userinfo1 = [userinfo.username]  # username str
            username = userinfo1[0]
            userinfo2 = [userinfo.userteam]  # team명 str
            userteam = userinfo2[0]
            return render(request, 'complete.html',
                          {'worktables': worktables, 'comp2': comp2, 'room2': room2, "idd2": idd2,
                           "idd3": idd3, "username":username, "userteam":userteam})  # templates 내 html
        elif status1 == "조치완료":  # pw값 일치하는지 확인
            worktables = worktable.objects.all().order_by('-no')  # db 동기화
            comp2 = worktable.objects.filter(job = search1) #team명과 search1값이 같은 항목을 필터링한다.
            room2 = room.objects.filter(roomno=search4)  # team명과 search2값이 같은 항목을 필터링한다.
            idd3 = users.objects.filter(userid=idd2)
            userinfo = users.objects.get(userid=idd2)
            userinfo1 = [userinfo.username]  # username str
            username = userinfo1[0]
            userinfo2 = [userinfo.userteam]  # team명 str
            userteam = userinfo2[0]
            return render(request, 'completecheck.html', {'worktables': worktables,'comp2':comp2,'room2':room2, "idd2": idd2, "idd3": idd3, #templates 내 html연결
                                                     "username": username, "userteam": userteam})
        else:
            worktables = worktable.objects.all().order_by('-no')  # db 동기화
            comp2 = worktable.objects.filter(job=search1)  # team명과 search1값이 같은 항목을 필터링한다.
            room2 = room.objects.filter(roomno=search4)  # team명과 search2값이 같은 항목을 필터링한다.
            idd3 = users.objects.filter(userid=idd2)
            userinfo = users.objects.get(userid=idd2)
            userinfo1 = [userinfo.username]  # username str
            username = userinfo1[0]
            userinfo2 = [userinfo.userteam]  # team명 str
            userteam = userinfo2[0]
            messages.error(request, "WARNING: [상태]값이 [접수]일 경우에만 진행됩니다.")  # 경고
            return render(request, 'completealarm.html', {'worktables': worktables, 'comp2': comp2, 'room2': room2,
                                                     "idd2": idd2, "idd3": idd3, "username":username, "userteam":userteam})  # templates 내 html연결

def completecheck(request): #완료 창 오픈 // 완료
    if request.method =='POST': #매소드값이 post인 값만 받는다
    # 기존 값들 정보 불러오기
        status1 = request.POST.get('job3')  # html job3의 값을 받는다.
        search4 = request.POST.get('job2') #html job2의 값을 받는다.
        search1 = request.POST.get('job1') #html job1의 값을 받는다.
        idd2 = request.POST.get('idd2')  # html loginid의 값을 받는다.
        if status1 == "접수":  # pw값 일치하는지 확인
            worktables = worktable.objects.all().order_by('-no')  # db 동기화
            comp2 = worktable.objects.filter(job = search1) #team명과 search1값이 같은 항목을 필터링한다.
            room2 = room.objects.filter(roomno=search4)  # team명과 search2값이 같은 항목을 필터링한다.
            idd3 = users.objects.filter(userid=idd2)
            userinfo = users.objects.get(userid=idd2)
            userinfo1 = [userinfo.username]  # username str
            username = userinfo1[0]
            userinfo2 = [userinfo.userteam]  # team명 str
            userteam = userinfo2[0]
            return render(request, 'complete.html', {'worktables': worktables,'comp2':comp2,'room2':room2, "idd2": idd2, "idd3": idd3, #templates 내 html연결
                                                     "username": username, "userteam": userteam})
        elif status1 == "조치완료":  # pw값 일치하는지 확인
            worktables = worktable.objects.all().order_by('-no')  # db 동기화
            comp2 = worktable.objects.filter(job = search1) #team명과 search1값이 같은 항목을 필터링한다.
            room2 = room.objects.filter(roomno=search4)  # team명과 search2값이 같은 항목을 필터링한다.
            idd3 = users.objects.filter(userid=idd2)
            userinfo = users.objects.get(userid=idd2)
            userinfo1 = [userinfo.username]  # username str
            username = userinfo1[0]
            userinfo2 = [userinfo.userteam]  # team명 str
            userteam = userinfo2[0]
            return render(request, 'completecheck.html', {'worktables': worktables,'comp2':comp2,'room2':room2, "idd2": idd2, "idd3": idd3, #templates 내 html연결
                                                     "username": username, "userteam": userteam})
        else:
            worktables = worktable.objects.all().order_by('-no')  # db 동기화
            comp2 = worktable.objects.filter(job=search1)  # team명과 search1값이 같은 항목을 필터링한다.
            room2 = room.objects.filter(roomno=search4)  # team명과 search2값이 같은 항목을 필터링한다.
            idd3 = users.objects.filter(userid=idd2)
            userinfo = users.objects.get(userid=idd2)
            userinfo1 = [userinfo.username]  # username str
            username = userinfo1[0]
            userinfo2 = [userinfo.userteam]  # team명 str
            userteam = userinfo2[0]
            messages.error(request, "WARNING: [상태]값이 [접수or조치완료]일 경우에만 진행됩니다.")  # 경고
            return render(request, 'completealarm.html', {'worktables': worktables, 'comp2': comp2, 'room2': room2,
                                                     "idd2": idd2, "idd3": idd3, "username": username, "userteam": userteam})  # templates 내 html연결

def completeapproval(request): #조치완료승인 // 완료
    if request.method == 'POST':  # 매소드값이 post인 값만 받는다
        jobno1 = request.POST.get('jobno')  # html jobno의 값을 받는다.
        condition = worktable.objects.get(job=jobno1)

    # 설비팀 팀장여부 판단하기
        idd = request.POST.get('idd2') #로그인 이름받기
        idcheck = users.objects.get(userid=idd)
        autocheck1 =[idcheck.auth]
        autocheck = autocheck1[0] #사용자 설비팀 확인
    #팀장 확인 및 값 변경
        if autocheck == 5:
            managers = request.POST.get('manager1')  # html 결재자 이름의 값을 받는다.
            today = date.datetime.today()
            dates = today.strftime('%y%m%d') #결재일 받기
            app = managers + " / 20"+ dates
            condition.check = app
            condition.status = "종결"
            condition.save()
    #화면 전환
            worktables = worktable.objects.all().order_by('-no')  # db 동기화
            idd2 = request.POST.get('idd2')  # html idd의 값을 받는다.
            messages.error(request, "해당 Job No.수리가 종결되었습니다.")  # 경고
            return render(request, 'completealarm.html', {'worktables': worktables, "idd2": idd2})  # templates 내 html연결
    #팀장이 아닐 시 경고창
        else:
            worktables = worktable.objects.all().order_by('-no')  # db 동기화
            idd2 = request.POST.get('idd2')  # html idd의 값을 받는다.
            messages.error(request, "WARNING: 해당Job 승인권한이 없습니다.")  # 경고
            return render(request, 'completealarm.html', {'worktables': worktables, "idd2": idd2})  # templates 내 html연결

def completereject(request): #조치완료반려 // 완료
    if request.method == 'POST':  # 매소드값이 post인 값만 받는다
        jobno1 = request.POST.get('jobno')  # html jobno의 값을 받는다.
        condition = worktable.objects.get(job=jobno1)
        reason = request.POST.get('comprejectreason')  # html 반려사유 값을 받는다.
    # 설비팀 팀장여부 판단하기
        idd = request.POST.get('idd2') #로그인 이름받기
        idcheck = users.objects.get(userid=idd)
        autocheck1 =[idcheck.auth]
        autocheck = autocheck1[0] #사용자 설비팀 확인
    #팀장 확인 및 값 변경
        if autocheck == 5:
        # 설비팀 담당자 이메일 생성
            repcheck1 = [condition.engrep]
            repcheck = repcheck1[0]
            repemail1 = users.objects.get(username = repcheck)
            repemail2 = [repemail1.useremail]
            repemail = repemail2[0]
        # 이메일 내용 생성
            work2 = worktable.objects.get(job=jobno1)
            summary1 = [work2.summary]
            summary2 = summary1[0] #완료내용불러오기
            summary5 = [work2.description]
            summary6 = summary5[0] #요청내용불러오기
            summary7 = [work2.rep]
            summary8 = summary7[0] # 담당자불러오기
            summary9 = [work2.roomname]
            summary10 = summary9[0] # room name불러오기
            summary11 = [work2.roomno]
            summary12 = summary11[0] # room no불러오기
            emailtext = "수리제작의뢰서 Job No:" + jobno1 +"가 조치완료가 [반려]되었습니다. \n\n" + \
                        "신청자: " + summary8 + \
                        "\n위치: " + summary10 + " (" + summary12 +")" +\
                        "\n요청내용: " + summary6 +\
                        "\n작업내용: " + summary2 + \
                        "\n반려사유: " + reason + \
                        "\n Link : http://dmbio.synology.me:803"
            titletext = "수리제작의뢰서 조치완료 반려메일 // Job No:" + jobno1
            email1 = EmailMessage(titletext, emailtext, to=[repemail])
            email1.send()
        # 데이터 업데이트
            condition.summary ="미완료"
            condition.status = "접수"
            condition.save()
    #화면 전환
            worktables = worktable.objects.all().order_by('-no')  # db 동기화
            idd2 = request.POST.get('idd2')  # html idd의 값을 받는다.
            messages.error(request, "해당 Job No.조치완료가 반려되었습니다.")  # 경고
            return render(request, 'completealarm.html', {'worktables': worktables, "idd2": idd2})  # templates 내 html연결
    #팀장이 아닐 시 경고창
        else:
            worktables = worktable.objects.all().order_by('-no')  # db 동기화
            idd2 = request.POST.get('idd2')  # html idd의 값을 받는다.
            messages.error(request, "WARNING: 해당Job 승인권한이 없습니다.")  # 경고
            return render(request, 'completealarm.html', {'worktables': worktables, "idd2": idd2})  # templates 내 html연결

##########접수버튼########

def reject(request): #반려 //
    if request.method =='POST': #매소드값이 post인 값만 받는다
        # 접수 인터락
        reason = request.POST.get('rejectreason')  # html 반려사유 값을 받는다.
        idd1 = request.POST.get('idd2')  # html loginid 값을 받는다.
        idd = users.objects.get(userid=idd1)
        acceptid = [idd.username]
        userid = acceptid[0]  # 접수원 ID
        acceptauth2 = [idd.auth]
        acceptauth = acceptauth2[0]  # 접수원 권한

        if acceptauth == 4 or acceptauth == 5:
            # 이메일 내용 정보 필터링
            search = request.POST.get('reject1')  # html job no 값을 받는다.
            search2 = worktable.objects.get(job=search)
            info11 = [search2.job]
            info1 = info11[0]  # job no str값
            info22 = [search2.team]
            info2 = info22[0]  # team str값
            info33 = [search2.rep]
            info3 = info33[0]  # rep str값
            info44 = [search2.roomno]
            info4 = info44[0]  # roomname str값
            info55 = [search2.description]
            info5 = info55[0]  # 내용 str값
            info66 = [search2.userid]
            info6 = info66[0]  # 유져아이디 str값

        # 이메일 내용 작성
            titletext = "수리제작의뢰서 요청반려메일 // Job No:" + info1
            emailtext = "수리제작의뢰서 Job No:" + info1 + "가 반려되었습니다." + \
                        "\n\n팀:" + info2 + "\n신청자: " + info3 + "(" + info6 + ")" + "\n위치: " + info4 + \
                        "\n요청내용: " + info5 + \
                        "\n시스템운영팀 담당자: " + userid +\
                        "\n반려사유: " + reason + \
                        "\n Link : http://dmbio.synology.me:803"

        # 이메일 보내기
            repemail2 = users.objects.get(userid=info6)
            repemail = [repemail2.useremail]
            email1 = EmailMessage(titletext, emailtext, to=repemail)
            email1.send()
        # status값 변경/저장
            work2 = worktable.objects.get(job=search)  # team명과 search값이 같은 항목을 필터링한다.
            work2.status = "반려"
            work2.engrep = userid
            work2.save()
            worktables = worktable.objects.all().order_by('-no')  # db 동기화
            idd2 = request.POST.get('idd2')  # html id의 값을 받는다.
            messages.error(request, "해당 Job No. 반려처리가 완료되었습니다.")  # 경고
            return render(request, 'popupalarm.html', {'worktables': worktables, "idd2": idd2})  # templates 내 html연결
        else:
            worktables = worktable.objects.all().order_by('-no')  # db 동기화
            idd2 = request.POST.get('idd2')  # html id의 값을 받는다.
            messages.error(request, "WARNING: 수리제작의뢰서 [접수]는 수리제작담당자만 가능합니다.")  # 경고
            return render(request, 'popupalarm.html', {'worktables': worktables, "idd2": idd2})  # templates 내 html연결

def accept(request): #접수 //
    if request.method =='POST': #매소드값이 post인 값만 받는다
    #접수 인터락
        idd1 = request.POST.get('idd2')  # html loginid 값을 받는다.
        idd = users.objects.get(userid=idd1)
        acceptid = [idd.username]
        userid = acceptid[0] #접수원 ID
        acceptauth2 = [idd.auth]
        acceptauth = acceptauth2[0]  # 접수원 권한
        status = request.POST.get('status1')  # html loginid 값을 받는다.

        if acceptauth == 4 or acceptauth == 5:
            if status =="신청완료":
        #이메일 내용 정보 필터링
                search = request.POST.get('accept1')  # html job no 값을 받는다.
                search2 = worktable.objects.get(job=search)
                info11 = [search2.job]
                info1 = info11[0] #job no str값
                info22 = [search2.team]
                info2 = info22[0]  # team str값
                info33 = [search2.rep]
                info3 = info33[0]  # rep str값
                info44 = [search2.roomno]
                info4 = info44[0]  # roomname str값
                info55 = [search2.description]
                info5 = info55[0]  # 내용 str값
                info66 = [search2.userid]
                info6 = info66[0]  # 신청자 str값

                #이메일 내용 작성
                titletext = "수리제작의뢰서 요청승인메일 // Job No:" + info1
                emailtext = "수리제작의뢰서 Job No:" + info1 + "가 접수되었습니다." + \
                            "\n\n팀:" + info2 + "\n신청자: " + info3 + "(" + info6 + ")" + "\n위치: " + info4 + \
                            "\n요청내용: " + info5 + \
                            "\n시스템운영팀 담당자: " + userid + \
                            "\n Link : http://dmbio.synology.me:803"

            #이메일 보내기
                repemail2 = users.objects.get(userid=info6)
                repemail = [repemail2.useremail]
                email1 = EmailMessage(titletext, emailtext, to=repemail)
                email1.send()
            #status값 변경/저장
                work2 = worktable.objects.get(job=search)  # team명과 search값이 같은 항목을 필터링한다.
                work2.status = "접수"
                work2.engrep = userid
                work2.save()
                worktables = worktable.objects.all().order_by('-no')  # db 동기화
                idd2 = request.POST.get('idd2')  # html id의 값을 받는다.
                messages.error(request, "해당 Job No. 접수가 완료되었습니다.")  # 경고
                return render(request, 'popupalarm.html', {'worktables': worktables, "idd2": idd2})  # templates 내 html연결
            else:
                worktables = worktable.objects.all().order_by('-no')  # db 동기화
                idd2 = request.POST.get('idd2')  # html id의 값을 받는다.
                messages.error(request, "WARNING: [상태]값이 [신청완료]일 경우에만 진행됩니다.")  # 경고
                return render(request, 'popupalarm.html', {'worktables': worktables, "idd2": idd2})  # templates 내 html연결
        else:
            worktables = worktable.objects.all().order_by('-no')  # db 동기화
            idd2 = request.POST.get('idd2')  # html id의 값을 받는다.
            messages.error(request, "WARNING: 수리제작의뢰서 [접수]는 수리제작담당자만 가능합니다.")  # 경고
            return render(request, 'popupalarm.html', {'worktables': worktables, "idd2": idd2})  # templates 내 html연결

def popupclose(request):
    worktables = worktable.objects.all().order_by('-no')  # db 동기화
    idd2 = request.POST.get('idd2')  # html idd의 값을 받는다.
    return render(request, 'list.html', {'worktables': worktables, "idd2": idd2})  # templates 내 html연결

def delete(request): #삭제 // 완료
    if request.method =='POST': #매소드값이 post인 값만 받는다
        search = request.POST.get('cancle1') #html name2의 값을 받는다.
        idd2 = request.POST.get('idd2')  # html idd의 값을 받는다.
        idcheck1 = worktable.objects.get(job = search)
        idcheck =[idcheck1.userid]
        idcheck = idcheck[0] #userid 받아오기
        if idd2 == idcheck:
            worktable.objects.filter(job = search).delete() #team명과 search값이 같은 항목을 필터링한다.
            worktables = worktable.objects.all().order_by('-no')  # db 동기화
            return render(request, 'list.html', {'worktables': worktables, "idd2": idd2})  # templates 내 html연결
        else:
            messages.error(request, "WARNING: 신청자만 삭제가 가능합니다.")  # 경고창
            worktables = worktable.objects.all().order_by('-no')  # db 동기화
            return render(request, 'popupalarm.html', {'worktables': worktables, "idd2": idd2})  # templates 내 html연결

def teamreject(request): #삭제 // 완료
    if request.method == 'POST':  # 매소드값이 post인 값만 받는다
        status1 = request.POST.get('jobno')  # html jobno의 값을 받는다.
        reason = request.POST.get('teamrejectreason')  # html 반려사유 값을 받는다.
        status2 = worktable.objects.get(job=status1)
        statuschk =[status2.status]
        status3 = statuschk[0] #status값 받기
        teamchk =[status2.team]
        team = teamchk[0] #status값 받기
    # 팀장여부 판단하기
        namechk = request.POST.get('manager1')
        managername = manager.objects.filter(teamname=team)
        managerchk1 = managername.values('name')  # sql문 dataframe으로 변경
        df1 = pd.DataFrame.from_records(managerchk1)
        dflen1 = len(df1.index)  # 팀장 인원수 확인
        for j in range(dflen1):
            managerchk = df1.iat[j, 0]
            if namechk == managerchk:
                if status3 == "신청":  # pw값 일치하는지 확인
                    # 신청완료 정보값 변경
                    today = date.datetime.today()
                    dates = today.strftime('%y%m%d')  # 결재일 받기
                    app = "반려" + " / 20" + dates
                    status2.approval = app
                    status2.status = "반려"
                    status2.save()
                    # 메일내용 작성
                    info1 = request.POST.get('jobno')
                    info22 = [status2.team]  # 팀
                    info2 = info22[0]
                    info33 = [status2.rep]  # 신청자
                    info3 = info33[0]
                    info44 = [status2.userid]  # 신청자 아이디
                    info4 = info44[0]
                    info55 = [status2.roomno]  # 룸번호
                    info5 = info55[0]
                    info66 = [status2.description]  # 내용
                    info6 = info66[0]
                    repemail2 = users.objects.get(userid=info4)
                    repemail1 = [repemail2.useremail]
                    repemail = repemail1[0] #신청인 이메일 주소
                    #메일 내용 확정 및 메일 보내기
                    titletext = "수리제작의뢰서 요청 반려메일 // Job No:" + info1
                    emailtext = "수리제작의뢰서 Job No:" + info1 + "가 신청서가 [반려]되었습니다." + \
                            "\n\n팀:" + info2 + "\n신청자: " + info3 + "(" + info4 + ")" + "\n위치: " + info5 + \
                            "\n요청내용: " + info6 +"\n반려사유: " + reason + \
                            "\n Link : http://dmbio.synology.me:803"
                    email = EmailMessage(titletext, emailtext, to=[repemail])
                    email.send()
                    #화면 전환
                    worktables = worktable.objects.all().order_by('-no')  # db 동기화
                    idd2 = request.POST.get('idd2')  # html idd의 값을 받는다.
                    messages.error(request, "해당 Job No.가 반려처리 되었습니다.")  # 경고
                    return render(request, 'popupalarm.html', {'worktables': worktables, "idd2": idd2})  # templates 내 html연결
                else:
                    messages.error(request, "WARNING: [상태]값이 [신청]일 경우에만 진행됩니다.")  # 경고창
                    worktables = worktable.objects.all().order_by('-no')  # db 동기화
                    idd2 = request.POST.get('idd2')  # html idd의 값을 받는다.
                    return render(request, 'popupalarm.html',
                                  {'worktables': worktables, "idd2": idd2})  # templates 내 html연결
        else:
            worktables = worktable.objects.all().order_by('-no')  # db 동기화
            idd2 = request.POST.get('idd2')  # html idd의 값을 받는다.
            messages.error(request, "WARNING: 해당 Job No. 승인권한이 없습니다.")  # 경고창
            return render(request, 'popupalarm.html',
                          {'worktables': worktables, "idd2": idd2})  # templates 내 html연결

def approval(request): #삭제 // 완료
    if request.method == 'POST':  # 매소드값이 post인 값만 받는다
        status1 = request.POST.get('jobno')  # html jobno의 값을 받는다.
        status2 = worktable.objects.get(job=status1)
        statuschk =[status2.status]
        status3 = statuschk[0] #status값 받기
        teamchk =[status2.team]
        team = teamchk[0] #team값 받기

    # 팀장여부 판단하기
        namechk = request.POST.get('manager1')
        managername = manager.objects.filter(teamname=team)
        managerchk1 = managername.values('name')  # sql문 dataframe으로 변경
        df1 = pd.DataFrame.from_records(managerchk1)
        dflen1 = len(df1.index)  # 팀장 인원수 확인
        for j in range(dflen1):
            managerchk = df1.iat[j, 0]
            if namechk == managerchk:
                if status3 == "신청":  # pw값 일치하는지 확인
        #신청완료 정보값 변경
                    managers = request.POST.get('manager1')  # html 결재자 이름의 값을 받는다.
                    today = date.datetime.today()
                    dates = today.strftime('%y%m%d') #결재일 받기
                    app = managers + " / 20"+ dates
                    status2.approval = app
                    status2.status = "신청완료"
                    status2.save()
        #메일내용 작성
                    info1 = request.POST.get('jobno')
                    info22 = [status2.team] #팀
                    info2 = info22[0]
                    info33 = [status2.rep] #신청자
                    info3 = info33[0]
                    info44 = [status2.userid] #신청자 아이디
                    info4 = info44[0]
                    info55 = [status2.roomno]   #룸번호
                    info5 = info55[0]
                    info66 = [status2.description] #내용
                    info6 = info66[0]
        # level4 담당자에게 메일보내기
                    repemail2 = users.objects.filter(auth="4")  # 레벨4권한담당자한테 메일보내기
                    repemail = repemail2.values('useremail')  # sql문 dataframe으로 변경
                    df = pd.DataFrame.from_records(repemail)
                    dflen = len(df.index) #담당자 인원수 확인

        # level5에게 메일보내기
                    repemail22 = users.objects.filter(auth="5")  # 레벨4권한담당자한테 메일보내기
                    repemail2 = repemail22.values('useremail')  # sql문 dataframe으로 변경
                    df1 = pd.DataFrame.from_records(repemail2)
                    dflen1 = len(df1.index) #담당자 인원수 확인

        #메일보내기
                    info77 = [status2.roomname]
                    info7 = info77[0]
                    titletext = "수리제작의뢰서 요청메일 // Job No:" + info1
                    emailtext = "수리제작의뢰서 Job No:" + info1 + "가 신청완료되었습니다." + \
                            "\n\n팀:" + info2 + "\n신청자: " + info3 + "(" + info4 + ")" + "\n위치: " + info5 + " (" + info7 + ")" + \
                            "\n요청내용: " + info6 + \
                            "\n Link : http://dmbio.synology.me:803"

                    for k in range(dflen):
                            mailaddress = df.iat[k, 0]
                            email = EmailMessage(titletext, emailtext, to=[mailaddress])
                            email.send()
                    for j in range(dflen1):
                            mailaddress1 = df1.iat[j, 0]
                            email2 = EmailMessage(titletext, emailtext, to=[mailaddress1])
                            email2.send()

        # 신청자에게 메일보내기
                    repemail3 = users.objects.get(userid=info4)  # 레벨4권한담당자한테 메일보내기
                    info88 = [repemail3.useremail]  # 신청자 아이디
                    info8 = info88[0]
                    email1 = EmailMessage(titletext, emailtext, to=[info8])
                    email1.send()

                #화면반환
                    search2 = request.POST.get('jobno')  # html jono의 값을 받는다.
                    roomno2 = request.POST.get('roomno')  # html roomno의 값을 받는다.
                    userid1 = request.POST.get('idd2')  # html userid의 값을 받는다.
                    idd2 = request.POST.get('idd2')  # html loginid의 값을 받는다.
                    worktables = worktable.objects.all().order_by('-no')  # db 동기화
                    work2 = worktable.objects.filter(job=search2)  # team명과 search값이 같은 항목을 필터링한다.
                    roomname = room.objects.filter(roomno=roomno2)
                    user = users.objects.filter(userid=userid1)
                    idd3 = users.objects.filter(userid=idd2)
                    return render(request, 'popup.html',
                                  {'worktables': worktables, 'work2': work2, 'roomname': roomname, 'user': user, 'idd2': idd2,
                                   'idd3': idd3})
                else:
                    messages.error(request, "WARNING: [상태]값이 [신청]일 경우에만 진행됩니다.") #경고창
                    worktables = worktable.objects.all().order_by('-no')  # db 동기화
                    idd2 = request.POST.get('idd2')  # html idd의 값을 받는다.
                    return render(request, 'popupalarm.html', {'worktables': worktables, "idd2": idd2})  # templates 내 html연결
        else:
            worktables = worktable.objects.all().order_by('-no')  # db 동기화
            idd2 = request.POST.get('idd2')  # html idd의 값을 받는다.
            messages.error(request, "WARNING: 해당 Job No. 승인권한이 없습니다.")  # 경고창
            return render(request, 'popupalarm.html',  {'worktables': worktables, "idd2": idd2})  # templates 내 html연결

def popup(request):  # 수리제작 확인창
    if request.method == 'POST':  # 매소드값이 post인 값만 받는다
    #기존 값들 정보 불러오기
        search2 = request.POST.get('popup1')  # html popup1의 값을 받는다.
        roomno2 = request.POST.get('popup2')  # html popup2의 값을 받는다.
        status1 = request.POST.get('popup3')  # html popup3의 값을 받는다.
        userid1 = request.POST.get('popup4')  # html popup3의 값을 받는다.
        idd2 = request.POST.get('idd2')  # html loginid의 값을 받는다.
        if status1 == "신청":
            worktables = worktable.objects.all().order_by('-no')  # db 동기화
            work2 = worktable.objects.filter(job=search2) # team명과 search값이 같은 항목을 필터링한다.
            roomname = room.objects.filter(roomno=roomno2)
            user = users.objects.filter(userid=userid1)
            idd3 = users.objects.filter(userid=idd2)
            userinfo = users.objects.get(userid=idd2)
            userinfo1 = [userinfo.username]  # username str
            username = userinfo1[0]
            userinfo2 = [userinfo.userteam]  # team명 str
            userteam = userinfo2[0]
            signal ="signal"
            return render(request, 'popup.html',
                  {'worktables': worktables, 'work2': work2, 'roomname': roomname, 'user': user, 'idd2': idd2,
                   'idd3': idd3, "username": username, "userteam": userteam, "search2": search2, "signal":signal})

        elif status1 == "신청완료":
            worktables = worktable.objects.all().order_by('-no')  # db 동기화
            work2 = worktable.objects.filter(job=search2) # team명과 search값이 같은 항목을 필터링한다.
            roomname = room.objects.filter(roomno=roomno2)
            user = users.objects.filter(userid=userid1)
            idd3 = users.objects.filter(userid=idd2)
            userinfo = users.objects.get(userid=idd2)
            userinfo1 = [userinfo.username]  # username str
            username = userinfo1[0]
            userinfo2 = [userinfo.userteam]  # team명 str
            userteam = userinfo2[0]
            return render(request, 'popup.html', {'worktables': worktables, 'work2': work2,'roomname': roomname,'user':user,'idd2':idd2,'idd3':idd3,
                                                  "username":username, "userteam":userteam, "search2":search2})
        else:
            worktables = worktable.objects.all().order_by('-no')  # db 동기화
            work2 = worktable.objects.filter(job=search2)  # team명과 search값이 같은 항목을 필터링한다.
            roomname = room.objects.filter(roomno=roomno2)
            user = users.objects.filter(userid=userid1)
            idd3 = users.objects.filter(userid=idd2)
            userinfo = users.objects.get(userid=idd2)
            userinfo1 = [userinfo.username]  # username str
            username = userinfo1[0]
            userinfo2 = [userinfo.userteam]  # team명 str
            userteam = userinfo2[0]
            messages.error(request, "WARNING: [상태]값이 [신청or신청완료]일 경우에만 진행됩니다.") #경고
            return render(request, 'popupalarm.html', {'worktables': worktables, 'work2': work2,'roomname': roomname,'user':user,'idd2':idd2,'idd3':idd3,
                                                       "username":username, "userteam":userteam})

def popupalarm(request):  # 수리제작 확인창
    if request.method == 'POST':  # 매소드값이 post인 값만 받는다
    #기존 값들 정보 불러오기
        search2 = request.POST.get('popup1')  # html popup1의 값을 받는다.
        roomno2 = request.POST.get('popup2')  # html popup2의 값을 받는다.
        status1 = request.POST.get('popup3')  # html popup3의 값을 받는다.
        userid1 = request.POST.get('popup4')  # html popup3의 값을 받는다.
        idd2 = request.POST.get('idd2')  # html loginid의 값을 받는다.
        if status1 == "신청":
            worktables = worktable.objects.all().order_by('-no')  # db 동기화
            work2 = worktable.objects.filter(job=search2) # team명과 search값이 같은 항목을 필터링한다.
            roomname = room.objects.filter(roomno=roomno2)
            user = users.objects.filter(userid=userid1)
            idd3 = users.objects.filter(userid=idd2)
            userinfo = users.objects.get(userid=idd2)
            userinfo1 = [userinfo.username]  # username str
            username = userinfo1[0]
            userinfo2 = [userinfo.userteam]  # team명 str
            userteam = userinfo2[0]
            return render(request, 'popup.html', {'worktables': worktables, 'work2': work2,'roomname': roomname,'user':user,'idd2':idd2,'idd3':idd3,
                                                  "username":username, "userteam":userteam})
        elif status1 == "신청완료":
            worktables = worktable.objects.all().order_by('-no')  # db 동기화
            work2 = worktable.objects.filter(job=search2) # team명과 search값이 같은 항목을 필터링한다.
            roomname = room.objects.filter(roomno=roomno2)
            user = users.objects.filter(userid=userid1)
            idd3 = users.objects.filter(userid=idd2)
            userinfo = users.objects.get(userid=idd2)
            userinfo1 = [userinfo.username]  # username str
            username = userinfo1[0]
            userinfo2 = [userinfo.userteam]  # team명 str
            userteam = userinfo2[0]
            return render(request, 'popup.html', {'worktables': worktables, 'work2': work2,'roomname': roomname,'user':user,'idd2':idd2,'idd3':idd3,
                                                  "username":username, "userteam":userteam})
        else:
            worktables = worktable.objects.all().order_by('-no')  # db 동기화
            work2 = worktable.objects.filter(job=search2)  # team명과 search값이 같은 항목을 필터링한다.
            roomname = room.objects.filter(roomno=roomno2)
            user = users.objects.filter(userid=userid1)
            idd3 = users.objects.filter(userid=idd2)
            userinfo = users.objects.get(userid=idd2)
            userinfo1 = [userinfo.username]  # username str
            username = userinfo1[0]
            userinfo2 = [userinfo.userteam]  # team명 str
            userteam = userinfo2[0]
            messages.error(request, "WARNING: [상태]값이 [신청or신청완료]일 경우에만 진행됩니다.") #경고
            return render(request, 'popupalarm.html', {'worktables': worktables, 'work2': work2,'roomname': roomname,'user':user,'idd2':idd2,'idd3':idd3,
                                                       "username":username, "userteam":userteam})

def update(request):
    return render(request, 'update.html')

def changecomp(request):
    if request.method == 'POST':  # 매소드값이 post인 값만 받는다
      #변경값받기
        jobnochange = request.POST.get('jobno')
        repchange = request.POST.get('rep')
        useridchange = request.POST.get('userid')
        teamchange = request.POST.get('team')
        roomnochange = request.POST.get('roomno')
        descriptionchange = request.POST.get('description')
      #room name불러오기
        rooms = room.objects.get(roomno=roomnochange)  # db 동기화
        roominfo1 = [rooms.roomname]
        roomnamechange = roominfo1[0] # roomname str
      #데이터 저장
        worktables = worktable.objects.get(job=jobnochange)  # db 동기화
        worktables.rep = repchange
        worktables.userid = useridchange
        worktables.team = teamchange
        worktables.roomno= roomnochange
        worktables.roomname = roomnamechange
        worktables.description= descriptionchange
        worktables.save()
    return render(request, 'changefinish.html')  # templates 내 html연결



##############################################################################################################
#################################################사무용품신청###################################################
##############################################################################################################

def supply(request): #사무용품신청
    if request.method =='POST': #매소드값이 post인 값만 받는다
        idd2 = request.POST.get('idd2')  # html loginid 값을 받는다.
        return render(request, 'supply.html', {"idd2": idd2}) #templates 내 html연결

def upload(request):
    if "file1" in request.FILES:
        #파일 업로드 하기!!!
        file1 = request.FILES["file1"]
        print(file1.name)
        print(file1.name[-3:]) #파일 확장명 추출하기
        fs = FileSystemStorage()
        name = fs.save(file1.name, file1) #파일저장 // 이름저장
        #파일 읽어오기!!!
        url = fs.url(name)
        print(url)
        context = {'url': url}
    else:
        file_name ="-"
    return render(request, 'supply.html', context)


def mysqltest(request): #메인홈 // 완료
    return render(request, 'mysqltest.html') #templates 내 html연결

def mysqltable(request): #메인홈 // 완료
    username = request.GET.get('username')  # html idd의 값을 받는다.
    print(username)
    worktables = worktable.objects.filter(rep = username)  # db 동기화
    return render(request, 'mysqltable.html', {"worktables":worktables}) #templates 내 html연결
