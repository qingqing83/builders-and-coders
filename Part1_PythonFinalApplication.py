#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 22:37:48 2020

@author: Swaggyching
"""

# NOTE TO PROF:
note = """Hi Prof! Please note that our program uses datetime and the 
excel file is generated everyday. The working file is edited based 
on the previous day's CSV. 

In a real life application, the manager is expected to update the
app on a daily basis, hence there would be no need to find and
rename the CSV. 

Hence, we need you to rename the 
UpdatedProjProgress_Nov102020 file to T-1 date:
E.g. UpdatedProjProgress_Nov242020 if you are running the codes on 
the 25th of November.

Thank you!"""

# print(note)

# Import libraries
#%%
import pandas as pd
import numpy as np
from datetime import date, timedelta
import warnings
import sys

warnings.filterwarnings("ignore") 
#%% 

# Import Dataframes and CSV
#%% add in worker id column 
workerlist_df = pd.read_csv("BPPL_WorkerListwAddress.csv")

def gen_id(finid):
    return finid[-4:]
workerlist_df['Worker ID'] = workerlist_df['FIN Number'].apply(gen_id)

workerlist_df.drop(columns=['FIN Number', 'Work Permit Number', 'Work Permit Expiry Date', 'Passport Number', 'Nationality', 'Contract Expiry Date', 'Security Bond Expiry Date', 'Date of Birth'])
#%%

# Datetime
#%% 
today = date.today()
yesterday = today - timedelta(days=1)
todays_date = today.strftime("%b%d%Y")
yesterdays_date = yesterday.strftime("%b%d%Y")
date_format = "%b%d%Y"

proj_yesterday_df = pd.read_csv(f"""UpdatedProjProgress_{yesterdays_date}.csv""")
proj_today_df = proj_yesterday_df
proj_today_df = proj_today_df.dropna(how = "all")
proj_yesterday_df = proj_yesterday_df.dropna(how = "all")


# Menu
#%% 
worker_df_column_names = ["Name of Worker", "Worker ID", "Reason for leave"]
reasons_for_leave_df = pd.DataFrame(columns = worker_df_column_names)

manager_df_column_names = ["Project ID", "Total SqFt of Project", "SqFt Left", "Days Left", "Deadline",	"% Left", "Workers Assigned"]
manager_update_proj_df = pd.DataFrame(columns = manager_df_column_names)

def main_nav():
    main_txt = """
    ==================================================================
             ヾ(⌐■_■)ノ♪ ヾ(⌐■_■)ノ♪  ヾ(⌐■_■)ノ♪  ヾ(⌐■_■)ノ♪           
                                 MAIN MENU              
    ==================================================================
    Good morning! Are you a manager or worker?
    [M] Manager
    [W] Worker
        
    [E] Exit
    """
    print(main_txt)
    main_input = input()
    if main_input.upper() == "M":
        manager_nav()
    elif main_input.upper() == "W":
        worker_nav()
    elif main_input.upper() == "E":
        print(("""
    ==================================================================
                         (｡◕‿◕｡) (｡◕‿◕｡) (｡◕‿◕｡)              
                         STAY SAFE AND GOOD BYE!             
    ==================================================================
    """))
        sys.exit()
    else:
        print("""
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                              (ノಠ益ಠ)ノ彡┻━┻
                     ERROR! PLEASE ONLY KEY IN OPTIONS
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """)
        return main_nav()

#%%

# Goodbye exit function
#%%
def exit_nav():
    bye_text = ("""
    ==================================================================
                         (｡◕‿◕｡) (｡◕‿◕｡) (｡◕‿◕｡)              
                         STAY SAFE AND GOOD BYE!             
    ==================================================================
    """)
    print(bye_text)
    return bye_text

#%%

# Manager function        
#%%        
def manager_nav():
    manager_txt = """
    ==================================================================
                                   (͠≖ ͜ʖ͠≖)         
                            MANAGER FUNCTION MENU              
    ==================================================================
    Good morning! Which function do you need?
    [A] Update Project Progress
    [B] Worker Availability 
    [C] Dispatch Worker
        
    [E] Exit
    """
    print(manager_txt)
    manager_input = input()
    if manager_input.upper() == "A":
        proj_nav()
        return manager_nav()
    elif manager_input.upper() == "B":
        try:
            view_worker_avail()
        except FileNotFoundError:
            print("""
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                              (ノಠ益ಠ)ノ彡┻━┻
            YOUR WORKERS HAVE NOT UDPATED ATTENDANCE TODAY!
            Please get them to update before you can view!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """)
            manager_nav()
        manager_nav()
    elif manager_input.upper() == "C":
        try:
            dispatch_worker()
            check = True
        except FileNotFoundError:
            print("""
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                              (ノಠ益ಠ)ノ彡┻━┻
               YOU HAVE NOT UPDATED ON YESTERDAY'S PROGRESS
            Please update, and then you can start to dispatch!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                """)
            manager_nav()
    elif manager_input.upper() == "E":
        return main_nav()
    else:
        print("""
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                              (ノಠ益ಠ)ノ彡┻━┻
                     ERROR! PLEASE ONLY KEY IN OPTIONS
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """)
        return manager_nav()

def proj_nav():
    from datetime import date, timedelta
    from datetime import datetime
    today = date.today()
    yesterday = today - timedelta(days=1)
    todays_date = today.strftime("%b%d%Y")
    yesterdays_date = yesterday.strftime("%b%d%Y")
    date_format = "%b%d%Y"
    proj_nav_txt = """
    ==================================================================
                                  (͠≖ ͜ʖ͠≖)         
                  MANAGER FUNCTION MENU: UPDATE PROJECTS              
    ==================================================================
    What option do you require?
    [A] Add New Project Details
    [B] Update Project Progress
    [C] Save Changes & Overview
    
    [E] Exit
    """
    print(proj_nav_txt)
    proj_nav_input = input()
    if proj_nav_input.upper() == "A":
        global proj_today_df
        proj_today_df = proj_today_df.append(pd.Series(new_proj_func(), index = ["Project ID", "Total SqFt of Project", "SqFt Left", "Days Left", "Deadline",	"% Left", "Site Worker Restriction", "Workers Assigned"]) , ignore_index = True)
        proj_nav()
    elif proj_nav_input.upper() == "B":
        print("""
    ==================================================================
                                  (͠≖ ͜ʖ͠≖)         
                  MANAGER FUNCTION MENU: UPDATE PROJECTS              
    ==================================================================
    """)
        for ind in proj_today_df.index:
            proj_id_row = str(round(proj_today_df["Project ID"][ind]))
            check = False
            while not check:
                try:
                    sqft_cleared_yest = int(input(f"""
    For {proj_id_row}, how many SqFt was completed yesterday? 
    """))
                    check = True
                except ValueError:
                    print("""
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                              (ノಠ益ಠ)ノ彡┻━┻
                     ERROR! PLEASE ONLY KEY IN NUMBERS
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """)
       
            proj_today_df["SqFt Left"][ind] -=  sqft_cleared_yest
            proj_today_df["% Left"][ind] = (proj_today_df["Total SqFt of Project"][ind] - proj_today_df["SqFt Left"][ind])/ proj_today_df["Total SqFt of Project"][ind]
            existing_proj_dt = datetime.strptime(proj_today_df["Deadline"][ind], "%b%d%Y")
            existing_proj_d = existing_proj_dt.date()
            proj_today_df["Days Left"][ind] = (existing_proj_d - date.today()).days
            if proj_today_df["SqFt Left"][ind] <= 0:
                print(f"""
    ==================================================================
                               ᕕ( ͡° ͜ʖ ͡°)ᕗ    
                              CONGRATULATIONS!
                      PROJECT {proj_today_df["Project ID"][ind]} is completed!        
    ==================================================================
    """)            
            elif proj_today_df["Days Left"][ind] <=5 and proj_today_df["Days Left"][ind] > 0:
                print(f"""
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                 ┌( ಠ_ಠ)┘
                    TIME IS RUNNING OUT! DAYS LEFT:
                                {proj_today_df["Days Left"][ind]}
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """)
        proj_nav()
    elif proj_nav_input.upper() == "C":
        proj_today_df_filtered = proj_today_df[proj_today_df['SqFt Left'] > 0] 
        print(proj_today_df_filtered.iloc[:,0:4])
        projdatewcsv = "UpdatedProjProgress_" + str(todays_date)
        proj_today_df_filtered.to_csv(f'''{projdatewcsv}.csv''', index = False)
        manager_nav()
    elif proj_nav_input.upper() == "E":
        manager_nav()
    else:
        print("""
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                              (ノಠ益ಠ)ノ彡┻━┻
                     ERROR! PLEASE ONLY KEY IN OPTIONS
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """)
        proj_nav()
        
def new_proj_func():
    from datetime import datetime
    today = datetime.today()
    global new_proj_list
    new_proj_list = []
    check = False
    while not check:
        try:
            new_proj_id = int(input("""
    ==================================================================
                               ᕕ( ͡° ͜ʖ ͡°)ᕗ         
                   MANAGER FUNCTION:NEW PROJECT DETAILS             
    ==================================================================
    Please key in the new Project ID (Postal Code):
    """))
            check = True
        except ValueError:
            print("""
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                              (ノಠ益ಠ)ノ彡┻━┻
                     ERROR! PLEASE ONLY KEY IN NUMBERS
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                  """)
    
    check = False
    while not check:
        try:            
            new_total_sqft = int(input(f"""  
    ------------------------------------------------------------------
    Please key in total SqFt of Project {new_proj_id}
    """))
            check = True
        except ValueError:
            print("""
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                           (ノಠ益ಠ)ノ彡┻━┻
                 ERROR! PLEASE ONLY KEY IN NUMBERS
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """)
    
    check = False
    while not check:
        try:                    
            new_proj_max_workers = int(input(f"""
    ------------------------------------------------------------------                                         
    Please key in manpower limitation for Project {new_proj_id}:
    """))
            check = True
        except ValueError:
            print("""
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                              (ノಠ益ಠ)ノ彡┻━┻
                    ERROR! PLEASE ONLY KEY IN NUMBERS
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                  """)
    check = False
    while not check:
        try:
            new_proj_deadline = input(f""" 
    ------------------------------------------------------------------    
    Please key in deadline for Project {new_proj_id}:
    Format: MMMDDYYYY 
    E.g.:   Nov012020
    """)
            new_proj_dt = datetime.strptime(new_proj_deadline, "%b%d%Y")
            check = True
        except: 
            print("""
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                               (ノಠ益ಠ)ノ彡┻━┻
                   ERROR! PLEASE ONLY KEY IN VALID DATES
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """)
    new_proj_dt = datetime.strptime(new_proj_deadline, "%b%d%Y")
    new_proj_d = new_proj_dt.strftime("%b%d%Y")
    new_daysleft_delta = (new_proj_dt - today).days
    if new_daysleft_delta < 0:
        print("""
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                               (ノಠ益ಠ)ノ彡┻━┻
                ERROR! PLEASE KEY IN DATES AFTER TODAY
                            PLEASE TRY AGAIN!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """)
        new_proj_func()
    new_percent_left = 100
    new_workers_to_fill = "To be filled!"
    new_proj_list.append(new_proj_id)
    new_proj_list.append(new_total_sqft)
    new_proj_list.append(new_total_sqft)
    new_proj_list.append(new_daysleft_delta)
    new_proj_list.append(str(new_proj_d))
    new_proj_list.append(new_percent_left)
    new_proj_list.append(new_proj_max_workers)
    new_proj_list.append(new_workers_to_fill)
    print("""
    ==================================================================
                           ヾ(⌐■_■)ノ♪ ヾ(⌐■_■)ノ♪      
                      PROJECTS UPDATED SUCCESSFULLY!
                            CLICK C TO SAVE!
    ==================================================================
    """)
    return new_proj_list   

def view_worker_avail():
    view_worker_avail_df = pd.read_csv(f"""UpdatedAttendance_{todays_date}.csv""")
    print(f"""
    ==================================================================
                           ᕕ( ͡° ͜ʖ ͡°)ᕗ         
           MANAGER FUNCTION:WORKER ABSENCE & REASON REPORT            
    ------------------------------------------------------------------
    
    {view_worker_avail_df}
    
    ======================== END OF REPORT ===========================
    """)
#%%
        
# Worker function
#%% 
def worker_nav():
    worker_txt = """
    ==================================================================
                         (▰˘◡˘▰) (▰˘◡˘▰) (▰˘◡˘▰)      
                        WORKER FUNCTION:ATTENDANCE             
    ==================================================================
    Good morning! Are you coming to work?
    [Y] Yes
    [N] No
        
    [E] Exit
    """
    print(worker_txt)
    worker_input = input()
    if worker_input.upper() == "Y":
        print("""
    ================================================================== 
                       THANK YOU! SEE YOU AT WORK!            
    ==================================================================
    """)
        worker_subnav()
    elif worker_input.upper() == "N":
        global reasons_for_leave_df
        reasons_for_leave_df = reasons_for_leave_df.append(pd.Series(absentee_input(), index=['Name of Worker', 'Worker ID', 'Reason for leave']), ignore_index = True)
        worker_subnav()
    elif worker_input.upper() == "E":
        exit_nav()
        return main_nav() 
    else:
        print("""    
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                               (ノಠ益ಠ)ノ彡┻━┻
                     ERROR! PLEASE ONLY KEY IN OPTIONS
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """)
        worker_nav()
    return reasons_for_leave_df

def worker_subnav():
    worker_subnav_txt = """
    ==================================================================
                           ヾ(⌐■_■)ノ♪ ヾ(⌐■_■)ノ♪      
                      ATTENDANCE RECORDED SUCCESSFULLY           
    ==================================================================
    Submit all attendance or next worker?
    [N] Next worker
    [S] Save to CSV and submit to manager
        
    [E] Exit
    """
    print(worker_subnav_txt)
    worker_subnav_input = input(
    )
    if worker_subnav_input.upper() == "N":
        worker_nav()
    elif worker_subnav_input.upper() == "S":
        datewcsv = "UpdatedAttendance_" + str(todays_date)
        reasons_for_leave_df.to_csv(f'''{datewcsv}.csv''', index = False)
        return main_nav()
    elif worker_subnav_input == "E":
        return main_nav()
    else: 
        print("""
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                               (ノಠ益ಠ)ノ彡┻━┻
                      INVALID ENTRY! PLEASE TRY AGAIN
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """)
        worker_subnav()

def get_fin():
    get_fin_txt = """
    ------------------------------------------------------------------  
    Input the last 4 digits of your FIN: 
    """
    print(get_fin_txt)
    get_fin_input = input().strip()[-4:].upper()
    while get_fin_input not in workerlist_df.values:
        print("""
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                               (ノಠ益ಠ)ノ彡┻━┻
                      INVALID ENTRY! PLEASE TRY AGAIN
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """)
        get_fin_txt = """
    ------------------------------------------------------------------  
    Input the last 4 digits of your FIN: 
    """
        print(get_fin_txt)
        get_fin_input = input().strip()[-4:].upper()
    workername = workerlist_df.loc[workerlist_df['Worker ID'] == get_fin_input, 'Name of Worker'].values[0]
    return workername
    
def get_reason():
    reason = input(f"""
    ------------------------------------------------------------------                
    Please key in your reason for not coming:
    """)
    return reason    

def absentee_input():
    output = []
    output.append(get_fin())
    output.append(workerlist_df[workerlist_df["Name of Worker"] == output[0]].loc[:, "Worker ID"].values[0])
    output.append(get_reason())
    return output
#%%

# Dispatch Worker
#%% 
def dispatch_worker():
    dispatch_worker_txt = f"""
    ==================================================================
                              ᕕ( ͡° ͜ʖ ͡°)ᕗ         
                    MANAGER FUNCTION: DISPATCH WORKER             
    ==================================================================
    """
    print(dispatch_worker_txt)
    dispatch_proj_today = pd.read_csv(f"""UpdatedProjProgress_{todays_date}.csv""")
    dispatch_proj_today = dispatch_proj_today.dropna(how = "all")
    for ind in dispatch_proj_today.index:
            proj_id_row = str(round(dispatch_proj_today["Project ID"][ind]))
            if dispatch_proj_today.loc[ind, "Workers Assigned"] == "To be filled!": 
                absent_worker_df = pd.read_csv(f"""UpdatedAttendance_{todays_date}.csv""")
                absent_worker_id_list = absent_worker_df["Worker ID"].tolist()
                assigned_workerid_list = dispatch_proj_today["Workers Assigned"].tolist()
                assigned_worker_id_separate_list = []
                for i in assigned_workerid_list:
                    split_list = i.split(", ")
                    assigned_worker_id_separate_list.extend(split_list)
                full_absent_list = []
                full_absent_list.extend(absent_worker_id_list)
                full_absent_list.extend(assigned_worker_id_separate_list)
                global workerlist_df
                full_worker_list = workerlist_df["Worker ID"].tolist()
                can_work_list = []
                dispatch_proj_today.loc[ind, "Workers Assigned"] = ""
                for i in full_worker_list:
                    if i not in full_absent_list:
                        can_work_list.append(i)    
                num = dispatch_proj_today["Site Worker Restriction"][ind]
                for i in range(0, num):
                    dispatch_proj_today["Workers Assigned"][ind] += str(can_work_list[i])
                    dispatch_proj_today["Workers Assigned"][ind] += ", "
                print(f"""
    ==================================================================
                          ヾ(⌐■_■)ノ♪ ヾ(⌐■_■)ノ♪      
                          NEW PROJECT {dispatch_proj_today["Project ID"][ind]}           
    ==================================================================
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++   
    You have not assigned any new workers to this! 
    We will assign {dispatch_proj_today["Site Worker Restriction"][ind]} workers for you! 
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    Workers assigned:
    {dispatch_proj_today["Workers Assigned"][ind]}
    ==================================================================
                          ヾ(⌐■_■)ノ♪ ヾ(⌐■_■)ノ♪      
                    DISPATCH RECORDED SUCCESSFULLY           
    ==================================================================
                        """)         
            else:
                absent_worker_df = pd.read_csv(f"""UpdatedAttendance_{todays_date}.csv""")
                absent_worker_id_list = absent_worker_df["Worker ID"].tolist()
                assigned_workerid_list = dispatch_proj_today["Workers Assigned"][ind]
                assigned_workerid_list = assigned_workerid_list.split(", ")
                can_work_list_proj = []
                for i in assigned_workerid_list:
                    if i not in absent_worker_id_list:
                        can_work_list_proj.append(i)
                        
                check = False 
                while not check:
                    try:
                        num_worker_dispatch = int(input(f"""
    For {proj_id_row}, how many people would you like to dispatch today?
    ------------------------------------------------------------------ 
    There are {len(can_work_list_proj)} people fit to work today:
    {can_work_list_proj}
    Prevailing restriction for this site is {dispatch_proj_today["Site Worker Restriction"][ind]}
    ------------------------------------------------------------------
    """))
                        check = True
                    except ValueError:
                        print("""
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                              (ノಠ益ಠ)ノ彡┻━┻
                     ERROR! PLEASE ONLY KEY IN NUMBERS
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                """)
                if num_worker_dispatch == 0:
                    work_completed_today = num_worker_dispatch
                    print(f"""
    ==================================================================
                           {proj_id_row} REPORT
    ==================================================================           
    Projected completion today: {work_completed_today} SqFt
    Project is put on hold!
    ======================== END OF REPORT ===========================
        """)
                elif num_worker_dispatch > dispatch_proj_today["Site Worker Restriction"][ind]:
                    print(f"""
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                             (ノಠ益ಠ)ノ彡┻━┻
           ERROR! You are not allowed to dispatch more than 
                                {dispatch_proj_today["Site Worker Restriction"][ind]} 
                 people due to COVID-19 regulations! 
             GENERATING REPORT FOR MAXIMUM DISPATCH INSTEAD...
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            """)           
                    work_completed_today = dispatch_proj_today["Site Worker Restriction"][ind] * 50
                    days_left = dispatch_proj_today["Days Left"][ind]
                    amount_left = dispatch_proj_today["SqFt Left"][ind]
                    prevailing_rate = amount_left//work_completed_today
                    print(f"""
    ==================================================================
                           {proj_id_row} REPORT
    ==================================================================           
        Projected completion today: {work_completed_today} SqFt
        Project will finish in {prevailing_rate} days!
    ======================== END OF REPORT ===========================
    """)
                    days_diff = prevailing_rate - days_left
                    cost_unit = days_diff*num_worker_dispatch*50/50
                    manpower_cost = cost_unit * 100
                    cost_crashing = 200*days_diff
                    if days_diff > 0:
                        print(f"""
                      !!!!!! WARNING !!!!!!
    You will not be able to finish this project on time at this rate!
    == OPTION 1 ==
    You will have to either extend your project by {days_diff} days.
    Crashing cost of {cost_crashing} will be incurred.
        
    == OPTION 2 ==
    Dispatch {cost_unit} more people today to ensure that the project finishes on time! 
    Cost of hiring extra manpower is {manpower_cost}
    """)
                        if manpower_cost > cost_crashing:
                            print("""
    ========================= RECOMMENDATION =========================
    We recommend to crash this project anyway and lengthen by {days_diff} days.
    ======================== END OF REPORT ===========================
    """)
                                        
                        else:
                            print("""
    ========================= RECOMMENDATION =========================
    We recommend that you hire more!
    ======================== END OF REPORT ===========================
    """)
                elif num_worker_dispatch <= dispatch_proj_today["Site Worker Restriction"][ind] :
                    work_completed_today = num_worker_dispatch * 50
                    days_left = dispatch_proj_today["Days Left"][ind]
                    amount_left = dispatch_proj_today["SqFt Left"][ind]
                    prevailing_rate = amount_left//work_completed_today
                    print(f"""
    ==================================================================
                          {proj_id_row} REPORT
    ==================================================================           
    Projected completion today: {work_completed_today} SqFt
    Project will finish in {prevailing_rate} days!
    """)
                    days_diff = prevailing_rate - days_left
                    cost_unit = days_diff*num_worker_dispatch*50/50
                    manpower_cost = cost_unit * 100
                    cost_crashing = 200*days_diff
                    if days_diff > 0:
                        print(f"""
                     !!!!!! WARNING !!!!!!
    You will not be able to finish this project on time at this rate!
    == OPTION 1 ==
    You will have to either extend your project by {days_diff} days.
    Crashing cost of {cost_crashing} will be incurred.
        
    == OPTION 2 ==
    Dispatch {cost_unit} more people today to ensure that the project finishes on time! 
    Cost of hiring extra manpower is {manpower_cost}
    """)
                        if manpower_cost > cost_crashing:
                            print("""
    ========================= RECOMMENDATION =========================
    We recommend to crash this project anyway and lengthen by {days_diff} days.
    ======================== END OF REPORT ===========================
    """)
                                        
                        else:
                            print("""
    ========================= RECOMMENDATION =========================
    We recommend that you hire more!
    ======================== END OF REPORT ===========================
    """)
    projdatewcsv = "UpdatedProjProgress_" + str(todays_date)
    dispatch_proj_today.to_csv(f'''{projdatewcsv}.csv''', index = False)
    return main_nav()
    #%%
main_nav()