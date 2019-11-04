import pandas as pd
import coreProcess

#***************************************************
# Input details:
#    1. target
#    2. csv file name
#    3. Delimiter
#**************************************************

target='G3'
dfo = pd.read_csv('students-data.csv',delimiter=";")
coreProcess.startProcess(dfo,target)

