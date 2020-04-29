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
        db_save['A257']='13390150';db_save['B257']='+5 퍼펙트컨트롤'
        db_save['C257']=0;db_save['D257']=0;db_save['E257']=0;db_save['F257']=0;db_save['G257']=0
        db_save['H257']=0;db_save['I257']=0;db_save['J257']=0;db_save['K257']=0;db_save['L257']=0
    if db_save['A258'].value!='22390240':
        db_save['A258']='22390240';db_save['B258']='+4 선지자의 목걸이'
        db_save['C258']=0;db_save['D258']=0;db_save['E258']=0;db_save['F258']=0;db_save['G258']=0
        db_save['H258']=0;db_save['I258']=0;db_save['J258']=0;db_save['K258']=0;db_save['L258']=0
    if db_save['A259'].value!='21390340':
        db_save['A259']='21390340';db_save['B259']='+4 독을 머금은 가시장갑'
        db_save['C259']=0;db_save['D259']=0;db_save['E259']=0;db_save['F259']=0;db_save['G259']=0
        db_save['H259']=0;db_save['I259']=0;db_save['J259']=0;db_save['K259']=0;db_save['L259']=0
    if db_save['A260'].value!='23390450':
        db_save['A260']='23390450';db_save['B260']='+5 할기의 링'
        db_save['C260']=0;db_save['D260']=0;db_save['E260']=0;db_save['F260']=0;db_save['G260']=0
        db_save['H260']=0;db_save['I260']=0;db_save['J260']=0;db_save['K260']=0;db_save['L260']=0
    if db_save['A261'].value!='31390540':
        db_save['A261']='31390540';db_save['B261']='+4 청면수라의 가면'
        db_save['C261']=0;db_save['D261']=0;db_save['E261']=0;db_save['F261']=0;db_save['G261']=0
        db_save['H261']=0;db_save['I261']=0;db_save['J261']=0;db_save['K261']=0;db_save['L261']=0
    if db_save['A262'].value!='32390650':
        db_save['A262']='32390650';db_save['B262']='+5 적귀의 차원석'
        db_save['C262']=0;db_save['D262']=0;db_save['E262']=0;db_save['F262']=0;db_save['G262']=0
        db_save['H262']=0;db_save['I262']=0;db_save['J262']=0;db_save['K262']=0;db_save['L262']=0
    if db_save['A263'].value!='33390750':
        db_save['A263']='33390750';db_save['B263']='+5 패스트퓨처 이어링'
        db_save['C263']=0;db_save['D263']=0;db_save['E263']=0;db_save['F263']=0;db_save['G263']=0
        db_save['H263']=0;db_save['I263']=0;db_save['J263']=0;db_save['K263']=0;db_save['L263']=0

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
        

    

    load_preset.save("preset.xlsx")
    load_preset.close()

update_preset()

        
