from django import forms
from django.core.exceptions import ValidationError

class UpdateComm_divForm(forms.Form):
    #Form의 필드를 정의함.
    f_comm_div_name = forms.CharField(max_length=200, label='공통구분 코드명', widget=forms.TextInput(attrs={'autocomplete':'off'}))
    f_summary = forms.CharField(max_length=2000, label='특이사항', widget=forms.TextInput(attrs={'autocomplete':'off','size':'40'}))
    f_create_dt = forms.DateField(label='최초생성일자', widget=forms.TextInput(attrs={'class':'cal','autocomplete':'off','size':'10'}))
    f_update_dt = forms.DateField(label='최종수정일자', widget=forms.TextInput(attrs={'class':'cal','autocomplete':'off','size':'10'}))

    #Form validation 처리
    def clean(self):
        cleaned_data = super().clean()
        f_create_dt = cleaned_data.get("f_create_dt")
        f_update_dt = cleaned_data.get("f_update_dt")

        if not any([field.errors for field in self]):   #필드에 error가 없는 경우에만 실행하기 위해
            if f_update_dt < f_create_dt:
                raise forms.ValidationError(
                    "최종수정일자는 최초생성일자 이후날짜여야 합니다!"
                )
