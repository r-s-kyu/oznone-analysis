
import re
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.cm as cm
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy.util as cutil
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties

# MSゴシック（日本語フォントの導入）
fp_1 = FontProperties(fname='C:\WINDOWS\Fonts\msgothic.ttc', size = 16)

# MS明朝
fp_2 = FontProperties(fname='C:\WINDOWS\Fonts\msmincho.ttc', size = 30)

#fortranで加工したファイル
file1="ex_ozonedata_20200920.txt"

# ファイルの日付を読み取る
date_regex = re.compile(r'(\d){8}') #日付け抽出のオブジェクト作成
date_mo = date_regex.search(file1) #ファイルの名前から日にちの部分を抽出
date_str = date_mo.group()
date_num = [date_str[0:4], date_str[4:6], date_str[6:8]] # year,month,dayに分別
# date_int = list(map(int,date_num)) #整数リストにする

# ファイルの読み込み
data = np.loadtxt(file1)

# 格子点の各緯度・経度の配列作成
lon = np.array([-179.5+x  for x in range(360)])
lat = np.array([-89.5+y for y in range(180)])
    

# 欠損値処理　0→None（図を描く際にプロットしてほしくないから）
data = np.loadtxt(file1)
for j in range(len(data)) :
    for i in range(len(data[0])):
        if(data[j][i]==0):
            data[j][i]=None


# 描写の開始
fig = plt.figure(figsize=(20,10))

proj = ccrs.AzimuthalEquidistant(central_longitude=0.0, central_latitude=-90.0)
ax = fig.add_subplot(1, 2, 2, projection=proj) 
ax.set_extent([-180, 180, -90, -30],ccrs.PlateCarree()) # 描画範囲(緯度経度)の指定
# 図の周囲を円形に切る
theta = np.linspace(0, 2*np.pi, 100)
center, radius = [0.5, 0.5], 0.5
verts = np.vstack([np.sin(theta), np.cos(theta)]).T
circle = mpath.Path(verts * radius + center)
ax.set_boundary(circle, transform=ax.transAxes)
# cyclicな点を追加する
cyclic_data, cyclic_lon = cutil.add_cyclic_point(data, coord=lon)

# 描写
CF = ax.contourf(cyclic_lon,lat,cyclic_data, transform=ccrs.PlateCarree(),
                clip_path=(circle, ax.transAxes) ) # clip_pathを指定して円形にする

# カラーバーの作成
plt.colorbar(CF, orientation="horizontal")
ax.coastlines()
ax.set_title(date_num[0] + "年" + date_num[1] + "月" + date_num[2] + "日 南極上空のオゾン分布", fontproperties = fp_1)
plt.show()