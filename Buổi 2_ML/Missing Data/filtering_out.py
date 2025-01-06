
from numpy import nan as NA
import pandas as pd

data = pd.DataFrame([[1., 6.5, 3.],
                     [1., NA, NA],
                     [NA, NA, NA],
                     [NA, 6.5, 3.]])
print(data)
print("-"*10)

#Drop các dòng có chứa ít nhất 1 NaN
cleaned = data.dropna()
print(cleaned)
print("-"*10)

#Drop dòng có tất cả record = NaN
cleaned2=data.dropna(how='all')
print(cleaned2)
print("-"*10)

#Drop các dòng có chứa NaN
cleaned3=data.dropna(how='any')
print(cleaned3)
print("-"*10)

