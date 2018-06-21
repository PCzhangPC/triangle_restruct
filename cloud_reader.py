# -*- coding: utf-8 -*-
from tin import *


class PcdReader():
    def __init__(self, path=None, p_list=None):
        self.path = path
        self.point_list = [] if p_list is None else p_list

    def read(self):
        i = 0
        with open(self.path) as f:
            for lines in f:
                if i >= 11 and i % 25 == 0:  ##排除前10行,并且做了一个点的简化，bun0可不用简化
                    xyz = lines.split()

                    for pos in range(len(xyz)):
                        xyz[pos] = float(xyz[pos])

                    tmp_point = Point(xyz[0], xyz[1], xyz[2])
                    self.point_list.append(tmp_point)
                i += 1

        self.point_list.sort(key=lambda x: x.z)  ##差值取点之后最好做的排序，不然开始的两个点容易太远, bun0可以不用
        return self.point_list


if __name__ == '__main__':   ### entrance
    # cloud = PcdReader(r'C:\Users\Administrator\Desktop\rabbit.pcd')
    # p_list = cloud.read_and_create()
    #
    # scene = Glscene()
    #
    # for point in p_list:
    #     scene.draw(point)
    # scene.show_scene()

    cloud = PcdReader(r'C:\Users\Administrator\Desktop\rabbit.pcd')
    p_list = cloud.read()

    tin = Tin(p_list)
    tin.create_tin()
    tin.cal_plane()

    scene = Glscene()
    scene.draw(tin)

    # for point in p_list:
    #     scene.draw(point)
    scene.draw(tin.plane)

    print tin.cal_volume()

    scene.show_scene()
