from django.db import models
#from django.db.models import Max
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.core.validators import MinLengthValidator

from uuid import uuid4
from datetime import datetime


# Create your models here.

class Comm_div(models.Model):
    comm_div_id = models.AutoField(primary_key=True, verbose_name='공통코드 구분 ID')
    comm_div_name = models.CharField(max_length=200, verbose_name='공통코드 구분')
    summary = models.CharField(max_length=2000, null=True, blank=True, verbose_name='비고')
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='생성일시', null=True, blank=True)
    update_dt = models.DateTimeField(auto_now=True, verbose_name='수정일시', null=True, blank=True)
    create_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='생성자id')
    update_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='수정자id')

    class Meta:
        managed = False

    def __str__(self):
        """String for representing the Model object."""
        return self.comm_div_name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('comm_div_update', args=[str(self.comm_div_id)])

class Comm_code(models.Model):
    comm_code = models.AutoField(primary_key=True, verbose_name='공통코드')
    comm_div_id = models.ForeignKey('Comm_div', related_name='fk_comm_code1', on_delete=models.SET_NULL, db_column='comm_div_id',  null=True)
    comm_code_name = models.CharField(max_length=200, verbose_name='공통코드명')
    ref_field = models.CharField(max_length=200, null=True, blank=True, verbose_name='참조필드')
    display_order = models.IntegerField(null=True, blank=True, verbose_name='표시 순서')


    USE_YN_DIV = (
        ('Y', 'Y'),
        ('N', 'N'),
    )

    use_yn = models.CharField(max_length=1, choices=USE_YN_DIV, default='Y', verbose_name='사용여부')
    summary = models.CharField(max_length=2000, null=True, blank=True, verbose_name='비고')
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='생성일시', null=True, blank=True)
    update_dt = models.DateTimeField(auto_now=True, verbose_name='수정일시', null=True, blank=True)
    create_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='생성자id')
    update_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='수정자id')

    class Meta:
        managed = False

    def __str__(self):
        """String for representing the Model object."""
        return self.comm_code_name


class Employee(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    emp_id = models.AutoField(primary_key=True, verbose_name='사원ID')
    emp_position_cd = models.ForeignKey('Comm_code', related_name='fk_employee1', on_delete=models.SET_NULL, null=True, db_column='emp_position_cd',  verbose_name='직위')
    emp_name = models.CharField(max_length=200, verbose_name='사원명')
    skill_grade_cd = models.ForeignKey('Comm_code', related_name='fk_employee2', on_delete=models.SET_NULL, null=True, db_column='skill_grade_cd', verbose_name='등급')

    GENDER_DIV = (
        ('m', '남'),
        ('f', '여'),
    )

    gender = models.CharField(max_length=1, choices=GENDER_DIV, default='m', verbose_name='성별')
    birthdate = models.DateField(verbose_name='생년월일', null=True)
    mobile_no = models.CharField(max_length=50, null=True, blank=True, verbose_name='모바일번호')
    emergency_telno = models.CharField(max_length=50, null=True, blank=True, verbose_name='비상연락처')
    emergency_rel = models.CharField(max_length=50, null=True, blank=True, verbose_name='비상연락처 관계')
    email_addr = models.EmailField(max_length=254, null=True, blank=True, verbose_name='이메일')
    postno = models.CharField(max_length=50, null=True, blank=True, verbose_name='우편번호')
    addr = models.CharField(max_length=400, null=True, blank=True, verbose_name='주소')
    addr_dtl = models.CharField(max_length=200, null=True, blank=True, verbose_name='상세주소')
    indate = models.DateField(verbose_name='입사일자', null=True)
    outdate = models.DateField(null=True, blank=True, verbose_name='퇴사일자')
    work_base_date = models.DateField(null=True, blank=True, verbose_name='경력 기간 산정 기준일')
    work_base_year = models.IntegerField(null=True, blank=True, verbose_name='기초 경력 년수')
    work_base_month = models.IntegerField(null=True, blank=True, verbose_name='기초 경력 개월수')
    evidence_method_cd = models.ForeignKey('Comm_code', related_name='fk_employee3', on_delete=models.SET_NULL, null=True, blank=True,
                                           db_column='evidence_method_cd', verbose_name='경력 증빙 점검 방법')

    skill_hw_cd = models.ManyToManyField('Comm_code', related_name='mk_employee1',  blank=True, db_column='skill_hw_cd', verbose_name='하드웨어')
    skill_os_cd = models.ManyToManyField('Comm_code', related_name='mk_employee2',  blank=True, db_column='skill_os_cd', verbose_name='운영체제')
    skill_olap_cd = models.ManyToManyField('Comm_code', related_name='mk_employee3',  blank=True, db_column='skill_olap_cd', verbose_name='OLAP/UI')
    skill_etl_cd = models.ManyToManyField('Comm_code', related_name='mk_employee4',  blank=True, db_column='skill_etl_cd', verbose_name='ETL')
    skill_dev_cd = models.ManyToManyField('Comm_code', related_name='mk_employee5',  blank=True, db_column='skill_dev_cd', verbose_name='개발언어')
    skill_db_cd = models.ManyToManyField('Comm_code', related_name='mk_employee6',  blank=True, db_column='skill_db_cd', verbose_name='데이터베이스')
    skill_was_cd = models.ManyToManyField('Comm_code', related_name='mk_employee7',  blank=True, db_column='skill_was_cd', verbose_name='개발플랫폼(WAS)')

    skill_main = models.CharField(max_length=2000, null=True, blank=True, verbose_name='전문분야')
    skill_major = models.CharField(max_length=2000, null=True, blank=True, verbose_name='주요사업')

    summary = models.CharField(max_length=2000, null=True, blank=True, verbose_name='비고')
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='생성일시', null=True, blank=True)
    update_dt = models.DateTimeField(auto_now=True, verbose_name='수정일시', null=True, blank=True)
    create_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='생성자id')
    update_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='수정자id')

    class Meta:
        managed = False

    def __str__(self):
        """String for representing the Model object."""
        return self.emp_name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('employee_update', args=[str(self.emp_id)])

#    def formfield_for_foreignkey(self, db_field, request, **kwargs):
#        if db_field.name == "emp_position_cd":
#            kwargs["queryset"] = Comm_code.objects.filter(comm_div_id=1)
#        elif db_field.name == "skill_grade_cd":
#            kwargs["queryset"] = Comm_code.objects.filter(comm_div_id=2)
#        elif db_field.name == "evidence_method_cd":
#            kwargs["queryset"] = Comm_code.objects.filter(comm_div_id=3)
#        elif db_field.name == "skill_hw_cd":
#            kwargs["queryset"] = Comm_code.objects.filter(comm_div_id=6)
#        elif db_field.name == "skill_os_cd":
#            kwargs["queryset"] = Comm_code.objects.filter(comm_div_id=7)
#        elif db_field.name == "skill_olap_cd":
#            kwargs["queryset"] = Comm_code.objects.filter(comm_div_id=8)
#        elif db_field.name == "skill_etl_cd":
#            kwargs["queryset"] = Comm_code.objects.filter(comm_div_id=9)
#        elif db_field.name == "skill_dev_cd":
#            kwargs["queryset"] = Comm_code.objects.filter(comm_div_id=10)
#        elif db_field.name == "skill_db_cd":
#            kwargs["queryset"] = Comm_code.objects.filter(comm_div_id=11)
#        elif db_field.name == "skill_was_cd":
#            kwargs["queryset"] = Comm_code.objects.filter(comm_div_id=12)
#        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class School_his(models.Model):
    school_his_id = models.AutoField(primary_key=True, verbose_name='학력이력ID')
    emp_id = models.ForeignKey('Employee', related_name='fk_school_his1', on_delete=models.SET_NULL, null=True, db_column='emp_id', verbose_name='사원')
    school_name = models.CharField(max_length=200, verbose_name='학교')
    school_subject = models.CharField(max_length=200, verbose_name='학과')
    graduate_date = models.DateField(verbose_name='졸업일자',null=True, blank=True)
    evidence_status_cd = models.ForeignKey('Comm_code', related_name='fk_school_his2', on_delete=models.SET_NULL, null=True, blank=True, db_column='evidence_status_cd', verbose_name='증빙점검')
    summary = models.CharField(max_length=2000, null=True, blank=True, verbose_name='비고')
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='생성일시', null=True, blank=True)
    update_dt = models.DateTimeField(auto_now=True, verbose_name='수정일시', null=True, blank=True)
    create_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='비고')
    update_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='비고')

    class Meta:
        managed = False

    def __str__(self):
        """String for representing the Model object."""
        return self.school_name


class License_his(models.Model):
    license_his_id = models.AutoField(primary_key=True, verbose_name='자격증이력ID')
    emp_id = models.ForeignKey('Employee', related_name='fk_license_his1', on_delete=models.SET_NULL, null=True, db_column='emp_id', verbose_name='사원')
    license_cd = models.ForeignKey('Comm_code', related_name='fk_license_his2', on_delete=models.SET_NULL, null=True, blank=True, db_column='license_cd', verbose_name='자격증')
    got_date = models.DateField(verbose_name='취득일',null=True)
    evidence_status_cd = models.ForeignKey('Comm_code', related_name='fk_license_his3', on_delete=models.SET_NULL, null=True, blank=True, db_column='evidence_status_cd', verbose_name='증빙점검')
    summary = models.CharField(max_length=2000, null=True, blank=True, verbose_name='비고')
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='생성일시', null=True, blank=True)
    update_dt = models.DateTimeField(auto_now=True, verbose_name='수정일시', null=True, blank=True)
    create_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='생성자id')
    update_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='수정자id')

    class Meta:
        managed = False

    def __str__(self):
        """String for representing the Model object."""
        return str(self.license_his_id)


class Work_his(models.Model):
    work_his_id = models.AutoField(primary_key=True, verbose_name='경력이력ID')
    emp_id = models.ForeignKey('Employee', related_name='fk_work_his1', on_delete=models.SET_NULL, null=True, db_column='emp_id', verbose_name='사원')
    company_name = models.CharField(max_length=200, verbose_name='회사명')
    work_start_date = models.DateField(verbose_name='경력시작일자', null=True)
    work_end_date = models.DateField(verbose_name='경력종료일자', null=True, blank=True)
    emp_position = models.CharField(max_length=200, verbose_name='직위')
    work_part = models.CharField(max_length=200, verbose_name='담당업무')
    evidence_status_cd = models.ForeignKey('Comm_code', related_name='fk_work_his2', on_delete=models.SET_NULL, null=True, blank=True, db_column='evidence_status_cd', verbose_name='증빙점검')
    summary = models.CharField(max_length=2000, null=True, blank=True, verbose_name='비고')
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='생성일시', null=True, blank=True)
    update_dt = models.DateTimeField(auto_now=True, verbose_name='수정일시', null=True, blank=True)
    create_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='생성자id')
    update_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='수정자id')

    class Meta:
        managed = False

    def __str__(self):
        """String for representing the Model object."""
        return self.company_name


class Education(models.Model):
    edu_id = models.AutoField(primary_key=True, verbose_name='교육ID')
    edu_name = models.CharField(max_length=200, verbose_name='교육명')
    edu_start_date = models.DateField(verbose_name='시작일', null=True)
    edu_end_date = models.DateField(verbose_name='종료일', null=True)

    USE_YN_DIV = (
        ('Y', 'Y'),
        ('N', 'N'),
    )

    request_yn = models.CharField(max_length=1, choices=USE_YN_DIV, verbose_name='위탁교육')
    agency_name = models.CharField(max_length=200, verbose_name='기관명')
    summary = models.CharField(max_length=2000, null=True, blank=True, verbose_name='비고')
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='생성일시', null=True, blank=True)
    update_dt = models.DateTimeField(auto_now=True, verbose_name='수정일시', null=True, blank=True)
    create_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='생성자id')
    update_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='수정자id')

    class Meta:
        managed = False
        # Resume app 사용자에게 부여할 권한 생성(Resume app의 model중에 하나의 model에 선언하면 공용으로 사용할 수 있음
        permissions = [
            ('private_closed', 'Private closed'), ('private_open', 'Private open'), ('public_closed', 'Public closed'), ('public_open', 'Public open')
        ]

    def __str__(self):
        """String for representing the Model object."""
        return self.edu_name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('education_update', args=[str(self.edu_id)])


class Edu_his(models.Model):
    edu_his_id = models.AutoField(primary_key=True, verbose_name='교육이력ID')
    emp_id = models.ForeignKey('Employee', related_name='fk_edu_his1', on_delete=models.SET_NULL, null=True, db_column='emp_id', verbose_name='사원')
    edu_id = models.ForeignKey('Education', related_name='fk_edu_his2', on_delete=models.SET_NULL, null=True, db_column='edu_id', verbose_name='교육')
    evidence_status_cd = models.ForeignKey('Comm_code', related_name='fk_edu_his3', on_delete=models.SET_NULL, null=True, blank=True, db_column='evidence_status_cd', verbose_name='증빙점검')
    summary = models.CharField(max_length=2000, null=True, blank=True, verbose_name='비고')
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='생성일시', null=True, blank=True)
    update_dt = models.DateTimeField(auto_now=True, verbose_name='수정일시', null=True, blank=True)
    create_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='생성자id')
    update_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='수정자id')

    class Meta:
        managed = False

    def __str__(self):
        """String for representing the Model object."""
        return str(self.edu_his_id)


class Order_comp(models.Model):
    order_comp_id = models.AutoField(primary_key=True, verbose_name='발추처ID')
    order_comp_name = models.CharField(max_length=200, verbose_name='발주처')
    indus_cd = models.ForeignKey('Comm_code', related_name='fk_order_comp1', on_delete=models.SET_NULL, null=True, db_column='indus_cd', verbose_name='고객사 업종')
    summary = models.CharField(max_length=2000, null=True, blank=True, verbose_name='비고')
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='생성일시', null=True, blank=True)
    update_dt = models.DateTimeField(auto_now=True, verbose_name='수정일시', null=True, blank=True)
    create_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='생성자id')
    update_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='수정자id')

    class Meta:
        managed = False

    def __str__(self):
        """String for representing the Model object."""
        return self.order_comp_name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('order_comp_update', args=[str(self.order_comp_id)])


# 컬럼에 대한 추가 validation 처리
title_validator = MinLengthValidator(3, "길이가 너무 짧습니다.")

class Pjt(models.Model):
    pjt_id = models.AutoField(primary_key=True, verbose_name='프로젝트ID')
    order_comp_id = models.ForeignKey('Order_comp', related_name='fk_pjt1', on_delete=models.SET_NULL, null=True, db_column='order_comp_id', verbose_name='발주처ID')
    pjt_name = models.CharField(max_length=200, verbose_name='사업명', validators=[title_validator])
    pjt_type_cd = models.ForeignKey('Comm_code', related_name='fk_pjt2', on_delete=models.SET_NULL, null=True, db_column='pjt_type_cd', verbose_name='프로젝트 형태')
    pjt_start_date = models.DateField(verbose_name='프로젝트 시작일자', null=True, blank=True)
    pjt_end_date = models.DateField(verbose_name='프로젝트 종료일자', null=True, blank=True)
    use_skill = models.CharField(max_length=500, null=True, blank=True, verbose_name='개발환경')
    pjt_location_cd = models.ForeignKey('Comm_code', related_name='fk_pjt3', on_delete=models.SET_NULL, null=True, blank=True, db_column='pjt_location_cd', verbose_name='프로젝트수행장소')
    summary = models.CharField(max_length=2000, null=True, blank=True, verbose_name='비고')
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='생성일시', null=True, blank=True)
    update_dt = models.DateTimeField(auto_now=True, verbose_name='수정일시', null=True, blank=True)
    create_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='생성자id')
    update_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='수정자id')

    class Meta:
        managed = False

    def __str__(self):
        """String for representing the Model object."""
        return self.pjt_name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('pjt_update', args=[str(self.pjt_id)])


class Pjt_his(models.Model):
    pjt_his_id = models.AutoField(primary_key=True, verbose_name='프로젝트이력ID')
    emp_id = models.ForeignKey('Employee', related_name='fk_pjt_his1', on_delete=models.SET_NULL, null=True, db_column='emp_id', verbose_name='사원')
    pjt_id = models.ForeignKey('pjt', related_name='fk_pjt_his2', on_delete=models.SET_NULL, null=True, db_column='pjt_id', verbose_name='프로젝트ID')
    company_name = models.CharField(max_length=200, verbose_name='근무처')
    join_start_date = models.DateField(verbose_name='참여 시작일자', null=True)
    join_end_date = models.DateField(verbose_name='참여 종료일자', null=True)
    kosa_conf_cd = models.ForeignKey('Comm_code', related_name='fk_pjt_his3', on_delete=models.SET_NULL, null=True, blank=True, db_column='kosa_conf_cd', verbose_name='KOSA 증빙')
    pjt_role = models.CharField(max_length=200, null=True, verbose_name='프로젝트 역할')
    insurance_conf_cd = models.ForeignKey('Comm_code', related_name='fk_pjt_his4', on_delete=models.SET_NULL, null=True, blank=True, db_column='insurance_conf_cd', verbose_name='건강보험 확인')
    his_status_cd = models.ForeignKey('Comm_code', related_name='fk_pjt_his5', on_delete=models.SET_NULL, null=True, blank=True, db_column='his_status_cd', verbose_name='이력상태')
    summary = models.CharField(max_length=2000, null=True, blank=True, verbose_name='비고')
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='생성일시', null=True, blank=True)
    update_dt = models.DateTimeField(auto_now=True, verbose_name='수정일시', null=True, blank=True)
    create_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='생성자id')
    update_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='수정자id')

    class Meta:
        managed = False

    def __str__(self):
        """String for representing the Model object."""
        return str(self.pjt_his_id)


class Vw_emp(models.Model):
    EMP_ID = models.IntegerField(primary_key=True, verbose_name='사번')
    POSITION_NAME = models.CharField(max_length=200, verbose_name='직위')
    EMP_NAME = models.CharField(max_length=200, verbose_name='사원명')
    SKILL_GRADE = models.CharField(max_length=200, verbose_name='등급')
    AVAIL_STATE = models.CharField(max_length=200, verbose_name='가동상태')
    AVAIL_MONTH = models.CharField(max_length=200, verbose_name='투입가능 시점')
    GENDER = models.CharField(max_length=200, verbose_name='성별')
    BIRTHDATE = models.DateField(verbose_name='생년월일')
    AGE = models.CharField(max_length=200, verbose_name='연령(만)')
    JUMIN = models.CharField(max_length=200, verbose_name='주민번호')
    LAST_SCHOOL = models.CharField(max_length=200, verbose_name='최종학력')
    ADDR = models.CharField(max_length=200, verbose_name='주소')
    INDATE = models.DateField(verbose_name='입사일자')
    OUTDATE = models.DateField(verbose_name='퇴사일자')
    INDATE_PERIOD = models.CharField(max_length=200, verbose_name='입사일 기준 경력 기간')
    OTHER_COMP_YN = models.CharField(max_length=200, verbose_name='타사경력 존재여부')
    TOTAL_PERIOD = models.CharField(max_length=200, verbose_name='전체 경력 기간')
    EVIDENCE_METHOD = models.CharField(max_length=200, verbose_name='경력 증빙 점검 방법')
    INFO_LICENSE_YN = models.CharField(max_length=200, verbose_name='정보처리기사')
    OTHER_LICENSE = models.CharField(max_length=1000, verbose_name='기타 자격증')
    REQUEST_YN_YN = models.CharField(max_length=200, verbose_name='위탁교육')
    OTHER_EDU = models.CharField(max_length=1000, verbose_name='기타교육')
    SUMMARY = models.CharField(max_length=2000, verbose_name='비고')

    class Meta:
        managed = False
        db_table = "vw_emp"

class Intro(models.Model):
    intro_id = models.AutoField(primary_key=True, verbose_name='introId')
    intro = models.CharField(max_length=2000, null=True, blank=True, verbose_name='내용')
    display_yn = models.CharField(max_length=10, verbose_name='표시여부')
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='생성일시', null=True, blank=True)
    update_dt = models.DateTimeField(auto_now=True, verbose_name='수정일시', null=True, blank=True)
    create_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='생성자id')
    update_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='수정자id')

    class Meta:
        managed = False

    def __str__(self):
        """String for representing the Model object."""
        return str(self.intro_id)

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('intro_update', args=[str(self.intro_id)])


#아래 model에 이미지 파일 upload하기 위해 경로 및 파일명 추출 하기 위한 함수 선언함.
def get_file_path(instance, filename):
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    return '/'.join(['upload_file/', ymd_path, uuid_name])


class Talk_mst(models.Model):
    talk_mst_id = models.AutoField(primary_key=True, verbose_name='talk_master ID')
    talk_class = models.CharField(max_length=200, verbose_name='talk 분류')
    talk_subject = models.CharField(max_length=200, verbose_name='talk 주제')
    talk_content = models.CharField(max_length=2000, null=True, blank=True, verbose_name='talk 내용')
    upload_files = models.FileField(upload_to=get_file_path, null=True, blank=True, verbose_name='파일')
    filename = models.CharField(max_length=64, null=True, verbose_name='첨부파일명')
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='생성일시', null=True, blank=True)
    update_dt = models.DateTimeField(auto_now=True, verbose_name='수정일시', null=True, blank=True)
    create_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='생성자id')
    update_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='수정자id')

    class Meta:
        managed = True

    def __str__(self):
        """String for representing the Model object."""
        return self.talk_subject

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('favorite_location_update', args=[str(self.talk_mst_id)])

class Talk_dtl(models.Model):
    talk_dtl_id = models.AutoField(primary_key=True, verbose_name='talk_detail ID')
    talk_mst_id = models.ForeignKey('Talk_mst', related_name='fk_talk_dtl1', on_delete=models.SET_NULL, db_column='talk_mst_id',  null=True)
    dtl_content = models.CharField(max_length=2000,  verbose_name='detail 내용')
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='생성일시', null=True, blank=True)
    update_dt = models.DateTimeField(auto_now=True, verbose_name='수정일시', null=True, blank=True)
    create_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='생성자id')
    update_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='수정자id')

    class Meta:
        managed = True

    def __str__(self):
        """String for representing the Model object."""
        return self.dtl_content
