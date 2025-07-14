import numpy as np
import pandas as pd

# 获取用户输入，带有默认值
def get_input_with_default(prompt, default):
    user_input = input(f"{prompt} (默认值: {default}，直接按Enter使用默认值): ")
    if user_input.strip() == "":
        return default
    try:
        return int(user_input)
    except ValueError:
        print(f"无效输入，使用默认值: {default}")
        return default

# 获取模拟参数
N_AGENTS = get_input_with_default("请输入模拟人数", 3000)
TIME_STEPS = get_input_with_default("请输入时间步长(年)", 40)

# 显示实际使用的参数
print(f"使用模拟人数: {N_AGENTS}")
print(f"使用时间步长: {TIME_STEPS}年")

# 其他参数
INIT_WEALTH = 10.0

# data for simulate_capacity
mu = 0.6
sigma = 0.1
# np.random.seed(2022)

def simulate_capacity(mu_SimCap = 0.6, sigma_SimCap = 0.1):
    """
    Simulates the capacity of a system using a Gaussian distribution.
    The function generates a random number from a Gaussian distribution with mean `mu` and standard deviation `sigma`.
    The generated number is constrained to be between 0 and 1 (exclusive).
    """
    random_number = 1
    while (random_number >= 1 or random_number <= 0):
        random_number = np.random.normal(mu_SimCap, sigma_SimCap)
    return random_number


class Person:
    """
    Represents a person in the simulation.
    Each person has a random position (x, y) and a capacity determined by a Gaussian
    """
    def __init__(self):
        self.x = np.random.randint(1, 101)
        self.y = np.random.randint(1, 101)
        self.capacity = simulate_capacity(mu, sigma)
        self.count_lucky = 0
        self.count_lucky_and_success = 0
        self.count_unlucky = 0
        self.count_unlucky_and_be_impacted = 0
        self.wealth = INIT_WEALTH

    def lucky_case(self):
        self.count_lucky += 1
        if self.capacity > np.random.random():
            self.count_lucky_and_success += 1
            self.wealth *= 2

    def unlucky_case(self):
        self.count_unlucky += 1
        if self.capacity < np.random.random():
            self.count_unlucky_and_be_impacted += 1
            self.wealth /= 2
        # self.wealth /= 2

    def is_case_impact(self, x_case, y_case):
        if (abs(x_case - self.x) < 10) and (abs(y_case - self.y) < 10):
            return True
        else:
            return False

people = [Person() for _ in range(N_AGENTS)]

# lucky_case
for _ in range(TIME_STEPS):
    x_case = np.random.randint(1, 101)
    y_case = np.random.randint(1, 101)
    for person in people:
        if person.is_case_impact(x_case, y_case):
            person.lucky_case()

# unlucky_case
for _ in range(TIME_STEPS):
    x_case = np.random.randint(1, 101)
    y_case = np.random.randint(1, 101)
    for person in people:
        if person.is_case_impact(x_case, y_case):
            person.unlucky_case()

# Prepare data for export
data = []
for person in people:
    data.append({
        'x': person.x,
        'y': person.y,
        'capacity': person.capacity,
        'wealth': person.wealth,
        'lucky_count': person.count_lucky,
        'lucky_and_success_count': person.count_lucky_and_success,
        'unlucky_count': person.count_unlucky,
        'unlucky_and_be_impacted_count': person.count_unlucky_and_be_impacted
    })

# Create a DataFrame
df = pd.DataFrame(data)

# Export to Excel file
df.to_excel('person_data.xlsx')

# 财富排序与统计分析
# 按财富降序排列
df_sorted = df.sort_values(by='wealth', ascending=False)

# 计算财富总和
total_wealth = df['wealth'].sum()

# 计算前20%人的人数
top_percent = 0.2
top_count = int(N_AGENTS * top_percent)

# 计算前20%人的财富总和
top_wealth = df_sorted['wealth'].head(top_count).sum()
top_wealth_capacity_avg = df_sorted['capacity'].head(top_count).mean()

# 输出统计结果
print("\n财富统计分析:")
print(f"所有{N_AGENTS}人的财富总和: {total_wealth:.2f}")
print(f"前{top_percent*100:.0f}%（{top_count}人）的财富总和: {top_wealth:.2f}")
print(f"前{top_percent*100:.0f}%人口占有总财富的{(top_wealth/total_wealth)*100:.2f}%")
print(f"前{top_percent*100:.0f}%人口的平均天赋值: {top_wealth_capacity_avg:.4f}")

# 可选：展示前10名最富有的人
print("\n财富排行榜前10名:")
top_10 = df_sorted[['wealth', 'capacity']].head(10).reset_index(drop=True)
for i, row in top_10.iterrows():
    print(f"第{i+1}名: 财富 = {row['wealth']:.2f}, 能力值 = {row['capacity']:.4f}")

# 计算前十富有的人的天赋平均数
top_wealth_capacity_avg = top_10['capacity'].mean()
print(f"\n财富前10名的人的天赋平均值: {top_wealth_capacity_avg:.4f}")

# 按天赋降序排列
df_capacity_sorted = df.sort_values(by='capacity', ascending=False)

# 获取天赋最高的前十人
top_capacity_10 = df_capacity_sorted[['wealth', 'capacity']].head(10).reset_index(drop=True)

# 计算天赋最高的前十人的财富和
top_capacity_wealth_sum = top_capacity_10['wealth'].sum()
print(f"\n天赋前10名的人的财富总和: {top_capacity_wealth_sum:.2f}")
print(f"天赋前10名的人占总财富的{(top_capacity_wealth_sum/total_wealth)*100:.2f}%")

# 展示天赋前10名
print("\n天赋排行榜前10名:")
for i, row in top_capacity_10.iterrows():
    print(f"第{i+1}名: 天赋值 = {row['capacity']:.4f}, 财富 = {row['wealth']:.2f}")

# 计算相关性
correlation = df['capacity'].corr(df['wealth'])
print(f"\n天赋与财富的相关系数(r):{correlation:.4f}")

# 查找同时在财富前十和天赋前十的人
wealth_top10_capacities = set(top_10['capacity'])
capacity_top10_capacities = set(top_capacity_10['capacity'])

# 查找交集
common_capacities = wealth_top10_capacities.intersection(capacity_top10_capacities)

print("\n是否有人同时在财富前十和天赋前十:")
if common_capacities:
    print(f"有 {len(common_capacities)} 人同时在两个前十名单中!")
    for capacity in common_capacities:
        wealth_info = top_10[top_10['capacity'] == capacity]
        capacity_info = top_capacity_10[top_capacity_10['capacity'] == capacity]
        
        wealth_rank = wealth_info.index[0] + 1
        capacity_rank = capacity_info.index[0] + 1
        wealth_value = wealth_info['wealth'].values[0]
        
        print(f"  - 天赋值: {capacity:.4f}, 财富排名: 第{wealth_rank}名, 天赋排名: 第{capacity_rank}名, 财富值: {wealth_value:.2f}")
else:
    print("没有人同时在财富前十和天赋前十")

input("按Enter键退出...")