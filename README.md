## 项目名称:多目标人脸分类整理器 (Multi-Target Face Organizer)v1.0.0
## 环境要求python 3.6 ~ 3.11
## 项目结构
    Multi_Target_Face_Organizer/
    ├── main.py                    # 主脚本，包含所有逻辑
    ├── target_faces/              # 存放目标人脸图片的文件夹（手动放置，如face3.jpg, face4.jpg等）
    ├── input_images/              # 输入文件夹，存放待处理的.jpg图片（手动放置）
    ├── output/                    # 输出文件夹（脚本自动创建）
    │   ├── face3_folder/          # 为face3.jpg创建的文件夹（匹配的图片移入）
    │   ├── face4_folder/          # 为face4.jpg创建的文件夹
    │   └── else/                  # 无人脸图片移入
    ├── requirements.txt           # 依赖文件（列出库版本）
    └── README.md                  # 项目说明文档
    |__ error.txt                  #见安装环节(安装如果报错必看)
    |__ solution.txt               #见安装环节(安装如果报错必看)
    |__ ex.txt                     #成功运行的结果示例
## 核心功能：
    -提取多个目标人脸图片的128维向量（用于识别基准）。
    -扫描输入文件夹，收集所有.jpg图片文件。
    -对每张图片进行人脸检测和匹配，将匹配的图片移动到对应目标人脸的文件夹；无人脸图片移动到“else”文件夹。
    -每处理一张图片打印处理信息（例如：文件名、匹配结果、移动路径）。
## 依赖库：
    face_recognition、os、shutil（用于文件移动）、cv2(备用)。
## 安装
    pip install -r requirements.txt
    -如果windows无法正常安装(错误日志如 error.txt 所示)，请按照流程安装CMake，或使用Anaconda Prompt解决(具体方法见 solution.txt )!!!
## 使用示例
    python main.py
## 注意事项：
    -假设目标人脸图片和输入图片都在同一工作目录下，或提供绝对路径。
    -匹配阈值可调（默认0.4）。
    -如果一张图片有多个人脸，选择距离最小的匹配（最相似的一个）。
    -文件移动使用shutil.move，确保不覆盖同名文件（可添加重命名逻辑）。
    -错误处理：跳过无法加载的图片，打印错误信息。
    
