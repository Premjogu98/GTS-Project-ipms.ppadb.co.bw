from selenium import webdriver
import time
import html
import sys, os
from datetime import datetime,timedelta
import Global_var
import wx
import string
import html
import re
from Scraping_things import scrap_data
import urllib.request
import urllib.parse
import requests

app = wx.App()

def ChromeDriver():
    browser = webdriver.Chrome(executable_path=str('C:\\chromedriver.exe'))
    browser.maximize_window()
    browser.get("https://ipms.ppadb.co.bw/login#")
    time.sleep(3)
    details_list = []
    count = 1
    a = True
    while a == True:
        No_records = ''
        try:
            for No_records in browser.find_elements_by_xpath(f'//*[@id="flexi"]/div'):
                No_records = No_records.get_attribute('innerText').strip()
                break
        except:
            pass
        
        if 'No records' in No_records:
            navigation_things(details_list,browser)
            a = False
        Deadline = ''
        for Deadline in browser.find_elements_by_xpath(f'//*[@id="flexi"]/tbody/tr[{str(count)}]//td[3]/div'):
            Deadline = Deadline.get_attribute('innerText').strip()
            break
        if 'Not Available' in Deadline:
            Deadline = datetime.today() + timedelta(days=2)
            Deadline = Deadline.strftime('%d/%m/%Y')
        if Deadline != "" :
            datetime_object = datetime.strptime(Deadline, '%d/%m/%Y')
            Deadline = datetime_object.strftime("%d-%m-%Y")

            datetime_object_pub = datetime.strptime(Deadline, '%d-%m-%Y')
            User_Selected_date = datetime.strptime(str(Global_var.From_Date), '%d-%m-%Y')

            timedelta_obj = datetime_object_pub - User_Selected_date
            day = timedelta_obj.days
            if day >= 0:
                for tender_no in browser.find_elements_by_xpath(f'//*[@id="flexi"]/tbody/tr[{str(count)}]/td[1]/div/span'):
                    tender_no_text = tender_no.get_attribute('innerText')
                    break
                test_list = []
                test_list.append(tender_no_text)
                for Tender_title in browser.find_elements_by_xpath(f'//*[@id="flexi"]/tbody/tr[{str(count)}]/td[2]/div/span/a'):
                    Tender_title_text = Tender_title.get_attribute('innerText').strip()
                    test_list.append(Tender_title_text)
                    Tender_title_url = Tender_title.get_attribute('outerHTML').replace('\n','')
                    Tender_title_id = Tender_title_url.partition("showCodes(")[2].partition(')">')[0].strip()
                    url1 = f'https://ipms.ppadb.co.bw/tenderNotice?docid={str(Tender_title_id)}&type=searchcodes'
                    url2 = f'https://ipms.ppadb.co.bw/v4workflow/ntPdfIpmsDownload?myParam={str(Tender_title_id)}&myValue=isDownloadAllAttachment'
                    test_list.append(url1)
                    test_list.append(url2)
                    break
                details_list.append(test_list)
                a = True
            else:
                navigation_things(details_list,browser)
                a = False
            if count == 10:
                for next_page in browser.find_elements_by_xpath('//*[@id="next"]'):
                    next_page.click()
                    break
                is_visible = False
                while is_visible == False:
                    for tender_no in browser.find_elements_by_xpath(f'//*[@id="flexi"]/tbody/tr[1]/td[1]/div/span'):
                        is_visible = True
                        count = 1
                        break
            else:
                count += 1
        else:
            # print('Deadline Not Given')
            for next_page in browser.find_elements_by_xpath('//*[@id="next"]'):
                next_page.click()
                break
            time.sleep(5)

def navigation_things(details_list,browser):
    for inside_details_list in details_list:
        tender_no = inside_details_list[0]
        tender_title = inside_details_list[1]
        del inside_details_list[0]
        del inside_details_list[0]
        main_outerHTML = ''
        for href in inside_details_list:
            browser.get(str(href))
            time.sleep(2)
            for href_outerHTML in browser.find_elements_by_xpath('/html/body'):
                href_outerHTML = href_outerHTML.get_attribute('outerHTML').strip().replace('</body>','').replace('<body>','').replace('href="v','href="https://ipms.ppadb.co.bw/v').replace('\n','').replace('\t','').replace('-----','')
                main_outerHTML += href_outerHTML
                break 
        scrap_data(main_outerHTML,tender_no,tender_title)
        print(f'Total: {str(len(details_list))} Deadline Not given: {Global_var.deadline_Not_given} duplicate: {Global_var.duplicate} inserted: {Global_var.inserted} expired: {Global_var.expired} QC Tenders: {Global_var.QC_Tenders}')
        time.sleep(3)
    wx.MessageBox(f'Total: {str(len(details_list))}\nDeadline Not given: {Global_var.deadline_Not_given}\nduplicate: {Global_var.duplicate}\ninserted: {Global_var.inserted}\nexpired: {Global_var.expired}\nQC Tenders: {Global_var.QC_Tenders}','ipms.ppadb.co.bw', wx.OK | wx.ICON_INFORMATION)
    browser.close()
    sys.exit() 

ChromeDriver()