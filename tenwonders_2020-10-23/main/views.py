import urllib.parse
from youtube_croller import parse, instagram_parse
from tablib import Dataset
from .resource import InfluencerResource
from django.shortcuts import render,redirect, HttpResponse, get_object_or_404,resolve_url
from django.contrib import messages
from django.http import HttpResponse
from .models import *
from login.models import Account
from openpyxl import load_workbook
from datetime import datetime



# Create your views here.

def main(request):
    context = {}
    if request.user.is_authenticated:
        work = Work.objects.all()
        account = Account.objects.get(user=request.user)
        notice = Notice.objects.all()
        mywork = []

        for i in work:
            if account in i.assigned_worker.all():
                mywork.append(i)

        context.setdefault('work', work)
        context.setdefault('nickname', account.nickname)
        context.setdefault('position', account.position)
        context.setdefault('notice',notice)
        context.setdefault('mywork',mywork)
    # if request.method == 'POST':

    #     youtube_search = request.POST.get('search_youtube')
    #     condition_up = request.POST.get('condition_up')#최대 구독자수
    #     condition_down = request.POST.get('condition_down')#최소 구독자수
    #     insta_search = request.POST.get('search_insta')
    #     internal_search = request.POST.get('search_DB')

    #     if youtube_search != None and insta_search == None and internal_search == None:
    #         condition_up = int(condition_up)
    #         condition_down = int(condition_down)
    #         result_list = parse.croller(youtube_search)
    #         i = 1
    #         for node in result_list:
    #             result = Youtube_result()
    #             result.id = i
    #             result.channel_name = node.channel_name
    #             result.subscriber_num = node.subscriber_num
    #             result.not_int_subscriber_num = node.not_int_subscriber_num
    #             result.profile_url = node.profile_url
    #             result.save()
    #             i +=1
    #         result_all = Youtube_result.objects.all()
    #         return render(request,'youtube_result.html',{'search':youtube_search, 'result':result_all, 'condition_up':condition_up, 'condition_down':condition_down})
    #     if insta_search != None and youtube_search == None and internal_search == None:
    #         result_list,relevent_keyword_list = instagram_parse.insta_croller(insta_search)
    #         output = ''
    #         for keyword in relevent_keyword_list:
    #             output = output + ('#'+keyword + ', ')
    #             if keyword == relevent_keyword_list[-1]:
    #                 output = output[:-2]
    #         i = 1
    #         for node in result_list:
    #             result = Instagram_result()
    #             result.id = i
    #             result.insta_id = node.insta_id
    #             result.profile_url = node.profile_url
    #             result.save()
    #             i +=1
    #         result_all = Instagram_result.objects.all()
    #         return render(request,'instagram_result.html',{'search':insta_search, 'result':result_all, 'relevent_keyword': output})    
    #     if internal_search != None and youtube_search == None and insta_search == None:
    #         all_influencer = Influencer_DB.objects.all()
    #         result = []
    #         for influencer in all_influencer:
    #             if internal_search in influencer.name or internal_search in influencer.insta_url or influencer.email == internal_search or internal_search in influencer.brand_name or internal_search in influencer.keyword:
    #                 result.append(influencer)
    #         return render(request,'internal_result.html',{'internal_search':internal_search,'result':result})
    return render(request,'main.html',context)

def internal_search(request):
    internal_search = request.POST.get('search_DB')
    account = Account.objects.get(user=request.user)
    all_influencer = Influencer_DB.objects.all()
    result = []
    if request.method == "POST":
        for influencer in all_influencer:
            if internal_search in influencer.name or internal_search in influencer.insta_url or influencer.email == internal_search or internal_search in influencer.brand_name or internal_search in influencer.keyword:
                result.append(influencer)
        return render(request,'internal_result.html',{'internal_search':internal_search,'result':result})
    return render(request,"internal_search.html",{"account":account})
                


# def go_back_and_clean(request):
#     old_youtube_result = Youtube_result.objects.all()
#     old_instagram_result = Instagram_result.objects.all()
#     old_instagram_result.delete()
#     old_youtube_result.delete()
#     return redirect('home')

def work_create(request):
    if request.method == 'POST':
        work_name = request.POST.get('work_name')
        content = request.POST.get('content')
        new_work = Work()
        new_work.name = work_name
        new_work.content = content
        new_work.save()
        return redirect('home')
    return render(request,'work_create.html')

def work_detail(request, work_id):
    account = Account.objects.get(user=request.user)
    all_account = Account.objects.all()
    work = Work.objects.get(pk = work_id)
    assigned_worker = work.assigned_worker.all()
    log = Log.objects.all()
    log_list = []
    for i in log:
        if i.work == work:
            log_list.append(i)

    not_assigned = []
    for i in all_account:
        if i.position == "근로장학생":
            if i not in assigned_worker:
                not_assigned.append(i)


    if request.method == "POST":
        myfile = request.FILES['myfile']
        myfile.name = work.name+'_'+datetime.today().strftime("%Y.%m.%d")+'_'+account.nickname
        work.file = myfile
        work.save()
        log = Log()
        log.work = work
        log.worker = account
        log.save()
        return render(request,"work_detail.html",{"work":work,"account":account,"not_assigned":not_assigned,"assigned":assigned_worker,"logs":log_list})

    
    return render(request,"work_detail.html",{"work":work,"account":account,"not_assigned":not_assigned,"assigned":assigned_worker,"logs":log_list})
    

def work_delete(request, work_id):
    work = Work.objects.get(id=work_id)
    work.delete()
    return redirect('home')

def assign_worker(request,work_id,worker_id):
    account = Account.objects.get(user=request.user)
    work = Work.objects.get(pk=work_id)
    worker = Account.objects.get(pk=worker_id)
    work.assigned_worker.add(worker)
    assigned_worker = work.assigned_worker.all()
    all_account = Account.objects.all()
    not_assigned = []
    for i in all_account:
        if i.position == "근로장학생":
            if i not in assigned_worker:
                not_assigned.append(i)
    return redirect('work_detail',work_id)

def exclude_worker(request,work_id,worker_id):
    account = Account.objects.get(user=request.user)
    work = Work.objects.get(pk=work_id)
    worker = Account.objects.get(pk=worker_id)
    work.assigned_worker.remove(worker)
    assigned_worker = work.assigned_worker.all()
    all_account = Account.objects.all()
    not_assigned = []
    for i in all_account:
        if i.position == "근로장학생":
            if i not in assigned_worker:
                not_assigned.append(i)
    return redirect('work_detail',work_id)


# def show_record(request,contract_id):
#     context = {}
#     account = Account.objects.get(user=request.user)
#     contract = get_object_or_404(Contract,pk=contract_id)
#     record = Record.objects.all().filter(contract=contract)
#     context.setdefault('account', account)
#     context.setdefault('record', record)
#     context.setdefault('contract', contract)
#     if request.method == 'POST':
#         insta_id = request.POST.get('insta_id')
#         influencer = request.POST.get('influencer')
#         feed_condition = request.POST.get('feed_condition')
#         new_record = Record()
#         new_record.contract = contract
#         new_record.insta_id = insta_id
#         new_record.influencer = influencer
#         new_record.writer = account.nickname
#         new_record.feed_condition = feed_condition
#         new_record.is_confirmed = False
#         new_record.save()
#         return render(request,'contract_board.html',context)
#     return render(request,'contract_board.html',context)

# def confirm(request, record_id, contract_id):
#     contract = get_object_or_404(Contract, pk = contract_id)
#     record = Record.objects.get(id=record_id)
#     record.is_confirmed = True
#     record.save()
#     return redirect('/contract_board/'+str(contract_id))

# def wait(request, record_id,contract_id):
#     contract = get_object_or_404(Contract, pk = contract_id)
#     record = Record.objects.get(id=record_id)
#     record.is_confirmed = False
#     record.save()
#     return redirect('/contract_board/'+str(contract_id))

# def delete(request, record_id, contract_id):
#     contract = get_object_or_404(Contract, pk = contract_id)
#     record = Record.objects.filter(contract=contract, id=record_id)
#     record.delete()
#     return redirect('/contract_board/'+str(contract_id))


# def btn_create(request):
#     if request.method == "POST":
#         celly_id = request.POST.get('celly_id')
#         celly_pw = request.POST.get('celly_pw')
#         if celly_id=='' or celly_pw == '':
#             messages.info(request,"모든 항목을 채워주세요.")
#             return redirect('btn_create')
#         new_btn = ID_btn()
#         new_btn.celly_id = celly_id
#         new_btn.celly_pw = celly_pw
#         new_btn.save()
#         return redirect('home')
#     return render(request,'create_celly_btn.html')

    
# def celly_btn_info(request, btn_id):
#     celly_btn = get_object_or_404(ID_btn, pk = btn_id)
#     account = Account.objects.get(user=request.user)
#     context = {'celly_btn':celly_btn, 'account':account }
#     if request.method == 'POST':
#         new_pw = request.POST.get('new_celly_pw')
#         celly_btn.celly_pw = new_pw
#         celly_btn.save()
#         return redirect('btn_info', btn_id)
            
#     return render(request, "btn_info.html",context)
        

def btn_push(request, btn_id):
    account = Account.objects.get(user=request.user)
    selected_btn = ID_btn.objects.get(id=btn_id)
    if selected_btn.now_using ==False:
        selected_btn.now_using = True
        selected_btn.using_worker = account.nickname
        selected_btn.save()
    else:
        selected_btn.now_using = False
        selected_btn.using_worker = '없음'
        selected_btn.save()
    
    return redirect('btn_info',btn_id)


def btn_delete(request,btn_id):
    selected_btn = ID_btn.objects.get(id=btn_id)
    selected_btn.delete()
    return redirect('home')

def btn_condition_change(request, btn_id):
    selected_btn = ID_btn.objects.get(id=btn_id)
    if selected_btn.dm_blocked == False:
        selected_btn.dm_blocked = True
        selected_btn.save()
    else:
        selected_btn.dm_blocked=False
        selected_btn.save()
    return redirect('btn_info',btn_id)


def notice_create(request):
    if request.method == 'POST':
        account = Account.objects.get(user=request.user)
        title = request.POST.get('title')
        content = request.POST.get('content')
        status = request.POST.get('status')
        new_notice = Notice()
        new_notice.title = title
        new_notice.content = content
        new_notice.writer = account
        new_notice.status = status
        new_notice.save()
        return redirect('home')
    return render(request,'notice_create.html')

def notice_detail(request, notice_id):
    account = Account.objects.get(user=request.user)
    notice = get_object_or_404(Notice, pk = notice_id)
    return render(request,'notice_detail.html',{'notice':notice, 'account':account})

def notice_delete(request, notice_id):
    notice = get_object_or_404(Notice, pk = notice_id)
    notice.delete()
    return redirect('home')

# 미팅 기록 기능
def meeting(request):
    account = Account.objects.get(user=request.user)
    meeting = Meeting.objects.all()
    search_meeting = []
    if request.method == "POST":
        column = request.POST.get('column')
        meeting_search = request.POST.get('meeting_search')
        
        if column == "회사명":
            for obj in meeting:
                if meeting_search in obj.company:
                    search_meeting.append(obj)
            meeting = search_meeting
        elif column == "담당자":
            for obj in meeting:
                if meeting_search in obj.encharge_name:
                    search_meeting.append(obj)
            meeting = search_meeting
        elif column == "연락처":
            for obj in meeting:
                if meeting_search in obj.phone_num:
                    search_meeting.append(obj)
            meeting = search_meeting
        elif column == "이메일":
            for obj in meeting:
                if meeting_search in obj.email:
                    search_meeting.append(obj)
            meeting = search_meeting
        elif column == "직원명":
            for obj in meeting:
                if meeting_search in obj.name.nickname:
                    search_meeting.append(obj)
            meeting = search_meeting
    return render(request, 'meeting.html',{'account':account,'meeting':meeting})

def meeting_create(request):
    account = Account.objects.get(user=request.user)
    meeting = Meeting.objects.all()
    if request.method == "POST":
        company = request.POST.get('company')
        encharge_name = request.POST.get('encharge_name')
        position = request.POST.get('position')
        phone_num = request.POST.get('phone_num')
        email = request.POST.get('email')
        company_address = request.POST.get('company_address')
        etc = request.POST.get('etc')
        new_meeting = Meeting()
        new_meeting.company = company
        new_meeting.encharge_name = encharge_name
        new_meeting.position = position
        new_meeting.phone_num = phone_num
        new_meeting.email = email
        new_meeting.company_address = company_address
        new_meeting.etc = etc
        new_meeting.name = account
        new_meeting.save()
        return redirect('meeting')
    return render(request,"meeting_create.html",{'account':account,'meeting':meeting})

def meeting_detail(request, meeting_id):
    account = Account.objects.get(user=request.user)
    meeting = get_object_or_404(Meeting, pk = meeting_id)
    return render(request,'meeting_detail.html',{'meeting':meeting, 'account':account}) 

def meeting_delete(request,meeting_id):
    meeting = get_object_or_404(Meeting,pk=meeting_id)
    meeting.delete()
    return redirect('meeting')






    
    













