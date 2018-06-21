# -*- coding: utf-8 -*-
from triangle import *
from show_window import*
import math
import numpy as np
from cloud_reader import*

class Plane():
    def __init__(self, para_list=None, show_range = None):
        self.plane_para = para_list
        self.show_range = show_range

    def show(self):
        if self.plane_para is not None:
            return self.gl_show_plane

    def gl_show_plane(self):
        if self.show_range is not None:
            a, b, c = self.plane_para
            x1 = self.show_range[0] * 1
            y1 = self.show_range[2] * 1
            z1 = (1 - a * x1 - b * y1) / c

            x2 = self.show_range[0] * 1
            y2 = self.show_range[3] * 1
            z2 = (1 - a * x2 - b * y2) / c

            x3 = self.show_range[1] * 1
            y3 = self.show_range[2] * 1
            z3 = (1 - a * x3 - b * y3) / c

            x4 = self.show_range[1] * 1
            y4 = self.show_range[3] * 1
            z4 = (1 - a * x4 - b * y4) / c

            glBegin(GL_LINE_LOOP)
            glVertex3f(x1, y1, z1)
            glVertex3f(x3, y3, z3)
            glVertex3f(x4, y4, z4)
            glVertex3f(x2, y2, z2)
            glEnd()


class Tin():
    def __init__(self, point_list=None):
        self.point_list = point_list  # 所有的点
        self.line_list = []  # 生成的边
        self.triangle_list = []  # 生成的三角形
        self.edge_to_expand = []  # 需要扩展的边
        self.plane = None
        self.extremum = []

    def gl_show_tin(self, line_type=True):
        if line_type:
            for line in self.line_list:
                line.gl_show_line()

        else:
            for tri in self.triangle_list:
                tri.gl_show_triangle()

    def show(self):
        return self.gl_show_tin

    def cal_plane(self):
        if len(self.point_list):
            xx_sum = 0
            yy_sum = 0
            zz_sum = 0
            xy_sum = 0
            xz_sum = 0
            yz_sum = 0
            x_sum = 0
            y_sum = 0
            z_sum = 0

            x_max = max((po.x for po in self.point_list))
            x_min = min((po.x for po in self.point_list))
            y_max = max((po.y for po in self.point_list))
            y_min = min((po.y for po in self.point_list))
            z_max = max((po.z for po in self.point_list))
            z_min = min((po.z for po in self.point_list))
            self.extremum = [x_max, x_min, y_max, y_min, z_max, z_min]

            for po in self.point_list:
                xx_sum += (po.x * po.x)
                yy_sum += (po.y * po.y)
                zz_sum += (po.z * po.z)
                xy_sum += (po.x * po.y)
                xz_sum += (po.x * po.z)
                yz_sum += (po.y * po.z)
                x_sum += po.x
                y_sum += po.y
                z_sum += po.z

            A = np.array([[xx_sum, xy_sum, xz_sum], [xy_sum, yy_sum, yz_sum], [xz_sum, yz_sum, zz_sum]])
            B = np.array([x_sum, y_sum, z_sum]).reshape(3, 1)

            plane_para = np.linalg.solve(A, B)
            self.plane = Plane(plane_para, self.extremum)

    def create_tin(self):
        # 生成第一个三角形
        line0 = Line(self.point_list[0], self.point_list[1])
        point3 = max_angle_point(line0, self.point_list[2:])

        dis_thre = line0.get_len() * 5.8 #bun0为3.3, RABBIT用5,8

        tri = Triangle(self.point_list[0], self.point_list[1], point3)
        line0, line1, line2 = tri.line_list[0], tri.line_list[1], tri.line_list[2]

        push_list(self.line_list, line0, line1, line2)
        push_list(self.edge_to_expand, line0, line1, line2)
        push_list(self.triangle_list, tri)

        tri_index = 0  # 正在扩展第几个三角形 * 3
        while len(self.edge_to_expand):
            #break
            line_expend = self.edge_to_expand[0]

            if line_expend.use_count < 2:
                the_triangle = self.triangle_list[tri_index / 3]
                left_tri_point = find_left_point(the_triangle, line_expend)
                side1 = cal_side(line_expend, left_tri_point)

                res, point_find = find_target_point(self.point_list, line_expend, the_triangle, side1, dis_thre)
                if res:  # 找出了这个点
                    tmp_line1 = line_expend
                    tmp_line2 = Line(point_find, line_expend.point1)
                    tmp_line3 = Line(point_find, line_expend.point2)

                    tri = Triangle(point_find, line_expend.point1, line_expend.point2)
                    if not tri_exist(tri, self.triangle_list):
                        tmp_line1.add_one_use_count()
                        self.edge_to_expand.append(tmp_line1)  # 不加到line_list里了，但是为了方便加到edge里

                        flag, tl = line_exist(tmp_line2, self.line_list)
                        if flag:  # 生成的线段存在
                            tl.add_one_use_count()
                            self.edge_to_expand.append(tl)
                        else:
                            self.line_list.append(tmp_line2)
                            self.edge_to_expand.append(tmp_line2)

                        flag, tl = line_exist(tmp_line3, self.line_list)
                        if flag:  # 生成的线段存在
                            tl.add_one_use_count()
                            self.edge_to_expand.append(tl)
                        else:
                            self.line_list.append(tmp_line3)
                            self.edge_to_expand.append(tmp_line3)

                        self.triangle_list.append(tri)

            self.edge_to_expand.remove(line_expend)  # 不用扩展（use_count>2) 不能扩展(没有找到点)
                                                     # 三角形已经出现过，或是扩展完毕，从edge里移除
            tri_index += 1
            print len(self.edge_to_expand)

    def cal_volume(self):
        volume_all = 0
        a, b, c = self.plane.plane_para
        divided = a ** 2 + b ** 2 + c ** 2

        for tri in self.triangle_list:
            subpo_list = []
            h_tmp = 0
            for po in tri.point_list:  #算出了三个投影点
                x = (a + (b ** 2 + c ** 2) * po.x - a * b * po.y - a * c * po.z) / divided
                y = (b + (a ** 2 + c ** 2) * po.y - a * b * po.x - b * c * po.z) / divided
                z = (c + (a ** 2 + b ** 2) * po.z - a * c * po.x - b * c * po.y) / divided
                tmp_po = Point(x, y, z)
                subpo_list.append(tmp_po)

                h_tmp += cal_length(tmp_po, po)

            h = h_tmp / 3
            sub_tri = Triangle(subpo_list[0], subpo_list[1], subpo_list[2])
            subs = sub_tri.cal_s()

            one_volume = h * subs
            volume_all += one_volume

        return volume_all


def cal_side(line, point):
    p1 = line.point1  # 不考虑z轴, 只在二维平面上考虑左右
    p2 = line.point2

    if p1.x - p2.x:
        A = (p1.y - p2.y) / (p1.x - p2.x)  # 直线的斜率 y = A x + B
        B = p1.y - A * p1.x

        return point.y - A * point.x - B

    return point.x - p1.x


def cal_distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2 + (point1.z - point2.z) ** 2)


def cal_angle(line, point):
    pa = line.point1
    pb = line.point2
    pc = point

    l_c = cal_distance(pa, pb)
    l_a = cal_distance(pa, pc)
    l_b = cal_distance(pb, pc)

    val = (l_a ** 2 + l_b ** 2 - l_c ** 2) / (l_a * l_b * 2)
    if val >= 1.0:
        angle = 0.0
    else:
        angle = math.acos(val)

    return angle


def max_angle_point(line, p_list):
    max_angle = -1
    t_index = -1

    for index, point in enumerate(p_list):
        tmp_angle = cal_angle(line, point)
        if tmp_angle > max_angle:
            max_angle = tmp_angle
            t_index = index

    return p_list[t_index]


def find_target_point(po_list, line, tri, side, thre):  #
    max_angle = -1
    t_index = -1

    for index, p in enumerate(po_list):
        if p not in tri.point_list:  # 不是这个三角形里的点
            tmp_angle = cal_angle(line, p)
            if tmp_angle > max_angle and cal_side(line, p) * side < 0:  # 角度最大且在不同side
                if Line(p, line.point1).get_len() <= thre and Line(p, line.point2).get_len() <= thre:  # 距离满足阈值要求
                    max_angle = tmp_angle
                    t_index = index

    if t_index == -1:
        return False, None
    else:
        return True, po_list[t_index]


def push_list(target_list, *item_list):
    for item in item_list:
        target_list.append(item)


def find_left_point(tri, line):
    if line in tri.line_list:
        # return [p for p in tri.line_list if (p != line.point1 and p != line.point2)][0]
        return filter(lambda x: (x != line.point1 and x != line.point2), tri.point_list)[0]


def line_exist(line, line_list):
    for l in line_list:
        if l == line:
            return True, l

    return False, None


def tri_exist(tri, tri_list):
    for t_tri in tri_list:
        if t_tri == tri:
            return True

    return False

if __name__ == '__main__':
    print math.acos(-0.65)
