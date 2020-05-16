## 코드를 무단으로 복제하여 개조 및 배포하지 말 것##

import requests
from bs4 import BeautifulSoup
import urllib.request
from urllib import parse
from json import loads
import tkinter.ttk
import tkinter.font
import tkinter.messagebox
from tkinter import *
import openpyxl
from openpyxl import load_workbook
import itertools
import threading
import time
import numpy as np
from collections import Counter
from math import floor
import webbrowser

def update_preset():

    load_preset=load_workbook("preset.xlsx", data_only=True)
    db_custom=load_preset["custom"]
    db_save=load_preset["one"]

    if db_custom['H1'].value==None:
        db_custom['G1']="up_stat"
        db_custom['H1']=0
    if db_custom['H2'].value==None:
        db_custom['G2']="bless_style"
        db_custom['H2']=3
    if db_custom['H3'].value==None:
        db_custom['G3']="crux_style"
        db_custom['H3']=2
    if db_custom['H4'].value==None:
        db_custom['G4']="bless_plt"
        db_custom['H4']=2
    if db_custom['H5'].value==None:
        db_custom['G5']="bless_cri"
        db_custom['H5']=1
    if db_custom['H6'].value==None:
        db_custom['G6']="up_stat_b"
        db_custom['H6']=0
        
    if db_custom['B14'].value==None:
        db_custom['A14']="ele_inchant"
        db_custom['B14']=116
    if db_custom['B15'].value==None:
        db_custom['A15']="ele_ora"
        db_custom['B15']=20
    if db_custom['B16'].value==None:
        db_custom['A16']="ele_gem"
        db_custom['B16']=7
    if db_custom['B17'].value==None:
        db_custom['A17']="ele_skill"
    db_custom['B17']=0  ## 자속강 비활성화
    if db_custom['B18'].value==None:
        db_custom['A18']="ele_mob_resist"
        db_custom['B18']=50
    if db_custom['B19'].value==None:
        db_custom['A19']="ele_buf_anti"
        db_custom['B19']=60
    if db_save['A257'].value!='13390150':
        db_save['A257']='13390150'
        db_save['C257']=0;db_save['D257']=0;db_save['E257']=0;db_save['F257']=0;db_save['G257']=0
        db_save['H257']=0;db_save['I257']=0;db_save['J257']=0;db_save['K257']=0;db_save['B257']=0
    for i in range(257,264):
        if db_save['B'+str(i)]!=0 and db_save['B'+str(i)]!=1:
            db_save['B'+str(i)]=0
    if db_save['A258'].value!='22390240':
        db_save['A258']='22390240'
        db_save['C258']=0;db_save['D258']=0;db_save['E258']=0;db_save['F258']=0;db_save['G258']=0
        db_save['H258']=0;db_save['I258']=0;db_save['J258']=0;db_save['K258']=0;db_save['B258']=0
    if db_save['A259'].value!='21390340':
        db_save['A259']='21390340'
        db_save['C259']=0;db_save['D259']=0;db_save['E259']=0;db_save['F259']=0;db_save['G259']=0
        db_save['H259']=0;db_save['I259']=0;db_save['J259']=0;db_save['K259']=0;db_save['B259']=0
    if db_save['A260'].value!='23390450':
        db_save['A260']='23390450'
        db_save['C260']=0;db_save['D260']=0;db_save['E260']=0;db_save['F260']=0;db_save['G260']=0
        db_save['H260']=0;db_save['I260']=0;db_save['J260']=0;db_save['K260']=0;db_save['B260']=0
    if db_save['A261'].value!='31390540':
        db_save['A261']='31390540'
        db_save['C261']=0;db_save['D261']=0;db_save['E261']=0;db_save['F261']=0;db_save['G261']=0
        db_save['H261']=0;db_save['I261']=0;db_save['J261']=0;db_save['K261']=0;db_save['B261']=0
    if db_save['A262'].value!='32390650':
        db_save['A262']='32390650'
        db_save['C262']=0;db_save['D262']=0;db_save['E262']=0;db_save['F262']=0;db_save['G262']=0
        db_save['H262']=0;db_save['I262']=0;db_save['J262']=0;db_save['K262']=0;db_save['B262']=0
    if db_save['A263'].value!='33390750':
        db_save['A263']='33390750'
        db_save['C263']=0;db_save['D263']=0;db_save['E263']=0;db_save['F263']=0;db_save['G263']=0
        db_save['H263']=0;db_save['I263']=0;db_save['J263']=0;db_save['K263']=0;db_save['B263']=0

    if db_save['A264'].value!='22400150':  ##2.2.0 패치 산물 14종 추가
        db_save['A264']='22400150'
        db_save['C264']=0;db_save['D264']=0;db_save['E264']=0;db_save['F264']=0;db_save['G264']=0
        db_save['H264']=0;db_save['I264']=0;db_save['J264']=0;db_save['K264']=0;db_save['B264']=0
    if db_save['A265'].value!='22400250':
        db_save['A265']='22400250'
        db_save['C265']=0;db_save['D265']=0;db_save['E265']=0;db_save['F265']=0;db_save['G265']=0
        db_save['H265']=0;db_save['I265']=0;db_save['J265']=0;db_save['K265']=0;db_save['B265']=0
    if db_save['A266'].value!='22400350':
        db_save['A266']='22400350'
        db_save['C266']=0;db_save['D266']=0;db_save['E266']=0;db_save['F266']=0;db_save['G266']=0
        db_save['H266']=0;db_save['I266']=0;db_save['J266']=0;db_save['K266']=0;db_save['B266']=0
    if db_save['A267'].value!='22400450':
        db_save['A267']='22400450'
        db_save['C267']=0;db_save['D267']=0;db_save['E267']=0;db_save['F267']=0;db_save['G267']=0
        db_save['H267']=0;db_save['I267']=0;db_save['J267']=0;db_save['K267']=0;db_save['B267']=0
    if db_save['A268'].value!='22400550':
        db_save['A268']='22400550'
        db_save['C268']=0;db_save['D268']=0;db_save['E268']=0;db_save['F268']=0;db_save['G268']=0
        db_save['H268']=0;db_save['I268']=0;db_save['J268']=0;db_save['K268']=0;db_save['B268']=0
    if db_save['A269'].value!='21400640':
        db_save['A269']='21400640'
        db_save['C269']=0;db_save['D269']=0;db_save['E269']=0;db_save['F269']=0;db_save['G269']=0
        db_save['H269']=0;db_save['I269']=0;db_save['J269']=0;db_save['K269']=0;db_save['B269']=0
    if db_save['A270'].value!='31400750':
        db_save['A270']='31400750'
        db_save['C270']=0;db_save['D270']=0;db_save['E270']=0;db_save['F270']=0;db_save['G270']=0
        db_save['H270']=0;db_save['I270']=0;db_save['J270']=0;db_save['K270']=0;db_save['B270']=0
    if db_save['A271'].value!='31400850':
        db_save['A271']='31400850'
        db_save['C271']=0;db_save['D271']=0;db_save['E271']=0;db_save['F271']=0;db_save['G271']=0
        db_save['H271']=0;db_save['I271']=0;db_save['J271']=0;db_save['K271']=0;db_save['B271']=0
    if db_save['A272'].value!='31400950':
        db_save['A272']='31400950'
        db_save['C272']=0;db_save['D272']=0;db_save['E272']=0;db_save['F272']=0;db_save['G272']=0
        db_save['H272']=0;db_save['I272']=0;db_save['J272']=0;db_save['K272']=0;db_save['B272']=0
    if db_save['A273'].value!='31401050':
        db_save['A273']='31401050'
        db_save['C273']=0;db_save['D273']=0;db_save['E273']=0;db_save['F273']=0;db_save['G273']=0
        db_save['H273']=0;db_save['I273']=0;db_save['J273']=0;db_save['K273']=0;db_save['B273']=0
    if db_save['A274'].value!='31401150':
        db_save['A274']='31401150'
        db_save['C274']=0;db_save['D274']=0;db_save['E274']=0;db_save['F274']=0;db_save['G274']=0
        db_save['H274']=0;db_save['I274']=0;db_save['J274']=0;db_save['K274']=0;db_save['B274']=0
    if db_save['A275'].value!='32401240':
        db_save['A275']='32401240'
        db_save['C275']=0;db_save['D275']=0;db_save['E275']=0;db_save['F275']=0;db_save['G275']=0
        db_save['H275']=0;db_save['I275']=0;db_save['J275']=0;db_save['K275']=0;db_save['B275']=0
    if db_save['A276'].value!='32401340':
        db_save['A276']='32401340'
        db_save['C276']=0;db_save['D276']=0;db_save['E276']=0;db_save['F276']=0;db_save['G276']=0
        db_save['H276']=0;db_save['I276']=0;db_save['J276']=0;db_save['K276']=0;db_save['B276']=0
    if db_save['A277'].value!='32401440':
        db_save['A277']='32401440'
        db_save['C277']=0;db_save['D277']=0;db_save['E277']=0;db_save['F277']=0;db_save['G277']=0
        db_save['H277']=0;db_save['I277']=0;db_save['J277']=0;db_save['K277']=0;db_save['B277']=0
    
    if db_custom['B4'].value==17:  ##2.3.0 쿨감보정 효율 개편
        db_custom['B4']=17 ## 탈리신 효율 아직 고려중

    if db_save['A278'].value!='11410100': ##2.3.1 진레전 추가
        db_save['A278']='11410100'
        db_save['A279']='11410110'
        db_save['A280']='11410120'
        db_save['A281']='11410130'
        db_save['A282']='11410140'
        db_save['A283']='11410150'
        db_save['A284']='21420100'
        db_save['A285']='21420110'
        db_save['A286']='21420120'
        db_save['A287']='21420130'
        db_save['A288']='21420140'
        db_save['A289']='21420150'
        db_save['A290']='33430100'
        db_save['A291']='33430110'
        db_save['A292']='33430120'
        db_save['A293']='33430130'
        db_save['A294']='33430140'
        db_save['A295']='33430150'
        for i in range(278,296):
            db_save['C'+str(i)]=0;db_save['D'+str(i)]=0;db_save['E'+str(i)]=0;db_save['F'+str(i)]=0;db_save['G'+str(i)]=0;
            db_save['H'+str(i)]=0;db_save['I'+str(i)]=0;db_save['J'+str(i)]=0;db_save['K'+str(i)]=0;db_save['B'+str(i)]=0;

    if db_custom['H7'].value==None: ## 2.4.0 아리아 증폭율 커스텀 추가
        db_custom['G7']="aria_up"
        db_custom['H7']="템에따라"

    if db_custom['B3'].value!=0:  ##3.0.0 각성스증 대개편
        db_custom['B3']=0 #비활성화

    if db_save['A296'].value!='11390850': ##신규 산물 5종+융합/잔향 추가
        db_save['A296']='11390850'
        db_save['A297']='12390950'
        db_save['A298']='13391050'
        db_save['A299']='14391150'
        db_save['A300']='15391250'
        db_save['A301']='41510';db_save['A302']='41520';db_save['A303']='41530';db_save['A304']='41540';db_save['A305']='41550'
        db_save['A306']='42510';db_save['A307']='42520';db_save['A308']='42530';db_save['A309']='42540';db_save['A310']='42550'
        db_save['A311']='43510';db_save['A312']='43520';db_save['A313']='43530';db_save['A314']='43540';db_save['A315']='43550'
        for i in ['C','D','E','F','G','H','I','J','K','B']:
            for j in range(296,316):
                db_save[i+str(j)]=0
        for i in ['C','D','E','F','G','H','I','J','K','B']:  ## 세이브 기능 확대
            db_custom[i+'26']='화'
            db_custom[i+'27']='50'
            db_custom[i+'28']='0'
            db_custom[i+'29']='17'
            db_custom[i+'30']='0'
            db_custom[i+'31']='0'
            db_custom[i+'32']='0'
            db_custom[i+'33']='0'
            db_custom[i+'34']='0'
            db_custom[i+'35']='0'
            db_custom[i+'36']='0'
            db_custom[i+'37']='전설↓'
            db_custom[i+'38']='10'
            db_custom[i+'39']='131'
            db_custom[i+'40']='131'
            db_custom[i+'41']='7'
            db_custom[i+'42']='0'
            db_custom[i+'43']='50'
            db_custom[i+'44']='60'
            db_custom[i+'45']='0'
            db_custom[i+'46']='3'
            db_custom[i+'47']='2'
            db_custom[i+'48']='2'
            db_custom[i+'49']='1'
            db_custom[i+'50']='0'
            db_custom[i+'51']='템에따라'
            db_custom['A52']='jobtype_select';db_custom[i+'52']='귀검사(남)'
            db_custom['A53']='jobup_select';db_custom[i+'53']='검신(진각)'
            db_custom['A54']='wep_job_select';db_custom[i+'54']='공통'
            db_custom['A55']='wep_type_select';db_custom[i+'55']='무기타입 선택'
            db_custom['A56']='wep_select';db_custom[i+'56']='(공통)흑천의 주인'
            db_custom['A57']='select_perfect';db_custom[i+'57']='단품포함(중간)'
            db_custom['A58']='style_select';db_custom[i+'58']='추뎀칭호'
            db_custom['A59']='creature_select';db_custom[i+'59']='크증크리쳐'
            db_custom['A60']='req_cool';db_custom[i+'60']='X(순데미지)'
            db_custom['A61']='inv_mod';db_custom[i+'61']='X(순데미지)'
            db_custom['A62']='inv_select1_1';db_custom[i+'62']='미부여'
            db_custom['A63']='inv_select1_2';db_custom[i+'63']='증뎀'
            db_custom['A64']='inv_select2_1';db_custom[i+'64']='10'
            db_custom['A65']='inv_select2_2';db_custom[i+'65']='5'
            db_custom['A66']='inv_select3_1';db_custom[i+'66']='축스탯%/1각'
            db_custom['A67']='inv_select3_2';db_custom[i+'67']='3%/60(상)'
            db_custom['A68']='inv_select4_1';db_custom[i+'68']='축스탯%/1각'
            db_custom['A69']='inv_select4_2';db_custom[i+'69']='3%/40(상)'
            
        
        

    

    load_preset.save("preset.xlsx")
    load_preset.close()


        
