from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
from resume.models import Comm_div, Comm_code
from django.views import generic
from books.models import Author, Book
from .forms import AuthorForm
from django.shortcuts import get_object_or_404

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


def AuthorUpdate(request, pk):

    if pk:
        #master model instance 생성
        author = Author.objects.get(author_id=pk)
    else:
        author = Author()

    # master form instance 생성 : 마스터 form 객체는 forms.py에 존재함. : 최초 user화면에 보여주는 수정대상 instance
    authorform = AuthorForm(instance=author)

    if request.method == "POST":     #user의 수정화면을 통한 instance 수정요청이면 데이터 처리.
        # master form instance 생성 : Post요청 data로 생성
        authorform = AuthorForm(request.POST)

        if pk:
            # master form instance 생성 : Post요청 data와 pk에 해당하는 마스터 모델 instance연계
            authorform = AuthorForm(request.POST, instance=author)


        if authorform.is_valid():
            authorform.save()
            return HttpResponseRedirect(reverse('author_list'))

    # template의 html에 Form과 data instance를 딕셔너리 자료형태를 생성한다.
    context = {
        'authorform': authorform,
        'author': author,
    }

    # template를 호출한다. context도 같이 넘긴다.
    return render(request, 'books/author_update.html', context)




def AuthorCreate(request):

    # author model 빈 instance 생성
    author = Author()

    # author form 빈 instance 생성 : 마스터 form 객체는 forms.py에 존재함. : 최초 user화면에 보여주는 빈 instance
    authorform =AuthorForm(instance=author)

    if request.method == "POST":     #user의 수정화면을 통한 instance 수정요청이면 데이터 처리.
        # master form instance 생성 : Post요청 data로 생성
        authorform = AuthorForm(request.POST)

        if authorform.is_valid():
            authorform.save()
            return HttpResponseRedirect(reverse('author_list'))
        else:
            print("author valid error발생")


    # template의 html에 Form과 data instance를 딕셔너리 자료형태를 생성한다.
    context = {
        'authorform': authorform,
        'author': author,
    }

    # template를 호출한다. context도 같이 넘긴다.
    return render(request, 'books/author_update.html', context)


def AuthorDelete(request, pk):
    # 파라미터pk로 받은 data가 존재한다면 가져온다
    author = get_object_or_404(Author, pk=pk)
    author.delete()
    return HttpResponseRedirect(reverse('author_list'))


