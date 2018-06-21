# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from show_window import *
import math
import sys

a = 0


def cal_length(po1, po2):
    return math.sqrt((po1.x - po2.x) ** 2 + (po1.y - po2.y) ** 2 + (po1.z - po2.z) ** 2)


class Point():
    def __init__(self, x=None, y=None, z=None):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __str__(self):
        return 'x: ' + str(self.x) + '    y: ' + str(self.y) + '    z: ' + str(self.z)

    __repr__ = __str__

    def gl_show_point(self):
        glBegin(GL_POINTS)
        glVertex3f(self.x, self.y, self.z)
        glEnd()

    def show(self):
        return self.gl_show_point

    def get_val(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def __cmp__(self, other):
        return cmp(self.get_val(), other.get_val())


class Line():
    def __init__(self, point1=None, point2=None):
        self.point1 = point1
        self.point2 = point2
        self.use_count = 1

    def add_one_use_count(self):
        self.use_count += 1

    def __eq__(self, other):
        return (self.point1 == other.point1 and self.point2 == other.point2) or \
               (self.point1 == other.point2 and self.point2 == other.point1)

    def __str__(self):
        return 'point1: ' + repr(self.point1) + '\n' + 'point2: ' + repr(self.point2)

    __repr__ = __str__

    def get_len(self):
        length = (self.point1.x - self.point2.x) ** 2 + (self.point1.y - self.point2.y) ** 2 \
              + (self.point1.z - self.point2.z) ** 2
        return math.sqrt(length)

    def gl_show_line(self):
        glBegin(GL_LINES)
        glVertex3f(self.point1.x, self.point1.y, self.point1.z)
        glVertex3f(self.point2.x, self.point2.y, self.point2.z)
        glEnd()

    def show(self):
        return self.gl_show_line


if __name__ == '__main__':
    p1 = Point(-0.2, -0.2, -1)
    p2 = Point(0, 0, 0)
    l1 = Line(p1, p2)

    # p3 = Point(0.3, 0.2, 0)
    # p4 = Point(0, 0, 0)
    # l2 = Line(p3, p4)
    #
    scene = Glscene()
    scene.draw(p1)
    scene.show_scene()





