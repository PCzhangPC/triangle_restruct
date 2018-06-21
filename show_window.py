# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import sys


def auto_rotate():
    global a
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glRotatef(0.1, 0.0, 0.0, 1.0)

    glPushMatrix()                       #保存当前视图矩阵
    glBegin(GL_LINES)                    # 旋转之后得重新draw一下？？  后面改成函数传入吧
    glVertex3f(-0.5, -0.5, -1)
    glVertex3f(0, 0.0, 0.0)
    glEnd()

    glPopMatrix()                        #压出来
    glutSwapBuffers()

class Glscene():
    def __init__(self, window_length=640, window_weight=400):
        glutInit(sys.argv)  # 初始化
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)  # 双缓冲
        glutInitWindowSize(window_length, window_weight)  # 窗口大小
        glutInitWindowPosition(800, 400)  # 窗口位置

        self.show_list = []
        self.angle = 0.5
        self.times = 1

    def resize_gl_scene(self, Width, Height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glViewport(0, 0, Width, Height)
        gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0.0, 0.1, 0.3, 0.0, 0.1, 0.0, 0.0, 1.0, 0.0)  # 相机位置和朝向

    def draw(self, obj):
        self.show_list.append(obj.show())

    def draw_func(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        for func in self.show_list:
            func()

        glPopMatrix()
        glutSwapBuffers()  # 双缓冲交换缓存区，即显示出来

        glFlush()

    def rotate_scene(self):
        glRotatef(self.angle, 0.0, 1, 0.0)
        self.draw_func()     #这里不能使用 glutDisplayFunc(self.draw_func)

        time.sleep(0.01)

    def on_mouse(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            glutIdleFunc(self.rotate_scene)

        elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            glutIdleFunc(None)

    def show_scene(self):
        glutCreateWindow("opengl")  # 创建窗口
        glutReshapeFunc(self.resize_gl_scene)  # 为了保证在窗口拉伸时正确的渲染

        glutDisplayFunc(self.draw_func)   #将所有要显示的draw出来
        glutMouseFunc(self.on_mouse)
        #glutIdleFunc(auto_rotate)  # 空闲调用
        glClearColor(0.1, 0.1, 0.5, 0.1)  # 背景颜色
        glutMainLoop()


