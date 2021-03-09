from django.shortcuts import render

# Create your views here.
from resume.models import Comm_div, Comm_code
from django.views import generic
from books.models import Author, Book

from django.db.models import Count

# 함수 로그인 권한 제어
from django.contrib.auth.decorators import login_required
# 클래스 로그인 권한 제어
from django.contrib.auth.mixins import LoginRequiredMixin
# 권한 CHECK
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

# 발주처 list
class AuthorList(generic.ListView):
    permission_required = 'resume.public_open'
    model = Author
    paginate_by = 10

    #검색 결과 (초기값)
    def get_queryset(self):
        filter_val_1 = self.request.GET.get('filter_1', '')  #filter_1 검색조건 변수명, '' 초기 검색조건값 <- like 검색결과 all 검색을 위해서 ''로 처리함.
        filter_val_2 = self.request.GET.get('filter_2', '')
        order = self.request.GET.get('orderby', 'author_name') #정렬대상 컬럼명(초기값)

        new_context = Author.objects.filter(
            author_name__icontains=filter_val_1,
        #    nation_cd__comm_code_name__icontains=filter_val_2,
        ).order_by(order)
        return new_context


    #검색 조건 (초기값)
    def get_context_data(self, **kwargs):
        context = super(AuthorList, self).get_context_data(**kwargs)
        context['filter_1'] = self.request.GET.get('filter_1', '')
        context['filter_2'] = self.request.GET.get('filter_2', '')
        context['orderby'] = self.request.GET.get('orderby', 'author_name') #정렬대상 컬럼명(초기값)
        return context

