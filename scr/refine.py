import re 
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


    def tokenize_article(self):
        return None 
    

    