import pandas as pd 
import os 
from tqdm import tqdm 
import warnings
import csv
warnings.filterwarnings('ignore')

confirm = pd.DataFrame()
# 결측 = pd.DataFrame()

path = 'D:/users/Desktop/Junhwi/국토연구원/HPU_Model/data/raw'
for folder in tqdm(os.listdir(path), desc='전체진행'):
    print('\n', folder, '\n')
    for file in tqdm(os.listdir(f'{path}/{folder}'), desc='1개월중 진행'):

        file_name = f'{path}/{folder}/{file}'
        # try: 
        temp = pd.read_csv(file_name)
        # except:
        #     temp = pd.read_table(f'{path}/{folder}/{file}', engine="python", error_bad_lines=False, sep=',', encoding='utf-8-sig', header=0,warn_bad_lines=False)

        total_shape = temp.shape[0]
        num_sports =  temp.loc[temp['naver_url'].apply(lambda x: 'sports' in str(x))].shape[0]
        num_entertain =  temp.loc[temp['article'].apply(lambda x: '수집불가 페이지' in str(x))].shape[0]

        target =  temp.loc[(~temp['naver_url'].apply(lambda x: 'sports' in str(x))) & (pd.isna(temp['article']))]
        target_shape = target.shape[0]

        confirm = confirm.append({'file':file, '총 레코드수':total_shape, '스포츠기사': num_sports,'연애기사':num_entertain ,'누락수': target_shape, '누락율':target_shape/total_shape}, ignore_index=True)
        # 결측 = 결측.append(target, ignore_index=True)

        del temp, total_shape, num_sports, target, target_shape

confirm.to_csv('D:/users/Desktop/Junhwi/국토연구원/HPU_Model/파일별결측내역서_221016.csv', index= False, encoding='utf-8-sig')
# 결측.to_csv('D:/users/Desktop/Junhwi/국토연구원/HPU_Model/결측레코드.csv', index=False, encoding='utf-8-sig')

