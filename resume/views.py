from django.shortcuts import render

# Create your views here.
from resume.models import Comm_div, Comm_code, Employee, School_his, Education, Order_comp, Pjt

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_divs = Comm_div.objects.all().count()

    # 공통코드 중 '학습Item'인 건수

    # The 'all()' is implied by default.
    num_comm_codes = Comm_code.objects.count()

    context = {
        'num_divs': num_divs,
        'num_comm_codes': num_comm_codes,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


from django.views import generic


# 공통구분 list
class  Comm_divList(generic.ListView):
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


@permission_required('plans.can_mark_returned')
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



#Comm_div를 delete하기 위한 function view
def Comm_divDelete(request, pk):
    # 파라미터pk로 받은 data가 존재한다면 가져온다
    comm_div = get_object_or_404(Comm_div, pk=pk)
    comm_div.delete()
    return HttpResponseRedirect(reverse('comm_div_list'))


# 발주처 list
class Order_compList(generic.ListView):
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



def Order_compDelete(request, pk):
    # 파라미터pk로 받은 data가 존재한다면 가져온다
    order_comp = get_object_or_404(Order_comp, pk=pk)
    order_comp.delete()
    return HttpResponseRedirect(reverse('order_comp_list'))



# 프로젝트 list
class PjtList(generic.ListView):
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


from django.contrib import messages
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



def PjtDelete(request, pk):
    # 파라미터pk로 받은 data가 존재한다면 가져온다
    pjt = get_object_or_404(Pjt, pk=pk)
    pjt.delete()
    return HttpResponseRedirect(reverse('pjt_list'))



# 발주처 popup용 list
class Order_comp_popup(generic.ListView):
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
class EducationList(generic.ListView):
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



def EducationDelete(request, pk):
    # 파라미터pk로 받은 data가 존재한다면 가져온다
    education = get_object_or_404(Education, pk=pk)
    education.delete()
    return HttpResponseRedirect(reverse('education_list'))




# 사원 list
class EmployeeList(generic.ListView):
    model = Employee
    paginate_by = 15

    #검색 결과 (초기값)
    def get_queryset(self):
        filter_val_1 = self.request.GET.get('filter_1', '')  #filter_1 검색조건 변수명, '' 초기 검색조건값 <- like 검색결과 all 검색을 위해서 ''로 처리함.
        filter_val_2 = self.request.GET.get('filter_2', '')
        order = self.request.GET.get('orderby', 'emp_name') #정렬대상 컬럼명(초기값)

        new_context = Employee.objects.filter(
            emp_name__icontains=filter_val_1,
            emp_position_cd__comm_code_name__icontains=filter_val_2,
        ).order_by(order)  #sort컬럼 2개이상도 가능 ","로 구분하여 입력하면됨.
        return new_context

    #검색 조건 (초기값)
    def get_context_data(self, **kwargs):
        context = super(EmployeeList, self).get_context_data(**kwargs)
        context['filter_1'] = self.request.GET.get('filter_1', '')
        context['filter_2'] = self.request.GET.get('filter_2', '')
        context['orderby'] = self.request.GET.get('orderby', 'emp_name') #정렬대상 컬럼명(초기값)
        return context



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


def EmployeeDelete(request, pk):
    # 파라미터pk로 받은 data가 존재한다면 가져온다
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return HttpResponseRedirect(reverse('employee_list'))



# 프로젝트 popup용 list
class Pjt_popup(generic.ListView):
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
        return context





from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus
import urllib

def Postno_Popup(request, pk):

    url = 'http://openapi.epost.go.kr/postal/retrieveNewAdressAreaCdSearchAllService/retrieveNewAdressAreaCdSearchAllService/getNewAddressListAreaCdSearchAll'

    queryParams = '?' + urlencode(
        {quote_plus('ServiceKey'): 'unb2bpjZn5ejbwxPpIOnQkgzJ7Tv0Q9AtcF8Y5nIp6TgrY%2BMZ8RM8WL8bwhfd7sRFwQe6V9Ee3kfEcqQ4d8BMA%3D%3D', quote_plus('srchwrd'): '공평동', quote_plus('countPerPage'): '10',
         quote_plus('currentPage'): '1'})

    post_rst = urllib.request.urlopen(url+queryParams).read().decode('utf-8')

    print(post_rst)


