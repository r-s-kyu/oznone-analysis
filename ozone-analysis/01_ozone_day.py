# %%
import re
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.cm as cm
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy.util as cutil
import urllib.request
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties

# 変数に日付（文字列）を代入[月、日は0埋め]
print("input year")
year=input()
print("input month")
month=input().zfill(2)
print("input day")
day=input().zfill(2)

# Webページからファイル読み込み（ここではbytes列で読み込まれている）
file='https://ozonewatch.gsfc.nasa.gov/data/omi/Y' + year +'/L3_ozone_omi_' + year + month + day + '.txt'
print(file)

f = urllib.request.urlopen(file)         

# # # ファイルの日付を読み取る
# date_regex = re.compile(r'(\d){8}') #日付け抽出のオブジェクト作成
# date_mo = date_regex.search(file) #ファイルの名前から日にちの部分を抽出
# date_str = date_mo.group()
# date_num = [date_str[0:4], date_str[4:6], date_str[6:8]] # year,month,dayに分別

ozone_data = [[]*360]*180
int_data = [[]*360]*180

# -------各緯度のデータをline_read_processを用いて処理----------
def lat_read_process(line_inf, j, data):   
    line_inf = line_inf.replace('\n','')
    if(j<14):
        line_read_process(line_inf, data, len(line_inf))
    else:
        line_read_process(line_inf, data, len(line_inf)-15)
    return data

# ---------各行を読む関数、行の最初が0の時とそうでないときで場合分け----
def line_read_process( line, data, length):
    line_list=[line[i: i+3] for i in range(1, length, 3)]
    for j in range(int(length/3)):
        data.append(line_list[j])
    return data


for i in range(3):
    skip = f.readline().decode()  #上から3行は読み飛ばし

# 各緯度でのデータ読み込み    
for lat in range(180):
    da=[]
    for j in range(15):
        line_inf = f.readline().decode()
        lat_read_process(line_inf, j, da)
    # print(len(data[lat]))
    ozone_data[lat]=da
    int_data[lat] = list(map(float, ozone_data[lat]))

f.close()

# numpy.array型にする
data = np.array(int_data)

#データ読み取り成功
print("Ozone data is completely processed")



lon = np.array([-179.5+x  for x in range(360)])
lat = np.array([-89.5+y for y in range(180)])


#  ------------欠損値処理----------------------
for j in range(len(data)) :
    for i in range(len(data[0])):
        if(data[j][i]==0):
            data[j][i]=None


fp_1 = FontProperties(fname='C:\WINDOWS\Fonts\msgothic.ttc', size = 16) # MSゴシック
fp_2 = FontProperties(fname='C:\WINDOWS\Fonts\msmincho.ttc', size = 30) # MS明朝

# -------------描写の開始-----------------------------
fig = plt.figure(figsize=(10,5))

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
# 追加されたかどうかの確認
# print(lon)
# print(cyclic_lon)
# 
CF = ax.contourf(cyclic_lon,lat,cyclic_data, transform=ccrs.PlateCarree(),
                clip_path=(circle, ax.transAxes) ) # clip_pathを指定して円形にする
#
plt.colorbar(CF, orientation="horizontal")
ax.coastlines()
ax.set_title( year + "年" + month + "月" + day + "日", fontproperties = fp_1)
plt.show()



