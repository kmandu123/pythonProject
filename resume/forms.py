from django import forms
from .models import Comm_div, Comm_code, Employee, School_his, License_his, Work_his, Education, Edu_his, Order_comp, Pjt, Pjt_his
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError

class Comm_divForm(forms.ModelForm):
# 필드별로 재정의할때
#    comm_div_name = forms.CharField(max_length=200, label='공통코드 구분', widget=forms.TextInput(attrs={'autocomplete':'off', 'size':'30'}))
#    summary = forms.CharField(max_length=2000, label='비고', widget=forms.TextInput(attrs={'autocomplete':'off', 'size':'50'}))

    class Meta:
        model = Comm_div
        fields = ('comm_div_id',  'comm_div_name', 'summary', 'create_id', 'update_id')

#속성별로 재정의 할때
        widgets = {
            'comm_div_name': forms.TextInput(attrs={'autocomplete':'off', 'size':'30'}),
            'summary': forms.TextInput(attrs={'autocomplete':'off', 'size':'50'}),
        }

        labels = {
            'comm_div_name': '이름',
            'summary': '비고',
        }



class Comm_codeForm(forms.ModelForm):
    class Meta:
        model = Comm_code
        fields = '__all__'

        widgets = {
            'display_order': forms.TextInput(attrs={'autocomplete': 'off', 'size': '2'}),
            'summary': forms.Textarea(attrs={'autocomplete': 'off', 'cols': '63', 'rows': '1'}),
        }



 # detail form 객체 생성
Comm_codeFormset = inlineformset_factory(Comm_div, Comm_code, form=Comm_codeForm,
                    extra=1, can_delete=True)



class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
#        fields = ('emp_id',  'emp_position_cd', 'emp_name', 'skill_grade_cd', 'gender', 'birthdate', 'mobile_no')

        # 속성별로 재정의 할때
        widgets = {
            'birthdate': forms.TextInput(attrs={'class': 'cal', 'autocomplete': 'off', 'size': '10'}),
            'indate': forms.TextInput(attrs={'class': 'cal', 'autocomplete': 'off', 'size': '10'}),
            'outdate': forms.TextInput(attrs={'class': 'cal', 'autocomplete': 'off', 'size': '10'}),
            'work_base_date': forms.TextInput(attrs={'class': 'cal', 'autocomplete': 'off', 'size': '10'}),
            'addr': forms.TextInput(attrs={'autocomplete': 'off', 'size': '60'}),
            'addr_dtl': forms.TextInput(attrs={'autocomplete': 'off', 'size': '60'}),
            'emp_name': forms.TextInput(attrs={'autocomplete': 'off', 'size': '10'}),
            'postno': forms.TextInput(attrs={'autocomplete': 'off', 'size': '10'}),
            'work_base_year': forms.TextInput(attrs={'autocomplete': 'off', 'size': '3'}),
            'work_base_month': forms.TextInput(attrs={'autocomplete': 'off', 'size': '3'}),
            'skill_main': forms.Textarea(attrs={'autocomplete': 'off', 'cols': '63', 'rows': '3'}),
            'skill_major': forms.Textarea(attrs={'autocomplete': 'off', 'cols': '66', 'rows': '3'}),
            'summary': forms.Textarea(attrs={'autocomplete': 'off', 'cols': '63', 'rows': '2'}),

            'skill_hw_cd': forms.SelectMultiple(attrs={'size': '10'}),
            'skill_os_cd': forms.SelectMultiple(attrs={'size': '10'}),
            'skill_olap_cd': forms.SelectMultiple(attrs={'size': '10'}),
            'skill_etl_cd': forms.SelectMultiple(attrs={'size': '10'}),
            'skill_dev_cd': forms.SelectMultiple(attrs={'size': '10'}),
            'skill_db_cd': forms.SelectMultiple(attrs={'size': '10'}),
            'skill_was_cd': forms.SelectMultiple(attrs={'size': '10'}),
        }

    # fk로 설정된 공통코드 구분 필터링 정의
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['emp_position_cd'].queryset = Comm_code.objects.filter(comm_div_id=1)
        self.fields['skill_grade_cd'].queryset = Comm_code.objects.filter(comm_div_id=2)
        self.fields['evidence_method_cd'].queryset = Comm_code.objects.filter(comm_div_id=3)
        self.fields['skill_hw_cd'].queryset = Comm_code.objects.filter(comm_div_id=6)
        self.fields['skill_os_cd'].queryset = Comm_code.objects.filter(comm_div_id=7)
        self.fields['skill_olap_cd'].queryset = Comm_code.objects.filter(comm_div_id=8)
        self.fields['skill_etl_cd'].queryset = Comm_code.objects.filter(comm_div_id=9)
        self.fields['skill_dev_cd'].queryset = Comm_code.objects.filter(comm_div_id=10)
        self.fields['skill_db_cd'].queryset = Comm_code.objects.filter(comm_div_id=11)
        self.fields['skill_was_cd'].queryset = Comm_code.objects.filter(comm_div_id=12)


class School_hisForm(forms.ModelForm):
    class Meta:
        model = School_his
        fields = ('school_name', 'school_subject', 'graduate_date', 'evidence_status_cd', 'summary')

    # fk로 설정된 공통코드 구분 필터링 정의
    def __init__(self, *args, **kwargs):
        super(School_hisForm, self).__init__(*args, **kwargs)
        self.fields['evidence_status_cd'].queryset = Comm_code.objects.filter(comm_div_id=4)


 # detail form 객체 생성
School_hisFormset = inlineformset_factory(Employee, School_his, form=School_hisForm,
#                    fields=('school_his_id', 'emp_id', 'school_name', 'school_subject', 'graduate_date', 'evidence_status_cd', 'summary'),
                    widgets={
                            'graduate_date': forms.TextInput(attrs={'autocomplete': 'off','size': 10, 'class': 'cal'}),
                            'summary': forms.TextInput(attrs={'size': 70})
                    },
                    extra=1, can_delete=True)


class License_hisForm(forms.ModelForm):
    class Meta:
        model = License_his
        fields = ('license_cd', 'got_date', 'evidence_status_cd', 'summary')

    # fk로 설정된 공통코드 구분 필터링 정의
    def __init__(self, *args, **kwargs):
        super(License_hisForm, self).__init__(*args, **kwargs)
        self.fields['license_cd'].queryset = Comm_code.objects.filter(comm_div_id=5)
        self.fields['evidence_status_cd'].queryset = Comm_code.objects.filter(comm_div_id=4)


 # detail form 객체 생성
License_hisFormset = inlineformset_factory(Employee, License_his, form=License_hisForm,
                    widgets={
                            'got_date': forms.TextInput(attrs={'autocomplete': 'off', 'size': 10, 'class': 'cal'}),
                            'summary': forms.TextInput(attrs={'size': 70})
                    },
                    extra=1, can_delete=True)



class Work_hisForm(forms.ModelForm):
    class Meta:
        model = Work_his
        fields = ('company_name', 'work_start_date', 'work_end_date', 'emp_position', 'work_part', 'evidence_status_cd', 'summary')

    # fk로 설정된 공통코드 구분 필터링 정의
    def __init__(self, *args, **kwargs):
        super(Work_hisForm, self).__init__(*args, **kwargs)
        self.fields['evidence_status_cd'].queryset = Comm_code.objects.filter(comm_div_id=4)


 # detail form 객체 생성
Work_hisFormset = inlineformset_factory(Employee, Work_his, form=Work_hisForm,
                    widgets={
                            'work_start_date': forms.TextInput(attrs={'autocomplete': 'off', 'size': 10, 'class': 'cal'}),
                            'work_end_date': forms.TextInput(attrs={'autocomplete': 'off', 'size': 10, 'class': 'cal'}),
                            'summary': forms.TextInput(attrs={'size': 70})
                    },
                    extra=1, can_delete=True)


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = '__all__'

        # 속성별로 재정의 할때
        widgets = {
            'edu_name': forms.TextInput(attrs={'autocomplete': 'off', 'size': '60'}),
            'edu_start_date': forms.TextInput(attrs={'class': 'cal', 'autocomplete': 'off', 'size': '10'}),
            'edu_end_date': forms.TextInput(attrs={'class': 'cal', 'autocomplete': 'off', 'size': '10'}),
            'summary': forms.Textarea(attrs={'autocomplete': 'off', 'cols': '63', 'rows': '3'}),
        }

    # 추가 validation 처리
    def clean(self):
        edu_start_date = self.cleaned_data['edu_start_date']
        edu_end_date = self.cleaned_data['edu_end_date']

        if edu_start_date and edu_end_date:
            if edu_start_date > edu_end_date:
                raise ValidationError("종료일자가 시작일자 이전 입니다. 다시 입력하세요!")

        return self.cleaned_data



class Edu_hisForm(forms.ModelForm):
    class Meta:
        model = Edu_his
#        fields = ('edu_id', 'emp_id', 'evidence_status_cd', 'summary')
        fields = '__all__'

    # fk로 설정된 공통코드 구분 필터링 정의
    def __init__(self, *args, **kwargs):
        super(Edu_hisForm, self).__init__(*args, **kwargs)
        self.fields['evidence_status_cd'].queryset = Comm_code.objects.filter(comm_div_id=4)


 # detail form 객체 생성
Edu_hisFormset = inlineformset_factory(Education, Edu_his, form=Edu_hisForm,
                    widgets={
                            'summary': forms.TextInput(attrs={'size': 70})
                    },
                    extra=1, can_delete=True)

 # detail form 객체 생성
Edu_hisFormset2 = inlineformset_factory(Employee, Edu_his, form=Edu_hisForm,
                    widgets={
                            'summary': forms.TextInput(attrs={'size': 70})
                    },
                    extra=1, can_delete=True)




class Order_compForm(forms.ModelForm):
    class Meta:
        model = Order_comp
        fields = '__all__'

        # 속성별로 재정의 할때
        widgets = {
            'summary': forms.Textarea(attrs={'autocomplete': 'off', 'cols': '63', 'rows': '3'}),
        }

    # fk로 설정된 공통코드 구분 필터링 정의
    def __init__(self, *args, **kwargs):
        super(Order_compForm, self).__init__(*args, **kwargs)
        self.fields['indus_cd'].queryset = Comm_code.objects.filter(comm_div_id=13)


class PjtForm(forms.ModelForm):
    class Meta:
        model = Pjt
        fields = '__all__'

        # 속성별로 재정의 할때
        widgets = {
            'pjt_name': forms.Textarea(attrs={'autocomplete': 'off', 'cols': '40', 'rows': '1'}),
            'use_skill': forms.Textarea(attrs={'autocomplete': 'off', 'cols': '40', 'rows': '1'}),
            'pjt_start_date': forms.TextInput(attrs={'class': 'cal', 'autocomplete': 'off', 'size': '10'}),
            'pjt_end_date': forms.TextInput(attrs={'class': 'cal', 'autocomplete': 'off', 'size': '10'}),
            'summary': forms.Textarea(attrs={'autocomplete': 'off', 'cols': '40', 'rows': '1'}),
        }

    # fk로 설정된 공통코드 구분 필터링 정의
    def __init__(self, *args, **kwargs):
        super(PjtForm, self).__init__(*args, **kwargs)
        self.fields['pjt_type_cd'].queryset = Comm_code.objects.filter(comm_div_id=14)
        self.fields['pjt_location_cd'].queryset = Comm_code.objects.filter(comm_div_id=15)

    # 추가 validation 처리
    def clean(self):
        pjt_start_date = self.cleaned_data['pjt_start_date']
        pjt_end_date = self.cleaned_data['pjt_end_date']

        if pjt_start_date and pjt_end_date:
            if pjt_start_date > pjt_end_date:
                raise ValidationError("종료일자가 시작일자 이전 입니다. 다시 입력하세요!")

        return self.cleaned_data




 # detail form 객체 생성
PjtFormset = inlineformset_factory(Order_comp, Pjt, form=PjtForm,
                    extra=1, can_delete=True)



class Pjt_hisForm(forms.ModelForm):
    class Meta:
        model = Pjt_his
        fields = '__all__'

        # 속성별로 재정의 할때
        widgets = {
            'join_start_date': forms.TextInput(attrs={'class': 'cal', 'autocomplete': 'off', 'size': '10'}),
            'join_end_date': forms.TextInput(attrs={'class': 'cal', 'autocomplete': 'off', 'size': '10'}),
            'summary': forms.Textarea(attrs={'autocomplete': 'off', 'cols': '40', 'rows': '2'}),
        }

    # fk로 설정된 공통코드 구분 필터링 정의
    def __init__(self, *args, **kwargs):
        super(Pjt_hisForm, self).__init__(*args, **kwargs)
        self.fields['kosa_conf_cd'].queryset = Comm_code.objects.filter(comm_div_id=16)
        self.fields['insurance_conf_cd'].queryset = Comm_code.objects.filter(comm_div_id=17)
        self.fields['his_status_cd'].queryset = Comm_code.objects.filter(comm_div_id=18)

    # 추가 validation 처리
    def clean(self):
        join_start_date = self.cleaned_data['join_start_date']
        join_end_date = self.cleaned_data['join_end_date']

        if join_start_date and join_end_date:
            if join_start_date > join_end_date:
                raise ValidationError("종료일자가 시작일자 이전 입니다. 다시 입력하세요!")

        return self.cleaned_data



 # detail form 객체 생성
Pjt_hisFormset = inlineformset_factory(Pjt, Pjt_his, form=Pjt_hisForm,
                    extra=1, can_delete=True)


 # detail form 객체 생성
Pjt_hisFormset2 = inlineformset_factory(Employee, Pjt_his, form=Pjt_hisForm,
                    widgets={
                        'company_name': forms.Textarea(attrs={'autocomplete': 'off', 'cols': '20', 'rows': '2'}),
                        'pjt_role': forms.Textarea(attrs={'autocomplete': 'off', 'cols': '20', 'rows': '2'}),
                        'join_start_date': forms.TextInput(attrs={'class': 'cal', 'autocomplete': 'off', 'size': '8'}),
                        'join_end_date': forms.TextInput(attrs={'class': 'cal', 'autocomplete': 'off', 'size': '8'}),
                        'summary': forms.Textarea(attrs={'autocomplete': 'off', 'cols': '20', 'rows': '2'}),
                    },
                    extra=1, can_delete=True)

