# Photo Watermark - 图片水印工具

一个基于 Python 的命令行工具，用于为图片添加基于 EXIF 拍摄时间的水印。

## 📋 功能特性

- 自动读取图片的 EXIF 信息，提取拍摄时间
- 将拍摄时间作为水印添加到图片上
- 支持自定义水印字体大小、颜色和位置
- 批量处理目录中的所有图片
- 支持多种图片格式（JPG, PNG, TIFF, BMP）

## 🛠️ 安装依赖

```bash
pip install Pillow
```

## 🚀 使用方法

### 基本使用

```bash
python watermark.py /path/to/your/images
```

### 自定义参数

```bash
# 自定义字体大小和颜色
python watermark.py /path/to/your/images --font_size 30 --color "255,0,0,160"

# 使用十六进制颜色和左上角位置
python watermark.py /path/to/your/images --color "#FF0000" --position 左上角

# 使用颜色名称和居中位置
python watermark.py /path/to/your/images --color blue --position 居中
```

### 命令行参数说明

| 参数          | 说明                                    | 默认值                          |
| ------------- | --------------------------------------- | ------------------------------- |
| `input_dir`   | 输入图片目录路径                        | (必填)                          |
| `--font_size` | 水印字体大小                            | 24                              |
| `--color`     | 水印颜色（支持RGB、十六进制或颜色名称） | "255,255,255,128"（白色半透明） |
| `--position`  | 水印位置（左上角/居中/右下角）          | "右下角"                        |

### 支持的颜色名称

- black
- white
- red
- green
- blue
- yellow
- gray

## 📁 输出结果

程序会在原目录下创建一个名为 `原目录名_watermark` 的子目录，所有添加水印后的图片将保存在这个目录中。

## 📝 注意事项

1. 如果图片没有 EXIF 信息，水印将显示 "无日期信息"
2. 水印颜色支持 RGBA 格式，其中 A 为透明度（0-255）
3. 支持的图片格式：JPG, JPEG, PNG, TIFF, BMP

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

