def making_cases(case_list,god,mode):
    ##모드
    ##1: 표준533
    ##2: 표준3332
    ##3: 상의변형2333
    ##4: 하의변형3233
    ##5: 신발변형3323
    ##6: 32/33

    #신화
    #0:없음
    #1:상의
    #2:팔찌
    #3:귀걸이
    result_list=[]
    
    if mode==1: ################################################################################
        if god==0:
            for i in case_list:
                temp_make=[]
                for j in i:
                    if int(j) <116:
                        set_type_list=['11','12','13','14','15']
                    elif int(j) <120:
                        set_type_list=['21','22','23']
                    elif int(j) <124:
                        set_type_list=['31','32','33']
                    for k in set_type_list:
                        temp_make.append(k+str(j)[1:3]+'0')
                result_list.append(temp_make)
        if god==1:
            for i in case_list:
                temp_make=[]
                for j in i:
                    if int(j) <116:
                        set_type_list=['12','13','14','15']
                        temp_make.append('11'+str(j)[1:3]+'1')
                    elif int(j) <120:
                        set_type_list=['21','22','23']
                    elif int(j) <124:
                        set_type_list=['31','32','33']
                    for k in set_type_list:
                        temp_make.append(k+str(j)[1:3]+'0')
                result_list.append(temp_make)
        if god==2:
            for i in case_list:
                temp_make=[]
                for j in i:
                    if int(j) <116:
                        set_type_list=['11','12','13','14','15']
                    elif int(j) <120:
                        set_type_list=['22','23']
                        temp_make.append('21'+str(j)[1:3]+'1')
                    elif int(j) <124:
                        set_type_list=['31','32','33']
                    for k in set_type_list:
                        temp_make.append(k+str(j)[1:3]+'0')
                result_list.append(temp_make)
        if god==3:
            for i in case_list:
                temp_make=[]
                for j in i:
                    if int(j) <116:
                        set_type_list=['11','12','13','14','15']
                    elif int(j) <120:
                        set_type_list=['21','22','23']
                    elif int(j) <124:
                        set_type_list=['31','32']
                        temp_make.append('33'+str(j)[1:3]+'1')
                    for k in set_type_list:
                        temp_make.append(k+str(j)[1:3]+'0')
                result_list.append(temp_make)


    elif mode==2: ################################################################################
        if god==0:
            for i in case_list:
                temp_make=[]
                for j in i:
                    if int(j) < 116:
                        set_type_list=['13','14']
                    elif int(j) <128:
                        set_type_list=['12','21','32']
                    elif int(j) <132:
                        set_type_list=['11','22','31']
                    elif int(j) <136:
                        set_type_list=['15','23','33']
                    for k in set_type_list:
                        temp_make.append(k+str(j)[1:3]+'0')
                result_list.append(temp_make)
        if god==1:
            for i in case_list:
                temp_make=[]
                for j in i:
                    if int(j) < 116:
                        set_type_list=['13','14']
                    elif int(j) <128:
                        set_type_list=['12','21','32']
                    elif int(j) <132:
                        set_type_list=['22','31']
                        temp_make.append('11'+str(j)[1:3]+'1')
                    elif int(j) <136:
                        set_type_list=['15','23','33']
                    for k in set_type_list:
                        temp_make.append(k+str(j)[1:3]+'0')
                result_list.append(temp_make)
        if god==2:
            for i in case_list:
                temp_make=[]
                for j in i:
                    if int(j) < 116:
                        set_type_list=['13','14']
                    elif int(j) <128:
                        set_type_list=['12','32']
                        temp_make.append('21'+str(j)[1:3]+'1')
                    elif int(j) <132:
                        set_type_list=['11','22','31']
                    elif int(j) <136:
                        set_type_list=['15','23','33']
                    for k in set_type_list:
                        temp_make.append(k+str(j)[1:3]+'0')
                result_list.append(temp_make)
        if god==3:
            for i in case_list:
                temp_make=[]
                for j in i:
                    if int(j) < 116:
                        set_type_list=['13','14']
                    elif int(j) <128:
                        set_type_list=['12','21','32']
                    elif int(j) <132:
                        set_type_list=['11','22','31']
                    elif int(j) <136:
                        set_type_list=['15','23']
                        temp_make.append('33'+str(j)[1:3]+'1')
                    for k in set_type_list:
                        temp_make.append(k+str(j)[1:3]+'0')
                result_list.append(temp_make)


    elif mode==3: ################################################################################
        if god==0:
            for i in case_list:
                temp_make=[]
                for j in i:
                    if int(j) < 116:
                        set_type_list=['11','13','14']
                    elif int(j) <128:
                        set_type_list=['12','21','32']
                    elif int(j) <132:
                        set_type_list=['22','31']
                    elif int(j) <136:
                        set_type_list=['15','23','33']
                    for k in set_type_list:
                        temp_make.append(k+str(j)[1:3]+'0')
                result_list.append(temp_make)
        if god==1:
            for i in case_list:
                temp_make=[]
                for j in i:
                    if int(j) < 116:
                        set_type_list=['13','14']
                        temp_make.append('11'+str(j)[1:3]+'1')
                    elif int(j) <128:
                        set_type_list=['12','21','32']
                    elif int(j) <132:
                        set_type_list=['22','31']
                    elif int(j) <136:
                        set_type_list=['15','23','33']
                    for k in set_type_list:
                        temp_make.append(k+str(j)[1:3]+'0')
                result_list.append(temp_make)
        if god==2:
            for i in case_list:
                temp_make=[]
                for j in i:
                    if int(j) < 116:
                        set_type_list=['11','13','14']
                    elif int(j) <128:
                        set_type_list=['12','32']
                        temp_make.append('21'+str(j)[1:3]+'1')
                    elif int(j) <132:
                        set_type_list=['22','31']
                    elif int(j) <136:
                        set_type_list=['15','23','33']
                    for k in set_type_list:
                        temp_make.append(k+str(j)[1:3]+'0')
                result_list.append(temp_make)
        if god==3:
            for i in case_list:
                temp_make=[]
                for j in i:
                    if int(j) < 116:
                        set_type_list=['11','13','14']
                    elif int(j) <128:
                        set_type_list=['12','21','32']
                    elif int(j) <132:
                        set_type_list=['22','31']
                    elif int(j) <136:
                        set_type_list=['15','23']
                        temp_make.append('33'+str(j)[1:3]+'1')
                    for k in set_type_list:
                        temp_make.append(k+str(j)[1:3]+'0')
                result_list.append(temp_make)


    elif mode==4: ################################################################################
        if god==0:
            for i in case_list:
                temp_make=[]
                for j in i:
                    if int(j) < 116:
                        set_type_list=['12','13','14']
                    elif int(j) <128:
                        set_type_list=['21','32']
                    elif int(j) <132:
                        set_type_list=['11','22','31']
                    elif int(j) <136:
                        set_type_list=['15','23','33']
                    for k in set_type_list:
                        temp_make.append(k+str(j)[1:3]+'0')
                result_list.append(temp_make)
        if god==1:
            for i in case_list:
                temp_make=[]
                for j in i:
                    if int(j) < 116:
                        set_type_list=['12','13','14']
                    elif int(j) <128:
                        set_type_list=['21','32']
                    elif int(j) <132:
                        set_type_list=['22','31']
                        temp_make.append('11'+str(j)[1:3]+'1')
                    elif int(j) <136:
                        set_type_list=['15','23','33']
                    for k in set_type_list:
                        temp_make.append(k+str(j)[1:3]+'0')
                result_list.append(temp_make)
        if god==2:
            for i in case_list:
                temp_make=[]
                for j in i:
                    if int(j) < 116:
                        set_type_list=['12','13','14']
                    elif int(j) <128:
                        set_type_list=['32']
                        temp_make.append('21'+str(j)[1:3]+'1')
                    elif int(j) <132:
                        set_type_list=['11','22','31']
                    elif int(j) <136:
                        set_type_list=['15','23','33']
                    for k in set_type_list:
                        temp_make.append(k+str(j)[1:3]+'0')
                result_list.append(temp_make)
        if god==3:
            for i in case_list:
                temp_make=[]
                for j in i:
                    if int(j) < 116:
                        set_type_list=['12','13','14']
                    elif int(j) <128:
                        set_type_list=['21','32']
                    elif int(j) <132:
                        set_type_list=['11','22','31']
                    elif int(j) <136:
                        set_type_list=['15','23']
                        temp_make.append('33'+str(j)[1:3]+'1')
                    for k in set_type_list:
                        temp_make.append(k+str(j)[1:3]+'0')
                result_list.append(temp_make)


    elif mode==5: ################################################################################
        if god==0:
            for i in case_list:
                temp_make=[]
                for j in i:
                    if int(j) < 116:
                        set_type_list=['13','14','15']
                    elif int(j) <128:
                        set_type_list=['12','21','32']
                    elif int(j) <132:
                        set_type_list=['11','22','31']
                    elif int(j) <136:
                        set_type_list=['23','33']
                    for k in set_type_list:
                        temp_make.append(k+str(j)[1:3]+'0')
                result_list.append(temp_make)
        if god==1:
            for i in case_list:
                temp_make=[]
                for j in i:
                    if int(j) < 116:
                        set_type_list=['13','14','15']
                    elif int(j) <128:
                        set_type_list=['12','21','32']
                    elif int(j) <132:
                        set_type_list=['22','31']
                        temp_make.append('11'+str(j)[1:3]+'1')
                    elif int(j) <136:
                        set_type_list=['23','33']
                    for k in set_type_list:
                        temp_make.append(k+str(j)[1:3]+'0')
                result_list.append(temp_make)
        if god==2:
            for i in case_list:
                temp_make=[]
                for j in i:
                    if int(j) < 116:
                        set_type_list=['13','14','15']
                    elif int(j) <128:
                        set_type_list=['12','32']
                        temp_make.append('21'+str(j)[1:3]+'1')
                    elif int(j) <132:
                        set_type_list=['11','22','31']
                    elif int(j) <136:
                        set_type_list=['23','33']
                    for k in set_type_list:
                        temp_make.append(k+str(j)[1:3]+'0')
                result_list.append(temp_make)
        if god==3:
            for i in case_list:
                temp_make=[]
                for j in i:
                    if int(j) < 116:
                        set_type_list=['13','14','15']
                    elif int(j) <128:
                        set_type_list=['12','21','32']
                    elif int(j) <132:
                        set_type_list=['11','22','31']
                    elif int(j) <136:
                        set_type_list=['23']
                        temp_make.append('33'+str(j)[1:3]+'1')
                    for k in set_type_list:
                        temp_make.append(k+str(j)[1:3]+'0')
                result_list.append(temp_make)



    if mode==6: ################################################################################
        if god==0:
            for i in case_list:
                temp_make=[]
                for j in i:
                    if len(j)==3:
                        if int(j) <116:
                            pass
                        elif int(j) <120:
                            set_type_list=['21','22','23']
                        elif int(j) <124:
                            set_type_list=['31','32','33']
                        for k in set_type_list:
                            temp_make.append(k+str(j)[1:3]+'0')
                    elif len(j)==15: ## X11 X22 X33 X44 X55 
                        temp_make.append('11'+j[1:3]+'0')
                        temp_make.append('12'+j[4:6]+'0')
                        temp_make.append('13'+j[7:9]+'0')
                        temp_make.append('14'+j[10:12]+'0')
                        temp_make.append('15'+j[13:]+'0')
                result_list.append(temp_make)
        if god==1:
            for i in case_list:
                temp_make=[]
                for j in i:
                    if len(j)==3:
                        if int(j) <116:
                            pass
                        elif int(j) <120:
                            set_type_list=['21','22','23']
                        elif int(j) <124:
                            set_type_list=['31','32','33']
                        for k in set_type_list:
                            temp_make.append(k+str(j)[1:3]+'0')
                    elif len(j)==15: ## X11 X22 X33 X44 X55 
                        temp_make.append('11'+j[1:3]+'1')
                        temp_make.append('12'+j[4:6]+'0')
                        temp_make.append('13'+j[7:9]+'0')
                        temp_make.append('14'+j[10:12]+'0')
                        temp_make.append('15'+j[13:]+'0')
                result_list.append(temp_make)
        if god==2:
            for i in case_list:
                temp_make=[]
                for j in i:
                    if len(j)==3:
                        if int(j) <116:
                            pass
                        elif int(j) <120:
                            set_type_list=['22','23']
                            temp_make.append('21'+str(j)[1:3]+'1')
                        elif int(j) <124:
                            set_type_list=['31','32','33']
                        for k in set_type_list:
                            temp_make.append(k+str(j)[1:3]+'0')
                    elif len(j)==15: ## X11 X22 X33 X44 X55 
                        temp_make.append('11'+j[1:3]+'0')
                        temp_make.append('12'+j[4:6]+'0')
                        temp_make.append('13'+j[7:9]+'0')
                        temp_make.append('14'+j[10:12]+'0')
                        temp_make.append('15'+j[13:]+'0')
                result_list.append(temp_make)
        if god==3:
            for i in case_list:
                temp_make=[]
                for j in i:
                    if len(j)==3:
                        if int(j) <116:
                            pass
                        elif int(j) <120:
                            set_type_list=['21','22','23']
                        elif int(j) <124:
                            set_type_list=['31','32']
                            temp_make.append('33'+str(j)[1:3]+'1')
                        for k in set_type_list:
                            temp_make.append(k+str(j)[1:3]+'0')
                    elif len(j)==15: ## X11 X22 X33 X44 X55 
                        temp_make.append('11'+j[1:3]+'0')
                        temp_make.append('12'+j[4:6]+'0')
                        temp_make.append('13'+j[7:9]+'0')
                        temp_make.append('14'+j[10:12]+'0')
                        temp_make.append('15'+j[13:]+'0')
                result_list.append(temp_make)



    return result_list
