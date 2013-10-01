### Karnataka eProcurement Tenders

This is the project for scraping [Karnataka eProcurement Tenders](https://eproc.karnataka.gov.in/eprocurement/common/eproc_tenders_list.seam). 
Scraping is done on daily basis and the SQLite DB is updated. THe SQLite DB in this git repo is just for developement and doesnt have the latest data.

The latest DB [Updated Daily] is available for download at [OpenBangalore](http://docs.openbangalore.org.s3.amazonaws.com/procurements.sqlite.tar.lzma)

````


//This table contains the basic info of the tender
TABLE "tender" 
"Tender_Number" ,
"Department_Location" , 
"Tender_Title" , 
"Tender_Type" ,
"Category" , 
"Sub_Category" ,
"Estimated_Value" , 
"NIT_Published_Date" , 
"Last_Date_for_Bid_Submission" ,
"notice_url" , 
"download_docs_url" , 
"Notice_Inviting_Tender_Details" , 
"error"  

//This table contains the links to documents that belogs to a tender.
TABLE "document" 
"name_of_the_document"
"Tender_Number" , 
"type_of_the_document" , 
"url_of_the_document"  


````

### How to explore

1. Download [procurements.sqlite.tar.lzma](http://docs.openbangalore.org.s3.amazonaws.com/procurements.sqlite.tar.lzma)
2. Unzip using [7zip](http://www.7-zip.org/) 
3. Install Firfox
4. Install Firefox addon - [SQLite manager](https://addons.mozilla.org/en-US/firefox/addon/sqlite-manager/)
5. Restart Firefox
6. Go to Firefox - Tools - SQLite Manager
7. In SQLite manager - Database - Connect Database and choose the extracted file in step 2
8. Expand tables on left
9. Click on the document or tender table
10. If you want it as csv, right click on table and export table

### Coming soon
- Code a simple RSS feed to subscribe to latest tenders 
- Simple UI to explore the data
- Download the documents along with scraping info

### Authors
<table>
  <tr>
    <td><img src="http://www.gravatar.com/avatar/4545b2a84b0ae407abc97ad8f23cc28b?s=60"></td><td valign="middle">Thejesh GN<br><a href="http:/thejeshgn.com">http://thejeshgn.com</a></td>
    <td>i-at-thejeshgn-com <br> GPG ID :  0xBFFC8DD3C06DD6B0</td>
  </tr>
</table>
