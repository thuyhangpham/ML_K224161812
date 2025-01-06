
from numpy import nan as NA
import pandas as pd

data = pd.DataFrame([[1., 6.5, 3.],
                  	[1., NA, NA],
                  	[NA, NA, NA],
                  	[NA, 6.5, 3.]])
print(data)
print("-"*10)

#Fill NA value with mean of each row
cleaned_mean=data.fillna(data.mean())
print(cleaned_mean)
print("-"*10)

#Fill NA value with median of each row
cleaned_median=data.fillna(data.median())
print(cleaned_median)
print("-"*10)

#Fill NA value with mode of each row
cleaned_mode=data.fillna(data.mode().iloc[0])
print(cleaned_mode)
print("-"*10)