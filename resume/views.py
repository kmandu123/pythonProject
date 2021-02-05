from django.shortcuts import render

# Create your views here.
from resume.models import Comm_div, Comm_code, Employee, School_his, Education

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

class Comm_divListView(generic.ListView):
    model = Comm_div

class Comm_divDetailView(generic.DetailView):
    model = Comm_div


#Comm_div를 update하기 위한 function view
import  datetime
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import Comm_divForm, EmployeeForm, School_hisFormset, License_hisFormset, Work_hisFormset, EducationForm, Edu_hisFormset, Edu_hisFormset2, Skill_hisFormset
#inline Formsets 사용
from django.forms import inlineformset_factory
from django import forms

@permission_required('plans.can_mark_returned')
def UpdateComm(request, pk):

    if pk:
        #master model instance 생성
        comm_div = Comm_div.objects.get(comm_div_id=pk)
    else:
        comm_div = Comm_div()

    # master form instance 생성 : 마스터 form 객체는 forms.py에 존재함. : 최초 user화면에 보여주는 수정대상 instance
    comm_div_form = Comm_divForm(instance=comm_div)

    # detail form 객체 생성
    Comm_codeFormset = inlineformset_factory(Comm_div, Comm_code, fields=('comm_code', 'comm_div_id', 'comm_code_name', 'ref_field', 'display_order', 'use_yn', 'summary'),
                                        widgets={'summary': forms.TextInput(attrs={'size': 70}), 'display_order': forms.TextInput(attrs={'size': 3})}, extra=0, can_delete=True)

    #detail from instance 생성 : 최초 user화면에 보여주는 수정대상 instance
    comm_code_formset = Comm_codeFormset(instance=comm_div)

    if request.method == "POST":     #user의 수정화면을 통한 instance 수정요청이면 데이터 처리.
        # master form instance 생성 : Post요청 data로 생성
        comm_div_form = Comm_divForm(request.POST)

        if pk:
            # master form instance 생성 : Post요청 data와 pk에 해당하는 마스터 모델 instance연계
            comm_div_form = Comm_divForm(request.POST, instance=comm_div)

        # detail form instance 생성 : Post요청 data로 생성
        comm_code_formset = Comm_codeFormset(request.POST, request.FILES)

        if comm_div_form.is_valid():
            created_comm_div = comm_div_form.save(commit=False)
            comm_code_formset = Comm_codeFormset(request.POST, request.FILES, instance=created_comm_div)

            if comm_code_formset.is_valid():
                created_comm_div.save()
                comm_code_formset.save()
                return HttpResponseRedirect(reverse('comm_divs'))
            else:
                print("detail valid error발생")
                print(comm_code_formset.errors)

    # template의 html에 Form과 data instance를 딕셔너리 자료형태를 생성한다.
    context = {
        'comm_div_form': comm_div_form,
        'comm_code_formset': comm_code_formset,
        'comm_div': comm_div,
    }

    # template를 호출한다. context도 같이 넘긴다.
    return render(request, 'resume/update_comm_div.html', context)



#Comm_div를 create하기 위한 function view
def CreateComm(request):
    # master model 빈 instance 생성
    comm_div = Comm_div()

    # master form 빈 instance 생성 : 마스터 form 객체는 forms.py에 존재함. : 최초 user화면에 보여주는 빈 instance
    comm_div_form = Comm_divForm(instance=comm_div)

    # detail form 객체 생성
    Comm_codeFormset = inlineformset_factory(Comm_div, Comm_code,
                       fields=('comm_code', 'comm_div_id', 'comm_code_name', 'ref_field', 'display_order', 'use_yn', 'summary'),
                       widgets={
                                'summary': forms.TextInput(attrs={'size': 70}),
                                'display_order': forms.TextInput(attrs={'size': 3})
                               },
                       extra=1, can_delete=True)


    if request.method == "POST":
        # master form instance 생성 : Post요청 data로 생성
        comm_div_form = Comm_divForm(request.POST)

        # detail form instance 생성 : Post요청 data로 생성
        comm_code_formset = Comm_codeFormset(request.POST, request.FILES)

        if comm_div_form.is_valid():
            created_comm_div = comm_div_form.save(commit=False)
            comm_code_formset = Comm_codeFormset(request.POST, request.FILES, instance=created_comm_div)

            if comm_code_formset.is_valid():
                created_comm_div.save()
                comm_code_formset.save()
                return HttpResponseRedirect(reverse('comm_divs'))
            else:
                print("detail valid error발생")
                print(comm_code_formset.errors)

    else:
        comm_div_form = Comm_divForm(instance=comm_div)
        comm_code_formset = Comm_codeFormset()


    # template의 html에 Form을 딕셔너리 자료형태를 생성한다.
    context = {
        'comm_div_form': comm_div_form,
        'comm_code_formset': comm_code_formset,
    }

    # template를 호출한다. context도 같이 넘긴다.
    return render(request, 'resume/create_comm_div.html', context)




#Comm_div를 delete하기 위한 function view
def DeleteComm(request, pk):
    # 파라미터pk로 받은 data가 존재한다면 가져온다
    comm_div = get_object_or_404(Comm_div, pk=pk)
    comm_div.delete()
    return HttpResponseRedirect(reverse('comm_divs'))


# 사원 list
class EmployeeList(generic.ListView):
    model = Employee



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


        if employee_form.is_valid():
            created_employee = employee_form.save(commit=False)
            school_hisformset = School_hisFormset(request.POST, request.FILES, instance=created_employee)
            license_hisformset = License_hisFormset(request.POST, request.FILES, instance=created_employee)
            work_hisformset = Work_hisFormset(request.POST, request.FILES, instance=created_employee)
            edu_hisformset2 = Edu_hisFormset2(request.POST, request.FILES, instance=created_employee)

            if school_hisformset.is_valid() and license_hisformset.is_valid() and work_hisformset.is_valid() and edu_hisformset2.is_valid() and skill_hisformset.is_valid():
                created_employee.save()
                school_hisformset.save()
                license_hisformset.save()
                work_hisformset.save()
                edu_hisformset2.save()
                return HttpResponseRedirect(reverse('employee_list'))
            else:
                print("detail valid error발생")
                print(school_hisformset.errors)
                print(license_hisformset.errors)
                print(work_hisformset.errors)
                print(edu_hisformset2.errors)

    # template의 html에 Form과 data instance를 딕셔너리 자료형태를 생성한다.
    context = {
        'employee_form': employee_form,
        'school_hisformset': school_hisformset,
        'license_hisformset': license_hisformset,
        'work_hisformset': work_hisformset,
        'edu_hisformset2': edu_hisformset2,
        'employee': employee,
    }

    # template를 호출한다. context도 같이 넘긴다.
    return render(request, 'resume/employee_update.html', context)



# 교육 list
class EducationList(generic.ListView):
    model = Education


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
