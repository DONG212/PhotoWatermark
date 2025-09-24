import argparse
import os
from PIL import Image, ImageDraw, ImageFont, ExifTags
from PIL.ExifTags import TAGS
import sys
import tkinter as tk
from tkinter import filedialog, messagebox


def select_image_file():
    """打开文件选择对话框让用户选择图片"""
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    file_path = filedialog.askopenfilename(
        title="选择要添加水印的图片",
        filetypes=[
            ("图片文件", "*.jpg *.jpeg *.png *.tiff *.bmp"),
            ("JPEG 文件", "*.jpg *.jpeg"),
            ("PNG 文件", "*.png"),
            ("所有文件", "*.*")
        ]
    )

    if not file_path:
        print("未选择任何文件，程序退出。")
        sys.exit(0)

    return file_path


def get_exif_date(image_path):
    """获取图片的EXIF拍摄日期信息"""
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()

        if exif_data:
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == 'DateTimeOriginal':
                    return value
                elif tag == 'DateTime':
                    return value
        return None
    except Exception as e:
        print(f"读取EXIF信息时出错: {e}")
        return None


def parse_date(date_str):
    """解析EXIF日期格式为年月日"""
    if date_str:
        # EXIF日期格式通常为 "YYYY:MM:DD HH:MM:SS"
        return date_str.split(' ')[0].replace(':', '-')
    return "未知日期"


def add_watermark_to_image(input_path, output_path, date_text, font_size, color, position):
    """为单张图片添加水印"""
    try:
        # 打开图片
        image = Image.open(input_path).convert('RGBA')
        width, height = image.size

        # 创建透明层用于水印
        watermark = Image.new('RGBA', image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(watermark)

        # 尝试使用默认字体，如果失败则使用内置字体
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
            except:
                font = ImageFont.load_default()

        # 计算文本尺寸
        bbox = draw.textbbox((0, 0), date_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # 计算水印位置
        margin = 20
        if position == "左上角":
            x = margin
            y = margin
        elif position == "居中":
            x = (width - text_width) // 2
            y = (height - text_height) // 2
        elif position == "右下角":
            x = width - text_width - margin
            y = height - text_height - margin
        else:
            x = margin
            y = margin

        # 绘制水印文本
        draw.text((x, y), date_text, font=font, fill=color)

        # 合并图片和水印
        watermarked = Image.alpha_composite(image, watermark)

        # 转换为RGB模式保存为JPEG
        if output_path.lower().endswith(('.jpg', '.jpeg')):
            watermarked = watermarked.convert('RGB')

        watermarked.save(output_path)
        return True

    except Exception as e:
        print(f"处理图片 {input_path} 时出错: {e}")
        return False


def parse_color(color_str):
    """解析颜色参数"""
    color_str = color_str.strip().lower()

    # 预定义颜色名称
    color_names = {
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'yellow': (255, 255, 0),
        'gray': (128, 128, 128),
        'silver': (192, 192, 192)
    }

    if color_str in color_names:
        return color_names[color_str] + (128,)  # 添加默认透明度

    if color_str.startswith('#'):
        # 十六进制格式
        try:
            r = int(color_str[1:3], 16)
            g = int(color_str[3:5], 16)
            b = int(color_str[5:7], 16)
            return (r, g, b, 128)  # 添加默认透明度
        except:
            pass

    # RGB格式
    if ',' in color_str:
        try:
            parts = color_str.split(',')
            if len(parts) == 3:
                r, g, b = [int(p.strip()) for p in parts]
                return (r, g, b, 128)  # 添加默认透明度
            elif len(parts) == 4:
                r, g, b, a = [int(p.strip()) for p in parts]
                return (r, g, b, a)
        except:
            pass

    # 默认颜色（黑色带透明度）
    return (0, 0, 0, 128)


def main():
    """主函数：解析命令行参数并处理图片"""
    parser = argparse.ArgumentParser(description='为图片添加基于EXIF拍摄时间的水印')
    parser.add_argument('--font_size', type=int, default=24, help='水印字体大小（默认: 24）')
    parser.add_argument('--color', default='255,255,255,128',
                        help='水印颜色（支持RGB、十六进制或颜色名称，默认: 白色半透明）')
    parser.add_argument('--position', choices=['左上角', '居中', '右下角'], default='右下角',
                        help='水印位置（默认: 右下角）')

    args = parser.parse_args()

    print("=== 图片水印添加工具 ===")
    print("请选择要添加水印的图片...")

    # 打开文件选择对话框
    input_path = select_image_file()
    print(f"已选择图片: {input_path}")

    # 获取文件所在目录和文件名
    input_dir = os.path.dirname(input_path)
    filename = os.path.basename(input_path)

    # 创建输出目录
    output_dir = os.path.join(input_dir, f"{os.path.basename(input_dir)}_watermark")
    os.makedirs(output_dir, exist_ok=True)

    # 解析颜色
    color = parse_color(args.color)

    # 获取拍摄日期
    exif_date = get_exif_date(input_path)
    date_text = parse_date(exif_date) if exif_date else "无日期信息"
    print(f"拍摄时间: {date_text}")

    # 生成输出路径
    output_path = os.path.join(output_dir, filename)

    # 添加水印
    if add_watermark_to_image(input_path, output_path, date_text, args.font_size, color, args.position):
        print(f"✓ 水印添加成功!")
        print(f"✓ 输出文件: {output_path}")
        print(f"✓ 水印内容: {date_text}")
        print(f"✓ 保存位置: {output_dir}")
    else:
        print("✗ 水印添加失败!")


if __name__ == "__main__":
    main()