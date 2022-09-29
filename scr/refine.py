# 자연어 처리를 위한 모듈 
import re 
from konlpy.tag import Mecab 

import pandas as pd 
import sys
from datetime import datetime 
import os

from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')


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
    def __init__(self, HPU_dict_path, mecab_ko_dict_path, data_path):
        self.HPU_dict_path = HPU_dict_path
        self.mecab_path = mecab_ko_dict_path 
        self.data_path = data_path 
        if not os.path.exists(f'{self.data_path}/compiled'):
            os.mkdir(f'{self.data_path}/compiled')
        if not os.path.exists(f'{self.data_path}/result'):
            os.mkdir(f'{self.data_path}/result')
        

        self.tokenizer = Mecab(self.mecab_path)
        self.manager()
        
    def manager(self):
        mode = self.mode_selector()
        if mode == '1':
            self.compile_option_1()
        elif mode == '2':
            self.compile_option_2()
        elif mode == '3':
            self.compile_option_3()
        elif mode == '0':
            self.compile_option_0()
        else: 
            sys.exit("사용자의 요청으로 프로그램을 종료합니다.")

    def mode_selector(self):
        mode = {'1': '1개 파일만 컴파일 진행', '2': '컴파일된 파일이 없는 모든 파일을 컴파일', '3': '여러개의 파일 선택 컴파일', '0': '모든 파일 컴파일', '*':'종료'}
        selected = input("컴파일 옵션을 선택해주세요! \n1: 1개 파일만 컴파일 진행\n2: 컴파일된 파일이 없는 모든 파일을 컴파일\n3: 여러개의 파일 선택 컴파일\n0: 모든 파일 컴파일\n*: 프로그램 종료\n (원하시는 번호를 입력후 엔터를 눌러주세요!): ")

        # 입력값 확인 
        if selected not in ['0','1','2','3','*']:
            sys.exit("잘못된 컴파일 옵션 선택입니다. 확인후 프로그램을 다시 시작해주세요!")

        # 입력 재확인 
        confirm = input(f"선택하신 컴파일 옵션이 \n\"{mode[selected]}\"가 맞습니까? (y/n): ")
        if confirm == 'n':
            self.mode_selector()
        else: 
            return selected 
    
    def compile_option_1(self):
        '''
        1개 파일을 대상으로 컴파일을 진행합니다. 
        입력의 형식은 yyyymm의 파일명입니다. 
        '''
        print("1개 파일 컴파일 옵션을 선택하셨습니다. ")
        target_file_name = input('컴파일 대상 폴더의 이름을 yyyymm형식으로 정확히 입력후 Enter를 눌러주세요: ')
        confirm = input(f'대상 폴더가 {target_file_name}이 맞습니까? (y/n): ')
        
        if confirm == 'n':
            self.compile_option_1()
        monthly_data_path = f'{self.data_path}/raw/{target_file_name}'
        save_result_path = f'{self.data_path}/compiled/{target_file_name}.csv'

        self.compile(monthly_data_path, save_result_path)
        print(f"{target_file_name}에 대한 컴파일이 완료되었습니다. ")
        return None

    def compile_option_2(self):
        '''
        데이터 중, 컴파일 되지 않은 파일에 대해 컴파일을 진행합니다. 
        '''
        compiled_files = set([str(x).strip() for x in os.listdir('D:/users/Desktop/Junhwi/국토연구원/HPU_Model/data/compiled')]) 
        raw_files = set([str(x).strip() for x in os.listdir('D:/users/Desktop/Junhwi/국토연구원/HPU_Model/data/raw')]) 
        
        diff = sorted(list(set(raw_files) - set(compiled_files)), reverse=False)
        len_diff = len(diff)

        for x in diff:
            print(f'Folder: {x}')
        confirm = input(f"총 {len_diff}개의 컴파일 대상 파일이 발견되었습니다. 일괄 처리를 진행할까요? (y/n): ")

        if confirm == 'n':
            sys.exit("사용자의 요청에 의해 컴파일이 중단되었습니다.")
        
        for target_file_name in tqdm(diff, desc = '다중 컴파일 진행현황'):
            monthly_data_path = f'{self.data_path}/raw/{target_file_name}'
            save_result_path = f'{self.data_path}/compiled/{target_file_name}.csv'

            self.compile(monthly_data_path, save_result_path)
        
        print(f"컴파일이 완료되었습니다. ")        
        return None

    def compile_option_3(self):
        '''
        사용자의 다중 입력을 기준으로 컴파일을 진행합니다. 
        '''
        input_target = sorted(list(map(str, input('컴파일을 진행하고자 하는 파일의 이름을 yyyymm형식으로 정확히 입력해주세요 (구분자는 ','으로  입력 완료시 Enter를 눌러주십시오): ').split(' '))), reverse=False)
        
        confirm = input(f"선택하신 항목이\n{input_target}\n이 맞습니까? (y/n): ")
        
        if confirm == 'n':
            self.compile_option_3
        
        raw_files = set([str(x).strip() for x in os.listdir('D:/users/Desktop/Junhwi/국토연구원/HPU_Model/data/raw')]) 
        input_target = set(input_target)

        diff = sorted(list(set(input_target) - set(raw_files)), reverse=False)
        if len(diff) > 0:
            sys.exit(f"입력된 대상 파일 중, {diff} 파일이 존재하지 않습니다. 프로그램을 종료합니다.")
        
        input_target = list(input_target)
        for target_file_name in tqdm(input_target, desc = '다중 컴파일 진행현황'):
            monthly_data_path = f'{self.data_path}/raw/{target_file_name}'
            save_result_path = f'{self.data_path}/compiled/{target_file_name}.csv'

            self.compile(monthly_data_path, save_result_path)
        
        print(f"컴파일이 완료되었습니다. ")        

        return None

    def compile_option_0(self):
        '''
        일괄 처리를 진행합니다. 
        '''
        target = sorted(os.listdir('D:/users/Desktop/Junhwi/국토연구원/HPU_Model/data/raw'), reverse= True)
        for target_file_name in tqdm(target, desc = '다중 컴파일 진행현황'):
            monthly_data_path = f'{self.data_path}/raw/{target_file_name}'
            save_result_path = f'{self.data_path}/compiled/{target_file_name}.csv'

            self.compile(monthly_data_path, save_result_path)
        
        print(f"컴파일이 완료되었습니다. ")

        return None 



    def confirm_ready_made(self, file_name, warn = True, skip = True):
        '''
        지정된 파일 경로에, 이미 컴파일 되어있는 파일이 존재할 경우 True를,
        존재하지 않을 경우 False를 반환합니다. 
        '''
        if warn == True:
            compiled_path = f'{self.data_path}/compiled'
            if file_name in os.listdir(compiled_path):
                if skip == True:
                    return None 
                else: 
                    confirm = input(f"컴파일된 파일 목록에 {file_name}이(가) 이미 존재합니다. 컴파일을 계속하시겠습니까? (y/n): ")
                    if confirm == 'n':
                        sys.exit("사용자의 요청으로 인해 프로그램이 종료됩니다.")
                    return None 


    def confirm_monthly_data(self,target_raw_path, warn = True, skip =True):
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

                if skip == True:
                    return None 
                else:
                    confirm = input("컴파일을 계속하시겠습니까? (y/n): ")
                    if confirm == 'y':
                        return None 
                    elif confirm == 'n':
                        sys.exit("사용자의 컴파일 중단으로 프로그램이 종료됩니다. ")
                    else:
                        sys.exit("잘못된 명령입니다. 프로그램을 종료합니다. ")
        return None 

    
    def compile(self, monthly_data_path, save_result_path, warn = True, skip =True):
        
        # 컴파일된 파일의 존재여부 확인 
        file_name = save_result_path.split('/')[-1]
        self.confirm_ready_made(file_name, warn, skip)

        # 일자별 데이터 중 누락 언론사 존재 여부 파악 
        self.confirm_monthly_data(monthly_data_path, warn, skip)

        # 데이터 처리 시작 
        data = self.merge_monthly_data(monthly_data_path=monthly_data_path)
        data = self.tokenize_article(data)
        data = self.find_group_of_word(data)
        data = self.find_group_of_word(data)
        data = self.write_word_group_TF(data)
        data = self.grouping_article(data)

        data.to_csv(save_result_path, index=False, encoding='utf-8-sig')

        return None 

    def merge_monthly_data(self, monthly_data_path, drop_entertain_sport = True):
        data = pd.DataFrame()
        for file in os.listdir(monthly_data_path):
            # 개별 데이터 파일 로드 
            try: 
                temp = pd.read_csv(f'{monthly_data_path}/{file}')
            except:
                # bad sector 가 존재하는 데이터를 불러오기 위한 예외처리
                temp = pd.read_table(f'{monthly_data_path}/{file}', engine="python", error_bad_lines=False, sep=',', encoding='utf-8-sig', header=0,warn_bad_lines=False)
            

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

            # 기사 본문이 존재하지 않는 데이터 제거 
            temp.dropna(subset=['article'], inplace=True)
            if drop_entertain_sport:
                # 기사의 형식이 연애기사거나, 스포츠 기사인 경우를 제외합니다.
                temp.drop(temp.loc[temp['naver_url'].str.contains('sports.news.nave')].index, inplace=True)
                temp.drop(temp.loc[(temp['article'].str.contains('수집불가 페이지')|(temp['article'].str.contains('entertain.naver.com')))].index, inplace=True)

            # 기사 본문 정제 
            temp['article'] = temp['article'].apply(lambda  x: re.sub(r'\n',' ', str(x))).apply(lambda  x: re.sub(r'\t',' ', str(x))).apply(lambda  x: re.sub(r'\s',' ', str(x)))


            data = data.append(temp, ignore_index= True)
        
        return data  

    def tokenize_article(self, df):
        tokenizer = self.tokenizer
        df['tokenized_article'] = df['article'].apply(lambda x: tokenizer.nouns(str(x)))

        return df

    def find_group_of_word(self, df):
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

    def write_word_group_TF(self, df, min_freq = 1):
        '''
        find_group_of_word 함수를 통해 생성된 열들을 기반으로 
        단어의 출현 여부를 확인해 T/F 값을 기입합니다. 
        '''
        def confirm_TF(word_list, min_freq):
            if len(word_list) == 0:
                return 'F' 
            elif len(word_list) >= min_freq:
                return 'T'

            else:
                return 'T'

        df['H_TF'] = df['H_word'].apply(lambda x: confirm_TF(x, 2))
        df['P_TF'] = df['P_word'].apply(lambda x: confirm_TF(x,1))
        df['U-A_TF'] = df['U-A_word'].apply(lambda x: confirm_TF(x,1))
        df['U-R_TF'] = df['U-R_word'].apply(lambda x: confirm_TF(x,1))

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