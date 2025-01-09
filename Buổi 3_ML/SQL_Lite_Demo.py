import sqlite3
import pandas as pd

try:
    # Kết nối đến cơ sở dữ liệu SQLite
    sqlite_connection = sqlite3.connect("../database/Chinook_Sqlite.sqlite")
    print('Kết nối CSDL thành công!')

    # Tạo con trỏ để thao tác với CSDL
    cursor = sqlite_connection.cursor()

    # Viết và thực thi câu lệnh SQL
    query = 'SELECT * FROM InvoiceLine LIMIT 5;'
    cursor.execute(query)

    # Chuyển kết quả truy vấn thành DataFrame và in ra
    df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
    print(df)

    # Đóng con trỏ
    cursor.close()

except sqlite3.Error as error:
    # Xử lý lỗi nếu xảy ra
    print('Đã xảy ra lỗi: ', error)

finally:
    # Đóng kết nối đến CSDL dù có lỗi hay không
    if sqlite_connection:
        sqlite_connection.close()
        print('Đã đóng kết nối CSDL SQLite.')
