from K224161812.ontap_oop.FileFactory import FileFactory
from K224161812.ontap_oop.product import Product

# Đọc dữ liệu
ff = FileFactory()
dataset = ff.readData("mydataset.json", Product)

# 1. Lọc các sản phẩm có giá từ a tới b
def filter_products_by_price(dataset, a, b):
    return [product for product in dataset if a <= product.price <= b]

# Sử dụng hàm lọc
a = float(input("Nhập giá tối thiểu: "))
b = float(input("Nhập giá tối đa: "))
filtered_products = filter_products_by_price(dataset, a, b)

print(f"Danh sách sản phẩm có giá từ {a} tới {b}:")
if filtered_products:
    for product in filtered_products:
        print(product)
else:
    print("Không có sản phẩm nào trong khoảng giá này.")

# 2. Xoá tất cả các sản phẩm có giá nhỏ hơn x
def remove_products_below_price(dataset, x):
    return [product for product in dataset if product.price >= x]

# Sử dụng hàm xóa
x = float(input("Nhập giá tối thiểu để giữ lại sản phẩm: "))
dataset = remove_products_below_price(dataset, x)

print(f"Danh sách sản phẩm sau khi xóa các sản phẩm có giá nhỏ hơn {x}:")
if dataset:
    for product in dataset:
        print(product)
else:
    print("Không còn sản phẩm nào trong danh sách.")