import time
from datetime import datetime
import Global_var
from Insert_On_Datbase import insert_in_Local
import sys , os
import string
import time
from datetime import datetime
import html
import re
import wx
app = wx.App()

def remove_html_tag(string):
    cleanr = re.compile('<.*?>')
    main_string = re.sub(cleanr, '', string)
    return main_string

def scrap_data(main_outerHTML,tender_no,tender_title):

    SegField = []
    for data in range(42):
        SegField.append('')
    
    a = True
    while a == True:
        try:
            scrap_outerHTML = main_outerHTML.replace('\n',' ').replace('&nbsp;',' ').replace('&amp;','&')
            scrap_outerHTML = re.sub('\s+', ' ', scrap_outerHTML)

            SegField[13] = tender_no.strip()

            tender_title = string.capwords(str(tender_title))
            if len(tender_title) >= 200:
                tender_title = str(tender_title)[:200]+'...'
                tender_title = string.capwords(str(tender_title))
            SegField[19] = tender_title.strip()
            
            deadline = scrap_outerHTML.partition('Bid Re-encryption/Bid Submission</td>')[2].partition("</tr>")[0].strip()
            deadline = deadline.partition('</td>')[2].partition("</td>")[0].strip()
            deadline = remove_html_tag(deadline)
            deadline = datetime.strptime(str(deadline).strip(), "%d/%m/%Y %H:%M %p")
            main_deadline = deadline.strftime("%Y-%m-%d")
            SegField[24] = main_deadline

            Department = scrap_outerHTML.partition('Procuring Department :</strong>')[2].partition("</span>")[0].strip()
            Department = Department.upper()
            SegField[12] = Department

            Tender_offers = scrap_outerHTML.partition('Tender offers are invited for the provision of</strong>')[2].partition('</span>')[0].strip()
            if len(Tender_offers) >= 700:
                Tender_detail = str(Tender_detail)[:700]+'...'
                Tender_detail = string.capwords(str(Tender_detail))

            Eligibility_Criteria = scrap_outerHTML.partition('Other Eligibility Criteria :</strong>')[2].partition('</span>')[0].strip()
            Eligibility_Criteria = string.capwords(str(Eligibility_Criteria))

            Schemes_Description = scrap_outerHTML.partition('Reservation Schemes Description :</strong>')[2].partition('</span>')[0].strip()
            Schemes_Description = string.capwords(str(Schemes_Description))

            Envelope_Procedure = scrap_outerHTML.partition('Envelope Procedure :</strong>')[2].partition('</span>')[0].strip()
            Envelope_Procedure = string.capwords(str(Envelope_Procedure))

            Security_Amount = scrap_outerHTML.partition('Tender Security Amount (BWP) :</strong>')[2].partition('</span>')[0].strip()

            Document_Fees = scrap_outerHTML.partition('Tender Document Fees (BWP) :</strong>')[2].partition('</span>')[0].strip()


            SegField[18] = f'{SegField[19]}<br>\nTender offers are invited for the provision: {Tender_offers.strip()}<br>\nOther Eligibility Criteria: {Eligibility_Criteria.strip()}<br>\nReservation Schemes Description : {Schemes_Description.strip()}<br>\nEnvelope Procedure : {Envelope_Procedure.strip()}<br>\nTender Security Amount (BWP) : {Security_Amount.strip()}<br>\nTender Document Fees (BWP): {Document_Fees.strip()}'

            SegField[14] = '2'
            SegField[22] = "0"
            SegField[26] = "0.0"
            SegField[27] = "0"  # Financier
            SegField[7] = 'BW'
            SegField[28] = 'https://ipms.ppadb.co.bw/login'
            SegField[31] = 'ipms.ppadb.co.bw'

            for SegIndex in range(len(SegField)):
                print(SegIndex, end=' ')
                print(SegField[SegIndex])
                SegField[SegIndex] = html.unescape(str(SegField[SegIndex]))
                SegField[SegIndex] = str(SegField[SegIndex]).replace("'", "''")

            if len(SegField[19]) >= 200:
                SegField[19] = str(SegField[19])[:200]+'...'

            if len(SegField[18]) >= 1500:
                SegField[18] = str(SegField[18])[:1500]+'...'

            if SegField[19] == '':
                wx.MessageBox(' Short Desc Blank ','ipms.ppadb.co.bw', wx.OK | wx.ICON_INFORMATION)
            else:
                # check_date(get_htmlsource, SegField)
                pass
            a = False
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",
                  exc_tb.tb_lineno)
            a = True
            time.sleep(5)


def check_date(get_htmlSource, SegField):
    deadline = str(SegField[24])
    curdate = datetime.now()
    curdate_str = curdate.strftime("%Y-%m-%d")
    try:
        if deadline != '':
            datetime_object_deadline = datetime.strptime(deadline, '%Y-%m-%d')
            datetime_object_curdate = datetime.strptime(curdate_str, '%Y-%m-%d')
            timedelta_obj = datetime_object_deadline - datetime_object_curdate
            day = timedelta_obj.days
            if day > 0:
                insert_in_Local(get_htmlSource, SegField)
            else:
                print("Expired Tender")
                Global_var.expired += 1
        else:
            print("Deadline Not Given")
            Global_var.deadline_Not_given += 1
    except Exception as e:
        exc_type , exc_obj , exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error ON : " , sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname , "\n" ,exc_tb.tb_lineno)