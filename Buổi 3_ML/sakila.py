from email.utils import decode_rfc2231

from flask import Flask
from flaskext.mysql import MySQL
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans
import numpy as np
app = Flask(__name__)


def getConnect(server, port, database, username, password):
    try:
        mysql = MySQL()
        # MySQL configurations
        app.config['MYSQL_DATABASE_HOST'] = server
        app.config['MYSQL_DATABASE_PORT'] = port
        app.config['MYSQL_DATABASE_DB'] = database
        app.config['MYSQL_DATABASE_USER'] = username
        app.config['MYSQL_DATABASE_PASSWORD'] = password
        mysql.init_app(app)
        conn = mysql.connect()
        return conn
    except mysql.connector.Error as e:
        print("Error = ", e)
    return None

def closeConnection(conn):
    if conn is not None:
        conn.close()
def queryDataset(conn, sql):
    cursor = conn.cursor()

    cursor.execute(sql)
    df = pd.DataFrame(cursor.fetchall())

    return df
conn = getConnect('localhost', 3306, 'sakila', 'root', '@Obama123')

sql = """
SELECT c.customer_id, COUNT(r.rental_id) AS total_rentals, 
       COUNT(DISTINCT i.film_id) AS unique_films
FROM customer c
JOIN rental r ON c.customer_id = r.customer_id
JOIN inventory i ON r.inventory_id = i.inventory_id
GROUP BY c.customer_id;
"""

df1 = queryDataset(conn, sql)

print(df1)

print(df1.columns)

# Vẽ biểu đồ histogram phân phối dữ liệu
def showHistogram(df1, columns):
    plt.figure(figsize=(8,6))
    for column in columns:
        sns.histplot(df1[column], bins=20, kde=True)
        plt.title(f'Distribution of {column}')
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.show()

showHistogram(df1, ['total_rentals', 'unique_films'])

# Áp dụng KMeans để phân cụm
def elbowMethod(df1, columns):
    X = df1[columns].values
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

elbowMethod(df1, ['total_rentals', 'unique_films'])

# Chọn số cụm tối ưu (giả sử chọn k=4)
def runKMeans(df1, columns, clusters=4):
    X = df1[columns].values
    model = KMeans(n_clusters=clusters, init='k-means++', max_iter=500, random_state=42)
    df1['cluster'] = model.fit_predict(X)
    return df1, model.cluster_centers_

df, centroids = runKMeans(df1, ['total_rentals', 'unique_films'], clusters=4)

# Hiển thị kết quả phân cụm
def visualizeKMeans(df1, columns):
    plt.figure(figsize=(10,6))
    sns.scatterplot(x=df1[columns[0]], y=df1[columns[1]], hue=df1['cluster'], palette='tab10', s=100)
    plt.xlabel(columns[0])
    plt.ylabel(columns[1])
    plt.title("Customer Clusters Based on Film Interest")
    plt.legend(title="Cluster")
    plt.show()

visualizeKMeans(df1, ['total_rentals', 'unique_films'])

# Hiển thị 3D Plot
def visualize3DKmeans(df1, columns):
    fig = px.scatter_3d(df1, x=columns[0], y=columns[1], z=columns[2], color=df1['cluster'].astype(str),
                         title="3D Clustering of Customers", hover_data=['customer_id'])
    fig.show()

visualize3DKmeans(df1, ['total_rentals', 'unique_films', 'cluster'])

# Đóng kết nối MySQL
closeConnection(conn)



