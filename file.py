import pandas as pd

df = pd.read_excel('res/MeteoSt-RAD.xls')
print(df)

print ('/////////////')

print df.get_values()[3]
