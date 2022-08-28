import os 
import pandas as pd 


path = 'D:/Users/wnsgnl/Desktop/paper_master2/analysis/data/raw'

temp = [] 
for file in os.listdir(path): 
    sub_file = f'{path}/{file}'
    t =  [file, len(os.listdir(sub_file))]
    temp.append(t)

a = pd.DataFrame(temp, columns=['file','size']) 

a.to_excel(r'D:\Users\wnsgnl\Desktop\paper_master2\analysis\res.xlsx')
