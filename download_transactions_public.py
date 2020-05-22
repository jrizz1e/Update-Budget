#IMPROVEMENTS: add timeout feature, add to scheduled tasks


#access and download this month's transactions
#then subtract expenses from correct budget category
#lastly create a bar chart showing how much has been spent and how much is left in each category

import pyautogui
import time
from datetime import date
import glob
import os
import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt

#login info
username='####'
password = '####'


#date info
today = date.today()
first_of_month = today.replace(day=1).strftime("%m/%d/%Y")
today = today.strftime("%m/%d/%Y")

def locate_then_click(image):
    searchlocation = pyautogui.locateOnScreen(image, confidence=0.7)
    searchpoint = pyautogui.center(searchlocation)
    time.sleep(3.0)
    pyautogui.click(searchpoint)

def download_transactions():
    #open new window in chrome
    locate_then_click(r"C:\Users\Jonathan\Budget\chrome_icon.JPG")
    time.sleep(3.0)
    pyautogui.hotkey('ctrl', 'n')
    #go to chase.com and wait for it to load
    pyautogui.typewrite('chase.com\n')
    time.sleep(10.0)
    #locate sign in button and click
    locate_then_click(r"C:\Users\Jonathan\Budget\sign_in_button.JPG")
    time.sleep(3.0)
    #reenter username
    pyautogui.press('tab')
    time.sleep(3.0)
    pyautogui.typewrite(username)
    time.sleep(3.0)
    #enter password
    pyautogui.press('tab')
    time.sleep(3.0)
    pyautogui.typewrite(password+'\n')
    #let page load
    time.sleep(15.0)
    #search for Search (third result)
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(3.0)
    pyautogui.write('search', interval=0.5)
    time.sleep(3.0)
    pyautogui.press('enter', presses=2, interval=2)
    time.sleep(3.0)
    pyautogui.hotkey('ctrl', 'enter')
    time.sleep(3.0)
    #press tab 4 times to get to correct textbox
    pyautogui.press('tab', presses=3, interval=2)
    #enter first of month
    pyautogui.typewrite(first_of_month)
    time.sleep(3.0)
    #scroll down
    pyautogui.scroll(-400)
    time.sleep(3.0)
    #locate and click search button
    locate_then_click(r"C:\Users\Jonathan\Budget\search.JPG")
    time.sleep(3.0)
    #locate and click download icon
    locate_then_click(r"C:\Users\Jonathan\Budget\download_icon.JPG")
    time.sleep(3.0)
    #scroll up
    pyautogui.scroll(200)
    time.sleep(3.0)
    #locate and click download button
    locate_then_click(r"C:\Users\Jonathan\Budget\download_button.JPG")
    time.sleep(3.0)
    #close window
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('shift') 
    pyautogui.keyDown('w') 
    time.sleep(1.0)
    pyautogui.keyUp('ctrl')
    pyautogui.keyUp('shift') 
    pyautogui.keyUp('w') 
    print('Sucessfully downloaded transactions')
    return True

#run code to download transactions
download_transactions()

#access the downloaded transactions
list_of_files = glob.glob(r'C:\Users\Jonathan\Downloads\*.csv')
latest_file = max(list_of_files, key=os.path.getctime)

#read into pandas and analyze
transactions = pd.read_csv(latest_file)

budget_category = transactions['Category']

map = {np.nan:'Misc', 'Fees & Adjustments':'Misc', 'Food & Drink':'Food', 'Travel':'Misc', 'Groceries':'Food', 'Professional Services':'Misc',
 'Health & Wellness':'Home', 'Gas':'Gas', 'Personal':'Misc', 'Home':'Home', 'Education':'Misc', 'Automotive':'Misc', 'Shopping':'Misc',
 'Bills & Utilities':'Home', 'Gifts & Donations':'Misc', 'Entertainment':'Misc'}
transactions['budget_category'] = budget_category.map(map)

transactions['budget_category'][transactions['Description'] == 'STATE FARM  INSURANCE'] = 'Insurance'
transactions['Amount'][transactions['Type'] == 'Payment'] = 0

#total amount to spend in each category
food_total = 400
gas_total = 150
home_total = 300
insurance_total = 114
misc_total = 150

#amount remaining in each category
food = food_total + transactions['Amount'][transactions['budget_category']=='Food'].sum()
gas = gas_total + transactions['Amount'][transactions['budget_category']=='Gas'].sum()
home = home_total + transactions['Amount'][transactions['budget_category']=='Home'].sum()
insurance = insurance_total + transactions['Amount'][transactions['budget_category']=='Insurance'].sum()
misc = misc_total + transactions['Amount'][transactions['budget_category']=='Misc'].sum()


#helper function for plotting
def roundup(x):
    return x if x % 100 == 0 else x + 100 - x % 100

#plot results
N = 5
spent = [-1*(food-food_total), -1*(gas-gas_total), -1*(home-home_total), -1*(insurance-insurance_total), -1*(misc-misc_total)]
left = [food, gas, home, insurance, misc]
for i in range(0, len(spent)):
    if left[i] <= 0:
        left[i] = 0

ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence

p1 = plt.bar(ind, spent, width)
p2 = plt.bar(ind, left, width,
             bottom=spent)

print(spent)
print(left)
plt.ylabel('Dollars')
plt.title('Budget Synopsis as of '+today)
plt.xticks(ind, ('Food', 'Gas', 'Home', 'Insurance', 'Misc'))
plt.yticks(np.arange(0, max(500, roundup(max(spent))), 25))
plt.legend((p1[0], p2[0]), ('Spent', 'Remaining'))
plt.savefig(r'C:\Users\Jonathan\Desktop\budget_plot.png')
