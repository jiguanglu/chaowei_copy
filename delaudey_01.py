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
    # A = math.degrees(math.acos((a * a - b * b - c * c) / (-2 * b * c)))
    B = math.degrees(math.acos((b * b - a * a - c * c) / (-2 * a * c)))
    # C = math.degrees(math.acos((c * c - a * a - b * b) / (-2 * a * b)))
    # 输出三个角的角度
    # print("There three angles are",i ,round(A,2),round(B,2),round(C,2))
    if z == 'v_angle':
        # print('v_angle are',i,180-round(B,2))
        return 180 - round(B, 2)
    elif z == "inner_angle":
        return round(B, 2)
        # print("inner_angle are",i ,round(A,2))


# 形成夹角的两边比例
def side_ratio(x1, y1, x2, y2, x3, y3):
    # #计算三条边长
    a = math.sqrt((x2 - x3) * (x2 - x3) + (y2 - y3) * (y2 - y3))
    # b=math.sqrt((x1-x3)*(x1-x3)+(y1-y3)*(y1-y3))
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
    # print(all_inner_angles)
    list1 = sorted(all_inner_angles.items(), key=lambda x: x[0])
    return list1
    # return len(all_inner_angles)


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
            # print(x1, y1, x2, y2, x3, y3)
            # all_vertices_angles.append(np.float32(angles(x1, y1, x2, y2, x3, y3,z='v_angle')))
            angle = np.float32(angles(x1, y1, x2, y2, x3, y3, z='v_angle'))
            len_rio = side_ratio(x1, y1, x2, y2, x3, y3)
            # all_vertices_angles.append({angle:[[x1,y1],[x2,y2],[x3,y3]]})
            all_vertices_angles[angle] = [[x1, y1], [x2, y2], [x3, y3], len_rio]
    # 对字典按照key排序
    list1 = sorted(all_vertices_angles.items(), key=lambda x: x[0])
    # return all_vertices_angles
    return list1


def vertices_triangls(all_vertices_points):
    new_all_vertices_points = all_vertices_points[0:-2]
    # print('所有的顶点坐标为：  ', all_vertices_points)
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
        # print(p1)
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
    # print('vertices_triangl=========', vertices_triangl)
    return vertices_triangl


# 返回内部角度，和顶点角度，和画出图形
def return_angles(points1, pic_id):
    ##str转化为int
    points = []
    for i in points1:
        i = list(map(int, i))
        points.append(i)
    points2d = np.array(points)
    # print('points2d======',points1)

    if len(points2d) > 2:
        #     point = points2d[0][0]+15,points2d[0][1]+15]
        # print(points2d[0][0])
        ch2d = spatial.ConvexHull(points2d)  # 上述点的对象

        # print(ch2d.simplices) #每条边线的两个顶点在points2d的下标
        # print(ch2d.vertices) #多边形每个顶点在points2d的下标
        vertices = list(ch2d.vertices)
        # print(vertices)
        # 删除非顶点的点
        for i in range(0, len(ch2d.simplices)):
            # print('i = ', i)
            if i + 1 < len(ch2d.simplices) and ch2d.simplices[i][0] == ch2d.simplices[i + 1][0]:
                # print(points2d[ch2d.simplices[i][0]][0])
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

        # print('all_vertices_points = ', all_vertices_points)
        # print('all_inner_points = ', all_inner_points)

        all_vertices_angles = vertices_angles(all_vertices_points)
        all_inner_angles = inner_angles(all_inner_points, all_vertices_points)
        # print('vertices====',all_vertices_angles)
        # print('inner=====',all_inner_angles)
        #
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


# def return_same_v_points(vertices_triangls_dict, same_vertices_triangl, inner_points):
#     same_points = []
#     for i in same_vertices_triangl:
#         pointsList = list(list(vertices_triangls_dict.keys())[list(vertices_triangls_dict.values()).index(i)])
#         # print(pointsList)
#         # 还要判断此点是否是原图中的内点
#         if pointsList[:2] not in same_points and pointsList[:2] not in inner_points:
#             same_points.append(pointsList[:2])
#             # print('pointsList[:2]', pointsList[:2])
#         if pointsList[2:4] not in same_points and pointsList[2:4] not in inner_points:
#             same_points.append(pointsList[2:4])
#             # print('pointsList[2:4]', pointsList[2:4])
#         if pointsList[4:] not in same_points and pointsList[4:] not in inner_points:
#             same_points.append(pointsList[4:])
#             # print('pointsList[4:]', pointsList[4:])
#     return same_points


# def get_key(dict, value):
#     return [k for k, v in dict.items() if v == value]


"比较颜色，需要调用非缺失的点的坐标，这里函数返回的就是 ori，cur相同顶角的点的坐标"


# def return_same_points(points):
#     point = []
#     for i in points:
#         # print(i)
#         # print(i[0][0:2])
#         if list(i[0][0:2]) not in point:
#             point.append(list(i[0][0:2]))
#         if list(i[0][2:4]) not in point:
#             point.append(list(i[0][2:4]))
#         if list(i[0][4:]) not in point:
#             point.append(list(i[0][4:]))
#     return point


# "当相同的顶点数为2时候，可以使用顶点与内点的夹角去做对比。这种情况比较特殊，可以使用以函数"
#
#
# def v_inner_angles(v_points, inner_points):
#     coor_angle_ratio = []
#     v_len = len(v_points)
#     inner_len = len(inner_points)
#     for i in range(v_len):
#         if i + 1 < v_len:
#             for j in range(inner_len):
#                 x1 = v_points[i][0]
#                 y1 = v_points[i][1]
#                 x2 = inner_points[j][0]
#                 y2 = inner_points[j][1]
#                 x3 = v_points[i + 1][0]
#                 y3 = v_points[i + 1][1]
#                 angle = angles(x1, y1, x2, y2, x3, y3, 'inner_angle')
#                 len_rio = side_ratio(x1, y1, x2, y2, x3, y3)
#                 # v_ratio.append([angle, len_rio])
#                 coor_angle_ratio.append([[x1, y1, x2, y2, x3, y3], [angle, len_rio]])
#                 # coor_angle_ratio[x1, y1, x2, y2, x3, y3] = [angle,len_rio]

    # return coor_angle_ratio


"判断ori_pic的顶点是否是cur_pic中内部点"


def compare_oriV_is_curIn(v_point, cur_inner_points):
    flag = 0
    for i in cur_inner_points:
        if abs(i[0] - v_point[0]) < 10 and abs(i[1] - v_point[1]) < 10:
            flag = 1
    return flag


"12.23修改  顶点与内点形成的夹角"


def v_angles_alt(pic,flag):
    coor_angle_ratio = []
    v_points = pic[2][:-2]
    inner_points = pic[3]
    v_len = len(v_points)
    for i in range(v_len):
        if i + 1 < v_len:
            for j in range(i + 1, v_len):
                for k in inner_points:
                    x1 = v_points[i][0]
                    y1 = v_points[i][1]
                    x2 = k[0]
                    y2 = k[1]
                    x3 = v_points[j][0]
                    y3 = v_points[j][1]
                    angle = angles(x1, y1, x2, y2, x3, y3, 'inner_angle')
                    len_rio = side_ratio(x1, y1, x2, y2, x3, y3)
                    # v_ratio.append([angle, len_rio])
                    coor_angle_ratio.append([[x1, y1, x2, y2, x3, y3], [angle, len_rio]])
    if flag == 'cur':
        for i in range(v_len):
            # 把i前面的数据放到后面
            p1 = v_points.copy()
            if i < v_len:
                k = i + 1
                while k > 0:
                    point = p1[0]
                    p1.remove(point)
                    p1.append(point)
                    k = k - 1
            # 删除最后一个跟起点相同的数据
            p1.pop()
            # print(p1)
            for j in range(len(p1) - 1):
                z = j + 1
                x1 = p1[j][0]
                y1 = p1[j][1]
                x2 = v_points[i][0]
                y2 = v_points[i][1]
                x3 = p1[z][0]
                y3 = p1[z][1]
                angle = angles(x1, y1, x2, y2, x3, y3, z='inner_angle')
                len_rio = side_ratio(x1, y1, x2, y2, x3, y3)
                coor_angle_ratio.append([[x1, y1, x2, y2, x3, y3], [angle, len_rio]])
        return coor_angle_ratio
    else:
        return coor_angle_ratio


def compare_color(ori_vertices_triang, cur_vertices_triang, cur_color):
    ori_color_change = []
    cur_points = cur_vertices_triang[0]
    cur_point01 = cur_points[0:2]
    cur_point02 = cur_points[2:4]
    cur_point03 = cur_points[4:]

    ori_points = ori_vertices_triang[0]
    ori_point01 = ori_points[0:2]
    ori_point02 = ori_points[2:4]
    ori_point03 = ori_points[4:]
    for i in cur_color:
        if i[:2] == cur_point01:
            ori_color_change.append([ori_point01,i[2]])
        if i[:2] == cur_point02:
            ori_color_change.append([ori_point02,i[2]])
        if i[:2] == cur_point03:
            ori_color_change.append([ori_point03,i[2]])
    return ori_color_change


"当cur点>=3个点的时候，可以使用此种方法"
def compare_v_angles(ori_pic, cur_pic, cur_color):
    print('开始比对=====================================================================================================')
    if len(cur_pic[2][:-2]+cur_pic[3]) >= 3:

        ori_points_color = []
        cur_vertices_triangl01 = []
        ori_vertices_triangl01 = []

        ori_angles_ratio = v_angles_alt(ori_pic,'cur')
        cur_angles_ratio = v_angles_alt(cur_pic,'cur')
        # print('cur_angles_ratio ===',cur_angles_ratio)
        # print('ori_angles_ratio ===',ori_angles_ratio)
        for i in cur_angles_ratio:
            # print('early cur_points=',i)
            '[[1025, 488, 2116, 1475, 2294, 2294], [144.4, 0.5696818509937047]]'
            for j in ori_angles_ratio:
                # print('early cur_points=',i)
                # print('early ori_points=', j)
                if abs(i[1][0] - j[1][0]) < 21 and abs(i[1][1] - j[1][1]) < 2 and abs(i[0][0] - j[0][0]) < 20 \
                        and abs(i[0][1] - j[0][1]) < 20 and abs(i[0][2] - j[0][2]) < 20 and abs(i[0][3] - j[0][3]) < 20\
                        and abs(i[0][4] - j[0][4]) < 20 and abs(i[0][5] - j[0][5]) < 20:
                    ori_vertices_triangl01.append(j.copy()[0])
                    cur_vertices_triangl01.append(i.copy()[0])
                    color = compare_color(j,i,cur_color)
                    # ori_points_color.append(color)
                    ori_points_color = ori_points_color+color
                    # print('compare_color =====',color)
                    # print('i========', i)
                    # print('j========', j)
        # print('ori_vertices_triangl01 =====', ori_vertices_triangl01)
        # print('cur_vertices_triangl01 =====', cur_vertices_triangl01)
        # print(ori_points_color)


        "这里ori的指示灯坐标，但是对应的颜色是cur指示灯颜色"
        ori_same_color = []
        for i in ori_points_color:
            if i not in ori_same_color:
                ori_same_color.append(i)

        # print('ori_same_color =====', ori_same_color)
        all_points = ori_pic[2][:-2].copy()+ori_pic[3].copy()
        same_points = []
        for i in ori_vertices_triangl01:
            point01 = i[0:2]
            # print('point01 = ',point01)
            point02 = i[2:4]
            # print('point02 = ', point02)
            point03 = i[4:]
            # print('point03 = ', point03)
            if point01 in all_points:
                all_points.remove(point01)
            if point02 in all_points:
                all_points.remove(point02)
            if point03 in all_points:
                all_points.remove(point03)

            if point01 not in same_points:
                same_points.append(point01)
            if point02 not in same_points:
                same_points.append(point02)
            if point03 not in same_points:
                same_points.append(point03)
        # print('same_points ========', same_points)
        # print('len(cur_pic[2]+cur_pic[3])===',len(ori_pic[2][:-2]+ori_pic[3]))
        print('all_points=========================',all_points)
        return all_points,ori_same_color
    else:
        "说明当前指示灯的个数少于3个"
        return -1
