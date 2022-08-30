from edit_user_dict import * 
from konlpy.tag import Mecab

test_sentence = '부동산 가격의 안정화를 위해 금융 통화 위원회가 규제 손보기에 나섰다.'
mecab_path = 'C:/mecab'
mecab_dict_path = 'C:/mecab/mecab-ko-dic'
HPU_dict_path= 'D:/users/Desktop/Junhwi/국토연구원/HPU_Model/HPU_dict.xlsx'

tokenizer = Mecab(mecab_dict_path)

result = tokenizer.morphs(test_sentence)
print(result)
del tokenizer 
del Mecab 

compile_user_dict = compile_user_dict(HPU_dict_path= HPU_dict_path, mecab_path=mecab_path)
compile_user_dict.manager()

from konlpy.tag import Mecab
tokenizer = Mecab(mecab_dict_path)

result = tokenizer.morphs(test_sentence)
print(result)
