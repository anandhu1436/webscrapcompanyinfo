
#This is the Generic File for Web-Scraping Knowledge Graph
#Importing Libraries
import logging
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from random import randint
from datetime import date
import os
#created log file with format
logging.basicConfig(filename="error.log",filemode="w",format='%(asctime)s - %(message)s',level=logging.ERROR)
def get_path_w():
    '''Return the path of the the files in the INPUT,OUTPUT,SUPPORTING_FILES,MASTER(optional)'''
    script_path = os.path.abspath("config.txt")
    #script_path = os.path.abspath(os.path.join(script_path, '../SCRIPTS/'))
    input_file_path= os.path.abspath(os.path.join(script_path, '../INPUT/'))
    output_file_path= os.path.abspath(os.path.join(script_path, '../OUTPUT/'))
    support_file_path= os.path.abspath(os.path.join(script_path, '../SUPPORT_FILES/'))
    return script_path,input_file_path,output_file_path,support_file_path

script_path,input_file_path,output_file_path,support_file_path=get_path_w()

for filename in os.listdir(support_file_path):
        os.unlink(support_file_path+'//'+filename)
for filename in os.listdir(output_file_path):
        os.unlink(output_file_path+'//'+filename)

def import_files(input_file_path):
    '''This function get all the files in the INPUT folders
    if it is a "csv" file then mention the separator in the config file and
    for a file which is in excel we don't need to mention it '''
    for filename in os.listdir(input_file_path):
        if filename.endswith('.xlsx'):
            excel_files=pd.read_excel(input_file_path+'//'+filename,encoding='utf-8',dtype=str,sheet_name=0)
            print("Read Excel File Name: "+filename)
            print("Displaying Sample Record:")
            print(excel_files.iloc[1])
        else:
            print("File Format Not Supported: "+filename)
    return excel_files

def get_col_list():
    """Get columns used in webscraping"""
    config_path = os.path.abspath("config.txt")
    #config_path= os.path.abspath(os.path.join(script_path, '../SCRIPTS/'))
    get_config_value=pd.read_csv(config_path,sep=':', engine='python')
    get_row_values=get_config_value[get_config_value['NAME']=='COLUMNS']
    col_names=get_row_values['VALUES'].tolist()
    return eval(col_names[0])

columns_list=get_col_list()

input_url=import_files(input_file_path)
driver=webdriver.Chrome(r"chromedriver.exe")
input_url.fillna('',inplace=True)

column_list=input_url.columns
print(column_list)

#print(input_url.columns)
#input_url['STD_POSTAL_CODE']=input_url['STD_POSTAL_CODE'].apply(lambda x:'"'+x+'"')
#input_url['STD_POSTAL_CODE']=input_url['STD_POSTAL_CODE'].apply(lambda x:x.replace('"', ''))
#input_url['STD_POSTAL_CODE']=input_url['STD_POSTAL_CODE'].apply(lambda x:'"'+x+'"')

input_url=input_url.astype(str)
input_url['Search'] = input_url[columns_list].apply(lambda x: ' '.join(x), axis = 1)
print(column_list)

datalist=[]
url_list=[]
x=0
y=0
z=0

count=0
googleurls=[]
domain_file=open(r'googledomains1.txt')
for domains in domain_file:
    googleurls.append(domains)

headerlist=[]
allproducts=[]
i = 0

name_to_use=[]
kg_title=[]
kg_subtitle=[]
kg_address=[]
kg_website=[]
kg_phone=[]
type_com=[]
alllll=[]

input_url['Search'] = input_url[columns_list].apply(lambda x: ' '.join(x), axis = 1)

search_list=list(input_url['Search']) #.unique())
count=1
marked=[]
f=0
for line in search_list:
    print(count)
    
    #Start from first google domain from the list,once list is completed
    if x>=(len(googleurls)-1): 
        x=0
        
    #Get the google domain from the list for searching
    search_engine=googleurls[x]
    
    #value update to use next google domain
    x=x+1
    z=z+1
    
    #search query on google
    #search=str(line) + "  " + str(code)
    #search1=search.encode("utf-8")
    
    connected=False#set connected
    while not connected:#this loo execute till try part is executed without any error
        
        try:
            #time.sleep(randint(2,4))
            driver.get(search_engine)
            time.sleep(1)
            inputElement = driver.find_element_by_name("q")
            inputElement.send_keys(line)
            inputElement.submit()
            
            #time.sleep(randint(1,1))
            html1=driver.page_source
            connected=True
        except KeyboardInterrupt:#to check cntrl c
            logging.error("Keyboard interrupt error")#adding error to logging
            marked.append(count)
            f=1#sets flag
            connected=True#end first loop
            
        except:
            
            marked.append(count)#marked to find where partial data to be stored
            logging.error("error for data-"+str(count))#adding error to logging
    if f!=1:
        soup1=BeautifulSoup(html1, 'lxml')
        print(line)
        print('=========================================================')
        
        #print(soup1.find_all('div',{'data-attrid':'title'})[0].find('span').get_text().encode("utf-8"))
        if ((len(soup1.find_all('div',{'class':'bNg8Rb'}))>0)or(len(soup1.find_all('div',{'class':'kp-blk knowledge-panel Wnoohf OJXvsb'}))>0)or(len(soup1.find_all('div',{'class':'ifM9O'}))>0)or(len(soup1.find_all('div',{'class':'mod'}))>0)):
            
            if (soup1.find_all('div',{'data-attrid':'title'})):
                title=soup1.find_all('div',{'data-attrid':'title'})[0].find('span').get_text().encode("utf-8")
                print('-----====',title)
                if title=='See results about':
                    continue
                name_to_use.append(line)
                kg_title.append(title)
                #p#rint(name_to_use)
            else:
                kg_title.append('No')
                name_to_use.append(line)


            if (soup1.find_all('div',{'class':'QqG1Sd'})):
                website=soup1.find_all('div',{'class':'QqG1Sd'})[0].find('a').get('href')
                print(website)
                print("-website---",website)
                kg_website.append(website)
            else:
                kg_website.append('No')


            if (soup1.find_all('span',{'class':'YhemCb'})):
                print('Company Type')
                com=soup1.find_all('span',{'class':'YhemCb'})[0].get_text()
                print("----",com)
                type_com.append(com)
            else:
                type_com.append('No')


            if (soup1.find_all('span',{'class':'LrzXr'})):
                print('ADDRESS')
                add=soup1.find_all('span',{'class':'LrzXr'})[0].get_text()
                print("----",add)
                kg_address.append(add)
            else:
                kg_address.append('No')


            print('**************')
            #full=(name_to_use+"|"+title+"|"+website+"|"+add+"|"+com)
            #alllll.append(full)
        else:
            name_to_use.append(line)
            kg_title.append('No')
            #kg_subtitle.append('No')
            type_com.append('No')
            kg_address.append('No')
            kg_website.append('No')
            #kg_phone.append('No')
            alllll.append("NO|NO|NO|NO|NO")

        """except:
            name_to_use.append(line)
            kg_title.append('No')
            #kg_subtitle.append('No')
            type_com.append('No')
            kg_address.append('No')
            kg_website.append('No')
            kg_phone.append('No')
            alllll.append("NO|NO|NO|NO|NO")
            print('==========================================')
            #url='Not Found'"""
    if (count in marked):
        data_ff=pd.DataFrame([name_to_use,kg_title,kg_website,kg_address,type_com]).transpose()
        data_ff.rename({'0':'Name','1':'Title','2':'Website','3':'Address','4':'Company_type'},inplace=True)
        data_ff.replace({'No':''},inplace=True)
        data_ff=pd.concat([input_url,data_ff],sort=False,axis=1)
        data_ff.to_excel(support_file_path+"\\OUTPUT_Initial_"+str(count)+".xlsx")#date.today()
    if f==1:
        break
    count=count+1
data_ff=pd.DataFrame([name_to_use,kg_title,kg_website,kg_address,type_com]).transpose()
data_ff.rename({'0':'Name','1':'Title','2':'Website','3':'Address','4':'Company_type'},inplace=True)
data_ff.replace({'No':''},inplace=True)
data_ff=pd.concat([input_url,data_ff],sort=False,axis=1)
data_ff.to_excel(support_file_path+"\\OUTPUT_Initial_"+str(count)+".xlsx")#date.today()
data_ff=pd.DataFrame([name_to_use,kg_title,kg_website,kg_address,type_com]).transpose()

#data_ff=data_ff.rename(columns={'0':'Name','1':'Title','2':'Website','3':'Address'},inplace=True)

data_ff=data_ff.replace({'No':''})#,inplace=True)
data_ff=pd.concat([input_url,data_ff],sort=False,axis=1)
data_ff.drop(['Search'], axis=1)
data_ff.to_excel(output_file_path+"\\OUTPUT_Final_"+str(date.today())+".xlsx")


print('==============================================')
print('===========PROCESSING DONE===================')
print('==============================================')
