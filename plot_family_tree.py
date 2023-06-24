import matplotlib.pyplot as plt
import matplotlib
import numpy as np

class Person:
    """管理每个人信息的类，包括姓名、世代、后代"""
    
    def __init__(self, name, generation):
        self.name = name
        self.generation = generation
        self.children = []
        self.max_child_number = 1  # 代表人数最多的一辈有几个人
        
    def add_child(self, child):
        """添加自己的直系后代"""
        self.children.append(child)

def compare_child_number(person):
    return person.max_child_number
        
class FamilyTree:
    """家谱"""
    
    def __init__(self, root):
        self.root = root
        
        self.x_length = 0.2  # 横线单位长度
        self.y_height = 2.5  # 竖线长度
        self.y_word = 0.5  # 人名中每个字中心的竖向距离
        self.y1 = self.y_word / 5
        self.y2 = 0.4 #
        
    def add_child(self, parent, child):
        """添加一个人的直系后代"""
        parent.children.append(child)
        
    def read_family_tree(self):
        """从已有文件中读取家谱信息"""
        
        
    def plot_tree(self):
        """绘制族谱"""
        self.read_family_tree()
        
        fig, ax = plt.subplots()
        self._plot_person(ax, self.root)
        plt.axis('off')
        plt.show()
        
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

root = Person('思温', 1)
child1 = Person('仕忠', 2)
child2 = Person('仕贤', 2)
grandchild1 = Person('敏', 3)

family_tree = FamilyTree(root)
family_tree.add_child(root, child1)
family_tree.add_child(root, child2)
family_tree.add_child(child1, grandchild1)

family_tree.plot_tree()