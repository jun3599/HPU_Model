# import os 
# from datetime import datetime 
# import re 
# import shutil



# origine = 'D:/Users/wnsgnl/Desktop/paper_master2/analysis/data/raw'
# to = 'G:/내 드라이브/국토연구원/뉴스결과물'


# for fold in os.listdir(origine):
#     for file in os.listdir(f'{origine}/{fold}'):
#         shutil.copy(f'{origine}/{fold}/{file}', f'{to}/{file}')


# origine = 'D:/Users/wnsgnl/Desktop/뉴스데이터'
# to = 'D:/Users/wnsgnl/Desktop/paper_master2/analysis/data/raw'


# for csv_file in os.listdir(origine): 
#     date = csv_file.split('_')[1]
#     date = datetime.strptime(date,'%Y%m%d')
#     date = date.strftime('%Y%m')

#     to_sub = f'{to}/{date}'
#     shutil.move(f'{origine}/{csv_file}', f'{to_sub}/{csv_file}')


    
