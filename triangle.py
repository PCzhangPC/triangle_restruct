from pointandline import *


class Triangle():
    def __init__(self, point1, point2, point3):
        self.point_list = [point1, point2, point3]
        self.line_list = [Line(point1, point2), Line(point2, point3), Line(point1, point3)]

    def gl_show_triangle(self, filling=True):
        if filling:
            glBegin(GL_TRIANGLES)
            glVertex3f(self.point_list[0].x, self.point_list[0].y, self.point_list[0].z)
            glVertex3f(self.point_list[1].x, self.point_list[1].y, self.point_list[1].z)
            glVertex3f(self.point_list[2].x, self.point_list[2].y, self.point_list[2].z)
            glEnd()

        else:
            for line in self.line_list:
                line.gl_show_line()

    def __str__(self):
        s = ''
        for i, point in enumerate(self.point_list):
            s += ('point' + str(i) + '  ' +  repr(point) + '\n')

        return s

    __repr__ = __str__

    def __eq__(self, other):
        return sorted(self.point_list) == sorted(other.point_list)

    def show(self):
        return self.gl_show_triangle

    def cal_s(self):
        l1, l2, l3 = self.line_list
        l1 = l1.get_len()
        l2 = l2.get_len()
        l3 = l3.get_len()
        p = (l1 + l2 + l3) / 2

        return math.sqrt(p * (p - l1) * (p - l2) * (p - l3))


if __name__ == '__main__':
    p1 = Point(-0.2, -0.2, -1)
    p2 = Point(0, 0, 0)
    p3 = Point(0.3, 0.2, 0)
    tri1 = Triangle(p1, p2, p3)

    p4 = Point(0.6, 0.2, -1)
    p5 = Point(0, 0, 0)
    p6 = Point(-0.3, -0.2, 0)
    tri2 = Triangle(p4, p5, p6)

    print tri1
    scene = Glscene()
    scene.draw(tri1)
    scene.draw(tri2)
    scene.show_scene()
