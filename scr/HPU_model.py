from calculate_index import * 
from edit_user_dict import * 
from refine import * 
import os 
import sys 

class HPU_model():
    def __init__(self, data_path, HPU_dict_path, mecab_path):
        self.data_path = data_path 
        self.HPU_dict_path = HPU_dict_path 
        
        self.mecab_path = mecab_path 
        self.mecab_kodict_path = f'{self.mecab_path}/mecab-ko-dic'

        self.clear = lambda: os.system('cls' if os.name=='nt' else 'clear')
        self.mode_selector()

    def mode_selector(self):
        cases = {'1':' HPU사전 컴파일', '2':' 컴파일된 HPU사전을 기반으로 뉴스 데이터 컴파일', '3':'컴파일된 뉴스데이터를 기반으로 지표산출', '4':'전체과정 진행'}

        mode = input(f"실행할 모드를 선택해주세요 \n {'='*50}\n1: {cases['1']}\n2:{cases['2']}\n3: {cases['3']}\n4: {cases['4']}\n{'='*50}\nInput (숫자 입력후 ENTER, 종료를 원할시 \"n\"입력): ")
        self.clear()

        if mode == 'n':
            sys.exit("사용자의 요청으로 인해 프로그램을 종료합니다.")
        if mode not in cases.keys():
            print("잘못된 입력입니다. \n")
            self.clear()
            self.mode_selector()
            
        
        confirm = input(f'선택하신 모드가 {cases[mode]}가 맞습니까? (y/n): ')
        if confirm == 'y':
            self.clear()
            pass 
        elif confirm == 'n':
            self.clear()
            self.mode_selector()
        else:
            print("잘못된 입력입니다. \n")
            self.clear()
            self.mode_selector()
 
        if mode == '1': 
            compile_user_dict(self.HPU_dict_path, self.mecab_path)
            print('HPU사전의 최신화가 완료되었습니다.')
            return None 

        elif mode == '2':
            refine_data(self.HPU_dict_path, self.mecab_kodict_path, self.data_path)
            print("뉴스 데이터의 컴파일이 완료되었습니다.")
            confirm = input("컴파일된 데이터를 기반으로 지표 산출을 진행하시겠습니까? (y/n): ")
            if confirm == 'y':
                self.clear()
                calculate_index(self.data_path)
            elif confirm == 'n':
                print("프로그램을 종료합니다. ")
                return None 
            else: 
                print("잘못된 입력입니다. 프로그램을 종료합니다. ")
                return None 

        elif mode == '3':
            self.clear()
            calculate_index(self.data_path)
            print("지표산출이 완료되었습니다.")
            return None 

        elif mode == '4':
            print("사용자 지정 단어사전을 컴파일합니다.")
            compile_user_dict(self.HPU_dict_path, self.mecab_path)
            print('HPU사전의 최신화가 완료되었습니다.')
            self.clear()

            print('뉴스 데이터 컴파일을 진행합니다. 이 작업은 완료되기까지 긴 시간이 소요됩니다. ')
            refine_data(self.HPU_dict_path, self.mecab_kodict_path, self.data_path)
            print("뉴스 데이터의 컴파일이 완료되었습니다.")
            self.claer()

            print("지표산출을 시작합니다.\n")
            calculate_index(self.data_path)
            print("지표산출이 완료되었습니다.")

            return None 

