import pandas as pd
import numpy as np
import re
import json

# dataset is downloaded from https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/rs6k-p7g6
data = pd.read_csv('../data/raw_data/DOHMH_New_York_City_Restaurant_Inspection_Results.csv')

# select columns of interest
isp_data = data[['CAMIS', 'DBA', 'BORO', 'BUILDING',
                 'STREET', 'ZIPCODE', 'PHONE', 
                 'CUISINE DESCRIPTION', 'INSPECTION TYPE',
                 'VIOLATION CODE', 'VIOLATION DESCRIPTION', 
                 'Latitude', 'Longitude', 'SCORE', 'GRADE']]

isp_data['INSPECTION DATE'] = pd.to_datetime(data['INSPECTION DATE'])

# code inspection types into four groups: 0 : initial inspection, 1 : re-inspection, 2: reopening, -2: nan
code = np.full([isp_data.shape[0]], -2)
re_ips = isp_data['INSPECTION TYPE'].str.contains('Re-inspection|Second', flags=re.IGNORECASE, regex=True)
re_op = isp_data['INSPECTION TYPE'].str.contains('Reopening', flags=re.IGNORECASE, regex=True)
code[re_ips == True] = 1
code[re_ips == False] = 0
code[re_op == True] = 2
isp_data['INSPECTION CODE'] = code

# replace all nans with -2
isp_data = isp_data.fillna(-2)

# check whether scores and grades match. If not, re-assign the grades.
dfg = isp_data.groupby(['CAMIS'])
for id in dfg.groups.keys():
    df = dfg.get_group(id)
    for i in range(df.shape[0]):
        
        if df.iloc[i]['SCORE'] >= 0:
            
            if df.iloc[i]['INSPECTION CODE'] == 2:
                if df.iloc[i]['GRADE'] != 'P':
                    isp_data.loc[df.iloc[i].name, 'GRADE'] = 'P'
                    
            elif df.iloc[i]['SCORE'] < 14:
                if df.iloc[i]['GRADE'] != 'A':
                    isp_data.loc[df.iloc[i].name, 'GRADE'] = 'A'
                    
            elif df.iloc[i]['INSPECTION CODE'] == 1:
                if 14 <= df.iloc[i]['SCORE'] < 28:
                    if df.iloc[i]['GRADE'] != 'B':
                        isp_data.loc[df.iloc[i].name, 'GRADE'] = 'B'
                        
                elif df.iloc[i]['GRADE'] != 'C':
                    isp_data.loc[df.iloc[i].name, 'GRADE'] = 'C'
                    
            elif df.iloc[i]['INSPECTION CODE'] == 0:
                if df.iloc[i]['GRADE'] != 'P':
                    isp_data.loc[df.iloc[i].name, 'GRADE'] = 'P'
                
        elif df.iloc[i]['GRADE'] != -2 :
            isp_data.loc[df.iloc[i].name, 'GRADE'] = -2
            
            
# replace cuisine description with code
code_to_cuisine = dict(zip(range(len(set(isp_data['CUISINE DESCRIPTION']))), set(isp_data['CUISINE DESCRIPTION'])))
cuisine_to_code = dict(zip(set(isp_data['CUISINE DESCRIPTION']), range(len(set(isp_data['CUISINE DESCRIPTION'])))))
isp_data['CUISINE DESCRIPTION'].replace(cuisine_to_code, inplace=True)

# replace violation description with code
code_to_violation = dict(zip(range(len(set(isp_data['VIOLATION DESCRIPTION'])) - 1), list(set(isp_data['VIOLATION DESCRIPTION']))[: -1]))
violation_to_code = dict(zip(list(set(isp_data['VIOLATION DESCRIPTION']))[: -1], range(len(set(isp_data['VIOLATION DESCRIPTION'])) - 1)))
isp_data['VIOLATION DESCRIPTION'].replace(violation_to_code, inplace=True)

# save restaurant information
rst_info = isp_data[['CAMIS', 'DBA', 'BORO', 'BUILDING',
                     'STREET', 'ZIPCODE', 'PHONE',
                     'CUISINE DESCRIPTION',
                     'Latitude', 'Longitude']].drop_duplicates()

rst_info.to_csv('../data/clean_data/nyc_restaurants_info.csv')

# save inspection information
isp_info = isp_data[['CAMIS', 'INSPECTION CODE', 'VIOLATION DESCRIPTION', 
                     'INSPECTION DATE', 'SCORE', 'GRADE']]\
                     [isp_data['SCORE'] != -2].sort_values(['CAMIS', 'INSPECTION DATE'])

isp_info.to_csv('../data/clean_data/nyc_restaurants_grades.csv', index=False)

with open('../data/clean_data/code_to_cuisine.txt', 'w') as json_file:
    json.dump(code_to_cuisine, json_file)
    
with open('../data/clean_data/cuisine_to_code.txt', 'w') as json_file:
    json.dump(cuisine_to_code, json_file)

with open('../data/clean_data/code_to_violation.txt', 'w') as json_file:
    json.dump(code_to_violation, json_file)

with open('../data/clean_data/violation_to_code.txt', 'w') as json_file:
    json.dump(violation_to_code, json_file)
    
