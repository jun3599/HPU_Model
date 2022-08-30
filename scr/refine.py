import re 
import pandas as pd 
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
    
    def confirm_monthly_data(self):
        '''
        1. 데이터의 무결성을 확인 
        2. 제외된 언론사 정보가 있으면, 해당 내용을 보고하고 - 유저에게 방안을 선택하도록 옵션을 부여 
        '''
        return None 

    
    def compile(self):

        

        return None 


    def tokenize_article(self):
        return None 
    

    