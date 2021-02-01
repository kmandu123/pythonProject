from django.shortcuts import render

# Create your views here.
from resume.models import Comm_div, Comm_code

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

from .forms import Comm_divForm
#inline Formsets 사용
from django.forms import inlineformset_factory

@permission_required('plans.can_mark_returned')
def UpdateComm(request, pk):
    from django import forms

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
def CreateComm_div(request):

    from django import forms
    # inlineformset 생성
    CommFormset = inlineformset_factory(Comm_div, Comm_code, fields=('comm_code_name', 'ref_field', 'display_order', 'use_yn', 'summary'),
                                        widgets={'summary': forms.TextInput(attrs={'size': 70}), 'display_order': forms.TextInput(attrs={'size': 3})}, extra=0, can_delete=True)
    comm_div = Comm_div.objects.get()

    print("첫번째")

    # POST 요청이면 폼 데이터를 처리한다
    if request.method == 'POST':
        print("두번째")

        # 요청된 data를 FORM객체를 이용해 Form인스턴스를 생성한다.(binding)
        comm_div_update_form = UpdateComm_divForm(request.POST)
        # inline 새로 작성한 내용을 저장 <- 여기에 기술하지 않으면 마스터수정 없이 저장누를때 validation 수행하지 않고 error발생함.
#        formset = CommFormset(request.POST, instance=comm_div)

        # form이 유효한지 체크한다
        if comm_div_update_form.is_valid(): #and formset.is_valid():
            print("세번째")

            #동일한 comm_div_name 값이 있는지 check
            #chk_comm_div_name = list(Comm_div.objects.all().values())
            #chk_comm_div_name = Comm_div.objects.filter(comm_div_name = 'f_comm_div_name').exists

            #clean data를 모델 필드에 써넣어 처리한다.
            comm_div.comm_div_name = comm_div_update_form.cleaned_data['f_comm_div_name']
            comm_div.summary = comm_div_update_form.cleaned_data['f_summary']
            comm_div.create_dt = comm_div_update_form.cleaned_data['f_create_dt']
            comm_div.update_dt = comm_div_update_form.cleaned_data['f_update_dt']
            comm_div.save()

            #이위치에 반드시 아래 기록할 것 : 없으면 error발생함. if문 위에 기술했더니 error발생 함
            formset = CommFormset(request.POST, instance=comm_div)

            if formset.is_valid():
                formset.save()
                print("인라인 정상")
            else:
                print("인라인 error발생")
                print(formset.errors)


            # 새로운 URL로 보낸다. 예) update 성공메시지가 있는곳
            return HttpResponseRedirect(reverse('comm_divs'))
        #else:
        #    print("마스터 not valid")
        #    print(comm_div_update_form.errors)
        #    return HttpResponseRedirect(reverse('comm_divs'))

    # GET 요청이면 기본 폼을 생성(즉, 최초의 수정요청 화면으로 이동 시)
    else:
        print("네번째")

        # 일자계산하여 form의 날짜 필드에 default 값 세팅 : 예제
        #proposed_create_date = datetime.date.today() + datetime.timedelta(weeks=3)
        #comm_div_update_form = UpdateComm_divForm(initial={'f_create_date': proposed_create_date})

        #빈 form 전달
        comm_div_update_form = UpdateComm_divForm()

        # inline formset : 빈 form 전달
        formset = CommFormset()


    # template의 html에 Form과 data instance를 딕셔너리 자료형태를 생성한다.
    context = {
        'form': comm_div_update_form,
        'inline_form': formset,
    }

    print("다섯번째")

    # template를 호출한다. context도 같이 넘긴다.
    return render(request, 'resume/create_comm_div.html', context)


#Comm_div를 delete하기 위한 function view
def DeleteComm_div(request, pk):
    # 파라미터pk로 받은 data가 존재한다면 가져온다
    comm_div = get_object_or_404(Comm_div, pk=pk)
    comm_div.delete()
    return HttpResponseRedirect(reverse('comm_divs'))



