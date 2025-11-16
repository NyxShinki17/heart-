下面是一份简明的中文使用说明，覆盖运行环境、如何运行、可配置项、常见问题与自定义提示。

前提条件

已安装 Python（推荐 3.8+）。
Windows 自带的 Tkinter 通常随 Python 一起安装。如果你的环境缺少 Tkinter，请安装或使用 Python 安装器重新安装带 Tkinter 的版本。
如何运行

打开 PowerShell，进入文件所在目录：
运行脚本：
程序将弹出一个黑色背景的窗口，显示动态心形粒子效果。
主要文件和功能简介

heart.py: 主脚本，包含心形几何计算、粒子散布、缩放与渲染逻辑。
常量：
CANVAS_WIDTH, CANVAS_HEIGHT：画布尺寸（像素）。
CANVAS_CENTER_X, CANVAS_CENTER_Y：画布中心坐标（根据宽高自动计算）。
IMAGE_ENLARGE：心形基准放大倍数（默认 11）。
HEART_COLOR：心形颜色（例如 "aquamarine"）。
关键函数：
heart_function(t, shrink_ratio=IMAGE_ENLARGE)：根据参数 t 计算心形上的点坐标。
scatter_inside(x, y, beta=0.15)：在心形内部做随机扩散，beta 控制扩散强度。
shrink(x, y, ratio)：对坐标施加收缩力（用于 halo）。
curve(p)：用于生成动画节奏的曲线函数。
主要类：Heart
__init__(generate_frame=20)：初始化并预生成若干帧（默认 20）。
build(number)：在心形边缘生成初始粒子点（number 个）。
calc(frame)：计算传入帧编号对应的粒子集合并缓存到 self.all_points。
render(canvas, frame)：在 Tkinter 画布上绘制指定帧的粒子点。
可配置项（快速修改）

改变画布大小：修改 CANVAS_WIDTH / CANVAS_HEIGHT。
修改心形大小：更改 IMAGE_ENLARGE。
修改颜色：更改 HEART_COLOR 为任何 Tkinter 支持的颜色字符串（例如 "#ff6699"）。
生成帧数：在创建 Heart() 实例时传入不同 generate_frame（例如 Heart(generate_frame=40)）以得到更平滑但更耗内存的动画。
性能注意

程序在初始化时会生成较多粒子（默认 build(2000)），这会消耗 CPU 和内存。适当减小 build() 的参数和 generate_frame 可提升启动速度。
如果卡顿：尝试减小 halo_number、减少 build() 的数目，或减小 generate_frame。
常见问题与排查

错误：TypeError: scatter_inside() takes from 2 to 3 positional arguments but 4 were given
触发原因：调用 scatter_inside 时误将小数写成 0,27（逗号），应为 0.27（小数点）。已在代码中修复。
错误：ModuleNotFoundError: No module named 'tkinter'
触发原因：Python 安装未包含 Tkinter。解决：安装或重新安装带 Tkinter 的 Python 发行版，或在 Linux 上安装系统 Tk 包（例如 sudo apt install python3-tk）。
如果窗口一闪而过或没有显示，确认是运行环境（PowerShell）没有错误输出，或尝试在命令行直接执行并查看报错信息。
小贴士（自定义）

改变粒子颜色随帧变化：在 render 内使用 render_canvas.create_rectangle(..., fill=some_color_func(frame))，通过帧号计算颜色渐变。
保存为图片序列 / GIF：可在 render 内将 Canvas 存为图像（例如使用 Pillow 将 canvas.postscript() 转为图片），然后合成为 GIF（另需实现保存逻辑）。
减少内存：将 generate_frame 设置为较小值并在 draw 中增加帧间隔（main.after(10, ...)）降低 CPU 占用
