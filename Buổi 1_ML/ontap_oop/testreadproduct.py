from K224161812.ontap_oop.FileFactory import FileFactory
from K224161812.ontap_oop.product import Product
ff=FileFactory()
dataset=ff.readData("mydataset.json",Product)
print("Danh sách sản phẩm:")
for product in dataset:
    print(product)