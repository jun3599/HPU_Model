import pandas as pd 
import ast 
from tqdm import tqdm 
import os 

def write_word_group_TF(df, freq = 1):
        '''
        find_group_of_word 함수를 통해 생성된 열들을 기반으로 
        단어의 출현 여부를 확인해 T/F 값을 기입합니다. 
        '''
        def confirm_TF(word_list, min_freq):
            word_list = ast.literal_eval(str(word_list))
            if len(word_list) == 0:
                return 'F' 
            elif len(word_list) >= min_freq:
                return 'T'
            else:
                return 'F'
        df['pre_H_TF'] = df['H_word'].apply(lambda x: confirm_TF(x, 1))
        df['H_TF'] = df['H_word'].apply(lambda x: confirm_TF(x, 2))
        # df['P_TF'] = df['P_word'].apply(lambda x: confirm_TF(x,1))
        # df['U-A_TF'] = df['U-A_word'].apply(lambda x: confirm_TF(x,1))
        # df['U-R_TF'] = df['U-R_word'].apply(lambda x: confirm_TF(x,1))

        return df

def grouping_article(df):
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
    df['pre_HPU_A_TF'] = df.apply(lambda x: confirm_HPU_A_TF(x['pre_H_TF'],x['P_TF'],x['U-A_TF']), axis =1)
    df['HPU_R_TF'] = df.apply(lambda x: confirm_HPU_R_TF(x['H_TF'],x['P_TF'],x['U-R_TF']), axis =1)
    df['pre_HPU_R_TF'] = df.apply(lambda x: confirm_HPU_R_TF(x['pre_H_TF'],x['P_TF'],x['U-R_TF']), axis =1)
    
    return df 

path = "D:/users/Desktop/compiled_2"
for file in tqdm(os.listdir(path)):
    file_path = f'{path}/{file}'
    data = pd.read_csv(file_path)

    data = write_word_group_TF(data)
    data =grouping_article(data)

    data.to_csv(file_path, index=False, encoding='utf-8-sig')

    del data 