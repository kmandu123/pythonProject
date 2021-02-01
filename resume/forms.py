from django import forms
from .models import Comm_div

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