import pandas as pd
import numpy as np
import re
import json

# dataset is downloaded from https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/rs6k-p7g6
data = pd.read_csv('../data/raw_data/DOHMH_New_York_City_Restaurant_Inspection_Results.csv')

# select columns of interest
isp_data = data.copy()[['CAMIS', 'DBA', 'BORO', 'BUILDING',
                        'STREET', 'ZIPCODE', 'PHONE',
                        'CUISINE DESCRIPTION', 'INSPECTION TYPE',
                        'VIOLATION CODE', 'VIOLATION DESCRIPTION',
                        'Latitude', 'Longitude', 'SCORE', 'GRADE']]

isp_data.columns = ['camis', 'dba', 'boro', 'building',
                    'street', 'zipcode', 'phone', 
                    'cuisine description', 'inspection type',
                    'violation code', 'violation description', 
                    'latitude', 'longitude', 'score', 'grade']

isp_data['inspection date'] = pd.to_datetime(data['INSPECTION DATE'].copy())

# code inspection types into four groups: 0 : initial inspection, 1 : re-inspection, 2: reopening, -2: nan
code = np.full([isp_data.shape[0]], -2)
re_ips = isp_data['inspection type'].copy().str.contains('Re-inspection|Second', flags=re.IGNORECASE, regex=True)
re_op = isp_data['inspection type'].copy().str.contains('Reopening', flags=re.IGNORECASE, regex=True)
code[re_ips == True] = 1
code[re_ips == False] = 0
code[re_op == True] = 2
isp_data['inspection code'] = code

# replace all nans with -2
isp_data = isp_data.fillna(-2)

# check whether scores and grades match. If not, re-assign the grades.
dfg = isp_data.groupby(['camis'])
for id in dfg.groups.keys():
    df = dfg.get_group(id)
    for i in range(df.shape[0]):
        
        if df.iloc[i]['score'] >= 0:
            
            if df.iloc[i]['inspection code'] == 2:
                if df.iloc[i]['grade'] != 'P':
                    isp_data.loc[df.iloc[i].name, 'grade'] = 'P'
                    
            elif df.iloc[i]['score'] < 14:
                if df.iloc[i]['grade'] != 'A':
                    isp_data.loc[df.iloc[i].name, 'grade'] = 'A'
                    
            elif df.iloc[i]['inspection code'] == 1:
                if 14 <= df.iloc[i]['score'] < 28:
                    if df.iloc[i]['grade'] != 'B':
                        isp_data.loc[df.iloc[i].name, 'grade'] = 'B'
                        
                elif df.iloc[i]['grade'] != 'C':
                    isp_data.loc[df.iloc[i].name, 'grade'] = 'C'
                    
            elif df.iloc[i]['inspection code'] == 0:
                if df.iloc[i]['grade'] != 'P':
                    isp_data.loc[df.iloc[i].name, 'grade'] = 'P'
                
        elif df.iloc[i]['grade'] != -2 :
            isp_data.loc[df.iloc[i].name, 'grade'] = -2
            
            
# replace cuisine description with code
code_to_cuisine = dict(zip(range(len(set(isp_data['cuisine description']))), set(isp_data['cuisine description'])))
cuisine_to_code = dict(zip(set(isp_data['cuisine description']), range(len(set(isp_data['cuisine description'])))))

code_to_cuisine[cuisine_to_code['Latin (Cuban, Dominican, Puerto Rican, South & Central American)']] = \
'Latin (Cuban, Dominican, Puerto<br>Rican, South & Central American)'
cuisine_to_code['Latin (Cuban, Dominican, Puerto<br>Rican, South & Central American)'] =\
cuisine_to_code['Latin (Cuban, Dominican, Puerto Rican, South & Central American)']

isp_data['cuisine type'] = isp_data['cuisine description'].replace(cuisine_to_code)

# replace violation description with code
code_to_violation = dict(zip(range(len(set(isp_data['violation description']))), list(set(isp_data['violation description']))))
violation_to_code = dict(zip(list(set(isp_data['violation description'])), range(len(set(isp_data['violation description'])))))

# add breaks in violation descriptions
for item in isp_data['violation description']:
    l = item.split()
    temp = []
    i = 5
    while i < len(l):
        temp.append(' '.join(l[max(0, i - 10): i]))
        i += 10
    temp.append(' '.join(l[i - 10:]))
    item_br = '<br>'.join(temp)
    code_to_violation[violation_to_code[item]] = item_br
    violation_to_code[item_br] = violation_to_code[item]

violation_to_code['NA'] = violation_to_code['-2']
code_to_violation[violation_to_code['NA']] = 'NA'

isp_data['violation type'] = isp_data['violation description'].replace(violation_to_code)
isp_data['camis'] = isp_data['camis'].astype(str)

# save restaurant information
rst_info = isp_data[['CAMIS', 'DBA', 'BORO', 'BUILDING',
                     'STREET', 'ZIPCODE', 'PHONE',
                     'CUISINE DESCRIPTION',
                     'Latitude', 'Longitude']].drop_duplicates()

rst_info.to_csv('../data/clean_data/nyc_restaurants_info.csv')

# save restaurant information
rst_info = isp_data[['camis', 'dba', 'boro', 'building', 
                     'street', 'zipcode', 'phone',
                     'cuisine type',
                     'latitude', 'longitude']].drop_duplicates()
rst_info = rst_info.sort_values(['camis'])
rst_info['current_grade'] = isp_data.sort_values(['camis', 'inspection date']).groupby(['camis'])['grade'].apply(lambda x: x.iloc[-1]).values

rst_info.to_csv('../data/clean_data/nyc_restaurants_info.csv', index=False)

# save inspection information
isp_info = isp_data[['camis', 'dba', 'inspection code', 'violation type', 
                     'inspection date', 'score', 'grade']]\
[isp_data['score'] >= 0].sort_values(['camis', 'inspection date'])

isp_info.to_csv('../data/clean_data/nyc_restaurants_grades.csv', index=False)

# save analysis results
analysis_data = rst_info.groupby(['boro', 'cuisine type', 'current_grade'])[['dba']].count().reset_index()
analysis_data.columns = ['boro', 'cuisine type', 'grade', 'count']

analysis_data.to_csv('../data/clean_data/nyc_restaurants_analysis.csv', index=False)

# save dicts
with open('../data/clean_data/code_to_cuisine.txt', 'w') as json_file:
    json.dump(code_to_cuisine, json_file)
    
with open('../data/clean_data/cuisine_to_code.txt', 'w') as json_file:
    json.dump(cuisine_to_code, json_file)

with open('../data/clean_data/code_to_violation.txt', 'w') as json_file:
    json.dump(code_to_violation, json_file)

with open('../data/clean_data/violation_to_code.txt', 'w') as json_file:
    json.dump(violation_to_code, json_file)
    
