import turtle
import numpy as np

# 电机参数（示例值，需要根据实际情况调整）
Kp_values = [1.0, 2.0, 3.0]  # 比例增益值
Ki_values = [0.1, 0.2, 0.3]  # 积分增益值
Kd_values = [0.05, 0.1, 0.15]  # 微分增益值

# PID控制器初始化
class PIDController:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.set_point = 0
        self.p_error = 0
        self.i_error = 0
        self.last_error = 0

    def update(self, measured_value):
        # 计算误差
        error = self.set_point - measured_value
        self.i_error += error
        d_error = error - self.last_error

        # 计算PID输出
        output = self.Kp * error + self.Ki * self.i_error + self.Kd * d_error
        self.last_error = error
        return output

    def set_setpoint(self, set_point):
        self.set_point = set_point

# 电机模型（简化版）
class Motor:
    def __init__(self, Kt):
        self.Kt = Kt  # 电机转矩常数
        self.speed = 0

    def update(self, control_signal):
        # 简化的电机动态模型
        self.speed += self.Kt * control_signal  # 假设控制信号直接影响速度

# 主程序
def main():
    # 初始化turtle屏幕
    screen = turtle.Screen()
    screen.setup(1200, 800)  # 设置图像大小
    screen.title("PID Speed Control")

    # 设置目标速度
    target_speed = 10  # 目标速度为10

    # 仿真参数
    time_steps = 200  # 时间步数
    dt = 0.05  # 时间步长

    # 存储数据
    time = np.linspace(0, time_steps * dt, time_steps)
    target_speeds = target_speed * np.ones(len(time))

    # 绘制目标速度
    target_pen = turtle.Turtle()
    target_pen.color("red")
    target_pen.penup()
    target_pen.goto(0, target_speed)
    target_pen.pendown()
    target_pen.forward(time_steps * dt)
    target_pen.hideturtle()

    # 绘制不同PID参数下的实际速度
    for Kp, Ki, Kd in zip(Kp_values, Ki_values, Kd_values):
        pid = PIDController(Kp, Ki, Kd)
        motor = Motor(Kt=0.5)  # 假设Kt=0.5
        pid.set_setpoint(target_speed)

        measured_speeds = np.zeros(len(time))
        control_signals = np.zeros(len(time))

        for i in range(time_steps):
            # PID控制器计算控制信号
            control_signal = pid.update(motor.speed)
            control_signals[i] = control_signal

            # 更新电机速度
            motor.update(control_signal)

            # 记录实际速度
            measured_speeds[i] = motor.speed

        # 绘制实际速度
        actual_pen = turtle.Turtle()
        actual_pen.color("blue")
        actual_pen.penup()
        actual_pen.goto(0, 0)
        actual_pen.pendown()
        for i in range(len(time)):
            actual_pen.forward(dt * 1200 / (time_steps * dt))  # 将时间转换为屏幕距离
            actual_pen.right(90)
            actual_pen.forward(measured_speeds[i] / 10 * 600)  # 将速度转换为屏幕距离
            actual_pen.right(90)
            actual_pen.forward(dt * 1200 / (time_steps * dt))
            actual_pen.left(90)
        actual_pen.hideturtle()

    # 设置坐标轴
    x_axis = turtle.Turtle()
    x_axis.color("black")
    x_axis.penup()
    x_axis.goto(0, 0)
    x_axis.pendown()
    x_axis.forward(time_steps * dt * 1200 / (time_steps * dt))  # 将时间转换为屏幕距离
    x_axis.hideturtle()

    y_axis = turtle.Turtle()
    y_axis.color("black")
    y_axis.penup()
    y_axis.goto(0, 0)
    y_axis.left(90)
    y_axis.pendown()
    y_axis.forward(20 * 600 / 10)  # 将速度转换为屏幕距离
    y_axis.hideturtle()

    # 显示图像
    screen.mainloop()


if __name__ == '__main__':
    main()