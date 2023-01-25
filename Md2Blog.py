# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  用于将Typora写成的md文件转换成Jekyll可以识别的md文件
# ------------------------------------------------------------------------------
#  实现功能：
#  1. 解决Jekyll下md文件中的图片无法识别的问题
#  2. 解决Jekyll下md文件中的公式显示问题
#  具体使用方法，参照：
#  访问以下地址检查是否为最新：
#
#     VicoZhang, 中国广州
# ------------------------------------------------------------------------------
#
#  More information, visit:
#  Check the latest version:
#
#     VicoZhang, Canton, CHINA
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from pathlib import Path
import re
import functools
import shutil
import time
import argparse


def read_file(path):
    with open(path, encoding='utf-8') as f1:  # 注意编码必须是 utf-8
        _line = f1.read()
        _line = re.sub(img_pattern1, functools.partial(img_ops1), _line)
        _line = re.sub(img_pattern2, functools.partial(img_ops2), _line)
        _line = re.sub(equ_pattern, functools.partial(equ_ops), _line)
    return _line


def img_ops1(path):  # 修改 ![]() 格式插入的图片代码
    img_filename = path.group(2).split('/')[1]
    img_path = img_root / img_filename
    shutil.copy(src=img_path, dst=img_target_path)
    new_img_pattern = '![{}]({})'.format(path.group(1), '{{site.url}}/img/'+img_filename)
    return new_img_pattern


def img_ops2(path):  # 修改 <img ...> 格式插入的图片代码
    img_filename = path.group(1).split('/')[1]
    img_path = img_root / img_filename
    shutil.copy(src=img_path, dst=img_target_path)
    new_img_pattern = '<img src="{}" alt="{}" style="{}" />'\
        .format('{{site.url}}/img/' + img_filename, path.group(2), path.group(3))
    return new_img_pattern


def equ_ops(equ):  # 修改行间公式代码
    return '\n{}\n'.format(equ.group())


def write_file(path, data):
    with open(path, 'w', encoding='utf-8') as f2:  # 注意编码必须是 utf-8
        f2.writelines(data)


if __name__ == '__main__':
    ap = argparse.ArgumentParser("Input the md file path")
    ap.add_argument('-i', '--input', type=str, help='In put the md file path')

    args = ap.parse_args()
    md_path = Path(args.input)  # md 文件的路径

    # 初始设置
    post_path = Path(r'D:\vicozhang.github.io\_posts')  # Jekyll 目录下_post文件夹的路径
    img_root = md_path.with_suffix('.assets')  # md 文件对应图片文件夹路径，与 Typora 设置相关
    img_target_path = Path(r'D:\vicozhang.github.io\img')  # Jekyll 目录下_img文件夹的路径
    new_filename = time.strftime('%y-%m-%d-', time.localtime(time.time())) + md_path.name  # 符合 Jekyll 规定的命名

    img_pattern1 = re.compile(r'!\[(.*?)]\((.*?)\)')  # 匹配 ![]() 格式
    img_pattern2 = re.compile(r'<img src="(.*?)" alt="(.*?)" style="(.*?)" />')  # 匹配 <img ...> 格式
    equ_pattern = re.compile(r'\$\$(.*?)\$\$', re.S)  # 匹配公式

    content = read_file(md_path)
    write_file(post_path / new_filename, content)

    print('文件处理完成')
