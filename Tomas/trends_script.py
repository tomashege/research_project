from selenium import webdriver
import pandas as pd
import time
from datetime import date, timedelta
#change the values below to get the right results.

driver_link = '/Users/tomashegewisch/Downloads/chromedriver'
start_date = date(2020, 3, 15)
end_date = date(2020, 7, 15)

#you have to change this for every computer...
driver = webdriver.Chrome(driver_link)
the_trends = []
def get_trend_pre_day(date):
    country = "south-africa"
    #date = "2020-02-01"
    #time_international = "18"
    the_trends_on_day = []
    for time_international in range(0,24):
#         if time_international == 15 and date == "2020-03-24":
#             continue
        url = "https://getdaytrends.com/"+country+"/"+date+"/"+str(time_international)+"/"
        global driver
        driver.get(url)
        #time.sleep(2)
        try:
            clicker = driver.find_elements_by_xpath('//*[@id="trends"]/div/a')[0].click()
            a = driver.find_elements_by_xpath('//*[@id="trends"]/table/tbody/tr/td/a')
            print(country+" "+str(date)+" "+str(time_international))
            for i in a:
                the_trends.append(i.text)
        except:
            print("The trends on this day and time is not Available")
            driver = webdriver.Chrome(driver_link)



delta = timedelta(days=1)
while start_date <= end_date:
    #print (start_date.strftime("%Y-%m-%d"))
    get_trend_pre_day(start_date.strftime("%Y-%m-%d"))
    start_date += delta
        
#Remove The duplicates
print("Before duplicates: "+ str(len(the_trends)))
#the_trends = list(dict.fromkeys(the_trends))
the_trends_without_duplicates = [] 
[the_trends_without_duplicates.append(x) for x in the_trends if x not in the_trends_without_duplicates]
print("After duplicates are removed: " + str(len(the_trends_without_duplicates)))

#Create CSV File

out = "Trends,\n"
#create the document
for i in the_trends_without_duplicates:
    out+= str(i)+",\n"
#write the documnet
file_name = "trends: " + str(start_date) +  "-" + str(end_date) + ".csv" 
with open(file_name, "w")as text_file:
    text_file.write(out) 
print("file saved") 
