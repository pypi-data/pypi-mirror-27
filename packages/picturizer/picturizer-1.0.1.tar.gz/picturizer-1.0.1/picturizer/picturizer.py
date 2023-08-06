# coding: utf-8

import argparse
from PIL import Image

parser = argparse.ArgumentParser(prog='picturize')
parser.add_argument(
    '-i', # 短格式选项
    '--input', # 长格式选项
    metavar='source_path', # 参数占位说明符
    type=str, # 参数数据类型
    action='store', # 参数存储方式，值为常量，见文档
    dest='input_file', # 参数存储变量名
    required=True, # 是否强制需要
    nargs='?', # 参数消费个数，? 代表一个
    help='input file', # 选项帮助说明
)
parser.add_argument(
    '-o',
    '--output',
    metavar='store_path',
    type=str,
    action='store',
    dest='output_file',
    required=False,
    nargs='?',
    help='output file',
)
parser.add_argument(
    '-s',
    '--scale',
    metavar='a_scale',
    type=float,
    action='store',
    dest='scale',
    required=False,
    default=1, # 默认值
    nargs='?',
    help='scale of the picture, should be 0 < scale <= 1'
)
args = parser.parse_args()
input_file = args.input_file
output_file = args.output_file
scale = args.scale

OUTLINE_CHARS = list(r'$@&%B#=-. ') # 轮廓描绘字符
GRAY_RANGE = 256
GRAY_UNIT_RANGE = 256 / len(OUTLINE_CHARS) # 一个轮廓字符所管辖的灰度范围

def unit(r, g, b):
    gray = int((r * 19595 + g * 38469 + b * 7472) >> 16) # 计算灰度值
    outline_char_index = int(gray / GRAY_UNIT_RANGE)
    outline_char = OUTLINE_CHARS[outline_char_index]
    return outline_char

def outline(input_image, scale=1):
    source = Image.open(input_image)
    source_width, source_height = source.size
    output_width = int(source_width * scale)
    output_height = int(source_height * scale)

    source = source.resize((output_width, output_height), Image.NEAREST)
    outline = ''

    for height in range(output_height):
        for width in range(output_width):
            rgb = source.getpixel((width, height))[:3]
            outline += unit(*rgb)
        outline += '\n'
    
    return outline

def save_as_file(string_pic):
    if output_file:
        with open(output_file, 'w+') as f:
            f.write(string_pic)
        print('😀 picture has been saved to' + output_file)
    else:
        print('🤨 output file is not defined, so just print it out')

def picturize():
    pic = outline(input_file, scale)
    print(pic)
    save_as_file(pic)

if __name__ == '__main__':
    picturize()