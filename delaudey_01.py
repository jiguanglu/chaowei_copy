# -*- coding:utf-8 -*-
# author : jiguanglu
# e-mail : jiguang125@gmail.com

import numpy as np
from scipy import spatial
import math
from math import atan2, degrees
import matplotlib.pyplot as pl
import gc

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
# def vertices_points(vertices, points2d):
#     vertices_points = []
#     for i in vertices:
#         vertices_points.append(points2d[i].tolist())
#     return vertices_points


# return all inner_points
# def inner_points(vertices_points, points2d):
#     list = points2d.tolist()
#     for i in vertices_points:
#         if i in points2d:
#             list.remove(i)
#     return list


# 返回余弦定理求出角度
def angles(x1, y1, x2, y2, x3, y3, z):
    # x1,y1,x2,y2,x3,y3=1,1,6.5,1,6.5,2.5
    # #计算三条边长
    angle = 0
    a = math.sqrt((x2 - x3) * (x2 - x3) + (y2 - y3) * (y2 - y3))
    b = math.sqrt((x1 - x3) * (x1 - x3) + (y1 - y3) * (y1 - y3))
    c = math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
    # print('a = ',a)
    # print('b = ',b)
    # print('c = ',c)
    # 利用余弦定理计算三个角的角度
    # A = math.degrees(math.acos((a * a - b * b - c * c) / (-2 * b * c)))
   
    if a != 0 and c != 0:
        B = 0
        res = (b * b - a * a - c * c) / (-2 * a * c)
        if res>1:
            B = math.degrees(math.acos(1))
        elif res < -1:
            B = math.degrees(math.acos(-1))
        else:
            B =  math.degrees(math.acos(res))
        
        # B = math.degrees(math.acos((b * b - a * a - c * c) / (-2 * a * c)))
        # C = math.degrees(math.acos((c * c - a * a - b * b) / (-2 * a * b)))
        # 输出三个角的角度
        # print("There three angles are",i ,round(A,2),round(B,2),round(C,2))
        if z == 'v_angle':
            # print('v_angle are',i,180-round(B,2))
            angle = 180 - round(B, 2)
            #return 180 - round(B, 2)
        elif z == "inner_angle":
            angle = round(B, 2)
            #return round(B, 2)
            # print("inner_angle are",i ,round(A,2))
    #print(angle)
    return angle

# 形成夹角的两边比例
def side_ratio(x1, y1, x2, y2, x3, y3):
    # #计算三条边长

    a = math.sqrt((x2 - x3) * (x2 - x3) + (y2 - y3) * (y2 - y3))
    # b=math.sqrt((x1-x3)*(x1-x3)+(y1-y3)*(y1-y3))
    c = math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
    if a != 0 and c != 0:
        return a / c




# 返回内部角度，和顶点角度，和画出图形
def draw_plot(points1, pic_id):
    ##str转化为int
    points = []
    for i in points1:
        i = list(map(int, i))
        points.append(i)
    points2d = np.array(points)
    # print('points2d======',points1)

    if len(points2d) > 2:
        ch2d = spatial.ConvexHull(points2d)  # 上述点的对象

        poly = pl.Polygon(points2d[ch2d.vertices], fill=None, lw=2, color='r', alpha=0.9)
        ax = pl.subplot(aspect='equal')
        pl.plot(points2d[:, 0], points2d[:, 1], 'go')
        pl.title(pic_id)

        for i, pos in enumerate(points2d):
            pl.text(pos[0], pos[1], str(i), color='blue')
            ax.add_artist(poly)
        pl.show()
        # pl.savefig('%s.png' % pic_id)
    # pl.close()

    # 返回顶点夹角，返回内角
    #     return all_vertices_angles, all_inner_angles, all_vertices_points, all_inner_points

    # else:
    # return 'n_points<3'





def compare_color(ori_vertices_triangle, cur_vertices_triangle, cur_color):
    ori_color_change = []
    if len(ori_vertices_triangle) != 2:
        cur_points = cur_vertices_triangle[0]
        cur_point01 = cur_points[0:2]
        cur_point02 = cur_points[2:4]
        cur_point03 = cur_points[4:]

        ori_points = ori_vertices_triangle[0]
        ori_point01 = ori_points[0:2]
        ori_point02 = ori_points[2:4]
        ori_point03 = ori_points[4:]
        for i in cur_color:
            if i[:2] == cur_point01:
                ori_color_change.append([ori_point01, i[2]])
            if i[:2] == cur_point02:
                ori_color_change.append([ori_point02, i[2]])
            if i[:2] == cur_point03:
                ori_color_change.append([ori_point03, i[2]])

    else:
        for i in cur_color:
            if i[:2] == cur_vertices_triangle:
                ori_color_change.append([cur_vertices_triangle, i[2]])

    return ori_color_change

"当cur点>=3个点的时候,并且顶点缺失后，最少剩下两个顶点，可以使用此种方法"


"这次不分顶点与内部点，直接比较角度与边长比例和坐标比对"


def all_points_angles_ratio(points):
    points_first_copy = points.copy()
    coor_angle_ratio = []
    for i in points:

        x1 = i[0]
        y1 = i[1]
        points_first_copy.remove(i)
        for j in points_first_copy:
            x3 = j[0]
            y3 = j[1]
            points_second_copy = points_first_copy.copy()
            points_second_copy.remove(j)
            for k in points_second_copy:
                x2 = k[0]
                y2 = k[1]
                angle = angles(x1, y1, x2, y2, x3, y3, 'inner_angle')
                len_rio = side_ratio(x1, y1, x2, y2, x3, y3)
                # v_ratio.append([angle, len_rio])
                if angle != None and len_rio != None:
                    coor_angle_ratio.append([[x1, y1, x2, y2, x3, y3], [angle, len_rio]])
    return coor_angle_ratio


def compare_all_points(ori_points_angles_ratio, cur_points_angles_ratio, ori_points_, cur_points_, cur_color):
    print('开始比对=====================================================================================================')
    ori_points_color = []
    ori_same = []
    cur_same = []
    #print('ori_points_angles_ratio ==',ori_points_angles_ratio)
    #print('cur_points_angles_ratio ==',cur_points_angles_ratio)
    
    for i in ori_points_angles_ratio:
        #gc.collect()
        for j in cur_points_angles_ratio:

            if abs(i[1][0] - j[1][0]) < 22:
                if abs(i[1][1] - j[1][1]) < 3:
                    if abs(i[0][0] - j[0][0]) < 20:
                         if abs(i[0][1] - j[0][1]) < 20:
                              if abs(i[0][2] - j[0][2]) < 20:
                                   if abs(i[0][3] - j[0][3]) < 20:
                                        if abs(i[0][4] - j[0][4]) < 20:
                                             if abs(i[0][5] - j[0][5]) < 20:
                                                  if [i[0][0], i[0][1]] not in ori_same:
                                                      ori_same.append([i[0][0], i[0][1]])
                                                  if [i[0][2], i[0][3]] not in ori_same:
                                                      ori_same.append([i[0][2], i[0][3]])
                                                  if [i[0][4], i[0][5]] not in ori_same:
                                                      ori_same.append([i[0][4], i[0][5]])

                                                  if [j[0][0], j[0][1]] not in cur_same:
                                                      cur_same.append([j[0][0], j[0][1]])
                                                  if [j[0][2], j[0][3]] not in cur_same:
                                                      cur_same.append([j[0][2], j[0][3]])
                                                  if [j[0][4], j[0][5]] not in cur_same:
                                                      cur_same.append([j[0][4], j[0][5]])

                                                  color = compare_color(i, j, cur_color)
                                                  ori_points_color = ori_points_color + color
                                                  cur_points_angles_ratio.remove(j)
                                                  break
    "这里ori的指示灯坐标，但是对应的颜色是cur指示灯颜色"
    ori_same_color = []
    for i in ori_points_color:
        if i not in ori_same_color:
            ori_same_color.append(i)

    "返回消失的点"
    
    ori_points = np.array(ori_points_)
    ori_points = np.unique(ori_points,axis = 0)
    ori_points_ = ori_points.tolist()
    ori_points_copy = ori_points_.copy()


    cur_points = np.array(cur_points_)
    cur_points = np.unique(cur_points,axis = 0)
    cur_points_ = cur_points.tolist()
    cur_points_copy = cur_points_.copy()
    for i in ori_same:
        if i in ori_points_:
            ori_points_copy.remove(i)
    for j in cur_same:
        if j in cur_points_:
            cur_points_copy.remove(j)

    
    #print('ori_same_=======', ori_same)
    #print('ori_points ===',ori_points_)
    #print('cur_same_=======', cur_same)
    #print('cur_points ===',cur_points_)

    return ori_points_copy, ori_same_color


"当cur_img的点少于3的时候，需要使用此方法进行比对"


def compare_less_points(ori_points_, cur_points_, cur_color):
    print('开始比对=====================================================================================================')
    ori_points_color = []
    ori_same = []
    cur_same = []
    if len(cur_points_) < 3:
        for i in ori_points_:
            for j in cur_points_:
                if abs(i[0] - j[0]) < 20 and abs(i[1] - j[1]) < 20:
                    # print('i========', i)
                    # print('j========', j)
                    if [i[0],i[1]] not in ori_same:
                        ori_same.append([i[0],i[1]])
                    if [j[0],j[1]] not in cur_same:
                        cur_same.append([j[0],j[1]])
                    color = compare_color(i, j, cur_color)
                    ori_points_color = ori_points_color + color
    "这里ori的指示灯坐标，但是对应的颜色是cur指示灯颜色"
    ori_same_color = []
    for i in ori_points_color:
        if i not in ori_same_color:
            ori_same_color.append(i)

    "返回消失的点"
    ori_points_copy = ori_points_.copy()
    cur_points_copy = cur_points_.copy()
    for i in ori_same:
        if i in ori_points_:
            ori_points_copy.remove(i)
    for j in cur_same:
        if j in cur_points_:
            cur_points_copy.remove(j)

    return ori_points_copy, ori_same_color
