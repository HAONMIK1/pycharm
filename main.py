from main2 import *
from vodeo import *
import openpyxl

# 엑셀 파일 열기
workbook = openpyxl.load_workbook('as.xlsx')

# 첫 번째 시트 선택
sheet = workbook.active


one= "lo1 (2).JPG"
go(one,sheet['W2'].value)
play_video(0,13)
