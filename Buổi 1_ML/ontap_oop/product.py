class Product:
    def __init__(self, id=None, name=None, price=None): #khởi tạo att trong class
        self.id=id
        self.name=name
        self.price=price
    def __str__(self):
        infor=f"{self.id}\t{self.name}\t.{self.price}"
        return infor