from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
from resume.models import Comm_div, Comm_code
from django.views import generic
from books.models import Author, Book, Log
from .forms import AuthorForm, BookForm
from django.shortcuts import get_object_or_404
import os
import datetime
import json
from urllib.request import urlopen
import googlemaps
from django.db.models import Count

# 함수 로그인 권한 제어
from django.contrib.auth.decorators import login_required
# 클래스 로그인 권한 제어
from django.contrib.auth.mixins import LoginRequiredMixin
# 권한 CHECK
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

#ip로 주소 찾기
def get_location(ip):
    request = "https://geolocation-db.com/json/%s" % (ip)

    with urlopen(request) as url:
        data = json.loads(url.read().decode())
        return data["latitude"], data["longitude"], data["city"], data["state"]


# 페이지 접속 log기록
def write_log(client_ip,request,log_gb,user):
    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')

    addr_info = get_location(client_ip)

    # 구글서비스를 이용하여 위도/경도로 주소찾기
    addr = ''
    if addr_info[0] != 'Not found':
        gmaps = googlemaps.Client(key='AIzaSyCPbwbrbnKTrKAq_2qJ9qfhzmf0FL5P3J0')
        reverse_geocode_result = gmaps.reverse_geocode((addr_info[0], addr_info[1]), language='ko')
        addr = reverse_geocode_result[0].get('formatted_address')

    log_context = {'log_dt': nowDatetime, 'ip': client_ip, 'log_gb': log_gb, 'request': request, 'user': user, 'lat': addr_info[0], 'long': addr_info[1], 'state': addr_info[3], 'city': addr_info[2], 'addr': addr}

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if BASE_DIR.find('home'):  # linux이면
        file_path = BASE_DIR + '/log.txt'
    else:  # window이면
        file_path = BASE_DIR + '\log.txt'

    #파일에 저장
    f = open(file_path, 'a', encoding='utf8')
    f.write(log_context.__str__() + '\n')
    f.close()

    #db에 저장
    log = Log(client_ip=client_ip, log_gb=log_gb, request_info=request, create_dt=nowDatetime, user=user, lat=addr_info[0], long=addr_info[1], state=addr_info[3], city=addr_info[2], addr=addr)
    log.save()

#    print(log_context)


# 작가 list
class AuthorList(generic.ListView):
    model = Author
    paginate_by = 10



    #검색 결과 (초기값)
    def get_queryset(self):
        filter_val_1 = self.request.GET.get('filter_1', '')  #filter_1 검색조건 변수명, '' 초기 검색조건값 <- like 검색결과 all 검색을 위해서 ''로 처리함.
        filter_val_2 = self.request.GET.get('filter_2', '')
        order = self.request.GET.get('orderby', 'author_name') #정렬대상 컬럼명(초기값)

        #log 기록
        write_log(self.request.META['REMOTE_ADDR'], self.request, '작가조회',self.request.user)

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
    # log 기록
    write_log(request.META['REMOTE_ADDR'], request, '작가수정', request.user)

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
    # log 기록
    write_log(request.META['REMOTE_ADDR'], request, '작가생성', request.user)

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
    # log 기록
    write_log(request.META['REMOTE_ADDR'], request, '작가삭제', request.user)

    # 파라미터pk로 받은 data가 존재한다면 가져온다
    author = get_object_or_404(Author, pk=pk)
    author.delete()
    return HttpResponseRedirect(reverse('author_list'))


# Book list
class BookList(generic.ListView):
    model = Book
    paginate_by = 10

    #검색 결과 (초기값)
    def get_queryset(self):
        #log 기록
        write_log(self.request.META['REMOTE_ADDR'], self.request, '추천도서조회',self.request.user)

        filter_val_1 = self.request.GET.get('filter_1', '')  #filter_1 검색조건 변수명, '' 초기 검색조건값 <- like 검색결과 all 검색을 위해서 ''로 처리함.
        filter_val_2 = self.request.GET.get('filter_2', '')
        filter_val_3 = self.request.GET.get('filter_3', '')
        order = self.request.GET.get('orderby', 'author_name') #정렬대상 컬럼명(초기값)

        new_context = Book.objects.filter(
            author_name__icontains=filter_val_1,
            input_name__icontains=filter_val_2,
            genre_cd__comm_code_name__icontains=filter_val_3,
        ).order_by(order)
        return new_context


    #검색 조건 (초기값)
    def get_context_data(self, **kwargs):
        context = super(BookList, self).get_context_data(**kwargs)
        context['filter_1'] = self.request.GET.get('filter_1', '')
        context['filter_2'] = self.request.GET.get('filter_2', '')
        context['filter_3'] = self.request.GET.get('filter_3', '')
        context['orderby'] = self.request.GET.get('orderby', 'author_name') #정렬대상 컬럼명(초기값)
        return context


def BookCreate(request):
    # log 기록
    write_log(request.META['REMOTE_ADDR'], request, '추천도서 생성', request.user)

    # book model 빈 instance 생성
    book = Book()

    # author form 빈 instance 생성 : 마스터 form 객체는 forms.py에 존재함. : 최초 user화면에 보여주는 빈 instance
    bookform =BookForm(instance=book)

    if request.method == "POST":     #user의 수정화면을 통한 instance 수정요청이면 데이터 처리.
        # master form instance 생성 : Post요청 data로 생성
        bookform = BookForm(request.POST)

        if bookform.is_valid():
            bookform.save()
            return HttpResponseRedirect(reverse('book_list'))
        else:
            print("author valid error발생")


    # template의 html에 Form과 data instance를 딕셔너리 자료형태를 생성한다.
    context = {
        'bookform': bookform,
        'book': book,
    }

    # template를 호출한다. context도 같이 넘긴다.
    return render(request, 'books/book_update.html', context)


def BookUpdate(request, pk):
    # log 기록
    write_log(request.META['REMOTE_ADDR'], request, '추천도서 수정', request.user)

    if pk:
        #master model instance 생성
        book = Book.objects.get(book_id=pk)
    else:
        book = Book()

    # master form instance 생성 : 마스터 form 객체는 forms.py에 존재함. : 최초 user화면에 보여주는 수정대상 instance
    bookform = BookForm(instance=book)

    if request.method == "POST":     #user의 수정화면을 통한 instance 수정요청이면 데이터 처리.
        # master form instance 생성 : Post요청 data로 생성
        bookform = BookForm(request.POST)

        if pk:
            # master form instance 생성 : Post요청 data와 pk에 해당하는 마스터 모델 instance연계
            bookform = BookForm(request.POST, instance=book)


        if bookform.is_valid():
            bookform.save()
            return HttpResponseRedirect(reverse('book_list'))

    # template의 html에 Form과 data instance를 딕셔너리 자료형태를 생성한다.
    context = {
        'bookform': bookform,
        'book': book,
    }

    # template를 호출한다. context도 같이 넘긴다.
    return render(request, 'books/book_update.html', context)


def BookDelete(request, pk):
    # log 기록
    write_log(request.META['REMOTE_ADDR'], request, '추천도서 삭제', request.user)

    # 파라미터pk로 받은 data가 존재한다면 가져온다
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return HttpResponseRedirect(reverse('book_list'))
