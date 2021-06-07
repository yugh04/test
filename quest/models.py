from django.db import models

# Create your models here.

class worktable(models.Model): #수리제작의뢰서 테이블
    no = models.AutoField(primary_key=True)
    job = models.CharField(max_length=30)
    team = models.CharField(max_length=255)
    rep = models.CharField(max_length=255)
    roomname = models.CharField(max_length=255, default="")
    roomno = models.CharField(max_length=50)
    description = models.TextField()
    summary = models.TextField(default="미완료")
    status = models.CharField(max_length=50, default="신청")
    userid = models.CharField(max_length=64)
    approval = models.CharField(max_length=64, default="미승인")
    check = models.CharField(max_length=64, default="미승인")
    engrep = models.CharField(max_length=64, default="미지정")
    date = models.CharField(max_length=64, default="")
    finish_date = models.CharField(max_length=64, default="미완료")
    division = models.CharField(max_length=64, default="")
    get_date = models.CharField(max_length=64, default="미접수")
    attached_file = models.CharField(max_length=255)
    reason = models.TextField()
    attached_tag = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'worktable'

class users(models.Model): # 유저 테이블
    no = models.AutoField(primary_key=True)
    userid = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    userteam = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    useremail = models.CharField(max_length=255)
    usertel = models.CharField(max_length=255)
    auth = models.CharField(max_length=255)
    password_date = models.DateField()
    fail_count = models.CharField(max_length=255, default=0)
    login_lock = models.CharField(max_length=255, default="Unlock")

    class Meta:
        managed = False
        db_table = "users"

class room(models.Model): #룸이름 룸번호 테이블
    no = models.AutoField(primary_key=True)
    roomname = models.CharField(max_length=45)
    roomno = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'room'

class manager(models.Model): #팀장 테이블
    no = models.AutoField(primary_key=True)
    teamname = models.CharField(max_length=45)
    name = models.CharField(max_length=45)
    id = models.CharField(max_length=64)
    email = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'manager'



