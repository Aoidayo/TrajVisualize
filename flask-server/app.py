from flask import Flask,send_file
from flask_cors import CORS
import pandas as pd
import geopandas as gpd
from shapely import wkt
import random
import folium
import os
import time

app = Flask(__name__)
CORS(app,origins='http://localhost')

# 读取 CSV 文件
# 换成pre100.csv
raw_data = pd.read_csv('./data/913155_qgis_res_LinearSim_porto_256_knn.csv')


def random_color():
    # 生成随机颜色
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())

@app.route("/queryMap/<id>")
def generate_map_file(id):
    if os.path.exists('./query/map_{}_{}.html'.format("query",id)):
        return "OK"
    # raw_data = pd.read_csv('./data/913155_qgis_res_LinearSim_porto_256_knn.csv')
    # print(raw_data[:10])
    tmp = raw_data.loc[raw_data['class']==int(id)]
    print(tmp)
    tmp2 = tmp.loc[tmp['index'].str.endswith("query")].copy()
    print(tmp2)
    # print(tmp2['wkt'][0])
    tmp2['geometry'] = tmp2['wkt'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(tmp2, geometry='geometry')
    tiles = "https://server.arcgisonline.com/arcgis/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}"
    m = folium.Map(tiles=tiles, attr=id,location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()])
    # 为每个 LineString 添加一条线
    for _, row in gdf.iterrows():
        # 确保几何类型是 LineString
        if row.geometry.geom_type == 'LineString':
            # 创建 LineString 的坐标列表
            line_coords = [(point[1], point[0]) for point in row.geometry.coords]
            # 添加线到地图
            folium.PolyLine(line_coords, color=random_color(), weight=5, opacity=0.8).add_to(m)
        # break
    # 根据点的坐标计算边界
    bounds = m.get_bounds()

    # 调整地图的视图以适应所有标记
    m.fit_bounds(bounds)

    # 显示地图
    m.save('./query/map_{}_{}.html'.format("query",id))
    return "OK"

@app.route("/mapGenQuery/<id>")
def mapGenReturn(id):
    return send_file('./query/map_{}_{}.html'.format("query",id))


@app.route('/')
def hello():
    return 'Hello, this is a string from Flask!'

@app.route('/image')
def get_image():
    # 指定图片的路径
    image_path = 'imgs/image.png'
    # 返回图片
    return send_file(image_path, mimetype='image/png')

@app.route("/map")
def map():
    return send_file('./map.html')

@app.route('/user/<username>')
def show_user_profile(username):
    # 根据接收到的用户名执行相应的操作
    return 'User {}'.format(username)

# @app.route('/originTrajOnMap/<id>')
# def show_user_profile(id):
#     # 根据id生成

@app.route("/queries")
def get_queries():
    df = pd.read_csv("./data/unique_classes.csv")
    # return df['class']
    l1 = df['class'].tolist()
    print(l1)
    return l1[:100]

@app.route("/topk/<id>")
def generate_topk(id):
    time.sleep(2.0)
    tmp = raw_data.loc[raw_data['class']==int(id)]
    tmp2 = tmp.loc[tmp['index'].str.contains("-query-")].copy()
    tmp2['geometry'] = tmp2['wkt'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(tmp2, geometry='geometry')
    tiles = "https://server.arcgisonline.com/arcgis/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}"
    # all topk
    m = folium.Map(tiles=tiles, attr="topk_All:"+id,location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()])
    for _, row in gdf.iterrows():
        if row.geometry.geom_type == 'LineString':
            line_coords = [(point[1], point[0]) for point in row.geometry.coords]
            folium.PolyLine(line_coords, color=random_color(), weight=5, opacity=0.8).add_to(m)
    bounds = m.get_bounds()
    m.fit_bounds(bounds)
    m.save('./query/map_{}_{}.html'.format("query","all"))
    # separate topk
    cnt = 1
    for index, row in gdf.iterrows():
        print(index)
        print(row)
        m1 = folium.Map(tiles=tiles, attr=id,location=[row.geometry.centroid.y, row.geometry.centroid.x])
        if row.geometry.geom_type == 'LineString':
            # 创建 LineString 的坐标列表
            line_coords = [(point[1], point[0]) for point in row.geometry.coords]
            # 添加线到地图
            folium.PolyLine(line_coords, color=random_color(), weight=5, opacity=0.8).add_to(m1)
            bounds = m1.get_bounds()
            m1.fit_bounds(bounds)
            m1.save('./topk/map_{}_{}_{}.html'.format("topk","separate",cnt))
            cnt+=1
    # time.sleep(5)
    return "OK"

@app.route("/getTopkAll")
def getTopKAll():
    return send_file('./query/map_{}_{}.html'.format("query","all"))

@app.route("/getTopk/<cnt>")
def getTopkByCnt(cnt):
    return send_file('./topk/map_{}_{}_{}.html'.format("topk","separate",cnt))

if __name__ == '__main__':  
    app.run(debug=True,port=8000)
