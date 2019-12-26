# 凸包的二维／三维可视化

import numpy as np
# import pylab as pl
from scipy import spatial
# from scipy.spatial import Delaunay
import math
from math import atan2, degrees
import matplotlib.pyplot as pl



# 计算方位角函数
def AngleBtw2Points(pointA, pointB):
    changeInX = pointB[0] - pointA[0]
    changeInY = pointB[1] - pointA[1]
    if degrees(atan2(changeInY, changeInX)) < 0:
        return 180 + degrees(atan2(changeInY, changeInX))
    elif degrees(atan2(changeInY, changeInX)) == 180.0:
        return 180.0 - degrees(atan2(changeInY, changeInX))
    else:
        return degrees(atan2(changeInY, changeInX))


# 返回所有的顶点
def vertices_points(vertices, points2d):
    vertices_points = []
    for i in vertices:
        vertices_points.append(points2d[i].tolist())
    return vertices_points


# return all inner_points
def inner_points(vertices_points, points2d):
    list = points2d.tolist()
    for i in vertices_points:
        if i in points2d:
            list.remove(i)
    return list


# 返回余弦定理求出角度
def angles(x1, y1, x2, y2, x3, y3, z):
    # x1,y1,x2,y2,x3,y3=1,1,6.5,1,6.5,2.5
    # #计算三条边长
    a = math.sqrt((x2 - x3) * (x2 - x3) + (y2 - y3) * (y2 - y3))
    b = math.sqrt((x1 - x3) * (x1 - x3) + (y1 - y3) * (y1 - y3))
    c = math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
    # 利用余弦定理计算三个角的角度
    B = math.degrees(math.acos((b * b - a * a - c * c) / (-2 * a * c)))
    # 输出三个角的角度
    if z == 'v_angle':
        return 180 - round(B, 2)
    elif z == "inner_angle":
        return round(B, 2)


# 形成夹角的两边比例
def side_ratio(x1, y1, x2, y2, x3, y3):
    # #计算三条边长
    a = math.sqrt((x2 - x3) * (x2 - x3) + (y2 - y3) * (y2 - y3))
    c = math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
    return a / c


## 所有的内角，并且排序
def inner_angles(inner_points, vertices_points):
    all_inner_angles = {}
    for i in range(len(inner_points)):
        for j in range(len(vertices_points)):
            if j + 1 < len(vertices_points) - 1:
                x1 = vertices_points[j][0]
                y1 = vertices_points[j][1]
                x2 = inner_points[i][0]
                y2 = inner_points[i][1]
                x3 = vertices_points[j + 1][0]
                y3 = vertices_points[j + 1][1]
                angle = np.float32(angles(x1, y1, x2, y2, x3, y3, 'inner_angle'))
                len_rio = side_ratio(x1, y1, x2, y2, x3, y3)
                all_inner_angles[x1, y1, x2, y2, x3, y3] = [angle, len_rio]
    list1 = sorted(all_inner_angles.items(), key=lambda x: x[0])
    return list1


def vertices_angles(vertices_points):
    new_vertices_points = vertices_points
    new_vertices_points.append(vertices_points[0])
    new_vertices_points.append(vertices_points[1])
    all_vertices_angles = {}
    for i in range(len(new_vertices_points)):
        if i + 2 < len(new_vertices_points):
            x1 = new_vertices_points[i][0]
            y1 = new_vertices_points[i][1]
            x2 = new_vertices_points[i + 1][0]
            y2 = new_vertices_points[i + 1][1]
            x3 = new_vertices_points[i + 2][0]
            y3 = new_vertices_points[i + 2][1]
            angle = np.float32(angles(x1, y1, x2, y2, x3, y3, z='v_angle'))
            len_rio = side_ratio(x1, y1, x2, y2, x3, y3)
            all_vertices_angles[angle] = [[x1, y1], [x2, y2], [x3, y3], len_rio]
    # 对字典按照key排序
    list1 = sorted(all_vertices_angles.items(), key=lambda x: x[0])
    return list1


def vertices_triangls(all_vertices_points):
    new_all_vertices_points = all_vertices_points[0:-2]
    vertices_triangl = {}
    p_len = len(new_all_vertices_points)
    for i in range(p_len):
        # 把i前面的数据放到后面
        p1 = new_all_vertices_points.copy()
        if i < p_len:
            k = i + 1
            while k > 0:
                point = p1[0]
                p1.remove(point)
                p1.append(point)
                k = k - 1
        # 删除最后一个跟起点相同的数据
        p1.pop()
        for j in range(len(p1) - 1):
            v_ratio = []
            z = j + 1
            x1 = p1[j][0]
            y1 = p1[j][1]
            x2 = new_all_vertices_points[i][0]
            y2 = new_all_vertices_points[i][1]
            x3 = p1[z][0]
            y3 = p1[z][1]
            angle = angles(x1, y1, x2, y2, x3, y3, z='v_angle')
            len_rio = side_ratio(x1, y1, x2, y2, x3, y3)
            v_ratio.append([angle, len_rio])
            vertices_triangl[x1, y1, x2, y2, x3, y3] = v_ratio
    return vertices_triangl


# 返回内部角度，和顶点角度，和画出图形
def return_angles(points1, pic_id):
    ##str转化为int
    points = []
    for i in points1:
        i = list(map(int, i))
        points.append(i)
    points2d = np.array(points)

    if len(points2d) > 2:
        ch2d = spatial.ConvexHull(points2d)  # 上述点的对象

        vertices = list(ch2d.vertices)
        # 删除非顶点的点
        for i in range(0, len(ch2d.simplices)):
            if i + 1 < len(ch2d.simplices) and ch2d.simplices[i][0] == ch2d.simplices[i + 1][0]:
                x1 = points2d[ch2d.simplices[i][0]][0]
                x1_1 = points2d[ch2d.simplices[i + 1][0]][0]
                y1 = points2d[ch2d.simplices[i][0]][1]
                y1_1 = points2d[ch2d.simplices[i + 1][0]][1]
                x2 = points2d[ch2d.simplices[i][1]][0]
                x2_2 = points2d[ch2d.simplices[i + 1][1]][0]
                y2 = points2d[ch2d.simplices[i][1]][1]
                y2_2 = points2d[ch2d.simplices[i + 1][1]][1]
                angle_1 = AngleBtw2Points([x1, y1], [x2, y2])
                angle_2 = AngleBtw2Points([x1_1, y1_1], [x2_2, y2_2])
                if abs(angle_1 - angle_2) < 2:
                    vertices.remove(ch2d.simplices[i][0])
        all_vertices_points = vertices_points(vertices, points2d)
        all_inner_points = inner_points(all_vertices_points, points2d)


        all_vertices_angles = vertices_angles(all_vertices_points)
        all_inner_angles = inner_angles(all_inner_points, all_vertices_points)

        # poly = pl.Polygon(points2d[ch2d.vertices], fill=None, lw=2, color='r', alpha=0.9)
        # ax = pl.subplot(aspect='equal')
        # pl.plot(points2d[:, 0], points2d[:, 1], 'go')
        # pl.title(pic_id)
        #
        # for i, pos in enumerate(points2d):
        #     pl.text(pos[0], pos[1], str(i), color='blue')
        #     ax.add_artist(poly)
        # pl.show()
        # pl.savefig('%s.png' % pic_id)
        # pl.close()
        # pl.savefig('%s.png'%pic_id)
        # pl.show()
        # 返回顶点夹角，返回内角
        return all_vertices_angles, all_inner_angles, all_vertices_points, all_inner_points
    else:
        return 'n_points<3'


def return_same_v_points(vertices_triangls_dict, same_vertices_triangl, inner_points):
    same_points = []
    for i in same_vertices_triangl:
        pointsList = list(list(vertices_triangls_dict.keys())[list(vertices_triangls_dict.values()).index(i)])
        # 还要判断此点是否是原图中的内点
        if pointsList[:2] not in same_points and pointsList[:2] not in inner_points:
            same_points.append(pointsList[:2])
        if pointsList[2:4] not in same_points and pointsList[2:4] not in inner_points:
            same_points.append(pointsList[2:4])
        if pointsList[4:] not in same_points and pointsList[4:] not in inner_points:
            same_points.append(pointsList[4:])
    return same_points


def get_key(dict, value):
    return [k for k, v in dict.items() if v == value]


"比较颜色，需要调用非缺失的点的坐标，这里函数返回的就是 ori，cur相同顶角的点的坐标"


def return_same_points(points):
    point = []
    for i in points:
        if list(i[0][0:2]) not in point:
            point.append(list(i[0][0:2]))
        if list(i[0][2:4]) not in point:
            point.append(list(i[0][2:4]))
        if list(i[0][4:]) not in point:
            point.append(list(i[0][4:]))
    return point


"当相同的顶点数为2时候，可以使用顶点与内点的夹角去做对比。这种情况比较特殊，可以使用以函数"


def v_inner_angles(v_points, inner_points):
    coor_angle_ratio = []
    v_len = len(v_points)
    inner_len = len(inner_points)
    for i in range(v_len):
        if i + 1 < v_len:
            for j in range(inner_len):
                x1 = v_points[i][0]
                y1 = v_points[i][1]
                x2 = inner_points[j][0]
                y2 = inner_points[j][1]
                x3 = v_points[i + 1][0]
                y3 = v_points[i + 1][1]
                angle = angles(x1, y1, x2, y2, x3, y3, 'inner_angle')
                len_rio = side_ratio(x1, y1, x2, y2, x3, y3)
                coor_angle_ratio.append([[x1, y1, x2, y2, x3, y3], [angle, len_rio]])

    return coor_angle_ratio


"判断ori_pic的顶点是否是cur_pic中内部点"

def compare_oriV_is_curIn(v_point, cur_inner_points):
    flag = 0
    for i in cur_inner_points:
        if abs(i[0] - v_point[0]) < 10 and abs(i[1] - v_point[1]) < 10:
            flag = 1
    return flag

# 比较夹角,比较角度，比较组成角度的两条直线的长度,返回缺失的点,输入数据为return_angles的返回值的第一个list（顶点的角度）
def compare_v_angles(ori_pic, cur_pic):
    print('开始比对=====================================================================================================')
    dis_same_v_points = []
    ori_vertices_triangls_dict = vertices_triangls(ori_pic[2])
    cur_vertices_triangls_dict = vertices_triangls(cur_pic[2])
    cur_vertices_triangl = []
    ori_vertices_triangl = []
    ori_points = []
    cur_points = []
    # 比较角度和边长比例，来判断相同的顶点
    for i in cur_vertices_triangls_dict.values():
        for j in ori_vertices_triangls_dict.values():
            if abs(i[0][0] - j[0][0]) < 0.5 and abs(i[0][1] - j[0][1]) < 0.1 and \
                    abs(get_key(cur_vertices_triangls_dict, i)[0][2] - get_key(ori_vertices_triangls_dict, j)[0][
                        2]) < 20 \
                    and abs(
                get_key(cur_vertices_triangls_dict, i)[0][3] - get_key(ori_vertices_triangls_dict, j)[0][3]) < 20 \
                    and abs(
                get_key(cur_vertices_triangls_dict, i)[0][5] - get_key(ori_vertices_triangls_dict, j)[0][5]) < 20 :
                # 返回在基准图中与cur图的相同点的角度与边长比例 [angle, ratio]
                ori_vertices_triangl.append(j.copy())
                cur_vertices_triangl.append(i.copy())
                ori_points.append(get_key(ori_vertices_triangls_dict, j))
                cur_points.append(get_key(cur_vertices_triangls_dict, i))

    "返回相同顶角的点的坐标，当比较颜色的时候需要调用"
    points_in_ori = return_same_points(ori_points)
    points_in_cur = return_same_points(cur_points)

    ori_same_v_points = []
    cur_same_v_points = []
    if len(ori_points) != 0:
        # 返回相同的顶点与另外两个顶点之间夹角，边长比例，顶点坐标，目的是为了比较inner_points

        if len(ori_vertices_triangl) > 0:
            ori_same_v_points = list(list(ori_vertices_triangls_dict.keys())[
                                         list(ori_vertices_triangls_dict.values()).index(ori_vertices_triangl[0])])
            cur_same_v_points = list(list(cur_vertices_triangls_dict.keys())[
                                         list(cur_vertices_triangls_dict.values()).index(cur_vertices_triangl[0])])
            # 根据比较得到的顶点的角度与长度的对比都相似的。返回在ori中的没有变化的坐标
            ori_inner_points = ori_pic[3]
            cur_inner_points = cur_pic[3]


            same_points_in_ori = return_same_v_points(ori_vertices_triangls_dict, ori_vertices_triangl,
                                                      ori_inner_points)
            # 如果新图中的顶点为原图中的内点，也必须剔除。

            for j in ori_pic[2]:
                if j not in same_points_in_ori and j not in dis_same_v_points:
                    if compare_oriV_is_curIn(j,cur_inner_points) == 0:
                           dis_same_v_points.append(j)
            print('消失的顶点坐标', dis_same_v_points)
            # 当多边形的边的数量不同时候，返回缺失点的坐标
            if len(dis_same_v_points) == 0:  # 有两种情况，1：想同的顶点形成不了三角形，返回全部顶点坐标。 2：顶点全部相同
                return 'same_vertices', ori_same_v_points, cur_same_v_points, points_in_cur
            else:
                if len(ori_same_v_points) != 0 and len(cur_same_v_points) != 0:
                    return dis_same_v_points, ori_same_v_points, cur_same_v_points, points_in_cur
        else:
            return 'no points find'
    else:
        ori_v_points = ori_pic[2][:-1]
        ori_in_points = ori_pic[3]
        cur_v_points = cur_pic[2][:-1]
        cur_in_points = cur_pic[3]
        ori_v_inner_angles = v_inner_angles(ori_v_points, ori_in_points)
        cur_v_inner_angles = v_inner_angles(cur_v_points, cur_in_points)
        for i in cur_v_inner_angles:
            for j in ori_v_inner_angles:
                if abs(i[1][0] - j[1][0]) < 1 and abs(i[1][1] - j[1][1]) < 0.01:
                    "说明顶点和内点组成的角度相同，然后取出两个顶点，即为相同的顶点"
                    ori_same_v_points = (j[0])
                    cur_same_v_points = (i[0])
        ver = [ori_same_v_points[:2], ori_same_v_points[-2:]]
        for i in ori_pic[2][:-2]:
            if i not in ver:
                dis_same_v_points.append(i)
        return dis_same_v_points, ori_same_v_points, cur_same_v_points, points_in_cur


'cur 图片顶点与顶点之间的角度'


def vertices_vertices_angles(v_points, inner_points):
    all_angles = {}
    for i in inner_points:
        x1 = v_points[0][0]
        y1 = v_points[0][1]
        x2 = i[0]
        y2 = i[1]
        x3 = v_points[1][0]
        y3 = v_points[1][1]
        angle = np.float32(angles(x1, y1, x2, y2, x3, y3, 'inner_angle'))
        len_rio = side_ratio(x1, y1, x2, y2, x3, y3)
        all_angles[x1, y1, x2, y2, x3, y3] = [angle, len_rio]
    return all_angles


# 当多边形顶点完全相同时候，比较内部角度  ([ori[顶点1，顶点2],current[顶点1，顶点2],ori_all_inner_angles,cur_all_inner_angles ])
# 在ori和cur中取出两个相同的顶点，分别取出inner点与这两个点形成的角度，边长比例，如果不相同，此inner点的坐标
def compare_inner_angles(ori_cur_v, ori_all_inner_angles, cur_all_inner_angles):
    if ori_cur_v != 'no points find' and len(ori_cur_v[1]) != 0 and len(ori_cur_v[3]) != 0:
        ori_same_v_points = ori_cur_v[1]
        cur_same_v_points = ori_cur_v[2]

        # 除去两个基准点的剩下的顶点,是当前测 试的图
        "[ori_cur_v[2]= cur_same_v_points 为当前图与ori图顶点相同的点的坐标"
        ver = [ori_cur_v[2][:2], ori_cur_v[2][-2:]]
        'return all_vertices_angles, all_inner_angles, all_vertices_points, all_inner_points'
        cur_angles_remove = ori_cur_v[3].copy()

        '这里的cur_v_points为（当前图的所有顶点-比较后相同的顶点）,剩下的顶点在原图中为inner_point'
        cur_v_points = cur_all_inner_angles[2][:-2].copy()
        for i in ori_cur_v[3]:
            if i in cur_v_points:
                cur_v_points.remove(i)
        'cur_angles_remove 当前图移除去当作基准点两点的坐标，剩下的顶点的坐标'
        'all_angles 是返回 基准点与其它顶点组成的角度'
        all_angles = vertices_vertices_angles(ver, cur_v_points)
        cur_list = []
        ori_list = []
        # 当失去顶点，inner_point变成顶点，这里的cur_all_inner_angles就会少
        for i in cur_all_inner_angles[1]:
            if cur_same_v_points[:2] == list(i[0][0:2]) and cur_same_v_points[-2:] == list(i[0][-2:]):
                cur_list.append(i)
        for k in all_angles:
            cur_list.append((k, all_angles[k]))

        for z in ori_all_inner_angles[1]:
            if ori_same_v_points[:2] == list(z[0][0:2]) and ori_same_v_points[-2:] == list(z[0][-2:]):
                ori_list.append(z)

        cur_same_inner_points = []
        ori_same_inner_points = []
        ori_list_copy = ori_list.copy()
        dis_points = []
        for i in cur_list:
            for k in ori_list:
                'i[1][0] - k[1][0]) < 0.5 比较的是角度，i[1][1] - k[1][1]) < 0.1 比较的是边长比例，' \
                'abs(i[0][2] - k[0][2]) < 50 比较的是点坐标差值'
                if abs(i[1][0] - k[1][0]) < 2 and abs(i[1][1] - k[1][1]) < 0.1 and abs(i[0][2] - k[0][2]) < 20:
                    ori_same_inner_points.append([k[0]])
                    cur_same_inner_points.append([i[0]])
                    if k in ori_list_copy:
                        ori_list_copy.remove(k)
        "返回相同顶角的点的坐标，当比较颜色的时候需要调用"
        same_ori_points = return_same_points(ori_same_inner_points)
        same_cur_points = return_same_points(cur_same_inner_points)
        for j in ori_list_copy:
            point = list(j[0][2:4])
            dis_points.append(point)

        print('消失的inner_points ', dis_points)
        if ori_cur_v[0] == 'same_vertices':
            return dis_points
        else:
            return ori_cur_v[0] + dis_points
    elif ori_cur_v != 'no points find' and len(ori_cur_v[1]) != 0:
        return ori_cur_v[0]
    else:
        return 'no points find'

