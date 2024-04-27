import pandas as pd
import geopandas as gpd
from shapely import wkt
import folium
import random

def random_color():
    # 生成随机颜色
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())

# 读取 CSV 文件
df = pd.read_csv('./data/trim.csv')

# 将 WKT 字符串转换为几何对象
df['geometry'] = df['wkt'].apply(wkt.loads)

# 转换 DataFrame 为 GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry='geometry')

# tiles = 'https://wprd01.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=7'
tiles = "https://server.arcgisonline.com/arcgis/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}"

# 创建地图对象，中心坐标设置为 GeoDataFrame 的几何中心
m = folium.Map(tiles=tiles, attr='高德-常规图',location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()])

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
m.save('map.html')