import random
from math import sin, cos, pi, log
from tkinter import *

CANVAS_WIDTH = 840
CANVAS_HEIGHT = 680
CANVAS_CENTER_X = CANVAS_WIDTH / 2
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2
IMAGE_ENLARGE = 11

HEART_COLOR = "aquamarine"

def heart_function(t, shrink_ratio: float = IMAGE_ENLARGE):
    """
    爱心函数生成器 (Trình tạo hàm trái tim)
    :param shrink_ratio: 放大比例 (Tỉ lệ phóng to)
    :param t: 参数 (Tham số)
    :return: 坐标 (Tọa độ)
    """
    x = 17 * (sin(t) ** 3)
    y = -(16 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(3 * t))

    x*=IMAGE_ENLARGE
    y*=IMAGE_ENLARGE

    x += CANVAS_CENTER_X
    y += CANVAS_CENTER_Y

    return int(x), int(y)


def scatter_inside(x, y, beta=0.15):
    """
    随机内部扩散
    :param x: 原x
    :param y: 原y
    :param beta: 强度
    :return: 新坐标
    """
    ratio_x = -beta * log(random.random())
    ratio_y = -beta * log(random.random())

    dx = ratio_x * (x - CANVAS_CENTER_X)
    dy = ratio_y * (y - CANVAS_CENTER_Y)
    
    return x - dx, y - dy

def shrink(x,y, ratio):
    """
    坐标缩小
    :param x: 原x
    :param y: 原y
    :param ratio: 缩小比例
    :return: 新坐标
    """
    force = -1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.6)
    dx = ratio * force * (x - CANVAS_CENTER_X)
    dy = ratio * force * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy

def curve(p):
    """
    爱心曲线
    :param p: 参数
    :return: 坐标
    """
    return 2 * (2 * sin(4 *p)) / (2 * pi)

class Heart:
    """
    爱心类
    爱心类
    """
    
    def __init__(self,generate_frame=20):
        self._points = set()
        self._edge_diffusion_points = set()
        self._center_diffusion_points = set()
        self.all_points = {}
        self.build(2000)

        self.random_halo = 1000

        self.generate_frame = generate_frame
        for frame in range(self.generate_frame):
            self.calc(frame)
    
    def build(self, number):

        for _ in range(number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t)
            self._points.add((x, y))
        
        for _x, _y in self._points:
            for _ in range(3):
                x, y = scatter_inside(_x, _y, 0.27)
                self._center_diffusion_points.add((x,y))
    
    @staticmethod
    def calc_position(x, y, ratio):

        force = 1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.420)

        dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-1,1)
        dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-1,1)

        return x - dx, y - dy
    
    def calc(self, generate_frame):
        ratio = 15 * curve(generate_frame / 10 * pi)

        halo_radius = int(4 +  6 * (1 + curve (generate_frame / 10* pi)))
        halo_number = int(3000 + 4000 * abs(curve(generate_frame / 10 * pi) ** 2))

        all_points = []

        heart_halo_points = set()
        for _ in range(halo_number):
            t = random.uniform(0,2 * pi)
            x,y = heart_function(t, shrink_ratio=-15)
            x,y = shrink(x, y, halo_radius)

            heart_halo_points.add((x,y))
            x += random.randint(-60, 60)
            y += random.randint(-60, 60)
            size = random.choice((1, 1, 2))
            all_points.append((x, y, size))
            all_points.append((x+20, y+20, size))
            all_points.append((x-20, y-20, size))
            all_points.append((x+20, y-20, size))
            all_points.append((x-20, y+20, size))
        
    
        for x,y in self._points:
            x,y =  self.calc_position(x, y, ratio)
            size = random.randint(1,3)
            all_points.append((x, y, size))

        for x,y in self._center_diffusion_points:
            x,y =  self.calc_position(x, y, ratio)
            size = random.randint(1,2)
            all_points.append((x, y, size))

        self.all_points[generate_frame] = all_points

    def render(self, render_canvas, render_frame):
        for x, y, size in self.all_points[render_frame % self.generate_frame]:
            render_canvas.create_rectangle(x, y, x + size, y + size, width=0, fill=HEART_COLOR)


def draw(main: Tk, render_canvas: Canvas, render_heart: Heart, render_frame=0):
    render_canvas.delete("all")
    render_heart.render(render_canvas, render_frame)
    main.after(1, draw, main, render_canvas, render_heart, render_frame + 1)


if __name__ == "__main__":
    root = Tk()
    canvas = Canvas(root, bg='black', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
    canvas.pack()
    heart = Heart()
    draw(root, canvas, heart)
    root.mainloop()