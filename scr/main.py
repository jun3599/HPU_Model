from HPU_model import * 

if __name__ == "__main__":
    data_path = 'D:/users/Desktop/Junhwi/국토연구원/HPU_Model/data'
    HPU_dict_path = 'D:/users/Desktop/Junhwi/국토연구원/HPU_Model/HPU_dict.xlsx'
    mecab_path = "C:/mecab"
    sheet_name = 'HPU1'

    HPU_model(data_path=data_path, HPU_dict_path=HPU_dict_path, mecab_path=mecab_path, sheet_name=sheet_name)