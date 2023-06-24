import matplotlib.pyplot as plt
import matplotlib
import numpy as np

class Person:
    """管理每个人信息的类，包括姓名、世代、后代、个人编号"""
    
    def __init__(self, name, generation = -1, id = ""):
        self.name = name
        self.generation = generation
        self.ID = id # 个人身份编号
        
        self.children = [] # 存储子代person对象的列表
        self.max_child_number = 1  # 代表人数最多的一辈有几个人
    
    def add_ID(self, id):
        self.ID = id
            
    def add_child(self, child):
        """添加自己的直系后代"""
        self.children.append(child)

def compare_child_number(person):
    return person.max_child_number
        
class FamilyTree:
    """家谱"""
    
    def __init__(self, root):
        self.root = root
        self.dict = {}
        
        self.x_length = 0.2  # 横线单位长度
        self.y_height = 2.5  # 竖线长度
        self.y_word = 0.8  # 人名中每个字中心的竖向距离
        self.y1 = 0.1 # 子代名字离下方竖线距离微调，增大该值则距离减小
        self.y2 = 0.7 # 子代名字离上方竖线距离微调，增大该值则距离增大
        
        # 先将root加入到字典中
        if root.ID:
            self.dict[root.ID] = root 
        
    def add_child(self, parent, child):
        """添加一个人的直系后代"""
        parent.children.append(child)
                     
    def plot_tree(self):
        """绘制族谱"""
        self._read_family_tree()
        
        fig, ax = plt.subplots()
        self._plot_person(ax, self.root)
        plt.axis('off')
        plt.show()
    
    def _read_family_tree(self):
        """从已有文件中读取家谱信息"""
        with open('jiapu.txt', 'r') as f:
            next(f) # 跳过前两行
            next(f)
            for line in f:
                # 对字符处理的准备工作
                line = line.rstrip('\n') # 去掉行尾的换行符
                strings = line.split('\t') # 分割字符串
                # 去掉每个字符串中的双引号
                for i, s in enumerate(strings):
                    new_string = s.replace('"', '')
                    strings[i] = new_string
                
                # 正式开工
                if self.dict.get(strings[4], 0): # 如果字典中可以查到这个长辈
                    child = Person(strings[2], int(strings[3]), strings[5]) # 创建这个子代的实例
                    self.dict[strings[4]].add_child(child) # 添加到长辈的子代列表中
                    self.dict[strings[5]] = child # 将该子代添加到字典中
                else:
                    print("该行输入错误：{}".format(line))
        
        # 可以通过下面的输出文件，验证读取文件的正确
        # with open('test.txt', 'w') as o:
        #     for key, value in self.dict.items():
        #         parent_name = value.name
        #         children = value.children
        #         o.write(f"{parent_name} :")
        #         for child in children:
        #             o.write(f" {child.name}")
        #         o.write("\n")
        
    def _plot_person(self, ax, person, x=0, y=0):
        """绘制族谱中每个人的部分，递归调用"""
        
        self._plot_person_name(ax, person, x, y) # 绘制人名
           
        if person.children:
            x_arr, y_bottom = self._plot_connect_line(ax, person, x, y) # 绘制一个长辈到子代之间的连接线
            
            # if len(person.children) > 1:
            #     # 按照年龄从小到大排序
            #     sorted_children = sorted(person.children, key=compare_child_number)
                
            #     # 绘制的时候children的child多的放中间，少的放两边
                
                                
            for i, child in enumerate(person.children):
                x_child = x_arr[i]
                y_child_bottom = y_bottom - self.y_height
                self._plot_person(ax, child, x_child, y_child_bottom - self.y2) # 递归

    def _plot_person_name(self, ax, person, x, y):
        """将人名拆成单个字符，依次从上到下绘制"""
        
        for i, char in enumerate(person.name):
            # 计算每个字符应该出现的位置
            y_name = y - i * self.y_word
            # 绘制单个字符
            ax.text(x, y_name, char, fontsize = 10, ha='center', va='center')
    
    def _plot_connect_line(self, ax, person, x, y):
        """绘制一个长辈到子代之间的连接线"""
        
        # 先画一条竖线
        y_top = y - len(person.name) * self.y_word + self.y1  # 临时加减数字微调一下距离
        y_bottom = y_top - self.y_height
        ax.plot([x, x], [y_top, y_bottom], 'k-')
        
        # 再画一条横线
        children_num = len(person.children)
        if (children_num % 2):
            half = (children_num // 2) * self.x_length  
        else:   
            half = (children_num // 2 - 0.5) * self.x_length
        x_left = x - half
        x_right = x + half   
        ax.plot([x_left, x_right], [y_bottom, y_bottom], 'k-')
        
        # 再给每一个子代画一条竖线
        # 下面的序列表示每个子代的x方向位置
        x_arr = np.arange(x_left, x_right + self.x_length + 0.001, self.x_length) # 加0.001是因为浮点数不准确，如果不加序列的最后一个数就没了
        # x_arr = self._sort_x_arr(x_arr)
        for i in range(0, len(x_arr) - 1, 1):
            y_child_bottom = y_bottom - self.y_height
            ax.plot([x_arr[i], x_arr[i]], [y_bottom, y_child_bottom], 'k-')
            
        return x_arr, y_bottom
    
    def _sort_x_arr(arr_unsorted):
        """实现x_arr的重新排序，以满足孙代多的子代放在中间，少的放两边"""
        
        # 排序为从中心向两边，先左后右
        arr_sorted = arr_unsorted
        return arr_sorted   
                
# 设置中文字体
matplotlib.rcParams['font.family'] = ['SimHei']

debug = 0

if debug:
    root = Person('思温', 1)
    child1 = Person('仕忠', 2)
    child2 = Person('仕贤', 2)
    grandchild1 = Person('敏', 3)
    ggrandchild1 = Person('彪', 4)
    ggrandchild2 = Person('宪', 4)
    ggrandchild3 = Person('常', 4)

    grandchild1.add_child(ggrandchild1)
    grandchild1.add_child(ggrandchild2)
    grandchild1.add_child(ggrandchild3)

    family_tree = FamilyTree(root)
    family_tree.add_child(root, child1)
    family_tree.add_child(root, child2)
    family_tree.add_child(child1, grandchild1)
else:
    root = Person('思温', 1, 'S0010001')
    family_tree = FamilyTree(root)

family_tree.plot_tree()