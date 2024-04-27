import requests
# response = requests.get('http://127.0.0.1:8000/')
# print(response.text)
import pandas as pd
import geopandas as gpd
from shapely import wkt
import folium
import random
raw_data = pd.read_csv('./data/trim.csv')

def random_color():
    # 生成随机颜色
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())

def generate_map_file(id):
    # row
    tmp = df.loc[df['class']==id]
    print(tmp)
    # query
    # print("query")
    tmp1 = tmp.loc[tmp['index'].str.endswith("query")]
    print(tmp1)
    # detour
    tmp2 = tmp.loc[tmp['index'].str.endswith("detour")]
    print(tmp2)
    # -query-
    tmp3 = tmp.loc[tmp['index'].str.contains("-query-")]
    print(tmp3)
    # -detour-
    tmp4 = tmp.loc[tmp['index'].str.contains("-detour-")]
    print(tmp4)

def generate_map_file2(id):
    tmp = df.loc[df['class']==id]
    tmp2 = tmp.loc[tmp['index'].str.endswith("query")].copy()
    # print(tmp2)
    # print(tmp2['wkt'][0])
    tmp2['geometry'] = tmp2['wkt'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(tmp2, geometry='geometry')
    tiles = "https://server.arcgisonline.com/arcgis/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}"
    m = folium.Map(tiles=tiles, attr='a',location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()])
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
    m.save('map_{}_{}.html'.format("query",id))


def generate_topk(id):
    tmp = raw_data.loc[raw_data['class']==int(id)]
    tmp2 = tmp.loc[tmp['index'].str.contains("-query-")].copy()
    tmp2['geometry'] = tmp2['wkt'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(tmp2, geometry='geometry')
    tiles = "https://server.arcgisonline.com/arcgis/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}"
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
            m1.save('./topk/map_{}_{}_{}.html'.format("topk",id,cnt))
            
            cnt+=1
        # break
    # # 根据点的坐标计算边界
    # bounds = m.get_bounds()
    # # 调整地图的视图以适应所有标记
    # m.fit_bounds(bounds)
    # # 显示地图
    # m.save('./topk/map_{}_{}.html'.format("topk",id))

    # seperate topk
    # './topk/map_{}_{}_{}.html'.format("topk",id,id)

    
    return "OK"

def generate_pre100:
    