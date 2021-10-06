import random
import numpy as np
import time

def uniform():
    ret = random.uniform(0, 1)
    return ret

def randomint(a, b):
    ret = random.randint(a,b)
    return ret

dt = 0.01
mult = 1
n_pop = mult*10000
n_loc = mult*2750
n_net = mult*250
n_overlap = n_net + 1
n_hospitals = mult*2
n_asym = mult*10
maxppl = 10000
states = ["S", "A", "P", "MI", "SI", "R", "H"]
S = 0
A = 1
P = 2
MI = 3
SI = 4
R = 5
H = 6
n_states = 7
person_attr = 4
Cpars = [1, 1, 1, 1, 0.1, 0.1]

n = [0]*n_states

total_loc_confined_time = 14
total_isolation_time = 14
if_positive_test_after = 14
days_bw_hq_tests = 0
days_bw_lq_tests = 0
rate = np.empty((n_states, n_states))
pop = np.empty((n_pop, person_attr))
n_per_location = np.empty((n_loc, n_states))
people_linked_to = np.empty((n_loc, maxppl))
quarantine_confined = True
op_width = 1 + n_states + 3 + 2 + 1
positives = 0 


def shuffle(start, end, arr):
    if(end-start>1):
        for i in range(start,end):
            j = i + int((randomint(1,101)/((100/(end-i))+1)))
            t = arr[j]
            arr[j] = arr[i]
            arr[i] = t


def create_person(arr, state, home):
    arr[0] = state
    arr[1] = home
    arr[2] = randomint(0, n_net)
    arr[3] = home


def createPopulation():
    n[S] = n_pop-n_asym
    n[A] = n_asym
    n[P] = 0
    n[MI] = 0
    n[SI] = 0
    n[R] = 0
    n[H] = 0

    for i in range(0, n_loc):
        for j in range(0, n_states):
            n_per_location[i][j]=0

    for i in range(0, n_pop):
        home = randomint(n_overlap-1, n_loc)
        create_person(pop[i], S, home)
        n_per_location[pop[i][3]][S] += 1

    temp_people = [0]*n_asym
    random_person = 0

    for i in range(0, n_asym):
        flag = False
        while(flag == False):
            random_person = randomint(0,n_pop)
            flag = True

            for j in range(0, n_asym):
                if(temp_people[j] == random_person):
                    flag = False
                    break
        
        temp_people[i] = random_person
    
    for i in range(0, n_asym):
        pop[temp_people[i]][0] = 1
        n_per_location[pop[temp_people[i]][3]][S] -= 1
        n_per_location[pop[temp_people[i]][3]][A] += 1

    for i in range(0, n_loc):
        for j in range(0, maxppl):
            if(people_linked_to[i][j]==-1):
                break
            people_linked_to[i][j] =-1
    
    for i in range(0, n_loc):
        counter = 0
        for j in range(0, n_pop):
            if(pop[j][1]==i or pop[j][2]==i):
                people_linked_to[i][counter] = j
                counter += 1

            people_linked_to[i][counter] = -1  



def writetofile(output, tf, Tpars, begin_at, test_frac, time_taken, details, iter) :

    errno = 0
    filename = ("C:\Users\Adi\Desktop\BTP\exampl\Targeted_BeginAt_%s_DTR_%g_RAT_%g_%g_PCR_%g_%g_%f%f-%i.txt" % (begin_at,test_frac,Tpars[0][0],Tpars[0][3],Tpars[1][0],Tpars[1][3],uniform(),uniform(),iter))

    fh = open(filename, 'w')

    if (fh) :
        fh.write("###### TEST LOG ####################\n")
        fh.write("# Time taken               : %.2f s\n"%time_taken)

        fh.write("# Test Parameters: \n")
        fh.write("# %.2f %.2f %.2f %.2f\n" % (Tpars[0][0], Tpars[0][1], Tpars[0][2], Tpars[0][3]))
        fh.write("# %.2f %.2f %.2f %.2f\n" % (Tpars[1][0], Tpars[1][1], Tpars[1][2], Tpars[1][3]))

        fh.write("# Confined Less Infective? : %s\n" % str(details[0]))
        fh.write("# Homes Quarantined?       : %s\n" % str(details[1]))
        fh.write("# Quarantine when sampled? : %s\n"  % str(details[2]))
        fh.write("# Testing Started When     : %.2f%% recovered\n" % begin_at)
        fh.write("# Fraction Tested Daily    : %.2f%%\n" % test_frac)

        fh.write("# LQ Tests Done in total   : %d\n" % details[3])
        fh.write("# HQ Tests Done in total   : %d\n" % details[4])
        fh.write("# All Tests Done in total  : %d\n" % details[5])
        fh.write("# Results Given in total   : %d\n" % details[6])
        fh.write("# Locations Moved in total : %d\n" % details[7])
        fh.write("# Total recovered HCW      : %d\n" % details[8])
        fh.write("# Total HCW                : %d\n" % details[9])

        fh.write("# Rate Array: \n")
        for i in range(n_states) :
            fh.write("# ")
            for j in range(n_states) :
                fh.write("%5g " % rate[i][j])
            fh.write("\n")

        fh.write("###### END LOG #####################\n")
        fh.write("#\n")
        fh.write("# %s %s %s %s %s %s %s %s %s %s %s %s %s %s\n" % ("Day","nS","nA","nP","nMI","nSI","nR","nH","PCR_conducted_today", "RAT_conducted_today", "Tests_remaining_today", "Agents_currently_confined", "Quarantines_removed_today","Locations_in_quarantine_today"))

        for i in range(tf) :
            for j in range(op_width) :
                fh.write("%i " % output[i][j])
            fh.write("\n")
        
        fh.close()

    else :
        print("File error, %d\n" % (errno))    



def Targeted_Run(Tpars, tf, lock_homes, quarantine_when_sample_taken, begin_at, test_frac, iter):
    start = time.clock()
    is_confined = np.empty(n_pop, dtype=bool)
    being_tested = np.empty(n_pop, dtype=bool)
    loc_confined = np.empty(n_loc, dtype=bool)

    last_test_type = np.full((1,n_pop), -1000)
    last_test_result = np.full((1,n_pop), -1000)

    test_result = np.empty(n_pop)
    next_test_date = np.empty(n_pop)

    result_declared_date = np.full((1,n_pop), -1000)
    loc_confined_time = np.full((1,n_loc), -1000)
    person_isolated_time = np.full((1,n_pop), -1000)

    hq_tests_conducted = 0
    lq_tests_conducted = 0
    tests_conducted    = 0
    results_declared   = 0
    locations_moved    = 0
    r = np.empty((n_states,n_states))

    alphaH = 1 - Cpars[4]
    alphaQ = 1 - Cpars[5]

    tests_available_daily = (test_frac/100) * n_pop
    tests_remaining_today = (test_frac/100) * n_pop

    lq_tests_daily = Tpars[0][3]*tests_available_daily
    lq_tests_today = Tpars[0][3]*tests_available_daily

    hq_tests_daily = Tpars[1][3]*tests_available_daily
    hq_tests_today = Tpars[1][3]*tests_available_daily

    lq_sens = Tpars[0][0]
    lq_spec = Tpars[0][1]
    lq_delay= Tpars[0][2]

    hq_sens = Tpars[1][0]
    hq_spec = Tpars[1][1]
    hq_delay= Tpars[1][2]

    t = 0.0
    day  = 0
    midday_move_completed = False
    output = np.empty((tf+1, op_width))

    output[day][0] = day
    for s in range(0, n_states):
        output[day][s+1]=n[s]

    output[day][n_states+1]=hq_tests_conducted
    output[day][n_states+2]=lq_tests_conducted
    output[day][n_states+3]=tests_remaining_today
    output[day][n_states+4]=0
    output[day][n_states+5]=0
    output[day][n_states+6]=0

    exit_rate = np.empty(n_states)

    r[A][R] = rate[A][R]
    r[P][MI] = rate[P][MI]
    r[P][SI] = rate[P][SI]
    r[MI][R] = rate[MI][R]
    r[SI][R] = rate[SI][R]
    r[SI][H] = rate[SI][H]
    r[H][R] = rate[H][R] 

    exit_rate[A] = r[A][R]
    exit_rate[P] = r[P][MI] + r[P][SI]
    exit_rate[MI]= r[MI][R]
    exit_rate[SI]= r[SI][R] + r[SI][H]
    exit_rate[R] = 0
    exit_rate[H] = r[H][R]

    while(t<tf):
        if(midday_move_completed == False and (t-day)>0.5):
            midday_move_completed = True
            for i in range(0, n_pop):
                if((pop[i][0] != H) and (is_confined[i] == False) and (loc_confined[pop[i][3]] == False)):
                    locations_moved += 1
                    home_loc = pop[i][1]
                    work_loc = pop[i][2]
                    if(pop[i][3]==home_loc):
                        pop[i][3] = work_loc
                        n_per_location[home_loc][pop[i][0]] -= 1
                        n_per_location[work_loc][pop[i][0]] += 1

    
    for i in range(0, n_loc):
        N=0
        for j in range(0, n_states):
            N += n_per_location[i][j]

        if(N==0):    #faaltu me kara h jarurat nahi thi iski
            continue

        backup = np.empty(n_states)
        ind = np.empty(N)
        counter = 0

        for j in range(0, n_pop):
            if(people_linked_to[i][j] == -1):
                break
            elif(pop[people_linked_to[i][j]][3] == i):
                ind[counter] = people_linked_to[i][j]
                backup[pop[ind[counter]][0]] += 1
                counter += 1
        
        if(counter != N):
            print("Error in location",i ,", N=",N ,", counter =", counter)

        conf_by_state_in_loc = np.empty(n_states)
        tot_conf = 0
        if(quarantine_confined == True):
            for j in range(0, N):
                p = ind[j]           
                if(is_confined[p] == True):
                    conf_by_state_in_loc[pop[p][0]] += 1
                    tot_conf += 1

        
        if((loc_confined[i])==True and (conf_by_state_in_loc[S]+conf_by_state_in_loc[A]+conf_by_state_in_loc[P]+conf_by_state_in_loc[MI]+conf_by_state_in_loc[SI]+conf_by_state_in_loc[R]+conf_by_state_in_loc[H]) == 0):
            loc_confined[i]=False
            loc_confined_time[i]=-1000


        shuffle(0,N,ind)
        newN = n_per_location[i][S]+n_per_location[i][A]+n_per_location[i][P]+n_per_location[i][MI]+n_per_location[i][SI]+n_per_location[i][R]+n_per_location[i][H]
        V = newN - (alphaH*n_per_location[i][H])

        
        r[S][A] = rate[S][A] * (1/V) * (Cpars[0]*(n_per_location[i][A]- conf_by_state_in_loc[A]*alphaQ) + Cpars[1]*(n_per_location[i][P]- conf_by_state_in_loc[P]*alphaQ) + Cpars[2]*(n_per_location[i][MI]-conf_by_state_in_loc[MI]*alphaQ) + Cpars[3]*(n_per_location[i][SI]-conf_by_state_in_loc[SI]*alphaQ) + Cpars[4]*n_per_location[i][H])                                    

        r[S][P] = rate[S][P] * (1/V) * (Cpars[0]*(n_per_location[i][A]- conf_by_state_in_loc[A]*alphaQ) + Cpars[1]*(n_per_location[i][P]- conf_by_state_in_loc[P]*alphaQ) + Cpars[2]*(n_per_location[i][MI]-conf_by_state_in_loc[MI]*alphaQ) + Cpars[3]*(n_per_location[i][SI]-conf_by_state_in_loc[SI]*alphaQ) + Cpars[4]*n_per_location[i][H])                            

        exit_rate[S] = r[S][A] + r[S][P]

        for j in range(N):
            newN = n_per_location[i][S]+n_per_location[i][A]+n_per_location[i][P]+n_per_location[i][MI]+n_per_location[i][SI]+n_per_location[i][R]+n_per_location[i][H]    
            V = newN - alphaH*n_per_location[i][H]
            r[S][A] = rate[S][A] * (1/V) * (Cpars[0]*(n_per_location[i][A]- conf_by_state_in_loc[A]*alphaQ) + Cpars[1]*(n_per_location[i][P]- conf_by_state_in_loc[P]*alphaQ) + Cpars[2]*(n_per_location[i][MI]-conf_by_state_in_loc[MI]*alphaQ) + Cpars[3]*(n_per_location[i][SI]-conf_by_state_in_loc[SI]*alphaQ) + Cpars[4]*n_per_location[i][H])                                    
               
            r[S][P] = rate[S][P] * (1/V) * (Cpars[0]*(n_per_location[i][A]- conf_by_state_in_loc[A]*alphaQ) + Cpars[1]*(n_per_location[i][P]- conf_by_state_in_loc[P]*alphaQ) + Cpars[2]*(n_per_location[i][MI]-conf_by_state_in_loc[MI]*alphaQ) + Cpars[3]*(n_per_location[i][SI]-conf_by_state_in_loc[SI]*alphaQ) + Cpars[4]*n_per_location[i][H])  
            exit_rate[S] = r[S][A] + r[S][P]                       
            
            if((r[S][A] <0) or (r[S][P]<0)) :
                print("Negative rates")
            
            fro = pop[ind[j]][0]
            
            if(uniform() < exit_rate[fro]*dt) :
                p = uniform()
                temp = 0

                for to in range(n_states) :
                    temp = temp + (r[fro][to]/exit_rate[fro])
                    if(p<temp) :
                        pop[ind[j]][0] = to
                        n_per_location[i][fro] -= 1 
                        n_per_location[i][to] += 1
                        n[fro]-=1
                        n[to]+=1

                        if(is_confined[ind[j]]== True) :
                            conf_by_state_in_loc[fro] -=1
                            conf_by_state_in_loc[to] +=1
                            if((conf_by_state_in_loc[S]<0) or (conf_by_state_in_loc[A]<0) or (conf_by_state_in_loc[P]<0) or (conf_by_state_in_loc[MI]<0) or (conf_by_state_in_loc[SI]<0) or (conf_by_state_in_loc[R]<0) or (conf_by_state_in_loc[H]<0)) :
                                print("Negative confs\n")

                        if(to==H) :
                            h = random.randint(0,n_hospitals)
                            while(h==pop[ind[j]][2]) :
                                h = random.randint(0,n_hospitals)

                            for s in range(n_pop) :
                                if(people_linked_to[h][s] == -1) :
                                    people_linked_to[h][s] = ind[j]
                                    people_linked_to[h][s+1] = -1
                                    break              
                            
                            if(is_confined[ind[j]]== True) :
                                is_confined[ind[j]] = False
                                person_isolated_time[ind[j]] = -1000
                                conf_by_state_in_loc[H]-=1 

                            n_per_location[ pop[ind[j]][3]][H] -= 1
                            pop[ind[j]][3] = h
                            n_per_location[ pop[ind[j]][3]][H] +=1

                        elif (fro ==H and to == R) :
                            is_confined[ind[j]] = False
                            n_per_location[ pop[ind[j]][3] ][R]-= 1
                            pop[ind[j]][3] = pop[ind[j]][1]
                            n_per_location[ pop[ind[j]][3] ][R]+= 1        

                        r[S][A] = rate[S][A]* 1/V *(Cpars[0]*(n_per_location[i][A]- conf_by_state_in_loc[A]*alphaQ) + Cpars[1]*(n_per_location[i][P]- conf_by_state_in_loc[P]*alphaQ) + Cpars[2]*(n_per_location[i][MI]-conf_by_state_in_loc[MI]*alphaQ) + Cpars[3]*(n_per_location[i][SI]-conf_by_state_in_loc[SI]*alphaQ) +Cpars[4]*n_per_location[i][H])  

                        r[S][P] = rate[S][P]* 1/V *(Cpars[0]*(n_per_location[i][A]- conf_by_state_in_loc[A]*alphaQ) + Cpars[1]*(n_per_location[i][P]- conf_by_state_in_loc[P]*alphaQ) +Cpars[2]*(n_per_location[i][MI]-conf_by_state_in_loc[MI]*alphaQ) + Cpars[3]*(n_per_location[i][SI]-conf_by_state_in_loc[SI]*alphaQ) +Cpars[4]*n_per_location[i][H]) 
                        
                        exit_rate[S] = r[S][A] + r[S][P]
                        break