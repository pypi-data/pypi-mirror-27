# PyLf
![](./demo/out/I_can_eat_glass.jpg) <br>
PyLf is a lightweight Python library for simulating Chinese handwriting. It introduces a great deal of randomness in the 
process of Chinese handwriting to simulate the uncertainty of glyphs written by human beings.
## For Windows users
* [Windows用户必读！](https://github.com/Gsllchb/PyLf/wiki/Windows%E7%94%A8%E6%88%B7%E5%BF%85%E8%AF%BB%EF%BC%81)
## Installation
由于PyLf的依赖项[Pillow](https://python-pillow.org/)会与[PIL](http://www.pythonware.com/products/pil/)发生冲突，
如若您已安装[PIL](http://www.pythonware.com/products/pil/)，请先**手动卸载**：

    pip uninstall PIL

此外如若您并未安装[setuptools](https://pypi.python.org/pypi/setuptools),请先**手动安装**：

    pip install setuptools

安装PyLf：

    pip install pylf

## Walk through

    from PIL import Image, ImageFont
    from pylf import handwrite
    # 设置模板的参数
    template = {
        # 选择背景图片（图片的大小应大于‘box’所限定的范围）
        'background': Image.open("./something.png"),  
        # 限定“手写”的范围的左、上、右、下边界的坐标（以左上角为坐标原点）
        'box': (0, 0, 100, 100),
        # RGB（取值0~255）
        'color': (0, 0, 0),  
        # 选择字体
        'font': ImageFont.truetype("./something.ttf"),  
        # 平均字体大小
        'font_size': 10,
        # 绝对值越大字体大小的随机性越强  
        'font_size_sigma': 0.1,
        # 行间距
        'line_spacing': 15,
        # 绝对值越大行间距大小的随机性越强  
        'line_spacing_sigma': 0.1,
        # 字间距
        'word_spacing': 10,
        # 绝对值越大字间距大小的随机性越强  
        'word_spacing_sigma': 0.1,
        # 判断一个字符是否仅占用正常水平位置的一半
        'is_half_char': lambda c: c.isdigit() or c in ('！', '.', '？', ',', '，', '。', ' '),
        # 判断一个字符是否不能放在写在行首
        'is_end_char': lambda c: c in ('！', '.', '？', ',' , '，', '。')
    }
    # 需要“手写”的文本
    text = """your context"""
    # 开始“手写”
    images = handwrite(text, template)
    # 显示每一张生成的图片
    for image in images:
        image.show()

## Demo
* 我能吞下玻璃而不伤身体 <br>
![I_can_eat_glass](./demo/out/I_can_eat_glass.jpg)
* 《荷塘月色》 <br>
![荷塘月色0](./demo/out/荷塘月色/0.jpg)
![荷塘月色1](./demo/out/荷塘月色/1.jpg)
