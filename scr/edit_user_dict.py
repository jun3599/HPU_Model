import os 
import shutil 
import sys 
import subprocess

import pandas as pd 
from jamo import h2j, j2hcj


class compile_user_dict():
    def __init__(self, HPU_dict_path, mecab_path):
        self.HPU_dict_path = HPU_dict_path 
        self.mecab_path = mecab_path 

        try:
            self.HPU_dict = pd.read_excel(self.HPU_dict_path)
        except FileNotFoundError as e1:
            sys.exit("HPU_dict.xlsx파일이 지정된 경로에 존재하지 않습니다. 확인후 문의 부탁드립니다. ")

    def manager(self):

        pre_fix = ['대우,,,,NNP,*,F,대우,*,*,*,*,*\n', '구글,,,,NNP,*,T,구글,*,*,*,*,*\n']
        # HPU사전을 기반으로 단어들을 추출합니다. 

        custom_tokens = self.make_custom_tokens_list()
        # 단어를 입력 형식에 맞게 입력합니다. 
        dict_input = pre_fix
        for word in custom_tokens:
            jongsung_TF = self.get_jongsung_TF(word)
            new = f'{word},,,,NNP,*,{jongsung_TF},{word},*,*,*,*,*\n'
            dict_input.append(new)
        
        os.chdir(self.mecab_path)
        print(os.getcwd())
        # 사전에 변경사항을 저장합니다. 
        with open('./user-dic/nnp.csv', 'w', encoding = 'utf-8') as f:
            for line in dict_input:
                f.write(line)

        # 변경된 사항을 컴파일합니다. 
        p = subprocess.Popen('powershell.exe -ExecutionPolicy Unrestricted -file "./tools/add-userdic-win.ps1"', stdout=sys.stdout)
        p.communicate()
        p.wait()

        # 단어의 우선순위를 조정합니다. (사용자 지정파일을 컴파일하면서, 각 단어의 가중치가 초기화 되어있는 상태입니다.)
        with open ('./mecab-ko-dic/user-nnp.csv','r',encoding = 'utf-8') as f:
            pre = f.readlines()
        # 부여할 우선순위 dict 선언 
        # 해당 숫자는 비용을 의미, 즉 0에 가까울수록 좋음 
        weight_dict = self.calculate_priority(custom_tokens)
        # 가중치 수정 
        result = [] 
        for line in pre:
            # 한줄의 정보를 list로 분할해 정보 수정 
            info_item = line.split(',')
            word = info_item[0]
            if word not in weight_dict:
                new =  ",".join(info_item)
            else:
                new_weight = weight_dict[word]
                info_item[3] = new_weight
                new =  ",".join(map(str, info_item))
            result.append(new)
        
        # 변경내용 저장
        with open ('./mecab-ko-dic/user-nnp.csv','w',encoding = 'utf-8') as f:
            for line in result:
                f.write(line)
        # 변경된 사항을 컴파일합니다. 
        p = subprocess.Popen('powershell.exe -ExecutionPolicy Unrestricted -file "./tools/compile-win.ps1"', stdout=sys.stdout)
        p.communicate()
        
        return None 

    def make_custom_tokens_list(self):
        '''
        입력으로 받은 HPU dict를 길이를 기준으로 정렬합니다. 
        사용자 지정 단어를 토크나이저에 추가할때, "최장 일치의 원칙"에 의거, 가장 길이가 긴 단어의 우선순위를 가장 크게 부여하기 위함입니다. 

        복합어의 경우, 단일어보다 높은 우선순위를 가져야 하기 때문에 사전에 정렬시 복합어를 가장 뒤에 위치시킵니다. 
        '''

        # 지정 단어를 하나의 리스트로 통합
        custom_tokens = self.HPU_dict.drop_duplicates(subset=['word'])['word'].to_list()
        
        # 일부 복합어의 경우, 지정된 단일어를 포함하기 때문에 
        # 단일어를 우선적으로 삽입 후, 복합어를 삽입해야 합니다. 
        compound_word = []
        single_word = [] 
        for word in custom_tokens:
            if ' ' in word:
                compound_word.append(word)
            else:
                single_word.append(word)

        custom_tokens = single_word + compound_word
   
        return custom_tokens
  
    def get_jongsung_TF(self, string):
        '''
        mecab의 사용자 지정 사전에 단어를 추가하기 위해서는 단어의 마지막 글자의 종성 여부를 함께 입력해야 합니다. 
        jamo라이브러리를 활용해 단어의 종성 여부를 파악합니다. 

        '''
        # 글자가 단어별로 분할됩니다. 
        charactors = list(string)
        # 마지막 글자만 가져옵니다. 
        last_word = charactors[-1] 
        # j2hcj(h2j('한글자'))를 통해, 글자 하나를 'ㄱ ㅏ ㅇ' 형식으로 변환후
        # list를 통해 각각의 단어로 분리 
        last_jamo_list = list(j2hcj(h2j(last_word)))
        last_jamo = last_jamo_list[-1]

        # 참 거짓 탐사 
        jongsung_TF = "T"
        if last_jamo in ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']:
            jongsung_TF = "F"
        return jongsung_TF
    
    def calculate_priority(self, custom_tokens):
        # 지정 단어를 하나의 리스트로 통합
        weight_dict = {}
        for idx, word in enumerate(reversed(custom_tokens)):  
            weight_dict[word] = idx
        return weight_dict 



# 동작 확인 및 수정 요 



