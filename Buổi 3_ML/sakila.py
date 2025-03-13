from flask import Flask
from flaskext.mysql import MySQL
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans
import numpy as np

app = Flask(__name__)

# Kết nối MySQL
def getConnect(server, port, database, username, password):
    try:
        mysql = MySQL()
        app.config['MYSQL_DATABASE_HOST'] = server
        app.config['MYSQL_DATABASE_PORT'] = port
        app.config['MYSQL_DATABASE_DB'] = database
        app.config['MYSQL_DATABASE_USER'] = username
        app.config['MYSQL_DATABASE_PASSWORD'] = password
        mysql.init_app(app)
        conn = mysql.connect()
        return conn
    except Exception as e:
        print("Error:", e)
    return None

def closeConnection(conn):
    if conn is not None:
        conn.close()

# Hàm truy vấn dữ liệu từ MySQL
def queryDataset(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
    return df

# Kết nối đến MySQL
conn = getConnect('localhost', 3306, 'sakila', 'root', '@Obama123')

# Truy vấn dữ liệu Film & Inventory
sql = """
SELECT c.customer_id, 
       COUNT(r.rental_id) AS total_rentals, 
       COUNT(DISTINCT i.film_id) AS unique_films,
       COUNT(DISTINCT r.inventory_id) AS total_inventory_rented
FROM customer c
LEFT JOIN rental r ON c.customer_id = r.customer_id
LEFT JOIN inventory i ON r.inventory_id = i.inventory_id
GROUP BY c.customer_id;
"""

df = queryDataset(conn, sql)
df.columns = ['customer_id', 'total_rentals', 'unique_films', 'total_inventory_rented']

print(df.head())  # Kiểm tra dữ liệu sau khi lấy từ MySQL
print(df.columns)  # Xem danh sách cột

# Hiển thị biểu đồ phân phối dữ liệu
def showHistogram(df, columns):
    plt.figure(figsize=(8,6))
    for column in columns:
        sns.histplot(df[column], bins=20, kde=True)
        plt.title(f'Distribution of {column}')
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.show()

showHistogram(df, ['total_rentals', 'unique_films', 'total_inventory_rented'])

# Áp dụng Elbow Method để tìm số cụm tối ưu
def elbowMethod(df, columns):
    X = df[columns].values
    inertia = []
    for n in range(1, 11):
        model = KMeans(n_clusters=n, init='k-means++', max_iter=500, random_state=42)
        model.fit(X)
        inertia.append(model.inertia_)

    plt.figure(figsize=(10,6))
    plt.plot(range(1, 11), inertia, 'o-')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Inertia')
    plt.title('Elbow Method for Optimal K')
    plt.show()

elbowMethod(df, ['total_rentals', 'unique_films', 'total_inventory_rented'])

# Chạy KMeans với số cụm tối ưu (giả sử chọn k=4)
def runKMeans(df, columns, clusters=4):
    X = df[columns].values
    model = KMeans(n_clusters=clusters, init='k-means++', max_iter=500, random_state=42)
    df['cluster'] = model.fit_predict(X)
    return df, model.cluster_centers_

df, centroids = runKMeans(df, ['total_rentals', 'unique_films', 'total_inventory_rented'], clusters=4)

# Hiển thị kết quả phân cụm 2D
def visualizeKMeans(df, columns):
    plt.figure(figsize=(10,6))
    sns.scatterplot(x=df[columns[0]], y=df[columns[1]], hue=df['cluster'], palette='tab10', s=100)
    plt.xlabel(columns[0])
    plt.ylabel(columns[1])
    plt.title("Customer Clusters Based on Film & Inventory Interest")
    plt.legend(title="Cluster")
    plt.show()

visualizeKMeans(df, ['total_rentals', 'unique_films'])

# Hiển thị biểu đồ phân cụm 3D
def visualize3DKmeans(df, columns):
    fig = px.scatter_3d(df, x=columns[0], y=columns[1], z=columns[2], color=df['cluster'].astype(str),
                         title="3D Clustering of Customers", hover_data=['customer_id'])
    fig.show()

visualize3DKmeans(df, ['total_rentals', 'unique_films', 'total_inventory_rented'])

# Đóng kết nối MySQL
closeConnection(conn)
