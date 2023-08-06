'''
    字典是一个内置的数据结构，允许将数据与键而不是数字关联，这样可以使用内存中的数据与实际数据的结构保持一致，映射，散列，关联数组实际上就是指字典
'''
'''
    使用类有助于降低复杂性，降低复杂性意味着bug更少，bug更少意味着代码更可维护
'''

'''
    python遵循标准的面向对象编程模型，提供了一种方法允许将代码及其处理的数据定义一个类，
    一旦有了类的定义，就可以用它来创建数据对象，它会继承类的特性

    在面向对象的世界里，函数称为类的方法，数据称为累的属性，实例化的数据对象称为实例
'''

class Athlete:

    def __init__(self, name, dob=None, times=[]):

        self.name = name
        self.dob = dob
        self.times = times

    def top3(self):

        times = sorted((set([getrightitem(item) for item in self.times])))[:3]
        return times

    def add_time(self, time):

        self.times.append(time)

    def add_times(self, times):

        self.times.extend(times)
        

def getfiles(file):

    try:
        with open(file) as filedoc:

            file_list = filedoc.readline().strip().split(',')
            file_dict = {"name": file_list.pop(0), "dob": file_list.pop(0),
                         "times": file_list}
            return file_dict
    except IOError as error:

        print('error' + str(error))
        return None

def getrightitem(item):

    if '-' in item:
        splitter = '-'
    elif ':' in item:
        splitter = ':'
    else:
        return item

    return item.replace(splitter, '.')

files = ['../PythonNewTest/newscores/james2.txt',
         '../PythonNewTest/newscores/julie2.txt',
         '../PythonNewTest/newscores/mikey2.txt',
         '../PythonNewTest/newscores/sarah2.txt']

for item in files:

    data_item = getfiles(item)
    data = Athlete(data_item['name'], data_item['dob'], data_item['times'])
    print(data.name + "'s fastest times are:", data.times)
    print("The fastest three times are:", data.top3())


vera = Athlete('Vera')
vera.add_time('1.31')
print(vera.top3())
vera.add_times(['2.22', '1-21', '2:22'])
print(vera.top3())

