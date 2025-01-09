import sqlite3
import pandas as pd


def get_customers_with_invoices(database_path, min_invoices):
    try:
        # Kết nối đến cơ sở dữ liệu
        sqlite_connection = sqlite3.connect(database_path)
        print("Kết nối CSDL thành công!")

        # Truy vấn dữ liệu
        query = f"""
        SELECT Customer.CustomerId, Customer.FirstName, Customer.LastName, COUNT(Invoice.InvoiceId) AS InvoiceCount
        FROM Customer
        JOIN Invoice ON Customer.CustomerId = Invoice.CustomerId
        GROUP BY Customer.CustomerId, Customer.FirstName, Customer.LastName
        HAVING InvoiceCount >= {min_invoices};
        """

        # Chuyển đổi kết quả truy vấn thành DataFrame
        df = pd.read_sql_query(query, sqlite_connection)

        # Đóng kết nối
        sqlite_connection.close()
        print("Đã đóng kết nối CSDL.")

        return df

    except sqlite3.Error as error:
        print("Đã xảy ra lỗi: ", error)
        return None
result = get_customers_with_invoices("../database/Chinook_Sqlite.sqlite",7)
print(result)