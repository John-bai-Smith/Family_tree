import matplotlib.pyplot as plt, os,matplotlib
from tkinter.filedialog import *
from matplotlib.backends.backend_pdf import PdfPages
#from decorator import timer
matplotlib.use("Agg")

class Person:
    """管理每个人信息的类，包括姓名、世代、后代、个人编号"""

    def __init__(self, ration, name, generation=-1, parentID="", id=""):
        self.ration = ration
        self.name = name
        self.generation = generation
        self.parentID = parentID
        self.ID = id  # 个人身份编号
        self.children = []  # 存储子代person对象的列表
        self.x_person = 1  # 代表绘图时需要分配多大的横向空间
        self.x_position = 0 # 代表绘图时的横坐标位置

    def add_ID(self, id):
        self.ID = id

    def add_child(self, child):
        """添加自己的直系后代"""
        self.children.append(child)

class FamilyTree:
    """绘制家谱吊线图"""

    def __init__(self, page, filepath):
        self.arr=[]
        self.page = page
        self.dict = {}
        self.filepath = filepath # 操作的文件路径
        self.filename = os.path.splitext(os.path.basename(self.filepath))[0] # 操作的文件名
        self.coding = "utf-8"
        self.font_size = 13  # 人名的字体大小
        self.line_width = self.font_size / 50  # 控制线宽
        self.x_length = self.font_size / 58  # 横线单位长度
        self.y_height = self.font_size / 50  # 竖线长度
        self.y_word = self.font_size / 40  # 人名中每个字中心的竖向距离
        self.y1 = self.font_size / 75  # 子代名字离下方竖线距离微调，增大该值则距离减小
        self.y2 = self.font_size / 75  # 子代名字离上方竖线距离微调，增大该值则距离增大
        self.page_num = 1 # 某世--某世第几页
        self.pagenum = 8 # 每页世系总数
        self.first_ancestor = '' # 始祖名讳
        self.last = 1 # 最后一个成员的世系
        self.start = 1 # 第一个成员的世系数
        self.end = self.start + self.pagenum # 每页结束世系数
        self.page_width = 36 # 每页基础成员数量
        self.width = 0 # 画布宽度
        self.height = 0 # 画布高度

    def add_child(self, parent, child):
        """添加一个人的直系后代"""
        parent.children.append(child)
  
    def loca(self,num): # 定位指定世系的位置
        for i,char in enumerate(self.arr):
            if num == int(char[3]):
                return i
            
    def readTxtFile(self,FileName): # 文件转列表
        """将指定文本文件去掉行尾的换行符后以指定的分隔符转换成列表"""
        with open(FileName, mode='r',encoding=self.coding) as f:
            return [char.rstrip('\n').split('\t') for char in f]
    
    #@timer
    def draw_family(self): # 生成跨度8世的字典，绘制吊线图
        self.arr = self.readTxtFile(self.filepath)
        self.first_ancestor = self.arr [0][2] # 始祖名讳
        self.last = int(self.arr[len(self.arr)-1][3]) + 1 # 最后一个成员的世系
        self.start = int(self.arr[0][3]) # 第一个成员的世系数
        self.end = self.start + self.pagenum # 每页结束世系数
        pdf = PdfPages(self.filename + '分页吊线图.pdf')
        self.start = int(self.arr[0][3]) # 每页起始世系数
        self.end = self.start + self.pagenum # 每页结束世系数
        if self.end > self.last:
            self.end = self.last
        i = 0
        while 1:
            if i>= len(self.arr):
                if flag:
                    self.page_num = 1
                    self.page_family(pdf)
                else:
                    self.plot_tree(self.root,self.dict,pdf)
                break
            if int(self.arr[i][3]) == self.end:
                if flag:
                    self.page_num = 1
                    self.page_family(pdf)
                else:
                    self.plot_tree(self.root,self.dict,pdf)
                self.start = self.end - 1
                self.end = self.start + self.pagenum
                if self.end > self.last:
                    self.end = self.last
                i = self.loca(self.start) # 定位起始的位置
            elif len(self.dict) < 1:
                if self.start == int(self.arr[i + 1][3]): # 创建虚拟的始祖，并加入字典
                    self.root,self.dict,sum = self.init_dict()
                    flag = True
                    # print("添加虚拟始祖",self.root.ID)
                else:
                    self.root = Person(self.arr[i][1], self.arr[i][2], self.arr[i][3], self.arr[i][4], self.arr[i][5])
                    self.dict[self.root.ID] = self.root
                    flag = False
                    # print("添加真实始祖",self.root.name)
                    i += 1
                self.create_dict(self.arr[i],flag)  
                i += 1  
            else:
                self.create_dict(self.arr[i],flag)
                i += 1
        pdf.close()

    def init_dict(self): # 初始化临时字典并赋值
        dict = {}
        root = Person("", "", self.start, "", "S0"+str(self.start)+"000a")
        dict[root.ID] = root
        return root,dict,0
                
    def page_family(self,pdf): # 依据累计宽度生成临时字典，并绘制该字典
        self._count_children(self.root) 
        root,dict,sum = self.init_dict()
        for key, value in self.dict.items():
            for child in value.children:
                dict[root.ID].add_child(child)
                sum += child.x_person
                if sum >= self.page_width: 
                    self.plot_tree(root,dict,pdf)
                    root,dict,sum = self.init_dict()
                    self.page_num += 1
            if sum:
                self.plot_tree(root,dict,pdf)
                self.page_num += 1
            break

    def create_dict(self,char,flag):
        """创建字典"""
        root = Person(char[1], char[2], int(char[3]), char[4], char[5])
        if flag and self.start == int(char[3]):
            self.dict[self.root.ID].add_child(root)
            self.dict[char[5]] = root
        elif self.dict.get(char[4], 0) and int(char[3]) > self.start:
                self.dict[char[4]].add_child(root)  # 添加到长辈的子代列表中
                self.dict[char[5]] = root  # 将该子代添加到字典中
        else:
            print("该行输入错误：{}".format(char))
            if self.dict.get(char[4], 0):
                print(f"编号{char[4]}对应的人名是：{self.dict[char[4]].name}")
            else:
                print(f"编号{char[4]}对应的人名不存在")

        # 可以通过下面的输出文件，验证读取文件的正确
        # with open('test.txt', mode='w',encoding=self.coding) as o:
        #     for key, value in self.dict.items():
        #         o.write(f"{value.name} :")
        #         for child in value.children:
        #             o.write(f" {child.name}")
        #         o.write("\n")

    def plot_tree(self,root,dict,pdf):
        """绘制族谱"""
        self._count_children(root)  # 遍历整个族谱获取每个人要分配的横向距离
        self._count_x_position(root) # 遍历整个族谱，计算每个人的横坐标
        # self._output_all_x_person(dict) # 输出每个人的横向距离进行验证
        # 绘制
        if root.x_person < self.page_width:
             self.width = self.page_width / 52 * self.font_size  # 画布宽度设为始祖宽度与字体大小相关
        else:
            self.width = root.x_person / 52 * self.font_size  # 画布宽度设为始祖宽度与字体大小相关
        if self.end - self.start >= 7:
            self.height = (self.end - self.start) / 8.1 * self.font_size  # 画布高度设为代数与字体大小相关
        else:
            self.height = self.font_size / 1.06 # 画布高度设为代数与字体大小相关
        # 页面设置
        plt.style.use('bmh')
        plt.rcParams['font.family'] = ['kaiti']
        fig, ax = plt.subplots()
        ax.axis([-self.width / 2, self.width / 2, 1, self.height])
        ax.axis('off')
        fig.subplots_adjust(left=0, right=1, bottom=0.01, top=0.99)
        fig.set_size_inches(self.width, self.height)
        # 页面标识
        char = '温县后街郑氏四门族谱' + "   第"+str(self.page)+"页   " + self.first_ancestor + "祖 " + str(self.start) + " 世 -- " + str(self.end - 1) + " 世 第" + str(self.page_num) + "页"
        ax.text(-self.width / 15,  self.height - self.y_word * 6, char, fontsize=self.font_size+3, ha='center', va='center')
        if root.name:
            self._plot_person(ax, fig, root, self.height - self.y_word * 8)
        else:
            self._plot_person(ax, fig, root, self.height - self.y_word * 5)
        pdf.savefig(fig)
        self.page += 1
        self.dict.clear()
        plt.close()        

    def _output_all_x_person(self, dict):
        """输出每个人需分配的横向距离"""
        with open('x_person.txt', mode='w',encoding=self.coding) as o:
            for key, value in dict.items():
                o.write(f"{value.name} : {value.x_person}\n")

    def _count_children(self, person):
        """递归计算每个人所需分配的横向空间"""
        sum = 0
        if person.children and int(person.generation) < self.end:
            for i, child in enumerate(person.children):
                self._count_children(child)
                sum += child.x_person         
        if sum > 1:
            person.x_person = sum

    def _count_x_position(self, person):
        """确定每个人名字的横坐标"""
        num = len(person.children) 
        if num > 0 and int(person.generation) < self.end:
            self._calc_children_x_position(person)  # 先按照 父代横坐标在总分配空间中间 的方式计算子代的横坐标
            
            for child in person.children:    
                self._count_x_position(child) # 进入下一子代
                
            # 当从子代的递归返回后，根据子代横坐标对父代的横坐标进行修正
            if num > 1:
                x_left_children = person.children[0].x_position
                x_right_children = person.children[-1].x_position
                person.x_position = (x_left_children + x_right_children) / 2    
            else:
                person.x_position = person.children[0].x_position       
    
    def _plot_person(self, ax, fig, person, y = 0):
        """绘制族谱中每个人的部分，递归调用"""
        x = person.x_position       
        if int(person.generation) >= self.start:
            if person.ration == "嗣孙":
                y -= self.y_word + self.y2 + self.y1
                y_top = y + 2 * self.y_word + 1.1 * self.y1  # 名字少于两个字的按两个字算距离
                y_bottom = y_top - 3 * self.y_height - self.y2 - 1.22 * self.y1
                ax.plot([x, x], [y_top, y_bottom], 'k-', linewidth=self.line_width)
                y -= self.y_word + self.y2                   
        if person.name: # 虚拟的始祖不绘制
            self._plot_person_name(ax, person, y)  # 绘制人名
        if person.children and int(person.generation) < self.end:
            y_child_bottom = self._plot_connect_line(ax, person, y)  # 绘制一个长辈到子代之间的连接线
            for child in person.children:
                self._plot_person(ax, fig, child, y_child_bottom - self.y2)  # 递归              

    def _plot_person_name(self, ax, person, y):
        """将人名拆成单个字符，依次从上到下绘制"""
        for i, char in enumerate(person.name):
            # 计算每个字符应该出现的位置
            y_name = y - i * self.y_word
            # 绘制单个字符
            ax.text(person.x_position, y_name, char, fontsize=self.font_size, ha='center', va='center')

    def _plot_connect_line(self, ax, person, y):
        """绘制一个长辈到子代之间的连接线"""
        num = len(person.children)
        
        # 先画一条竖线
        y_top = y - 2 * self.y_word + self.y1  # 名字少于两个字的按两个字算距离
        y_bottom = y_top - self.y_height
        if person.name: # 虚拟的始祖不绘制
            ax.plot([person.x_position, person.x_position], [y_top, y_bottom], 'k-', linewidth=self.line_width)

        # 再画一条横线
        if person.name and num > 1: # 虚拟的始祖不绘制
            ax.plot([person.children[0].x_position, person.children[-1].x_position], [y_bottom, y_bottom], 'k-', linewidth=self.line_width)

        # 再给每一个子代画一条竖线
        y_child_bottom = y_bottom - self.y_height
        if person.name: # 虚拟的始祖不绘制
            for i in range(0, num, 1):
                ax.plot([person.children[i].x_position, person.children[i].x_position], [y_bottom, y_child_bottom], 'k-', linewidth=self.line_width)
        return y_child_bottom

    def _calc_children_x_position(self, person):
        """将相对位置转换为绝对位置"""
        x_arr_pre = self._calc_x_arr_pre(person)
        x_parent = self._calc_x_parent(person)
        x_arr = []
        for i, x_child in enumerate(x_arr_pre):
            relative_dis = x_child - x_parent
            absolute_pos = person.x_position + relative_dis
            person.children[i].x_position = absolute_pos

    def _calc_x_parent(self, person):
        """计算父代的相对位置"""
        max_num = person.x_person - 1
        x_parent = self._calc_center_pos(max_num)
        return x_parent

    def _calc_x_arr_pre(self, person):
        """计算子代的相对位置"""
        x_arr_pre = []
        base_len = 0
        for child in person.children:
            max_num = child.x_person - 1
            x_child = base_len + self._calc_center_pos(max_num)
            x_arr_pre.append(x_child)
            base_len += child.x_person * self.x_length
        return x_arr_pre

    def _calc_center_pos(self, num):
        """计算中心位置"""
        if (num % 2):
            pos = (num // 2) * self.x_length
        else:
            pos = (num // 2 - 0.5) * self.x_length
        return pos


if __name__ == "__main__":
    # 设置中文字体
    page = 97
    filepath = askopenfilename()
    family_tree = FamilyTree(page, filepath)
    family_tree.draw_family()