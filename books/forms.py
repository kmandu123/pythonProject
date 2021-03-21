from django import forms
from .models import Author, Book
from resume.models import Comm_code

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

        # 속성별로 재정의 할때
        widgets = {
            'book_name': forms.TextInput(attrs={'autocomplete': 'off', 'size': '40'}),
            'summary': forms.Textarea(attrs={'autocomplete': 'off', 'cols': '40', 'rows': '3'}),
            'read_date': forms.TextInput(attrs={'class': 'cal', 'autocomplete': 'off', 'size': '10'}),
        }


    # fk로 설정된 공통코드 구분 필터링 정의
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['genre_cd'].queryset = Comm_code.objects.filter(comm_div_id=19)
