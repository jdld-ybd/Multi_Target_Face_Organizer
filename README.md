## 项目名称:多目标人脸分类整理器 (Multi-Target Face Organizer)

[![Python Version](https://img.shields.io/badge/Python-3.6%20~%203.11-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
一款基于 `face_recognition` 开发的轻量级人脸批量识别工具，可自动检测图片中的人脸并与多个预设目标人脸匹配，将图片分类移动到对应文件夹，无人脸/不匹配的图片统一归类，适合快速整理含有人脸的图片库。

## 一、环境要求python 3.6-3.11

## 二、项目结构
    Multi_Target_Face_Organizer/
    ├── .github/
    │   ├── ISSUE_TEMPLATE/
    │   │   ├── bug_report.md
    │   │   └── feature_request.md
    │   └── PULL_REQUEST_TEMPLATE.md
    ├── main.py                    # 主脚本，包含所有逻辑
    ├── target_faces/              # 存放目标人脸图片的文件夹（手动放置，如face3.jpg, face4.jpg等）
    ├── input_images/              # 输入文件夹，存放待处理的图片（手动放置）
    ├── output/                    # 输出文件夹（脚本自动创建）
    │   ├── face3_folder/          # 为face3.jpg创建的文件夹（匹配的图片移入）
    │   ├── face4_folder/          # 为face4.jpg创建的文件夹
    │   └── else/                  # 无人脸图片移入
    ├── requirements.txt           # 依赖文件（列出库版本）
    └── README.md                  # 项目说明文档
    |__ CONTRIBUTING.md            # 贡献说明
    |__ error.txt                  # 见安装环节(安装如果报错必看)
    |__ solution.txt               # 见安装环节(安装如果报错必看)
    |__ ex.txt                     # 成功运行的结果示例

## 三、 核心功能：
- 提取多个目标人脸图片的128维向量（用于识别基准）。
- 扫描输入文件夹，收集所有图片文件。
- 对每张图片进行人脸检测和匹配，将匹配的图片移动到对应目标人脸的文件夹；无人脸图片移动到“else”文件夹。
- 每处理一张图片打印处理信息（例如：文件名、匹配结果、移动路径）。
- 🎯 支持同时匹配多个目标人脸（数量无限制）
- 📂 自动创建分类文件夹，匹配图片精准归类
- 🛡️ 完善的异常处理：跳过损坏图片，避免程序中断
- 📝 实时打印处理日志，清晰展示匹配状态/相似度/文件路径
- 🌍 跨平台兼容：支持 Windows/Linux/macOS
- 👍 GUI美观界面操作

## 四、快速开始

### 1. 准备工作
在项目根目录下找到并处理 2 个文件夹：
- `target_faces/`：放入需要匹配的目标人脸图片（建议单人脸正面照，格式为JPG或png或jpeg）
- `input_images/`：放入待整理的所有图片（格式为JPG或png或jpeg）
### 2. 依赖库：
    face_recognition、os、shutil（用于文件移动）、cv2(备用)……（具体请查看requirements.txt）
### 3. 安装
    pip install -r requirements.txt
- 如果windows无法正常安装(错误日志如 error.txt 所示)，请按照流程安装CMake，或使用Anaconda Prompt解决(具体方法见 solution.txt )!!!
### 4. 路径配置
TARGET_FOLDER = "target_faces"  # 目标人脸文件夹路径
INPUT_FOLDER = "input_images"   # 待处理图片文件夹路径
OUTPUT_FOLDER = "output"        # 结果输出文件夹路径
### 5. 匹配阈值（越小越严格，取值范围 0~1，默认 0.4）
TOLERANCE = 0.4
### 6. 目标人脸文件名列表示例（需与 target_faces/ 内的文件完全一致）
target_files = ["y.jpg", "t.jpg", "d.jpg"]
## 五、注意事项：
- 假设目标人脸图片和输入图片都在同一工作目录下，或提供绝对路径。
- 如果一张图片有多个人脸，选择距离最小的匹配（最相似的一个）。
- 文件移动使用shutil.move，确保不覆盖同名文件（可添加重命名逻辑）。
- 待整理图片数量较多时，程序运行时间会相应增加，请耐心等待；
- 支持 JPG/PNG/JPEG 格式，可修改 main.py 中筛选图片的逻辑 
## 六、贡献指南
本项目欢迎所有形式的贡献！详细的贡献步骤、代码规范、Issue/PR 提交要求见 CONTRIBUTING.md。
## 联系作者
如有问题 / 建议，可在 GitHub Issues 中提交，维护者会尽快回复
