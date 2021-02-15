from django.shortcuts import render

# Create your views here.
from resume.models import Comm_div, Comm_code, Employee, School_his, Education, Order_comp, Pjt, Vw_emp

from django.db.models import Count

# 함수 로그인 권한 제어
from django.contrib.auth.decorators import login_required
# 클래스 로그인 권한 제어
from django.contrib.auth.mixins import LoginRequiredMixin
# 권한 CHECK
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

#orm not filtering
from django.db.models import Q

@login_required
@permission_required('resume.public_open')
def index(request):
    """View function for home page of site."""

    # 전체 인원수
    emp_cnt = Employee.objects.all().count()

    # 직급별 인원수
    position_cnt = list(Employee.objects.values('emp_position_cd__comm_code_name').annotate(Count('emp_id')).order_by('emp_position_cd'))

    # 기술등급별 인원수
    skill_cnt = list(Employee.objects.values('skill_grade_cd__comm_code_name').annotate(Count('emp_id')).order_by('skill_grade_cd'))

    context = {
        'emp_cnt': emp_cnt,
        'position_cnt': position_cnt,
        'skill_cnt': skill_cnt,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


@login_required
@permission_required('resume.public_open')
def resume_index(request):
    """View function for home page of site."""

    # 전체 인원수
    emp_cnt = Employee.objects.all().count()

    # 직급별 인원수
    position_cnt = list(Employee.objects.values('emp_position_cd__comm_code_name').annotate(Count('emp_id')).order_by('emp_position_cd'))

    # 기술등급별 인원수
    skill_cnt = list(Employee.objects.values('skill_grade_cd__comm_code_name').annotate(Count('emp_id')).order_by('skill_grade_cd'))

    context = {
        'emp_cnt': emp_cnt,
        'position_cnt': position_cnt,
        'skill_cnt': skill_cnt,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'resume_index.html', context=context)



from django.views import generic


# 공통구분 list
class  Comm_divList(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = 'resume.public_open'
    model = Comm_div
    paginate_by = 15

    #검색 결과 (초기값)
    def get_queryset(self):
        filter_val_1 = self.request.GET.get('filter_1', '')  #filter_1 검색조건 변수명, '' 초기 검색조건값 <- like 검색결과 all 검색을 위해서 ''로 처리함.
        order = self.request.GET.get('orderby', 'comm_div_name') #정렬대상 컬럼명(초기값)

        new_context = Comm_div.objects.filter(
            comm_div_name__icontains=filter_val_1,
        ).order_by(order)
        return new_context

    #검색 조건 (초기값)
    def get_context_data(self, **kwargs):
        context = super(Comm_divList, self).get_context_data(**kwargs)
        context['filter_1'] = self.request.GET.get('filter_1', '')
        context['orderby'] = self.request.GET.get('orderby', 'comm_div_name') #정렬대상 컬럼명(초기값)
        return context





#Comm_div를 update하기 위한 function view
import  datetime
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import Comm_divForm, Comm_codeFormset, EmployeeForm, School_hisFormset, License_hisFormset, Work_hisFormset, EducationForm, Edu_hisFormset, Edu_hisFormset2, Order_compForm, PjtForm, PjtFormset, Pjt_hisFormset, Pjt_hisFormset2
#inline Formsets 사용
from django.forms import inlineformset_factory
from django import forms

@login_required
@permission_required('resume.public_open')
def Comm_divUpdate(request, pk):

    if pk:
        #master model instance 생성
        comm_div = Comm_div.objects.get(comm_div_id=pk)
    else:
        comm_div = Comm_div()

    # master form instance 생성 : 마스터 form 객체는 forms.py에 존재함. : 최초 user화면에 보여주는 수정대상 instance
    comm_divform = Comm_divForm(instance=comm_div)

    #detail from instance 생성 : 최초 user화면에 보여주는 수정대상 instance
    comm_codeformset = Comm_codeFormset(instance=comm_div)

    if request.method == "POST":     #user의 수정화면을 통한 instance 수정요청이면 데이터 처리.
        # master form instance 생성 : Post요청 data로 생성
        comm_divform = Comm_divForm(request.POST)

        if pk:
            # master form instance 생성 : Post요청 data와 pk에 해당하는 마스터 모델 instance연계
            comm_divform = Comm_divForm(request.POST, instance=comm_div)

        # detail form instance 생성 : Post요청 data로 생성
        comm_codeformset = Comm_codeFormset(request.POST, request.FILES)

        if comm_divform.is_valid():
            created_comm_div = comm_divform.save(commit=False)
            comm_codeformset = Comm_codeFormset(request.POST, request.FILES, instance=created_comm_div)

            if comm_codeformset.is_valid():
                created_comm_div.save()
                comm_codeformset.save()
                return HttpResponseRedirect(reverse('comm_div_list'))
            else:
                print("detail valid error발생")
                print(comm_codeformset.errors)


    # template의 html에 Form과 data instance를 딕셔너리 자료형태를 생성한다.
    context = {
        'comm_divform': comm_divform,
        'comm_codeformset': comm_codeformset,
        'comm_div': comm_div,
    }

    # template를 호출한다. context도 같이 넘긴다.
    return render(request, 'resume/comm_div_update.html', context)



@login_required
@permission_required('resume.public_open')
def Comm_divCreate(request):

    # master model 빈 instance 생성
    comm_div = Comm_div()

    # master form 빈 instance 생성 : 마스터 form 객체는 forms.py에 존재함. : 최초 user화면에 보여주는 빈 instance
    comm_divform = Comm_divForm(instance=comm_div)

    #detail from instance 생성 : 최초 user화면에 보여주는 수정대상 instance
    comm_codeformset = Comm_codeFormset(instance=comm_div)

    if request.method == "POST":     #user의 수정화면을 통한 instance 수정요청이면 데이터 처리.
        # master form instance 생성 : Post요청 data로 생성
        comm_divform = Comm_divForm(request.POST)

        # detail form instance 생성 : Post요청 data로 생성
        comm_codeformset = Comm_codeFormset(request.POST, request.FILES)

        if comm_divform.is_valid():
            created_comm_div = comm_divform.save(commit=False)
            comm_codeformset = Comm_codeFormset(request.POST, request.FILES, instance=created_comm_div)

            if comm_codeformset.is_valid():
                created_comm_div.save()
                comm_codeformset.save()
                return HttpResponseRedirect(reverse('comm_div_list'))
            else:
                print("detail valid error발생")
                print(comm_codeformset.errors)


    # template의 html에 Form과 data instance를 딕셔너리 자료형태를 생성한다.
    context = {
        'comm_divform': comm_divform,
        'comm_codeformset': comm_codeformset,
        'comm_div': comm_div,
    }

    # template를 호출한다. context도 같이 넘긴다.
    return render(request, 'resume/comm_div_update.html', context)


@login_required
@permission_required('resume.public_open')
#Comm_div를 delete하기 위한 function view
def Comm_divDelete(request, pk):
    # 파라미터pk로 받은 data가 존재한다면 가져온다
    comm_div = get_object_or_404(Comm_div, pk=pk)
    comm_div.delete()
    return HttpResponseRedirect(reverse('comm_div_list'))


# 발주처 list
class Order_compList(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = 'resume.public_open'
    model = Order_comp
    paginate_by = 15

    #검색 결과 (초기값)
    def get_queryset(self):
        filter_val_1 = self.request.GET.get('filter_1', '')  #filter_1 검색조건 변수명, '' 초기 검색조건값 <- like 검색결과 all 검색을 위해서 ''로 처리함.
        filter_val_2 = self.request.GET.get('filter_2', '')
        order = self.request.GET.get('orderby', 'order_comp_name') #정렬대상 컬럼명(초기값)

        new_context = Order_comp.objects.filter(
            order_comp_name__icontains=filter_val_1,
            indus_cd__comm_code_name__icontains=filter_val_2,
        ).order_by(order)
        return new_context

    #검색 조건 (초기값)
    def get_context_data(self, **kwargs):
        context = super(Order_compList, self).get_context_data(**kwargs)
        context['filter_1'] = self.request.GET.get('filter_1', '')
        context['filter_2'] = self.request.GET.get('filter_2', '')
        context['orderby'] = self.request.GET.get('orderby', 'order_comp_name') #정렬대상 컬럼명(초기값)
        return context


@login_required
@permission_required('resume.public_open')
def Order_compUpdate(request, pk):

    if pk:
        #master model instance 생성
        order_comp = Order_comp.objects.get(order_comp_id=pk)
    else:
        order_comp = Order_comp()

    # master form instance 생성 : 마스터 form 객체는 forms.py에 존재함. : 최초 user화면에 보여주는 수정대상 instance
    order_compform = Order_compForm(instance=order_comp)

    #detail from instance 생성 : 최초 user화면에 보여주는 수정대상 instance
    pjtformset = PjtFormset(instance=order_comp)

    if request.method == "POST":     #user의 수정화면을 통한 instance 수정요청이면 데이터 처리.
        # master form instance 생성 : Post요청 data로 생성
        order_compform = Order_compForm(request.POST)

        if pk:
            # master form instance 생성 : Post요청 data와 pk에 해당하는 마스터 모델 instance연계
            order_compform = Order_compForm(request.POST, instance=order_comp)

        # detail form instance 생성 : Post요청 data로 생성
        pjtformset = PjtFormset(request.POST, request.FILES)

        if order_compform.is_valid():
            created_order_comp = order_compform.save(commit=False)
            pjtformset = PjtFormset(request.POST, request.FILES, instance=created_order_comp)

            if pjtformset.is_valid():
                created_order_comp.save()
                pjtformset.save()
                return HttpResponseRedirect(reverse('order_comp_list'))
            else:
                print("detail valid error발생")
                print(pjtformset.errors)


    # template의 html에 Form과 data instance를 딕셔너리 자료형태를 생성한다.
    context = {
        'order_compform': order_compform,
        'pjtformset': pjtformset,
        'order_comp': order_comp,
    }

    # template를 호출한다. context도 같이 넘긴다.
    return render(request, 'resume/order_comp_update.html', context)

@login_required
@permission_required('resume.public_open')
def Order_compCreate(request):

    # master model 빈 instance 생성
    order_comp = Order_comp()

    # master form instance 생성 : 마스터 form 객체는 forms.py에 존재함. : 최초 user화면에 보여주는 수정대상 instance
    order_compform = Order_compForm(instance=order_comp)

    #detail from instance 생성 : 최초 user화면에 보여주는 수정대상 instance
    pjtformset = PjtFormset(instance=order_comp)


    if request.method == "POST":     #user의 수정화면을 통한 instance 수정요청이면 데이터 처리.
        # master form instance 생성 : Post요청 data로 생성
        order_compform = Order_compForm(request.POST)

        # detail form instance 생성 : Post요청 data로 생성
        pjtformset = PjtFormset(request.POST, request.FILES)

        if order_compform.is_valid():
            created_order_comp = order_compform.save(commit=False)
            pjtformset = PjtFormset(request.POST, request.FILES, instance=created_order_comp)

            if pjtformset.is_valid():
                created_order_comp.save()
                pjtformset.save()
                return HttpResponseRedirect(reverse('order_comp_list'))
            else:
                print("detail valid error발생")
                print(pjtformset.errors)


    # template의 html에 Form과 data instance를 딕셔너리 자료형태를 생성한다.
    context = {
        'order_compform': order_compform,
        'pjtformset': pjtformset,
        'order_comp': order_comp,
    }

    # template를 호출한다. context도 같이 넘긴다.
    return render(request, 'resume/order_comp_update.html', context)


@login_required
@permission_required('resume.public_open')
def Order_compDelete(request, pk):
    # 파라미터pk로 받은 data가 존재한다면 가져온다
    order_comp = get_object_or_404(Order_comp, pk=pk)
    order_comp.delete()
    return HttpResponseRedirect(reverse('order_comp_list'))



# 프로젝트 list
class PjtList(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = 'resume.public_open'
    model = Pjt
    paginate_by = 15

    #검색 결과 (초기값)
    def get_queryset(self):
        filter_val_1 = self.request.GET.get('filter_1', '')  #filter_1 검색조건 변수명, '' 초기 검색조건값 <- like 검색결과 all 검색을 위해서 ''로 처리함.
        filter_val_2 = self.request.GET.get('filter_2', '')
        order = self.request.GET.get('orderby', 'pjt_name') #정렬대상 컬럼명(초기값)

        new_context = Pjt.objects.filter(
            pjt_name__icontains=filter_val_1,
            order_comp_id__order_comp_name__icontains=filter_val_2,
        ).order_by(order)  #sort컬럼 2개이상도 가능 ","로 구분하여 입력하면됨.
        return new_context

    #검색 조건 (초기값)
    def get_context_data(self, **kwargs):
        context = super(PjtList, self).get_context_data(**kwargs)
        context['filter_1'] = self.request.GET.get('filter_1', '')
        context['filter_2'] = self.request.GET.get('filter_2', '')
        context['orderby'] = self.request.GET.get('orderby', 'pjt_name') #정렬대상 컬럼명(초기값)
        return context


@login_required
@permission_required('resume.public_open')
def PjtUpdate(request, pk):

    if pk:
        #master model instance 생성
        pjt = Pjt.objects.get(pjt_id=pk)
    else:
        pjt = Pjt()

    # master form instance 생성 : 마스터 form 객체는 forms.py에 존재함. : 최초 user화면에 보여주는 수정대상 instance
    pjtform = PjtForm(instance=pjt)

    #detail from instance 생성 : 최초 user화면에 보여주는 수정대상 instance
    pjt_hisformset = Pjt_hisFormset(instance=pjt)

    if request.method == "POST":     #user의 수정화면을 통한 instance 수정요청이면 데이터 처리.
        # master form instance 생성 : Post요청 data로 생성
        pjtform = PjtForm(request.POST)

        if pk:
            # master form instance 생성 : Post요청 data와 pk에 해당하는 마스터 모델 instance연계
            pjtform = PjtForm(request.POST, instance=pjt)

        # detail form instance 생성 : Post요청 data로 생성
        pjt_hisformset = Pjt_hisFormset(request.POST, request.FILES)

        if pjtform.is_valid():
            created_pjt = pjtform.save(commit=False)
            pjt_hisformset = Pjt_hisFormset(request.POST, request.FILES, instance=created_pjt)

            if pjt_hisformset.is_valid():
                created_pjt.save()
                pjt_hisformset.save()
                return HttpResponseRedirect(reverse('pjt_list'))
            else:
                print("detail valid error발생")
                print(pjt_hisformset.errors)


    # template의 html에 Form과 data instance를 딕셔너리 자료형태를 생성한다.
    context = {
        'pjtform': pjtform,
        'pjt_hisformset': pjt_hisformset,
        'pjt': pjt,
    }

    # template를 호출한다. context도 같이 넘긴다.
    return render(request, 'resume/pjt_update.html', context)



@login_required
@permission_required('resume.public_open')
def PjtCreate(request):

    # master model 빈 instance 생성
    pjt = Pjt()

    # master form instance 생성 : 마스터 form 객체는 forms.py에 존재함. : 최초 user화면에 보여주는 수정대상 instance
    pjtform = PjtForm(instance=pjt)

    #detail from instance 생성 : 최초 user화면에 보여주는 수정대상 instance
    pjt_hisformset = Pjt_hisFormset(instance=pjt)

    if request.method == "POST":     #user의 수정화면을 통한 instance 수정요청이면 데이터 처리.
        # master form instance 생성 : Post요청 data로 생성
        pjtform = PjtForm(request.POST)

        # detail form instance 생성 : Post요청 data로 생성
        pjt_hisformset = Pjt_hisFormset(request.POST, request.FILES)

        if pjtform.is_valid():
            created_pjt = pjtform.save(commit=False)
            pjt_hisformset = Pjt_hisFormset(request.POST, request.FILES, instance=created_pjt)

            if pjt_hisformset.is_valid():
                created_pjt.save()
                pjt_hisformset.save()
                return HttpResponseRedirect(reverse('pjt_list'))
            else:
                print("detail valid error발생")
                print(pjt_hisformset.errors)


    # template의 html에 Form과 data instance를 딕셔너리 자료형태를 생성한다.
    context = {
        'pjtform': pjtform,
        'pjt_hisformset': pjt_hisformset,
        'pjt': pjt,
    }

    # template를 호출한다. context도 같이 넘긴다.
    return render(request, 'resume/pjt_update.html', context)



@login_required
@permission_required('resume.public_open')
def PjtDelete(request, pk):
    # 파라미터pk로 받은 data가 존재한다면 가져온다
    pjt = get_object_or_404(Pjt, pk=pk)
    pjt.delete()
    return HttpResponseRedirect(reverse('pjt_list'))



# 발주처 popup용 list
class Order_comp_popup(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = 'resume.public_open'
    model = Order_comp
    paginate_by = 10
    context_object_name = 'order_comp_popup'
    template_name = 'resume/order_comp_popup.html'

    #검색 결과 (초기값)
    def get_queryset(self):
        filter_val_1 = self.request.GET.get('filter_1', '')  #filter_1 검색조건 변수명, '' 초기 검색조건값 <- like 검색결과 all 검색을 위해서 ''로 처리함.
        filter_val_2 = self.request.GET.get('filter_2', '')
        order = self.request.GET.get('orderby', 'order_comp_name') #정렬대상 컬럼명(초기값)

        new_context = Order_comp.objects.filter(
            order_comp_name__icontains=filter_val_1,
            indus_cd__comm_code_name__icontains=filter_val_2,
        ).order_by(order)
        return new_context

    #검색 조건 (초기값)
    def get_context_data(self, **kwargs):
        context = super(Order_comp_popup, self).get_context_data(**kwargs)
        context['filter_1'] = self.request.GET.get('filter_1', '')
        context['filter_2'] = self.request.GET.get('filter_2', '')
        context['orderby'] = self.request.GET.get('orderby', 'order_comp_name') #정렬대상 컬럼명(초기값)
        return context



# 교육 list
class EducationList(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = 'resume.public_open'

    model = Education
    paginate_by = 15

    #검색 결과 (초기값)
    def get_queryset(self):
        filter_val_1 = self.request.GET.get('filter_1', '')  #filter_1 검색조건 변수명, '' 초기 검색조건값 <- like 검색결과 all 검색을 위해서 ''로 처리함.
        filter_val_2 = self.request.GET.get('filter_2', '')
        order = self.request.GET.get('orderby', 'edu_name') #정렬대상 컬럼명(초기값)

        new_context = Education.objects.filter(
            edu_name__icontains=filter_val_1,
            agency_name__icontains=filter_val_2,
        ).order_by(order)
        return new_context

    #검색 조건 (초기값)
    def get_context_data(self, **kwargs):
        context = super(EducationList, self).get_context_data(**kwargs)
        context['filter_1'] = self.request.GET.get('filter_1', '')
        context['filter_2'] = self.request.GET.get('filter_2', '')
        context['orderby'] = self.request.GET.get('orderby', 'edu_name') #정렬대상 컬럼명(초기값)
        return context





@login_required
@permission_required('resume.public_open')
def EducationUpdate(request, pk):

    if pk:
        #master model instance 생성
        education = Education.objects.get(edu_id=pk)
    else:
        education = Education()

    # master form instance 생성 : 마스터 form 객체는 forms.py에 존재함. : 최초 user화면에 보여주는 수정대상 instance
    education_form = EducationForm(instance=education)

    #detail from instance 생성 : 최초 user화면에 보여주는 수정대상 instance
    edu_hisformset = Edu_hisFormset(instance=education)

    if request.method == "POST":     #user의 수정화면을 통한 instance 수정요청이면 데이터 처리.
        # master form instance 생성 : Post요청 data로 생성
        education_form = EducationForm(request.POST)

        if pk:
            # master form instance 생성 : Post요청 data와 pk에 해당하는 마스터 모델 instance연계
            education_form = EducationForm(request.POST, instance=education)

        # detail form instance 생성 : Post요청 data로 생성
        edu_hisformset = Edu_hisFormset(request.POST, request.FILES)

        if education_form.is_valid():
            created_education = education_form.save(commit=False)
            edu_hisformset = Edu_hisFormset(request.POST, request.FILES, instance=created_education)

            if edu_hisformset.is_valid():
                created_education.save()
                edu_hisformset.save()
                return HttpResponseRedirect(reverse('education_list'))
            else:
                print("detail valid error발생")
                print(edu_hisformset.errors)


    # template의 html에 Form과 data instance를 딕셔너리 자료형태를 생성한다.
    context = {
        'education_form': education_form,
        'edu_hisformset': edu_hisformset,
        'education': education,
    }

    # template를 호출한다. context도 같이 넘긴다.
    return render(request, 'resume/education_update.html', context)


# 신규입력 : 수정과 동일하지만 일부분 수정
# 수정1 : 함수명 변경 및 파라미터 pk 삭제
# 수정2 : if pk 지우고 master model 빈 instance 생성으로 변경
# 수정3 : 2번째 if pk 삭제
@login_required
@permission_required('resume.public_open')
def EducationCreate(request):
    # master model 빈 instance 생성
    education = Education()

    # master form instance 생성 : 마스터 form 객체는 forms.py에 존재함. : 최초 user화면에 보여주는 수정대상 instance
    education_form = EducationForm(instance=education)

    #detail from instance 생성 : 최초 user화면에 보여주는 수정대상 instance
    edu_hisformset = Edu_hisFormset(instance=education)

    if request.method == "POST":     #user의 수정화면을 통한 instance 수정요청이면 데이터 처리.
        # master form instance 생성 : Post요청 data로 생성
        education_form = EducationForm(request.POST)

        # detail form instance 생성 : Post요청 data로 생성
        edu_hisformset = Edu_hisFormset(request.POST, request.FILES)

        if education_form.is_valid():
            created_education = education_form.save(commit=False)
            edu_hisformset = Edu_hisFormset(request.POST, request.FILES, instance=created_education)

            if edu_hisformset.is_valid():
                created_education.save()
                edu_hisformset.save()
                return HttpResponseRedirect(reverse('education_list'))
            else:
                print("detail valid error발생")
                print(edu_hisformset.errors)


    # template의 html에 Form과 data instance를 딕셔너리 자료형태를 생성한다.
    context = {
        'education_form': education_form,
        'edu_hisformset': edu_hisformset,
        'education': education,
    }

    # template를 호출한다. context도 같이 넘긴다.
    return render(request, 'resume/education_update.html', context)



@login_required
@permission_required('resume.public_open')
def EducationDelete(request, pk):
    # 파라미터pk로 받은 data가 존재한다면 가져온다
    education = get_object_or_404(Education, pk=pk)
    education.delete()
    return HttpResponseRedirect(reverse('education_list'))




# 사원 list
class EmployeeList(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = 'resume.public_open'
    model = Employee
    paginate_by = 15

    #검색 결과 (초기값)
    def get_queryset(self):
        filter_val_1 = self.request.GET.get('filter_1', '')  #filter_1 검색조건 변수명, '' 초기 검색조건값 <- like 검색결과 all 검색을 위해서 ''로 처리함.
        filter_val_2 = self.request.GET.get('filter_2', '')
        order = self.request.GET.get('orderby', 'emp_name') #정렬대상 컬럼명(초기값)

        # 일부 data list에서 제외 처리함.
        if str(self.request.user) == 'kmandu':
            new_context = Employee.objects.filter(
                emp_name__icontains=filter_val_1,
                emp_position_cd__comm_code_name__icontains=filter_val_2,
            ).order_by(order)  #sort컬럼 2개이상도 가능 ","로 구분하여 입력하면됨.
        else:
            new_context = Employee.objects.filter(
                emp_name__icontains=filter_val_1,
                emp_position_cd__comm_code_name__icontains=filter_val_2,
            ).exclude(emp_id=2).order_by(order)  #sort컬럼 2개이상도 가능 ","로 구분하여 입력하면됨.

        return new_context

    #검색 조건 (초기값)
    def get_context_data(self, **kwargs):
        context = super(EmployeeList, self).get_context_data(**kwargs)
        context['filter_1'] = self.request.GET.get('filter_1', '')
        context['filter_2'] = self.request.GET.get('filter_2', '')
        context['orderby'] = self.request.GET.get('orderby', 'emp_name') #정렬대상 컬럼명(초기값)
        return context



@login_required
@permission_required('resume.public_open')
def EmployeeUpdate(request, pk):

    if pk:
        #master model instance 생성
        employee = Employee.objects.get(emp_id=pk)
    else:
        employee = Employee()

    # master form instance 생성 : 마스터 form 객체는 forms.py에 존재함. : 최초 user화면에 보여주는 수정대상 instance
    employee_form = EmployeeForm(instance=employee)

    #detail from instance 생성 : 최초 user화면에 보여주는 수정대상 instance
    school_hisformset = School_hisFormset(instance=employee)
    license_hisformset = License_hisFormset(instance=employee)
    work_hisformset = Work_hisFormset(instance=employee)
    edu_hisformset2 = Edu_hisFormset2(instance=employee)
    pjt_hisformset2 = Pjt_hisFormset2(instance=employee)



    if request.method == "POST":     #user의 수정화면을 통한 instance 수정요청이면 데이터 처리.
        # master form instance 생성 : Post요청 data로 생성
        employee_form = EmployeeForm(request.POST)


        if pk:
            # master form instance 생성 : Post요청 data와 pk에 해당하는 마스터 모델 instance연계
            employee_form = EmployeeForm(request.POST, instance=employee)

        # detail form instance 생성 : Post요청 data로 생성
        school_hisformset = School_hisFormset(request.POST, request.FILES)
        license_hisformset = License_hisFormset(request.POST, request.FILES)
        work_hisformset = Work_hisFormset(request.POST, request.FILES)
        edu_hisformset2 = Edu_hisFormset2(request.POST, request.FILES)
        pjt_hisformset2 = Pjt_hisFormset2(request.POST, request.FILES)



        if employee_form.is_valid():
            created_employee = employee_form.save(commit=False)
            school_hisformset = School_hisFormset(request.POST, request.FILES, instance=created_employee)
            license_hisformset = License_hisFormset(request.POST, request.FILES, instance=created_employee)
            work_hisformset = Work_hisFormset(request.POST, request.FILES, instance=created_employee)
            edu_hisformset2 = Edu_hisFormset2(request.POST, request.FILES, instance=created_employee)
            pjt_hisformset2 = Pjt_hisFormset2(request.POST, request.FILES, instance=created_employee)



            if school_hisformset.is_valid() and license_hisformset.is_valid() and work_hisformset.is_valid() and edu_hisformset2.is_valid() and pjt_hisformset2.is_valid():
                created_employee.save()
                employee_form.save_m2m()
                school_hisformset.save()
                license_hisformset.save()
                work_hisformset.save()
                edu_hisformset2.save()
                pjt_hisformset2.save()



                return HttpResponseRedirect(reverse('employee_list'))
            else:
                print("detail valid error발생")
                print(school_hisformset.errors)
                print(license_hisformset.errors)
                print(work_hisformset.errors)
                print(edu_hisformset2.errors)
                print(pjt_hisformset2.errors)



    # template의 html에 Form과 data instance를 딕셔너리 자료형태를 생성한다.
    context = {
        'employee_form': employee_form,
        'school_hisformset': school_hisformset,
        'license_hisformset': license_hisformset,
        'work_hisformset': work_hisformset,
        'edu_hisformset2': edu_hisformset2,
        'pjt_hisformset2': pjt_hisformset2,
        'employee': employee,
    }

    # template를 호출한다. context도 같이 넘긴다.
    return render(request, 'resume/employee_update.html', context)



# 신규입력 : 수정과 동일하지만 일부분 수정
# 수정1 : 함수명 변경 및 파라미터 pk 삭제
# 수정2 : if pk 지우고 master model 빈 instance 생성으로 변경
# 수정3 : 2번째 if pk 삭제
@login_required
@permission_required('resume.public_open')
def EmployeeCreate(request):
    # master model 빈 instance 생성
    employee = Employee()

    # master form instance 생성 : 마스터 form 객체는 forms.py에 존재함. : 최초 user화면에 보여주는 수정대상 instance
    employee_form = EmployeeForm(instance=employee)

    #detail from instance 생성 : 최초 user화면에 보여주는 수정대상 instance
    school_hisformset = School_hisFormset(instance=employee)
    license_hisformset = License_hisFormset(instance=employee)
    work_hisformset = Work_hisFormset(instance=employee)
    edu_hisformset2 = Edu_hisFormset2(instance=employee)
    pjt_hisformset2 = Pjt_hisFormset2(instance=employee)

    if request.method == "POST":     #user의 수정화면을 통한 instance 수정요청이면 데이터 처리.
        # master form instance 생성 : Post요청 data로 생성
        employee_form = EmployeeForm(request.POST)

        # detail form instance 생성 : Post요청 data로 생성
        school_hisformset = School_hisFormset(request.POST, request.FILES)
        license_hisformset = License_hisFormset(request.POST, request.FILES)
        work_hisformset = Work_hisFormset(request.POST, request.FILES)
        edu_hisformset2 = Edu_hisFormset2(request.POST, request.FILES)
        pjt_hisformset2 = Pjt_hisFormset2(request.POST, request.FILES)


        if employee_form.is_valid():
            created_employee = employee_form.save(commit=False)
            school_hisformset = School_hisFormset(request.POST, request.FILES, instance=created_employee)
            license_hisformset = License_hisFormset(request.POST, request.FILES, instance=created_employee)
            work_hisformset = Work_hisFormset(request.POST, request.FILES, instance=created_employee)
            edu_hisformset2 = Edu_hisFormset2(request.POST, request.FILES, instance=created_employee)
            pjt_hisformset2 = Pjt_hisFormset2(request.POST, request.FILES, instance=created_employee)

            if school_hisformset.is_valid() and license_hisformset.is_valid() and work_hisformset.is_valid() and edu_hisformset2.is_valid() and pjt_hisformset2.is_valid():
                created_employee.save()
                employee_form.save_m2m()
                school_hisformset.save()
                license_hisformset.save()
                work_hisformset.save()
                edu_hisformset2.save()
                pjt_hisformset2.save()
                return HttpResponseRedirect(reverse('employee_list'))
            else:
                print("detail valid error발생")
                print(school_hisformset.errors)
                print(license_hisformset.errors)
                print(work_hisformset.errors)
                print(edu_hisformset2.errors)
                print(pjt_hisformset2.errors)

    # template의 html에 Form과 data instance를 딕셔너리 자료형태를 생성한다.
    context = {
        'employee_form': employee_form,
        'school_hisformset': school_hisformset,
        'license_hisformset': license_hisformset,
        'work_hisformset': work_hisformset,
        'edu_hisformset2': edu_hisformset2,
        'pjt_hisformset2': pjt_hisformset2,
        'employee': employee,
    }

    # template를 호출한다. context도 같이 넘긴다.
    return render(request, 'resume/employee_update.html', context)


@login_required
@permission_required('resume.public_open')
def EmployeeDelete(request, pk):
    # 파라미터pk로 받은 data가 존재한다면 가져온다
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return HttpResponseRedirect(reverse('employee_list'))



# 프로젝트 popup용 list
class Pjt_popup(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = 'resume.public_open'
    model = Pjt
    paginate_by = 10
    context_object_name = 'pjt_popup'
    template_name = 'resume/pjt_popup.html'

    #검색 결과 (초기값)
    def get_queryset(self):
        filter_val_1 = self.request.GET.get('filter_1', '')  #filter_1 검색조건 변수명, '' 초기 검색조건값 <- like 검색결과 all 검색을 위해서 ''로 처리함.
        filter_val_2 = self.request.GET.get('filter_2', '')
        order = self.request.GET.get('orderby', 'pjt_name') #정렬대상 컬럼명(초기값)

        new_context = Pjt.objects.filter(
            pjt_name__icontains=filter_val_1,
            order_comp_id__order_comp_name__icontains=filter_val_2,
        ).order_by(order)  #sort컬럼 2개이상도 가능 ","로 구분하여 입력하면됨.
        return new_context

    #검색 조건 (초기값)
    def get_context_data(self, **kwargs):
        context = super(Pjt_popup, self).get_context_data(**kwargs)
        context['filter_1'] = self.request.GET.get('filter_1', '')
        context['filter_2'] = self.request.GET.get('filter_2', '')
        context['orderby'] = self.request.GET.get('orderby', 'pjt_name') #정렬대상 컬럼명(초기값)
        context['inputId'] = self.request.GET.get('inputId') #팝업 호출버튼 클릭 시 버튼을 클릭한 input type의 id 전달 : 팝업 선택 결과 return시 해당 input에 data 전달하기 위함.
        return context




# 엑셀 파일 생성 & 파일 download
from django.shortcuts import render
import pandas as pd


from django.http import HttpResponse, Http404
import os

#@login_required
@permission_required('resume.public_closed')
def DownloadEmp(request):
    vw_emp_cnt = Vw_emp.objects.all().count()
    vw_emp_list = list(Vw_emp.objects.all().values('POSITION_NAME', 'EMP_NAME', 'SKILL_GRADE'))

    school_his_list = list(School_his.objects.all().values('emp_id__emp_position_cd__comm_code_name', 'emp_id__emp_name', 'school_name', 'school_subject',
                                                           'graduate_date', 'evidence_status_cd__comm_code_name', 'summary'))


#    vw_emp_cnt = Vw_emp.objects.all().count()
#    print(Vw_emp.objects.all())
#    print(list(Vw_emp.objects.all().values()))

##### 엑셀 한개 sheet
#    df = pd.DataFrame(list(Vw_emp.objects.all().values()))  # 리스트에 기록
#    df = pd.DataFrame(list(Vw_emp.objects.all().values('POSITION_NAME', 'EMP_NAME')))  # 리스트에 기록 : 특정 필드선택가능
#    df.to_excel(excel_writer='emp.xlsx', sheet_name='01.인원', index=False) #to 엑셀파일, 열명 제외(index)

    ##### 엑셀 여러개 sheet
    if str(request.user) == 'kmandu':
        df1 = pd.DataFrame(list(Vw_emp.objects.all().values()))  # 리스트에 기록
    else:
        df1 = pd.DataFrame(list(Vw_emp.objects.all().values().exclude(EMP_ID=2)))  # 리스트에 기록


    df1.columns = ['사번','직위','사원명','등급','가동상태','투입 가능시점','성별','생년월일','연령(만)','주민번호','최종학력',
                   '주소','입사일자','퇴사일자','경력기간','타사경력 존재여부','전체 경력 기간','경력 증빙 점검 방법',
                   '정보처리 기사','기타 자격증','위탁교육','기타교육','비고'] #header명 변경

    if str(request.user) == 'kmandu':
        df2 = pd.DataFrame(list(School_his.objects.all().values('emp_id__emp_position_cd__comm_code_name', 'emp_id__emp_name', 'school_name', 'school_subject',
                                                               'graduate_date', 'evidence_status_cd__comm_code_name', 'summary')))  # 리스트에 기록 : 특정 필드선택가능
    else:
        df2 = pd.DataFrame(list(School_his.objects.all().values('emp_id__emp_position_cd__comm_code_name', 'emp_id__emp_name', 'school_name', 'school_subject',
                                                               'graduate_date', 'evidence_status_cd__comm_code_name', 'summary').exclude(emp_id=2)))  # 리스트에 기록 : 특정 필드선택가능

    df2.columns = ['직급','사원명','학교','학과','졸업일자','증빙 점검','비고'] #header명 변경
    df2.columns = pd.MultiIndex.from_tuples(zip(['개인정보', '개인정보', '경력', '경력','경력','경력','경력'], df2.columns)) #header 맨위 1줄 더 추가


    if request.method == "POST":
        # 엑셀 파일 생성 : start
        xlxs_dir = 'emp.xlsx'  # 경로 및 파일명 설정
        with pd.ExcelWriter(xlxs_dir) as writer:
            df1.to_excel(writer, sheet_name='01.인원', index=False)  # 첫번째 시트에 저장
            df2.to_excel(writer, sheet_name='02.학력', index=True)  # 두번째 시트에 저장
        # 엑셀 파일 생성 : end


        # 파일 download : start
        # Django project base directory
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = BASE_DIR + '\emp.xlsx'
        print('파일디렉토리:', file_path)

        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/force_download")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
            # If file is not exists
        raise Http404
        # 파일 download : end


    context = {
        'vw_emp_cnt' : vw_emp_cnt, 'vw_emp_list': vw_emp_list, 'school_his_list': school_his_list,
    }


    return render(request, 'resume/download_emp.html', context=context)









from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus
import urllib

@login_required
@permission_required('resume.public_closed')
def Postno_Popup(request, pk):

    url = 'http://openapi.epost.go.kr/postal/retrieveNewAdressAreaCdSearchAllService/retrieveNewAdressAreaCdSearchAllService/getNewAddressListAreaCdSearchAll'

    queryParams = '?' + urlencode(
        {quote_plus('ServiceKey'): 'unb2bpjZn5ejbwxPpIOnQkgzJ7Tv0Q9AtcF8Y5nIp6TgrY%2BMZ8RM8WL8bwhfd7sRFwQe6V9Ee3kfEcqQ4d8BMA%3D%3D', quote_plus('srchwrd'): '공평동', quote_plus('countPerPage'): '10',
         quote_plus('currentPage'): '1'})

    post_rst = urllib.request.urlopen(url+queryParams).read().decode('utf-8')

    print(post_rst)


