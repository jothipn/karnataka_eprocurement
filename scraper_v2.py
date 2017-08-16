import sys
import requests
import time
import csv
from bs4 import BeautifulSoup

if len(sys.argv) < 3:
    print("scraper_v2.py <from_date dd/mm/yyyy> <to_date dd/mm/yyyy> out-csv-file-name [num_pages]")
    print("For Example: python scraper_v2.py  01/08/2017 01/08/2017 my.csv 10")
    exit()

from_date=sys.argv[1]
to_date=sys.argv[2]

output = sys.argv[3]

try:
    final_page_number = int(sys.argv[4])
except:
    final_page_number = 31

#print("Running for " + str(final_page_number) + " pages")


f = open(output,'a')
writer=csv.writer(f, lineterminator='\n')

firsttime = True;

for page_number in range(1,final_page_number+1):
        time.sleep(3)
        request_session = requests.Session();
        jsf_sequence = 1
        html_src = request_session.get("https://eproc.karnataka.gov.in/eprocurement/common/eproc_tenders_list.seam", verify=False)
        soup = BeautifulSoup(html_src.content, "html.parser")
        ips = soup.findAll(name="jfs_sequence")
        
        #payload = {'eprocTenders:_link_hidden_': 'eprocTenders:dataScrollerIdidx'+str(page_number)}
        payload={}
        payload["eprocTenders:_link_hidden_"] = 'eprocTenders:dataScrollerIdidx'+str(page_number)
        payload["eprocTenders:dataScrollerId"] = 'idx' + str(page_number)
        payload["eprocTenders:tenderCreateDateTo"] = to_date
        payload["eprocTenders:tenderCreateDateFrom"] = from_date
        payload["eprocTenders:butSearch"]='Search'
        payload["eprocTenders_SUBMIT"] = 1
        payload["jsf_sequence"] = jsf_sequence
        session_cookie = html_src.cookies['JSESSIONID']
        
        html_src = requests.post("https://eproc.karnataka.gov.in/eprocurement/common/eproc_tenders_list.seam;jsessionid="+str(session_cookie), data=payload,  verify=False)
        #print ("Cookie for the session =", str(session_cookie))
        
        soup = BeautifulSoup(html_src.content, "html.parser")
        tables = soup.findAll(id="eprocTenders:browserTableEprocTenders:tbody_element")

        for i in range(1,len(tables[0].contents)):
            if getattr(tables[0].contents[i], 'name', None) == 'tr':
                row = tables[0].contents[i].contents
        
                data = {}
                data["Department_Location"] = str(row[1].contents[0])
                data["Tender_Number"] = str(row[2].contents[0])
                data["Tender_Title"] = str(row[3].contents[0])
                data["Tender_Type"] = str(row[4].contents[0])
                data["Category"] = str(row[5].contents[0]) 
                #data['error'] = 'no,'
        
                if len(row[6].contents) > 0:
                    data["Sub_Category"] = str(row[6].contents[0])
                else:
                    data["Sub_Category"] = ""
        
                if len(row[7].contents) > 0:
                    data["Estimated_Value"] =str(row[7].contents[0])
                else:
                    data["Estimated_Value"] = ""
        
                data["NIT_Published_Date"] =str(row[8].contents[0])
                data["Last_Date_for_Bid_Submission"] =str(row[9].contents[0])

                if (firsttime) :
                    firsttime = False;
                    writer.writerow(data.keys())
                writer.writerow(data.values())

f.close()
