import matplotlib.pyplot as plt
import matplotlib

class Person:
    """管理每个人信息的类，包括姓名、世代、后代、个人编号"""
    def __init__(self, name, generation = -1, id = ""):
        self.name = name
        self.generation = generation
        self.ID = id # 个人身份编号
        
        self.children = [] # 存储子代person对象的列表
        self.x_person = 1  # 代表绘图时需要分配多大的横向空间
    
    def add_ID(self, id):
        self.ID = id
            
    def add_child(self, child):
        """添加自己的直系后代"""
        self.children.append(child)

def compare_x_person(person):
    return person.x_person
        
class FamilyTree:
    """家谱"""
    def __init__(self, root):
        self.root = root
        self.dict = {}
        
        self.font_size = 6 # 人名的字体大小
        self.line_width = 0.2 # 控制线宽
        self.x_length = 1  # 横线单位长度
        self.y_height = 0.8  # 竖线长度
        self.y_word = 0.4  # 人名中每个字中心的竖向距离
        self.y1 = 0.1 # 子代名字离下方竖线距离微调，增大该值则距离减小
        self.y2 = 0.4 # 子代名字离上方竖线距离微调，增大该值则距离增大
        
        # 先将root加入到字典中
        if root.ID:
            self.dict[root.ID] = root 
        
    def add_child(self, parent, child):
        """添加一个人的直系后代"""
        parent.children.append(child)
                     
    def plot_tree(self):
        """绘制族谱"""
        # 从文件中读取
        self._read_family_tree()
        
        self._count_children(self.root) # 遍历整个族谱获取每个人要分配的横向距离 
        self._output_all_x_person() # 输出每个人的横向距离进行验证
        
        # 绘制
        fig, ax = plt.subplots()
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
        fig.set_size_inches(100, 25)
        self._plot_person(ax, self.root)
        plt.axis('off')
        fig.savefig('郑氏家谱.pdf', format='pdf')
        fig.savefig('郑氏家谱.png', format='png')
        # plt.show()
    
    def _output_all_x_person(self):
        """输出每个人需分配的横向距离"""
        with open('x_person.txt', 'w') as o:
            for key, value in self.dict.items():
                o.write(f"{value.name} : {value.x_person}\n")
    
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
                # if self.dict.get(strings[4], 0) and self.dict[strings[4]].name == strings[0]: # 如果字典中可以查到这个长辈
                if self.dict.get(strings[4], 0):
                    child = Person(strings[2], int(strings[3]), strings[5]) # 创建这个子代的实例
                    self.dict[strings[4]].add_child(child) # 添加到长辈的子代列表中
                    self.dict[strings[5]] = child # 将该子代添加到字典中
                else:
                    print("该行输入错误：{}".format(line))
                    if self.dict.get(strings[4], 0):
                        print(f"编号{strings[4]}对应的人名是：{self.dict[strings[4]].name}")
                    else:
                        print(f"编号{strings[4]}对应的人名不存在")
        
        # 可以通过下面的输出文件，验证读取文件的正确
        # with open('test.txt', 'w') as o:
        #     for key, value in self.dict.items():
        #         o.write(f"{value.name} :")
        #         for child in value.children:
        #             o.write(f" {child.name}")
        #         o.write("\n")
    
    def _count_children(self, person):
        """递归计算每个人所需分配的横向空间"""
        sum = 0
        if person.children:
            for child in person.children:
                self._count_children(child)
                sum += child.x_person

        if sum > 1:
            person.x_person = sum
        
    def _plot_person(self, ax, person, x=0, y=0):
        """绘制族谱中每个人的部分，递归调用"""
        self._plot_person_name(ax, person, x, y) # 绘制人名
           
        if person.children:
            x_arr, y_child_bottom = self._plot_connect_line(ax, person, x, y) # 绘制一个长辈到子代之间的连接线
            
            # if len(person.children) > 1:
            #     # 按照年龄从小到大排序
            #     sorted_children = sorted(person.children, key=compare_x_person)                
            #     # 绘制的时候children的child多的放中间，少的放两边                
                                
            for i, child in enumerate(person.children):
                x_child = x_arr[i]
                self._plot_person(ax, child, x_child, y_child_bottom - self.y2) # 递归

    def _plot_person_name(self, ax, person, x, y):
        """将人名拆成单个字符，依次从上到下绘制"""
        for i, char in enumerate(person.name):
            # 计算每个字符应该出现的位置
            y_name = y - i * self.y_word
            # 绘制单个字符
            ax.text(x, y_name, char, fontsize=self.font_size, ha='center', va='center')
    
    def _plot_connect_line(self, ax, person, x, y):
        """绘制一个长辈到子代之间的连接线"""
        # 先画一条竖线
        y_top = y - len(person.name) * self.y_word + self.y1  # 临时加减数字微调一下距离
        y_bottom = y_top - self.y_height
        ax.plot([x, x], [y_top, y_bottom], 'k-', linewidth=self.line_width)
        
        # 再画一条横线
        x_arr = self._trans_arr(person, x) # 表示每个子代的x方向位置 
        ax.plot([x_arr[0], x_arr[len(x_arr) - 1]], [y_bottom, y_bottom], 'k-', linewidth=self.line_width)
        
        # 再给每一个子代画一条竖线
        # x_arr = self._sort_x_arr(x_arr)
        y_child_bottom = y_bottom - self.y_height
        for i in range(0, len(x_arr), 1):     
            ax.plot([x_arr[i], x_arr[i]], [y_bottom, y_child_bottom], 'k-', linewidth=self.line_width)
            
        return x_arr, y_child_bottom
    
    def _trans_arr(self, person, x):
        """将相对位置转换为绝对位置"""
        x_arr_pre = self._calc_x_arr_pre(person)
        x_parent = self._calc_x_parent(person)
        x_arr = []
        for x_child in x_arr_pre:
            relative_dis = x_child - x_parent
            absolute_pos = x + relative_dis
            x_arr.append(absolute_pos)
        return x_arr
    
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
    
    def _sort_x_arr(self, arr_unsorted):
        """实现x_arr的重新排序，以满足孙代多的子代放在中间，少的放两边"""
        # 排序为从中心向两边，先左后右
        arr_sorted = arr_unsorted
        return arr_sorted   
                
# 设置中文字体
matplotlib.rcParams['font.family'] = ['SimHei']

root = Person('思温', 1, 'S0010001')
family_tree = FamilyTree(root)
family_tree.plot_tree()