import random
import pandas as pd  # 需要安装 pandas 和 openpyxl

class Person:
    def __init__(self):
        self.x = random.randint(1, 100)
        self.y = random.randint(1, 100)

# 生成10个Person对象
people = [Person() for _ in range(10)]

# 提取数据到列表
data = []
for person in people:
    data.append({
        'x': person.x,
        'y': person.y
    })

# 创建DataFrame
df = pd.DataFrame(data)

# 导出到Excel文件
df.to_excel('person_data.xlsx')