#
# get unemployment rates for CT and US
# Jake Kara, December 2017
#

# get unemployment rate CSV because these excel links:
# http://www1.ctdol.state.ct.us/lmi/unemploymentrate.asp
# seem to work in non-IE browsers or pandas/requests lib


import pandas as pd
from datetime import datetime

CT_FILENAME = "http://www1.ctdol.state.ct.us/lmi/unempXls.asp"
US_FILENAME = "http://www1.ctdol.state.ct.us/lmi/USUnempXls.asp"

def get_data(url):
    
    # read HTML
    ret = pd.read_html(url,skiprows=1,header=0)[0]
    
    # drop last row
    ret = ret.drop(len(ret) - 1, axis = 0)
    
    # set 
    ret = ret.rename(index=str,columns={"Unnamed: 0":"Month"})
    ret = ret.set_index("Month")
        
    return ret
  

def chronologize(df,label):
    ret = []
    
    for month in df.index:
        for year in df.columns:
            dtstr = str(month) + " " + str(year)
            date = datetime.strptime(dtstr,"%b %Y")
            #print date
            val = df.loc[month][year]
            #print date, val
            ret.append([date,val])
            
    ret = pd.DataFrame(ret,columns=["month",label]).sort_values(by="month")
    
    ret = ret.set_index("month")
    
    return ret


# save each table as-is from the site
ct = get_data(CT_FILENAME)
us = get_data(US_FILENAME)
ct.to_csv("ct.csv")
us.to_csv("us.csv")

# convert each table to a chronological list
ct_chron = chronologize(ct,"CT")
us_chron = chronologize(us,"US")
ct_chron.to_csv("ct_chron.csv")
us_chron.to_csv("us_chron.csv")

# combine the two lists
both = ct_chron.join(us_chron).sort_index()
both = both[(both["CT"].notnull()) & (both["US"].notnull())]
both.to_csv("both.csv")


