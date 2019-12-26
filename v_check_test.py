from delaudey_01 import *

ori_all_vertices_points =  [[1359, 2477], [1174, 2436], [1734, 1485], [2118, 1476], [2293, 1483], [1818, 2463], [1670, 2470]]
ori_all_inner_points =  [[1990, 1480], [1431, 2473], [1517, 2474], [1862, 1483]]
cur_all_vertices_points =  [[1025, 488], [2294, 1483], [1970, 2476], [1361, 2478]]
acur_ll_inner_points =  [[2116, 1475], [1989, 1479], [1668, 2471], [1816, 2464], [1427, 2476], [1859, 1482], [1735, 1486], [1515, 2477], [1734, 2468]]



def vertices_inner_triangls(all_vertices_points, all_inner_points):
    for i in all_vertices_points:
        for j in all_inner_points:
            return 0

    # new_all_vertices_points = all_vertices_points[0:-2]
    # # print('所有的顶点坐标为：  ', all_vertices_points)
    # vertices_triangl = {}
    # p_len = len(new_all_vertices_points)
    # for i in range(p_len):
    #     # 把i前面的数据放到后面
    #     p1 = new_all_vertices_points.copy()
    #     if i < p_len:
    #         k = i + 1
    #         while k > 0:
    #             point = p1[0]
    #             p1.remove(point)
    #             p1.append(point)
    #             k = k - 1
    #     # 删除最后一个跟起点相同的数据
    #     p1.pop()
    #     # print(p1)
    #     for j in range(len(p1) - 1):
    #         v_ratio = []
    #         z = j + 1
    #         x1 = p1[j][0]
    #         y1 = p1[j][1]
    #         x2 = new_all_vertices_points[i][0]
    #         y2 = new_all_vertices_points[i][1]
    #         x3 = p1[z][0]
    #         y3 = p1[z][1]
    #         angle = angles(x1, y1, x2, y2, x3, y3, z='v_angle')
    #         len_rio = side_ratio(x1, y1, x2, y2, x3, y3)
    #         v_ratio.append([angle, len_rio])
    #         vertices_triangl[x1, y1, x2, y2, x3, y3] = v_ratio
    # # print('vertices_triangl=========', vertices_triangl)
    # return vertices_triangl




# def compare_v_angles(ori_pic, cur_pic):
#     print('开始比对=====================================================================================================')
#     dis_same_v_points = []
#     ori_vertices_triangls_dict = vertices_triangls(ori_pic[2])
#     cur_vertices_triangls_dict = vertices_triangls(cur_pic[2])
#     # print('原图中顶点坐标',ori_pic[2][:-1])
#     # print('新图中顶点坐标',cur_pic[2][:-1])
#     # print('原图中的内点', ori_pic[3])
#     # print('当前图的内点', cur_pic[3])
#     # print('原始图顶点夹角', ori_vertices_triangls_dict)
#     # print('当前图顶点夹角', cur_vertices_triangls_dict)
#     cur_vertices_triangl = []
#     ori_vertices_triangl = []
#     ori_points = []
#     cur_points = []
#     # 比较角度和边长比例，来判断相同的顶点
#     for i in cur_vertices_triangls_dict.values():
#         # print('j')
#         for j in ori_vertices_triangls_dict.values():
#             if abs(i[0][0] - j[0][0]) < 0.5 and abs(i[0][1] - j[0][1]) < 0.1 and \
#                     abs(get_key(cur_vertices_triangls_dict, i)[0][2] - get_key(ori_vertices_triangls_dict, j)[0][
#                         2]) < 20 \
#                     and abs(
#                 get_key(cur_vertices_triangls_dict, i)[0][3] - get_key(ori_vertices_triangls_dict, j)[0][3]) < 20 \
#                     and abs(
#                 get_key(cur_vertices_triangls_dict, i)[0][5] - get_key(ori_vertices_triangls_dict, j)[0][5]) < 20 :
#                 # 返回在基准图中与cur图的相同点的角度与边长比例 [angle, ratio]
#                 ori_vertices_triangl.append(j.copy())
#                 cur_vertices_triangl.append(i.copy())
#                 # print('i = ', get_key(cur_vertices_triangls_dict, i))
#                 # print('j = ', get_key(ori_vertices_triangls_dict, j))
#                 ori_points.append(get_key(ori_vertices_triangls_dict, j))
#                 cur_points.append(get_key(cur_vertices_triangls_dict, i))
#
#     "返回相同顶角的点的坐标，当比较颜色的时候需要调用"
#     points_in_ori = return_same_points(ori_points)
#     points_in_cur = return_same_points(cur_points)
#     # print('所有相同的顶点在cur图中的坐标 ======',points_in_cur)
#
#     ori_same_v_points = []
#     cur_same_v_points = []
#     if len(ori_points) != 0:
#         # print('ori_points = ', ori_points)
#         # print('所有相同的顶点组成的角度 = ', cur_points)
#         # print('ori_vertices_triangl = ',ori_vertices_triangl)
#         # print('cur_vertices_triangl = ',cur_vertices_triangl)
#         # 返回相同的顶点与另外两个顶点之间夹角，边长比例，顶点坐标，目的是为了比较inner_points
#
#         if len(ori_vertices_triangl) > 0:
#             # a = list(ori_vertices_triangls_dict.values()).index(ori_vertices_triangl[0])
#             ori_same_v_points = list(list(ori_vertices_triangls_dict.keys())[
#                                          list(ori_vertices_triangls_dict.values()).index(ori_vertices_triangl[0])])
#             cur_same_v_points = list(list(cur_vertices_triangls_dict.keys())[
#                                          list(cur_vertices_triangls_dict.values()).index(cur_vertices_triangl[0])])
#             # 根据比较得到的顶点的角度与长度的对比都相似的。返回在ori中的没有变化的坐标
#             #     print('ori_same_v_points', ori_same_v_points)
#             #     print('cur_same_v_points', cur_same_v_points)
#             ori_inner_points = ori_pic[3]
#             cur_inner_points = cur_pic[3]
#             # print('当前图的内部点坐标为 ',cur_inner_points )
#
#
#             same_points_in_ori = return_same_v_points(ori_vertices_triangls_dict, ori_vertices_triangl,
#                                                       ori_inner_points)
#             # same_points_in_cur = return_same_v_points(cur_vertices_triangls_dict, cur_vertices_triangl,cur_inner_points )
#
#             # print('same points ', same_points_in_ori)
#             # print('same points ', ori_pic[2])
#             # 如果新图中的顶点为原图中的内点，也必须剔除。
#
#             # print('=====',ori_pic[2])
#             for j in ori_pic[2]:
#                 if j not in same_points_in_ori and j not in dis_same_v_points:
#                     # print('在原图中消失的顶点的坐标为 ', j)
#                     if compare_oriV_is_curIn(j,cur_inner_points) == 0:
#                     # for k in cur_inner_points:
#                     #     if abs(k[0] - j[0]) > 10 and abs(k[1] - j[1]) > 10 and j not in dis_same_v_points:
#                            dis_same_v_points.append(j)
#             print('消失的顶点坐标', dis_same_v_points)
#             # 当多边形的边的数量不同时候，返回缺失点的坐标
#             if len(dis_same_v_points) == 0:  # 有两种情况，1：想同的顶点形成不了三角形，返回全部顶点坐标。 2：顶点全部相同
#                 return 'same_vertices', ori_same_v_points, cur_same_v_points, points_in_cur
#             else:
#                 # print('返回缺失点的坐标', dis_same_v_points)
#                 if len(ori_same_v_points) != 0 and len(cur_same_v_points) != 0:
#                     return dis_same_v_points, ori_same_v_points, cur_same_v_points, points_in_cur
#         else:
#             return 'no points find'
#     else:
#         # same_ori_v_points = []
#         # same_cur_v_points = []
#         ori_v_points = ori_pic[2][:-1]
#         ori_in_points = ori_pic[3]
#         cur_v_points = cur_pic[2][:-1]
#         cur_in_points = cur_pic[3]
#         ori_v_inner_angles = v_inner_angles(ori_v_points, ori_in_points)
#         cur_v_inner_angles = v_inner_angles(cur_v_points, cur_in_points)
#         # print('ori_v_inner_angles = ', ori_v_inner_angles)
#         # print('cur_v_inner_angles = ', cur_v_inner_angles)
#         for i in cur_v_inner_angles:
#             for j in ori_v_inner_angles:
#                 if abs(i[1][0] - j[1][0]) < 1 and abs(i[1][1] - j[1][1]) < 0.01:
#                     "说明顶点和内点组成的角度相同，然后取出两个顶点，即为相同的顶点"
#                     ori_same_v_points = (j[0])
#                     cur_same_v_points = (i[0])
#         # print('same_ori_v_points @@@@@@@@@@@@@@',ori_same_v_points )
#         ver = [ori_same_v_points[:2], ori_same_v_points[-2:]]
#         for i in ori_pic[2][:-2]:
#             if i not in ver:
#                 dis_same_v_points.append(i)
#         print('ver$$$$$$$$$$$$$$$$$$$$$$$$$', ori_same_v_points)
#         return dis_same_v_points, ori_same_v_points, cur_same_v_points, points_in_cur
