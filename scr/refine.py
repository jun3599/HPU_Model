# 자연어 처리를 위한 모듈 
import re 
from konlpy.tag import Mecab 

import pandas as pd 
import sys
from datetime import datetime 
import os 


# 1. 컴파일 대상 폴더를 지정하도록 유도한다. 
# 2. 해당 데이터의 컴파일 버전이 있는지 확인 
#   2-1) 재 컴파일을 진행하거나
#   2-2) 컴파일 중지 

# 0. 컴파일시 진행작업 
#   0-1) 언론사 정보 lemmatization 
#   0-2) 제목, 본문 정보의 불순물 제거 
#   0-3) 본문 기준 토큰화 
#   0-4) 단어 출현 여부 검출 및 Y/N 기재 


class refine_data():
    def __init__(self, HPU_dict_path, mecab_path, data_path):
        self.HPU_dict_path = HPU_dict_path
        self.mecab_path = mecab_path 
        self.data_path = data_path 
        self.tokenizer = Mecab(self.mecab_path)
        
    # def mode_selector(self):

    def confirm_compile_target(self):
        '''
        1개 파일 컴파일 모드 
        다중 선택 모드 
        일괄처리 모드        
        '''

        return None 

    def confirm_ready_compiled(self,file_name):
        '''
        지정된 파일 경로에, 이미 컴파일 되어있는 파일이 존재할 경우 True를,
        존재하지 않을 경우 False를 반환합니다. 
        '''
        compiled_path = f'{self.data_path}/compiled'
        if file_name in os.listdir(compiled_path):
            return True 
        return False
    
    def confirm_monthly_data(self,target_raw_path, warn = True):
        '''
        1. 데이터의 무결성을 확인 
        2. 제외된 언론사 정보가 있으면, 해당 내용을 보고하고 - 유저에게 방안을 선택하도록 옵션을 부여 
        '''
        target_press = ['서울신문','서울경제','한겨레','세계일보','머니투데이','문화일보','매일경제','국민일보','KBS','동아일보','경향신문','MBC','한국경제','SBS','YTN']

        if warn == True:
            files = os.listdir(target_raw_path)
            files = [x.split('_')[0].strip() for x in files]

            diff = sorted(list(set(target_press) - set(files)), reverse=False)
            if len(diff)>1:
                print(f"{target_raw_path}경로상 데이터 파일에 일부 언론사가 누락되어 있습니다. 누락된 언론사의 이름은: ")
                for press in diff:
                    print(press)
                print("="*10)

                confirm = input("컴파일을 계속하시겠습니까? (y/n): ")
                if confirm == 'n':
                    sys.exit("사용자의 컴파일 중단으로 프로그램이 종료됩니다. ")

        return None 

    
    def compile(self):

        return None 

    def merge_monthly_data(self, monthly_data_path):
        data = pd.DataFrame()
        for file in os.listdir(monthly_data_path):
            
            temp = pd.read_csv(f'{monthly_data_path/file}', encoding='utf-8-sig' ,error_bad_lines=False)
            
            # 언론사 이름 통일 
            press = file.split('_')[0].strip()
            temp['press'] = press 

            # 기사 입력정보 정제 
            temp.drop(columns=['input_date_y'], inplace=True)
            temp.rename(columns={'input_date_x':'input_date'}, inplace=True)
            temp['input_date'] = pd.to_datetime(temp['input_date'], errors='ignore')

            # 기사 제목 정제 
            temp.drop(columns=['title_y'], inplace=True)
            temp.rename(columns={'title_x':'title'}, inplace=True)
            temp['title'] = temp['title'].apply(lambda  x: re.sub(r'\n',' ', str(x))).apply(lambda  x: re.sub(r'\t',' ', str(x))).apply(lambda  x: re.sub(r'\s',' ', str(x)))

            # 기사 본문 정제 
            temp['article'] = temp['article'].apply(lambda  x: re.sub(r'\n',' ', str(x))).apply(lambda  x: re.sub(r'\t',' ', str(x))).apply(lambda  x: re.sub(r'\s',' ', str(x)))


            data = data.append(temp, ignore_index= True)
        
        return data  



    def find_group_of_word(self, df, target_dict):
        '''
        HPU 단어사전을 기반으로 
        각 기사에서 각 단어군에 해당하는 단어들이 도출되면, 해당 내용을 H,P,U_A, U_R 컬럼에 담습니다. 
        '''
        def compare_article_list(tokenized_article_list, word_list):
            tokenized_article_list = set(tokenized_article_list)
            word_list = set(word_list)

            result = tokenized_article_list.intersection(word_list)
            return list(result) 
        
        try:
            target_dict = pd.read_excel(self.HPU_dict_path)
        except FileNotFoundError as nf:
            sys.exit(f'HPU사전이 지정된 경로에 존재하지 않습니다.  \nERROR CODE: {nf}')

        H = target_dict.loc[target_dict['tag'] == 'H', 'word'].to_list()
        P = target_dict.loc[target_dict['tag'] == 'P', 'word'].to_list()
        U_A = target_dict.loc[target_dict['tag'] == 'U-A', 'word'].to_list()
        U_R = target_dict.loc[target_dict['tag'] == 'U-R', 'word'].to_list()

        df['H_word'] = df['tokenized_article'].apply(lambda x: compare_article_list(x, H))
        df['P_word'] = df['tokenized_article'].apply(lambda x: compare_article_list(x, P))
        df['U-A_word'] = df['tokenized_article'].apply(lambda x: compare_article_list(x, U_A))
        df['U-R_word'] = df['tokenized_article'].apply(lambda x: compare_article_list(x, U_R))

        return df 

    def write_word_group_TF(self, df):
        '''
        find_group_of_word 함수를 통해 생성된 열들을 기반으로 
        단어의 출현 여부를 확인해 T/F 값을 기입합니다. 
        '''
        def confirm_TF(word_list):
            if len(word_list) == 0:
                return 'F' 
            else:
                return 'T'

        df['H_TF'] = df['H_word'].apply(lambda x: confirm_TF(x))
        df['P_TF'] = df['P_word'].apply(lambda x: confirm_TF(x))
        df['U-A_TF'] = df['U-A_word'].apply(lambda x: confirm_TF(x))
        df['U-R_TF'] = df['U-R_word'].apply(lambda x: confirm_TF(x))

        return df

    def grouping_article(self, df):
        '''
        write_word_group_TF를 통해 도출된 내역을 기반으로 
        HPU-uncertainity 와 HPU-Risk에 해당 하는 단어군을 파악해 TF로 기록합니다. 
        
        '''
        def confirm_HPU_A_TF(H_TF, P_TF, UA_TF):
            if (H_TF == 'T') & (P_TF == 'T') & (UA_TF == 'T'):
              HPU_A_TF = 'T'
            else:
                HPU_A_TF = 'F'
            return HPU_A_TF
        def confirm_HPU_R_TF(H_TF, P_TF, UR_TF):
            if (H_TF == 'T') & (P_TF == 'T') & (UR_TF == 'T'):
                HPU_R_TF = 'T'
            else:
                HPU_R_TF = 'F'
            return HPU_R_TF

        df['HPU_A_TF'] = df.apply(lambda x: confirm_HPU_A_TF(x['H_TF'],x['P_TF'],x['U-A_TF']), axis =1)
        df['HPU_R_TF'] = df.apply(lambda x: confirm_HPU_R_TF(x['H_TF'],x['P_TF'],x['U-R_TF']), axis =1)
        
        return df 