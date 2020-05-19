import math
import sys

def confirm(x1,y1,x2,y2,x3,y3):
    print(f"母球：({x1},{y1}) ｜ 被击球({x2},{y2}) | 球袋({x3},{y3})")
    print('=' * 40)

x1 = float(input('母球的x坐标：'))
y1 = float(input('母球的y坐标：'))

x2 = float(input('被击球的x坐标：'))
y2 = float(input('被击球的y坐标：'))

x3 = float(input('目标球袋的x坐标：'))
y3 = float(input('目标球袋的y坐标：'))

r = float(input('台球的半径：'))

print('=' * 40)
confirm(x1,y1,x2,y2,x3,y3)

d_squared = float(math.fabs(x1-x2) ** 2 + math.fabs(y1-y2) ** 2)
distance = math.sqrt(d_squared)
print(f'两球间距:{round(distance,3)}')

#初始时刻两球连线与x轴夹角
omega_degree = math.degrees(math.atan(math.fabs(y1-y2) / math.fabs(x1-x2)))

if y1 < y2 <y3 or y3 < y2 < y1:
    feasibility = True
else:
    feasibility = False

if not feasibility:
    print('此情况下需要经过撞墙')
    sys.exit(0)

dx = math.fabs(x2-x3)
dy = math.fabs(y2-y3)
psi1_rad = math.atan(dy / dx)
psi1_degree = math.degrees(psi1_rad)
print(f'被击球弹射角度：{psi1_degree}')

psi2_degree = 90 - psi1_degree
print(f'母球弹射角度：{psi2_degree}')

colli_x1 = x2 - 2 * r * math.cos(psi1_degree)
colli_y1 = y2 - 2 * r * math.sin(psi1_degree)

print(f'碰撞前母球位置：({round(colli_x1,3)},{round(colli_y1,3)})')

#射出角度
theta = math.degrees(math.atan(math.fabs(colli_y1-y1) / math.fabs(colli_x1-x1)))
print(f'射击的角度为：{round(theta,3)}')



