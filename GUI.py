#-*-coding:utf-8-*-
import Tkinter
import tkFileDialog, tkMessageBox
import database_handle as dbh
from cloud_reader import PcdReader

###------------have not finish ---------###

class AddProPage(Tkinter.Toplevel):
    def __init__(self, point_list):
        Tkinter.Toplevel.__init__(self)
        self.title('add new project')
        self.geometry("500x300+300+200")

        self.database_handle = dbh.DatabaseHandle()
        self.database_handle.create_project_table()

        self.name_input = ''
        self.filepath = Tkinter.StringVar()
        self.upload_flag = False

        label = Tkinter.Label(self, text='input project name')
        label.pack()

        self.entry = Tkinter.Entry(self)
        self.entry.pack()

        chose_button = Tkinter.Button(self, text='chose file', command=self.select_path)
        chose_button.pack()

        path_lable = Tkinter.Label(self, textvariable=self.filepath)
        path_lable.pack()

        upload_button = Tkinter.Button(self, text='upload', command=lambda: self.upload(point_list))
        upload_button.pack()

        create_button = Tkinter.Button(self, text='create', command=lambda: self.create_callback(point_list))
        create_button.pack()

    def create_callback(self, point_list):   #进行新建项目，并且读取文件的操作
        name_input = self.entry.get()
        if name_input == '':
            tkMessageBox.showinfo(message='name could not be null')
            return

        if not self.filepath.get():
            tkMessageBox.showinfo(message='chose file path first')
            return

        if not self.upload_flag:
            tkMessageBox.showinfo(message='should upload data')
            return

        pro_name = name_input
        pro_nums = len(point_list)
        pro_id = generate_id(pro_name)
        self.database_handle.insert_project(pro_name, pro_nums, pro_id)   #插入项目信息
        pro_data_table_name = pro_id + "_data"
        self.database_handle.create_pro_data_table(pro_data_table_name)   #新建项目的数据表
        self.database_handle.insert_data(pro_data_table_name, point_list)  #插入项目的点

        #value_list.append(name_input)
        self.destroy()   #结束，关闭

    def select_path(self):
        self.filepath.set(tkFileDialog.askopenfilename())

    def upload(self, point_list):
        cloud = PcdReader(self.filepath.get(), point_list)
        cloud.read()
        self.upload_flag = True

    @staticmethod
    def generate_id(pro_name):
        pass


class Mygui():
    def __init__(self):
        self.root = Tkinter.Tk()
        self.root.title('triangle restruct')
        self.root.geometry("500x300+300+200")
        self.root.minsize(300, 300)
        self.point_list = []
        self.tin = None
        self.select_pro_name = None
        self.select_pro_id = None

    def add_menu(self):
        self.menu = Tkinter.Menu(self.root)
        child_menu1 = Tkinter.Menu(self.menu)
        child_menu1.add_command(label=u'新建项目', command=self.callback_add_pro)
        child_menu1.add_command(label=u'选择项目', command=self.say)
        self.menu.add_cascade(label='file', menu=child_menu1)

        child_menu2 = Tkinter.Menu(self.menu)
        child_menu2.add_command(label=u'新建项目2')
        child_menu2.add_command(label=u'选择项目3')
        self.menu.add_cascade(label='caozuo', menu=child_menu2)

        self.root.config(menu=self.menu)   ###

    def callback_add_pro(self):
        AddProPage(self.point_list)  #读取的点放到point_list里

    def say(self):
        tkMessageBox.showinfo(message=len(self.point_list))

    def show(self):
        Tkinter.mainloop()


if __name__ == '__main__':

    gui = Mygui()
    gui.add_menu()
    gui.show()
