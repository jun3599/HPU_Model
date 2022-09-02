import pandas as pd 
from datetime import datetime 
from tqdm import tqdm 
import re 
import os 
import sys 

import warnings
warnings.filterwarnings('ignore')


# 시작일과 종료일에 대해 물어봄 

# 시작일과 종료일 사이의 모든 컴파일 데이터가 있는지 확인 
    # 이때, 일부 누락을 허용할것인가? 
    # 1차 배포시에는 불허 

# 저장될 컬럼에는, 언론사-기간 별 각 기사의 비중 및 계산값이 있어야함 

# 개별 파일을 계산하고 결과를 청크로 return 
# 모든 데이터가 모이면 표준편차 계산 


class calculate_index():
    def __init__(self, data_path) :
        self.data_path = data_path 
        self.compiled_list = os.listdir(f'{self.data_path}/compiled')
        self.today = datetime.now().strftime('%Y%m%d')
        self.manager()

    def manager(self):
        sd, ed = self.confirm_target()
        periods = self.get_series_of_month(sd,ed)

        save_path = f'{self.data_path}/result/분석결과_FROM{sd}TO{ed}_생성일{self.today}.xlsx'
        
        result = pd.DataFrame()
        for period in tqdm(periods, desc="지수 산출 진행률"):
            compiled_data_path = f'{self.data_path}/compiled/{period}.csv'
            chunk, presses = self.counter(compiled_data_path)
            result = result.append(chunk, ignore_index=True)
            del chunk 
        
        result = self.calculator(result, presses)
        result.to_excel(save_path, encoding='utf-8-sig', index=True)
        return None 

    
    def confirm_target(self):
        sd = input("분석을 진행할 \"시작\"년월을 yyyydd 형식으로 입력해주세요. (정확히 입력완료후 enter, 종료를 원하시면 *를 입력해주세요): ")
        if sd == '*':
            sys.exit("사용자의 요청에 의해 프로그램이 종료됩니다. ")
        if f'{sd}.csv' not in self.compiled_list:
            print(f"{sd}.csv 파일이 ./data/compiled 파일 내에 존재하지 않습니다.")
            self.confirm_target()

        ed = input("분석을 진행할 \"종료\"년월을 yyyydd 형식으로 입력해주세요. (정확히 입력완료후 enter, 종료를 원하시면 *를 입력해주세요): ")
        if ed == '*':
            sys.exit("사용자의 요청에 의해 프로그램이 종료됩니다. ")
        if f'{ed}.csv' not in self.compiled_list:
            print(f"{ed}.csv 파일이 ./data/compiled 파일 내에 존재하지 않습니다.")
            self.confirm_target()
        
        return sd, ed 
    
    def get_series_of_month(self,sd,ed):
        sd = datetime.strptime(sd, '%Y%m')
        ed = datetime.strptime(ed, '%Y%m')
        
        time_series = [x.strftime('%Y%m') for x in pd.date_range(sd, ed, freq='MS')]
        targets = [f'{x}.csv' for x in time_series]

        # 대상 시점 - 컴파일 연산을 통해 분석 대상 파일의 부재를 확인합니다. 
        diff = sorted(list(set(targets) - set(self.compiled_list)), reverse=False)
        if len(diff) > 0:
            print("분석 대상 시점중, 일부 시점의 데이터 누락이 존재합니다.")
            print('='*10)
            for file in diff:
                print(file)
            print("="*10)

            sys.exit('누락된 시점의 데이터를 먼저 컴파일하고 다시 시도해주세요')

        else:
            return time_series
    
  
    def counter(self, target_file):
        try:
            data = pd.read_csv(target_file)
        except: 
            # bad sector 가 존재하는 데이터를 불러오기 위한 예외처리
            data = pd.read_table(target_file, engine="python", error_bad_lines=False, sep=',', encoding='utf-8-sig', header=0,warn_bad_lines=False)
        
        date = datetime.strptime(data['input_date'].value_counts().keys().to_list()[0], '%Y-%m-%d').strftime('%Y%m')
        presses = list(data['press'].unique())
        
        datum = {}
        datum['period'] = date
        for press in presses: 
            total_shape = data.loc[data['press'] == press].shape[0]
            HPU_A_shape = data.loc[(data['press'] == press) & (data['HPU_A_TF'] == 'T')].shape[0]
            HPU_R_shape = data.loc[(data['press'] == press) & (data['HPU_R_TF'] == 'T')].shape[0]

            RF_HPU_A = HPU_A_shape/total_shape 
            RF_HPU_R = HPU_R_shape/total_shape 

            datum[f'TOTAL_NUM_{press}'] = total_shape
            datum[f'HPU_A_NUM_{press}'] = HPU_A_shape
            datum[f'HPU_R_NUM_{press}'] = HPU_R_shape
            
            datum[f'RF_HPU_A_NUM_{press}'] = RF_HPU_A
            datum[f'RF_HPU_R_NUM_{press}'] = RF_HPU_R 

        return datum, presses 

    def calculator(self, df, presses):
        
        for press in presses:
            df[f'SD_{press}'] = ''
            df[f'SD_{press}'][0] = df[f'TOTAL_NUM_{press}'].std(ddof = 0)

            SD = df[f'SD_{press}'][0]
            df[f'RF/SD_A_{press}'] = df[f'RF_HPU_A_NUM_{press}']/SD
            df[f'RF/SD_R_{press}'] = df[f'RF_HPU_R_NUM_{press}']/SD
        
        RF_SD_A_columns = [x for x in df.columns if 'RF/SD_A_' in x]
        RF_SD_R_columns = [x for x in df.columns if 'RF/SD_R_' in x]

        df['TOTAL_RF/SD_A'] = df[RF_SD_A_columns].sum(axis = 1)
        df['TOTAL_RF/SD_R'] = df[RF_SD_R_columns].sum(axis = 1)

        df['Zt_A'] = df['TOTAL_RF/SD_A']/len(presses)
        df['Zt_R'] = df['TOTAL_RF/SD_R']/len(presses)

        df['Zt_A/T'] = ''
        df['Zt_R/T'] = ''
        df['Zt_A/T'][0] = df['Zt_A'].mean()
        df['Zt_R/T'][0] = df['Zt_R'].mean()

        print(df['Zt_A/T'])
        print(df['Zt_A/T'].dtype)

        df['HPU_A'] = df['Zt_A']/df['Zt_A/T'][0] *100 
        df['HPU_R'] = df['Zt_R']/df['Zt_R/T'][0] *100

        # 컬럼 정렬 
        columns = ['period'] 
        for prefix in ['TOTAL_NUM_','HPU_A_NUM_','HPU_R_NUM_', 'RF_HPU_A_NUM_','RF_HPU_R_NUM_', 'SD_','RF/SD_A_','RF/SD_R_']:
            for press in presses:
                columns.append(f'{prefix}{press}')
        
        columns += ['TOTAL_RF/SD_A','TOTAL_RF/SD_R','Zt_A','Zt_R','Zt_A/T','Zt_R/T','HPU_A','HPU_R']

        df = df[columns]
        df.set_index('period', inplace = True)    
        return df 