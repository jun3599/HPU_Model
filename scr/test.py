import os 
import re 

files = os.listdir(r'D:\users\Desktop\Junhwi\국토연구원\HPU_Model\data\raw\202201')
files = [x.split('_')[0].strip() for x in files]

target_press = ['서울신문','서울경제','한겨레','세계일보','머니투데이','문화일보','매일경제','국민일보','KBS','동아일보','경향신문','MBC','한국경제','SBS','YTN']

print(sorted(list(set(target_press) - set(files)), reverse=False))