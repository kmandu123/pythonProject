from django.contrib import admin

# Register your models here.
from resume.models import Comm_div, Comm_code, Employee, School_his, License_his, Work_his, Education, Edu_his, Order_comp, Pjt, Pjt_his

# 마스터-detail 처리를 위해
class Comm_codeInline(admin.TabularInline):
    model = Comm_code
    extra = 0
    fields = ('comm_code_name', 'display_order', 'use_yn', 'summary')

# 마스터-detail 처리를 위해
class School_hisInline(admin.TabularInline):
    model = School_his
    extra = 0
    exclude = ['school_his_id']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "evidence_status_cd":
            kwargs["queryset"] = Comm_code.objects.filter(comm_div_name='증빙점검')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# 마스터-detail 처리를 위해
class Work_hisInline(admin.TabularInline):
    model = Work_his
    extra = 0
    exclude = ['work_his_id']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "evidence_status_cd":
            kwargs["queryset"] = Comm_code.objects.filter(comm_div_name='증빙점검')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# 마스터-detail 처리를 위해
class Edu_hisInline(admin.TabularInline):
    model = Edu_his
    extra = 0
    exclude = ['edu_his_id']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "evidence_status_cd":
            kwargs["queryset"] = Comm_code.objects.filter(comm_div_name='증빙점검')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# 마스터-detail 처리를 위해
class License_hisInline(admin.TabularInline):
    model = License_his
    extra = 0
    exclude = ['license_his_id']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "license_cd":
            kwargs["queryset"] = Comm_code.objects.filter(comm_div_name='자격증')
        elif db_field.name == "evidence_status_cd":
            kwargs["queryset"] = Comm_code.objects.filter(comm_div_name='증빙점검')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# 마스터-detail 처리를 위해
class PjtInline(admin.TabularInline):
    model = Pjt
    extra = 0
    exclude = ['pjt_id']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "pjt_type":
            kwargs["queryset"] = Comm_code.objects.filter(comm_div_name='프로젝트 형태')
        elif db_field.name == "pjt_location":
            kwargs["queryset"] = Comm_code.objects.filter(comm_div_name='프로젝트 장소')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# 마스터-detail 처리를 위해
class Pjt_hisInline(admin.TabularInline):
    model = Pjt_his
    extra = 0
    exclude = ['pjt_his_id']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "kosa_conf":
            kwargs["queryset"] = Comm_code.objects.filter(comm_div_name='KOSA 증빙')
        elif db_field.name == "insurance_conf":
            kwargs["queryset"] = Comm_code.objects.filter(comm_div_name='건강보험 확인')
        elif db_field.name == "his_status":
            kwargs["queryset"] = Comm_code.objects.filter(comm_div_name='이력상태')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)







@admin.register(Comm_div)
class Comm_divAdmin(admin.ModelAdmin):
    list_display = ('comm_div_name', 'summary')
    inlines = [Comm_codeInline]
    exclude = ('create_id','update_id')

@admin.register(Comm_code)
class Comm_codeAdmin(admin.ModelAdmin):
    list_display = ('comm_div_id', 'comm_code_name', 'display_order', 'use_yn', 'summary')
    list_filter = ('comm_div_id', )


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "emp_position_cd":
            kwargs["queryset"] = Comm_code.objects.filter(comm_div_name='직위')
        elif db_field.name == "skill_grade_cd":
            kwargs["queryset"] = Comm_code.objects.filter(comm_div_name='등급')
        elif db_field.name == "evidence_method_cd":
            kwargs["queryset"] = Comm_code.objects.filter(comm_div_name='경력 증빙 점검 방법')
        elif db_field.name == "skill_etl":
            kwargs["queryset"] = Comm_code.objects.filter(comm_div_name='기술 ETL')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    inlines = [School_hisInline, License_hisInline, Work_hisInline, Edu_hisInline]
    list_display = ('emp_name', 'emp_position_cd', 'skill_grade_cd', 'indate')



@admin.register(School_his)
class School_hisAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "evidence_status_cd":
            kwargs["queryset"] = Comm_code.objects.filter(comm_div_name='증빙점검')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(License_his)
class License_hisAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "license_cd":
            kwargs["queryset"] = Comm_code.objects.filter(comm_div_name='자격증')
        elif db_field.name == "evidence_status_cd":
            kwargs["queryset"] = Comm_code.objects.filter(comm_div_name='증빙점검')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



@admin.register(Work_his)
class Work_hisAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "evidence_status_cd":
            kwargs["queryset"] = Comm_code.objects.filter(comm_div_name='증빙점검')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "evidence_status_cd":
            kwargs["queryset"] = Comm_code.objects.filter(comm_div_name='증빙점검')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    inlines = [Edu_hisInline]
    list_display = ('edu_name', 'agency_name', 'edu_start_date', 'edu_end_date')


@admin.register(Edu_his)
class Edu_hisAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "evidence_status_cd":
            kwargs["queryset"] = Comm_code.objects.filter(comm_div_name='증빙점검')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Order_comp)
class Order_compAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "indus":
            kwargs["queryset"] = Comm_code.objects.filter(comm_div_name='업종')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    inlines = [PjtInline]


@admin.register(Pjt)
class PjtAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "pjt_type":
            kwargs["queryset"] = Comm_code.objects.filter(comm_div_name='프로젝트 형태')
        elif db_field.name == "pjt_location":
            kwargs["queryset"] = Comm_code.objects.filter(comm_div_name='프로젝트 장소')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    inlines = [Pjt_hisInline]
    list_filter = ('order_comp_id', )





@admin.register(Pjt_his)
class Pjt_hisAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "kosa_conf":
            kwargs["queryset"] = Comm_code.objects.filter(comm_div_name='KOSA 증빙')
        elif db_field.name == "insurance_conf":
            kwargs["queryset"] = Comm_code.objects.filter(comm_div_name='건강보험 확인')
        elif db_field.name == "his_status":
            kwargs["queryset"] = Comm_code.objects.filter(comm_div_name='이력상태')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
