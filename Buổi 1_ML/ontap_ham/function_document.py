def firstDegrere(a,b):
    """

    :param a: he so a
    :param b: he so b
    :return: tra ve 3 truong hop ket qua
    """
    if a==0 and b==0:
        print("Phuong trinh vo so nghiem")
    elif a==0 and b!=0:
        print("Phuong trinh vo nghiem")
    else:
        x=-b/a
        print("Nghiem cua phuong trinh= ",x)
print("Phuong trinh bac 1")
a= float(input("Nhap he so a= "))
b= float(input("Nhap he so b= "))
firstDegrere(a,b)

x=8
def increment():
    x=x+1
increment()
print(x)
