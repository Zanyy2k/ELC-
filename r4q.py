import os
import glob
import time 
import datetime
import numpy as np
import pandas as pd

# Show the starting time of the program
start_time = time.time()
print "Time Started :", datetime.datetime.time(datetime.datetime.now())

refPath = (r'C:/Users/zyu/Desktop/r4q/Reference')
# refPath = (r'/Users/zongdongyu/Desktop/Work/r4q/Reference')
refFiles = glob.glob(refPath +"/*.csv")

siPath = (r'C:/Users/zyu/Desktop/r4q/RawSI')
# siPath = (r'/Users/zongdongyu/Desktop/Work/r4q/RawSI')
siFiles = glob.glob(siPath +"/*.csv")

# stPath = raw_input('Please enter the dir path to Sell Through files (Example: C:/Users/zyu/Desktop/r4q/WithoutST): ')
stPath = (r'C:/Users/zyu/Desktop/r4q/RawST')
# stPath = (r'/Users/zongdongyu/Desktop/Work/r4q/RawST')
stFiles = glob.glob(stPath +"/*.csv") 

#mPath = = raw_input('Please enter the dir path to store merge files (Example: C:/Users/zyu/Desktop/r4q/WithoutST): ')
mPath = (r'C:/Users/zyu/Desktop/r4q/Merge')
# mPath = (r'/Users/zongdongyu/Desktop/Work/r4q/Merge')

i=0 
ref = {}

for fileRef in refFiles:
    print str((os.path.basename(fileRef).split('.'))[0])
    # locals()['ref'+str(i)] = pd.read_csv(fileRef,index_col =None, header =0, low_memory=False, dtype=str)
    data = pd.read_csv(fileRef,index_col =None, header =0, low_memory=False, dtype=str)
    ref[str((os.path.basename(fileRef).split('.'))[0])] = data

for fileSi in siFiles:
    print os.path.basename(fileSi)

    siDf = pd.read_csv(fileSi,index_col =None, header =0, low_memory=False, dtype=str)
    print 'siDf',siDf.shape
    siDf.columns = ['NODE_NAME','SALES_DIVISION_DESCRIPTION','BRAND_DESCRIPTION','CATEGORY_DESCRIPTION','PRODUCT_LINE_DESCRIPTION',
                    'SUB_PRODUCT_LINE_DESCRIPTION','DEMAND_TYPE','MAJOR_CATEGORY_DESCRIPTION','NEW_BASIC','ITEM_ID_4','ITEM_ID_6','ITEM_DESCRIPTION',
                    'BT_CG_DESCRIPTION','Month','Units','Value USD']

    for fileSt in stFiles:

        if((os.path.basename(fileSi).split())[5]) in (os.path.basename(fileSt)):
            print fileSt
            found = True
            break
        else:
            found = False

    if(found):
        print 'found :', found

        # Import the st file
        stDf = pd.read_csv(fileSt,index_col =None, header =0, low_memory=False, dtype=str)
        print 'StDf :',stDf.shape
        stDf.columns = ['NODE_NAME','SALES_DIVISION_DESCRIPTION','BRAND_DESCRIPTION','CATEGORY_DESCRIPTION','PRODUCT_LINE_DESCRIPTION',
                        'SUB_PRODUCT_LINE_DESCRIPTION','DEMAND_TYPE','MAJOR_CATEGORY_DESCRIPTION','NEW_BASIC','ITEM_ID_4','ITEM_ID_6','ITEM_DESCRIPTION',
                        'BT_CG_DESCRIPTION','Fiscal_Year','Forecast_Month','MTH','Retail Sell Thru Value','Retail Sell Thru Units']
        
        stDf['MTH'] = map(lambda x: x.upper(), stDf['MTH'])
        stDf = pd.merge(stDf,ref['ytdytg'],on=['MTH','Fiscal_Year'],how='left')
        stDf.drop(['Fiscal_Year','Forecast_Month','MTH','QTR','HALF','YTD','YYYYMM'], axis =1, inplace = True)
        print 'StDf + ytdytg',stDf.shape

        # Perform merge / join base on the common columns
        print 'Merge ST and SI'
        mDf = pd.merge(siDf,stDf, on=['NODE_NAME','SALES_DIVISION_DESCRIPTION','BRAND_DESCRIPTION','CATEGORY_DESCRIPTION','PRODUCT_LINE_DESCRIPTION',
                        'SUB_PRODUCT_LINE_DESCRIPTION','DEMAND_TYPE','MAJOR_CATEGORY_DESCRIPTION','NEW_BASIC','ITEM_ID_4','ITEM_ID_6','ITEM_DESCRIPTION',
                        'BT_CG_DESCRIPTION','Month'], how='outer')

#         # mDf['Retail Sell Thru Value'] = mDf['Retail Sell Thru Value'].fillna(0)
#         # mDf['Retail Sell Thru Units'] = mDf['Retail Sell Thru Units'].fillna(0)

        print 'mDf :',mDf.shape
    else:
        print 'found :',found
        siDf['Retail Sell Thru Units'] = 0
        siDf['Retail Sell Thru Value'] = 0
        mDf = siDf
        print 'mDf :',mDf.shape

    mDf = mDf[['NODE_NAME','SALES_DIVISION_DESCRIPTION','BRAND_DESCRIPTION',
        'CATEGORY_DESCRIPTION','PRODUCT_LINE_DESCRIPTION','SUB_PRODUCT_LINE_DESCRIPTION',
        'DEMAND_TYPE','MAJOR_CATEGORY_DESCRIPTION','NEW_BASIC','ITEM_ID_4','ITEM_ID_6',
        'ITEM_DESCRIPTION','BT_CG_DESCRIPTION','Month','Units','Value USD',
        'Retail Sell Thru Units','Retail Sell Thru Value']]


    mDf = pd.merge(mDf,ref['ytdytg'],on=['Month'],how= 'left')
    print 'ytdytg',mDf.shape
    
    # Add a new column for lag1 / lag0
    if('Lag0' in (os.path.basename(fileSi))):
        print ('Lag0' in (os.path.basename(fileSi)))
        mDf.insert(len(mDf.columns), 'CDP', 'Lag0')
    elif('Lag1' in (os.path.basename(fileSi))):
        print ('Lag1' in (os.path.basename(fileSi)))
        mDf.insert(len(mDf.columns), 'CDP', 'Lag1')
    print 'CDP inserted',mDf.shape

    mDf = pd.merge(mDf,ref['mkt'],on=['NODE_NAME'],how= 'left')
    print 'mkt',mDf.shape
    mDf = pd.merge(mDf,ref['brand'],on=['BRAND_DESCRIPTION'],how= 'left')
    print 'brand',mDf.shape
    mDf = pd.merge(mDf,ref['dt'],on=['DEMAND_TYPE'],how= 'left')
    print 'dt',mDf.shape
    mDf = pd.merge(mDf,ref['bt'],on=['BT_CG_DESCRIPTION'],how= 'left')
    print 'bt',mDf.shape
    mDf = pd.merge(mDf,ref['hero'],on=['ITEM_ID_4'],how= 'left')
    mDf['HERO1'] = mDf['HERO1'].fillna('Other Business')
    print 'hero',mDf.shape
    mDf = pd.merge(mDf,ref['keylaunches'],on=['ITEM_ID_4'],how= 'left')
    print 'keylaunches',mDf.shape
    mDf = pd.merge(mDf,ref['cc'],on=['ITEM_ID_4'],how= 'left')
    print 'cc',mDf.shape
    mDf = pd.merge(mDf,ref['reform'],on=['ITEM_ID_4'],how= 'left')
    mDf['Reform'] = mDf['Reform'].fillna('No')
    print 'reform',mDf.shape
    mDf = pd.merge(mDf,ref['bias'],on=['MARKET','ITEM_ID_6'],how= 'left')
    print 'bias',mDf.shape

    # output to csv file
    i+=1
    filename= 'merge_'+ str((os.path.basename(fileSi).split())[4])+' '+str((os.path.basename(fileSi).split())[5])
    # stDf.to_csv(os.path.join(mPath,filename), index = False, header = True)
    mDf.to_csv(os.path.join(mPath,filename), index = False, header = True)
    print 20*'-',filename,20*'-'

# Combine all the files into one
print 'Combining the merged files'
fileList = glob.glob(mPath +"/*.csv")
header = 'MARKET,DIVISION,BRAND,CATEGORY,PRODUCT LINE,SUB PRODUCT LINE,DT,MAJOR CATEGORY,NEW F12M,4D,6D,DESCRIPTION,BT,MONTH,SI UNIT,SI USD,ST UNIT,ST USD,MTH,QTR,HALF,FY,YTD,YYYYMM,CDP,MARKET (DP),DIVISION (DP),DT (DP),BT (DP),HERO1,HERO2,HERO3,KEY LAUNCHES,CUSHION,REFORM,BIAS\n'
with open(r'C:/Users/zyu/Desktop/r4q/r4q.csv','a') as file: 
    file.write(header)
    for files in fileList:    
        with open(files,"r") as inFile:
            inFile.readline()
            for row in inFile:
                file.write(row)
file.close()
print 'Combined into one file'

# Show the total time taken for the program
end_time = time.time() - start_time
print "Time Ended", datetime.datetime.time(datetime.datetime.now())
m, s = divmod(end_time, 60)
h, m = divmod(m, 60)
print "%d:%02d:%02d" % (h, m, s)