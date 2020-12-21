#크롤링을 위한 import
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
from youtube_croller import parse, instagram_parse
from tablib import Dataset
from .resource import InfluencerResource
from django.shortcuts import render,redirect, HttpResponse, get_object_or_404,resolve_url
from django.contrib import messages
from django.http import HttpResponse
from .models import *
from login.models import Account

# Create your views here.

def main(request):
    context = {}
    if request.user.is_authenticated:
        contract = Contract.objects.all()
        account = Account.objects.get(user=request.user)
        celly_btn = ID_btn.objects.all()
        context.setdefault('contract', contract)
        context.setdefault('nickname', account.nickname)
        context.setdefault('position', account.position)
        context.setdefault('celly_btn', celly_btn)
    if request.method == 'POST':

        youtube_search = request.POST.get('search_youtube')
        condition_up = request.POST.get('condition_up')#최대 구독자수
        condition_down = request.POST.get('condition_down')#최소 구독자수
        insta_search = request.POST.get('search_insta')
        internal_search = request.POST.get('search_DB')

        if youtube_search != None and insta_search == None and internal_search == None:
            condition_up = int(condition_up)
            condition_down = int(condition_down)
            result_list = parse.croller(youtube_search)
            i = 1
            for node in result_list:
                result = Youtube_result()
                result.id = i
                result.channel_name = node.channel_name
                result.subscriber_num = node.subscriber_num
                result.not_int_subscriber_num = node.not_int_subscriber_num
                result.profile_url = node.profile_url
                result.save()
                i +=1
            result_all = Youtube_result.objects.all()
            return render(request,'youtube_result.html',{'search':youtube_search, 'result':result_all, 'condition_up':condition_up, 'condition_down':condition_down})
        if insta_search != None and youtube_search == None and internal_search == None:
            result_list,relevent_keyword_list = instagram_parse.insta_croller(insta_search)
            output = ''
            for keyword in relevent_keyword_list:
                output = output + ('#'+keyword + ', ')
                if keyword == relevent_keyword_list[-1]:
                    output = output[:-2]
            i = 1
            for node in result_list:
                result = Instagram_result()
                result.id = i
                result.insta_id = node.insta_id
                result.profile_url = node.profile_url
                result.save()
                i +=1
            result_all = Instagram_result.objects.all()
            return render(request,'instagram_result.html',{'search':insta_search, 'result':result_all, 'relevent_keyword': output})    
        if internal_search != None and youtube_search == None and insta_search == None:
            all_influencer = Influencer_DB.objects.all()
            result = []
            for influencer in all_influencer:
                if internal_search in influencer.name or internal_search in influencer.insta_url or influencer.email == internal_search or internal_search in influencer.brand_name or internal_search in influencer.keyword:
                    result.append(influencer)
            return render(request,'internal_result.html',{'internal_search':internal_search,'result':result})
    return render(request,'main.html',context)


def go_back_and_clean(request):
    old_youtube_result = Youtube_result.objects.all()
    old_instagram_result = Instagram_result.objects.all()
    old_instagram_result.delete()
    old_youtube_result.delete()
    return redirect('home')

def create_contract(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        category = request.POST.get('category')
        end_date = request.POST.get('end_date')
        new_contract = Contract()
        new_contract.name = company_name
        new_contract.category = category
        new_contract.end_date = end_date
        new_contract.save()
        return redirect('home')
    return render(request,'create_contract.html')

def delete_contract(request, contract_id):
    contract = Contract.objects.get(id=contract_id)
    contract.delete()
    return redirect('home')

def show_record(request,contract_id):
    context = {}
    account = Account.objects.get(user=request.user)
    contract = get_object_or_404(Contract,pk=contract_id)
    record = Record.objects.all().filter(contract=contract)
    context.setdefault('account', account)
    context.setdefault('record', record)
    context.setdefault('contract', contract)
    if request.method == 'POST':
        insta_id = request.POST.get('insta_id')
        influencer = request.POST.get('influencer')
        feed_condition = request.POST.get('feed_condition')
        new_record = Record()
        new_record.contract = contract
        new_record.insta_id = insta_id
        new_record.influencer = influencer
        new_record.writer = account.nickname
        new_record.feed_condition = feed_condition
        new_record.is_confirmed = False
        new_record.save()
        return render(request,'contract_board.html',context)
    return render(request,'contract_board.html',context)

def confirm(request, record_id, contract_id):
    contract = get_object_or_404(Contract, pk = contract_id)
    record = Record.objects.get(id=record_id)
    record.is_confirmed = True
    record.save()
    return redirect('/contract_board/'+str(contract_id))

def wait(request, record_id,contract_id):
    contract = get_object_or_404(Contract, pk = contract_id)
    record = Record.objects.get(id=record_id)
    record.is_confirmed = False
    record.save()
    return redirect('/contract_board/'+str(contract_id))

def delete(request, record_id, contract_id):
    contract = get_object_or_404(Contract, pk = contract_id)
    record = Record.objects.filter(contract=contract, id=record_id)
    record.delete()
    return redirect('/contract_board/'+str(contract_id))


def btn_create(request):
    if request.method == "POST":
        celly_id = request.POST.get('celly_id')
        celly_pw = request.POST.get('celly_pw')
        if celly_id=='' or celly_pw == '':
            messages.info(request,"모든 항목을 채워주세요.")
            return redirect('btn_create')
        new_btn = ID_btn()
        new_btn.celly_id = celly_id
        new_btn.celly_pw = celly_pw
        new_btn.save()
        return redirect('home')
    return render(request,'create_celly_btn.html')

    
def celly_btn_info(request, btn_id):
    celly_btn = get_object_or_404(ID_btn, pk = btn_id)
    account = Account.objects.get(user=request.user)
    context = {'celly_btn':celly_btn, 'account':account }
    if request.method == 'POST':
        new_pw = request.POST.get('new_celly_pw')
        celly_btn.celly_pw = new_pw
        celly_btn.save()
        return redirect('btn_info', btn_id)
            
    return render(request, "btn_info.html",context)
        

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

    













