#!/usr/bin/env python

import sqlite3 as lite
import requests
from BeautifulSoup import BeautifulSoup
con = lite.connect('procurements.sqlite')
cur = con.cursor()

#page_number = 3
base_url = "https://eproc.karnataka.gov.in"
access_url = "https://eproc.karnataka.gov.in/eprocurement/common/eproc_tenders_list.seam"
jsf_sequence = 1
page_number = 6

request_session = requests.Session()
html_src = ""
if page_number == 1:
	html_src = request_session.get("https://eproc.karnataka.gov.in/eprocurement/common/eproc_tenders_list.seam")
else:
	html_src = request_session.get("https://eproc.karnataka.gov.in/eprocurement/common/eproc_tenders_list.seam")
	#soup2 = BeautifulSoup(html_src.content)
	#ips = soup2.findAll(name="jsf_sequence")
	#jsf_sequence = str(ips)
	print jsf_sequence

	payload = {'eprocTenders:_link_hidden_': 'eprocTenders:dataScrollerIdidx'+str(page_number), 'eprocTenders:dataScrollerId': 'idx'+str(page_number)}
	payload["eprocTenders:butSearch"]='Search'
	payload["eprocTenders_SUBMIT"] = 1
	payload["jsf_sequence"] = jsf_sequence
	jsf_sequence = jsf_sequence + 1

	#print html_src.cookies
	session_cookie = html_src.cookies['JSESSIONID']

	html_src = requests.post("https://eproc.karnataka.gov.in/eprocurement/common/eproc_tenders_list.seam;jsessionid="+str(session_cookie), data=payload)
	#print html_src.content
	#break
print "============ Starting the new page "+str(page_number)+"============"
print "Cookie for the session ="+str(session_cookie)

soup = BeautifulSoup(html_src.content)
tables = soup.findAll(id="eprocTenders:browserTableEprocTenders:tbody_element")
tender_table = tables[0]
for i in range(1,40):
	if getattr(tables[0].contents[i], 'name', None) == 'tr':
		row = tables[0].contents[i].contents
		#Primary key for the insertion is Tender_Number
		unique_keys = [ 'Tender_Number' ]
		print "Getting values for the Tender_Number = "+str(row[2].contents[0])
		cur.execute('select count(*) as tcount from tender where Tender_Number ="'+str(row[2].contents[0])+'"')
		data1 = cur.fetchone()
		print data1
		if int(data1[0])> 0:
			print "tender has been already parsed. skipping"
			continue

		#Get the basic information
		data = {"Department_Location":str(row[1].contents[0]), "Tender_Number":str(row[2].contents[0]), "Tender_Title":str(row[3].contents[0]),"Tender_Type":str(row[4].contents[0]),"Category":str(row[5].contents[0]) }
		data['error'] = 'no'

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
		
		#Get the URLS for downloading the stuff
		notice_url = None
		download_docs_url = None
		for j in range(0,len(row[10].contents)):
			link = row[10].contents[j]
			img = link.contents[1]
			#print img['title']
			if img['title'] == 'View Notice Inviting Tender details':
				notice_url = base_url+link['href']
				data["notice_url"] =str(notice_url)
			if img['title'] == 'Download Tender Documents':
				download_docs_url = base_url+link['href']
				data["download_docs_url"] =str(download_docs_url)
		
				
		#get the notice content
		print "Getting content of View Notice Inviting Tender details"
		print notice_url
		notice_info_content = ""
		try:
			if notice_url != None:
				notice_content = request_session.get(notice_url,timeout=10)
				#print notice_content.content
				notice_soup = BeautifulSoup(notice_content.content)
				notice_info = notice_soup.findAll(id="_id26")
				notice_info_content = notice_info[0].contents[0]
				#print notice_info_content
		except:
			print "ERROR WHILE GETTING NOTICE"		
			data['error']='yes'
		data["Notice_Inviting_Tender_Details"] =str(notice_info_content)

		try:
			print "Getting Documents page"
			print download_docs_url
			if download_docs_url != None:
				download_docs_url_content = request_session.get(download_docs_url,timeout=10)
				#print notice_content.content
				download_docs_url_soup = BeautifulSoup(download_docs_url_content.content)
				download_docs_url_info = download_docs_url_soup.findAll(id="_id26:_id30:tbody_element")
				#print download_docs_url_info[0].contents
				
				for k in range(0, len(download_docs_url_info[0].contents)):
					document_row = download_docs_url_info[0].contents[k]
					if getattr(document_row, 'name', None) == 'tr':
						#print document_row.contents
						type_of_the_document = str(document_row.contents[1].contents[0])
						url_of_the_document  = str(base_url+document_row.contents[2].contents[0]['href'])
						name_of_the_document = str(document_row.contents[2].contents[0].contents[0])
						document_unique_keys = [ 'Tender_Number','url_of_the_document' ]
						document = {"Tender_Number":data["Tender_Number"],"type_of_the_document":type_of_the_document,"url_of_the_document":url_of_the_document,"name_of_the_document":name_of_the_document}
						# Saving document
						cur.execute('INSERT INTO document (Tender_Number, type_of_the_document, url_of_the_document, name_of_the_document) VALUES (:Tender_Number, :type_of_the_document, :url_of_the_document, :name_of_the_document)', document)
						print name_of_the_document
						print base_url+url_of_the_document
						print type_of_the_document
		except:
			print "ERROR WHILE GETTING DOCUMENTS"		
			data['error']='yes'
		# Saving data:
		cur.execute('INSERT INTO tender (Tender_Number, Department_Location, Tender_Title, Tender_Type, Category, Sub_Category, Estimated_Value, NIT_Published_Date, Last_Date_for_Bid_Submission,notice_url,download_docs_url,Notice_Inviting_Tender_Details, error) VALUES (:Tender_Number, :Department_Location, :Tender_Title, :Tender_Type, :Category, :Sub_Category, :Estimated_Value, :NIT_Published_Date, :Last_Date_for_Bid_Submission, :notice_url, :download_docs_url, :Notice_Inviting_Tender_Details, :error)', data)
		con.commit()


con.close()