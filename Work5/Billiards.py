import math
import time
import sys
from sympy import solve, Symbol


class Ball():
    def __init__(self, x, y, r): # m
        self.x = float(x)
        self.y = float(y)
        self.r = float(r)
        # self.m = float(m)


class Hole():
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)


print('请输入必要的数据：\n' + '=' * 40)

ball_mother = Ball(
    x=input('母球的X坐标: '),
    y=input('母球的Y坐标: '),
    r=input('母球的半径: '),
   # m=input('母球的质量: '),
)

print('=' * 40)

ball_son = Ball(
    x=input('子球的X坐标: '),
    y=input('子球的Y坐标: '),
    r=input('子球的半径: '),
   # m=input('子球的质量: '),
)

print('=' * 40)

hole_goal = Hole(
    x=input('球洞的X坐标: '),
    y=input('球洞的Y坐标: ')
)

print('=' * 40)

coe_rotation = float(input('滚动摩擦系数：'))


def calc_angle_range():
    omega = math.degrees(
        math.atan(abs(ball_mother.y - ball_son.y) / abs(ball_mother.x - ball_son.x)))
   
    dist = math.sqrt(abs(ball_mother.x**2 - ball_son.x**2) +
                     abs(ball_mother.y**2 - ball_son.y**2))
   
    angle_range_top = omega + 2 * math.degrees(math.asin(2 * ball_mother.r / dist))
    angle_range_bottom = omega - 2 * math.degrees(math.asin(2 * ball_mother.r / dist))
    return round(angle_range_bottom, 3), round(angle_range_top, 3)

def angles():
    psi_son = math.degrees(math.atan(abs(hole_goal.y - ball_son.y) / abs(hole_goal.x - ball_son.x)))
    
    x_prior = ball_son.x - 2 * ball_mother.r * math.cos(psi_son)
    y_prior = ball_son.y - 2 * ball_mother.r * math.sin(psi_son)

    theta = math.degrees(math.atan(abs(y_prior - ball_mother.y) / abs(x_prior - ball_mother.x)))
    return round(theta, 3), psi_son

def verify():
    mini = calc_angle_range()[0]
    maxi = calc_angle_range()[1]

    if mini < angles()[0] < maxi:
        print('验证通过！\n --->')
    else:
        print('所得角度不在合理范围内，请检查数据/程序')
        sys.exit(0)

def calc_velocity():
    dist = math.sqrt((hole_goal.x - ball_son.x) ** 2 + (hole_goal.y - ball_son.y) ** 2)
    v_son_mini = math.sqrt(2 * coe_rotation * 9.8 * dist)
    
    v1 = Symbol('v1')
    v3 = Symbol('v3')
    answer = solve([v1 * math.sin(angles()[0]) - v_son_mini * math.sin(90 + angles()[1]) - v3 * math.sin(angles()[1]),
                    v1 * math.cos(angles()[0]) - v_son_mini * math.cos(90 + angles()[1]) - v3 * math.cos(angles()[1])]
                    , [v1,v3]
                )
    return round(abs(answer[v1]), 3)


print('=' * 40)

verify()
print(f'射击角度：{angles()[0]}')
print(f'射击角度范围：{calc_angle_range()} 内可以发生直接碰撞')
print(f'母球最小（实战时适当大一点）速度：{calc_velocity()} m/s')
print('Complete!')


