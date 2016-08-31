import pandas as pd
from urllib2 import Request, urlopen
import json
from pandas.io.json import json_normalize
pd.options.display.max_rows = 100

request=Request('https://ad-reporting.armadillo.xyz/api/queries/73/results.json?api_key=sJRqGJ0w9kqKLBTZS9TkNTE8ifzoE2Z0AZ6NrBcA')
response = urlopen(request)
elevations = response.read()
data = json.loads(elevations)
Missed_Avoid_top100=pd.DataFrame(data['query_result']['data']['rows'])

request2=Request('https://ad-reporting.armadillo.xyz/api/queries/74/results.json?api_key=sJRqGJ0w9kqKLBTZS9TkNTE8ifzoE2Z0AZ6NrBcA')
response2 = urlopen(request2)
elevations2 = response2.read()
data2 = json.loads(elevations2)
#json_normalize(data['data'])
pd.DataFrame(data2['query_result']['data']['rows'])

Final_score_df=pd.DataFrame(columns=['domain','symptom','score'])

Score_coeff_array=[]
for value in [1.]*3:
    Score_coeff_array.append(value)
for value in [0.5]*7:
    Score_coeff_array.append(value) 
for value in [0.25]*10:
    Score_coeff_array.append(value) 

for iterate in range(0,100):
    AD_7D_Avoid_sub = AD_7D_Avoid[(AD_7D_Avoid['kai_prj_nm']==Missed_Avoid_top100['domain'].loc[iterate]) & (AD_7D_Avoid['kai_srh_tms']==Missed_Avoid_top100['symptom'].loc[iterate])]
    AD_7D_Avoid_sub_Freq_Table = AD_7D_Avoid_sub.kai_sln_id.value_counts()/sum(AD_7D_Avoid_sub.kai_sln_id.value_counts())
    AD_7D_Avoid_sub_Freq_Table_df= pd.DataFrame({'case':AD_7D_Avoid_sub_Freq_Table.index,'weight':AD_7D_Avoid_sub_Freq_Table}).reset_index(drop=True)

    Missed_Avoid_top100_case_data_df=pd.DataFrame(Missed_Avoid_top100['case_data'].loc[iterate].split(','),columns=['case']).reset_index()
    Missed_Avoid_top100_case_data_df.rename(columns={'index': 'order'}, inplace=True)
    merged_df=Missed_Avoid_top100_case_data_df.merge(AD_7D_Avoid_sub_Freq_Table_df,on='case',how='inner').merge(Score_coeff_df,on='order',how='left')
    Final_score_df.loc[iterate] =[Missed_Avoid_top100['domain'].loc[iterate],Missed_Avoid_top100['symptom'].loc[iterate],sum(merged_df['weight']*merged_df['score'])]
print Final_score_df
Final_score_df.to_csv('final_score.csv')
