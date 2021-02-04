from django import forms
from .models import Comm_div, Comm_code, Employee, School_his, License_his, Work_his
from django.forms import inlineformset_factory

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
            'summary': forms.Textarea(attrs={'autocomplete': 'off', 'cols': '63', 'rows': '3'}),
        }

    # fk로 설정된 공통코드 구분 필터링 정의
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['emp_position_cd'].queryset = Comm_code.objects.filter(comm_div_id=1)
        self.fields['skill_grade_cd'].queryset = Comm_code.objects.filter(comm_div_id=2)
        self.fields['evidence_method_cd'].queryset = Comm_code.objects.filter(comm_div_id=3)


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