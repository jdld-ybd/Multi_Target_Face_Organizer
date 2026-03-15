import face_recognition
import os
import shutil

# 配置参数
TARGET_FOLDER = "target_faces"  # 目标人脸图片文件夹
INPUT_FOLDER = "input_images"   # 输入图片文件夹
OUTPUT_FOLDER = "output"        # 输出文件夹
TOLERANCE = 0.4                 # 匹配阈值

# 步骤1: 提取所有目标人脸的128维向量
def load_target_encodings(target_files):
    target_encodings = {}
    for target_file in target_files:
        try:
            image = face_recognition.load_image_file(os.path.join(TARGET_FOLDER, target_file))
            encodings = face_recognition.face_encodings(image)
            if encodings:
                target_encodings[target_file] = encodings[0]  # 假设每张图片只有一个人脸
                print(f"已提取 {target_file} 的128维向量")
            else:
                print(f"警告：{target_file} 中未检测到人脸，跳过")
        except Exception as e:
            print(f"加载 {target_file} 出错：{e}")
    return target_encodings

# 步骤2: 读取输入文件夹内的所有.jpg文件名
def get_jpg_files(folder):
    jpg_files = [f for f in os.listdir(folder) if f.lower().endswith('.jpg')]
    return jpg_files

# 步骤3: 处理每张图片，匹配并移动
def process_images(jpg_files, target_encodings):
    # 创建输出文件夹结构
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    for target in target_encodings.keys():
        os.makedirs(os.path.join(OUTPUT_FOLDER, f"{os.path.splitext(target)[0]}_folder"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_FOLDER, "else"), exist_ok=True)
    
    for jpg_file in jpg_files:
        input_path = os.path.join(INPUT_FOLDER, jpg_file)
        try:
            image = face_recognition.load_image_file(input_path)
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            if not face_encodings:
                # 无脸，移到else
                output_path = os.path.join(OUTPUT_FOLDER, "else", jpg_file)
                shutil.move(input_path, output_path)
                print(f"{jpg_file}：无人脸，已移动到 else 文件夹")
                continue
            
            # 有脸，计算与所有目标的距离，选择最匹配的
            best_match = None
            min_distance = float('inf')
            for target_name, target_encoding in target_encodings.items():
                distances = face_recognition.face_distance([target_encoding], face_encodings[0])  # 假设取第一张脸
                distance = distances[0]
                if distance < min_distance:
                    min_distance = distance
                    best_match = target_name
            
            if min_distance < TOLERANCE:
                # 匹配，移到对应文件夹
                folder_name = f"{os.path.splitext(best_match)[0]}_folder"
                output_path = os.path.join(OUTPUT_FOLDER, folder_name, jpg_file)
                shutil.move(input_path, output_path)
                print(f"{jpg_file}：匹配 {best_match} (距离: {min_distance:.2f})，已移动到 {folder_name}")
            else:
                # 不匹配，移到else
                output_path = os.path.join(OUTPUT_FOLDER, "else", jpg_file)
                shutil.move(input_path, output_path)
                print(f"{jpg_file}：不匹配任何目标 (最小距离: {min_distance:.2f})，已移动到 else 文件夹")
        
        except Exception as e:
            print(f"处理 {jpg_file} 出错：{e}")

# 主函数
if __name__ == "__main__":
    # 指定目标人脸文件列表（可手动修改）
    target_files = ["y.jpg", "t.jpg", "y.jpg", "d.jpg"]  # 示例，添加更多
    
    target_encodings = load_target_encodings(target_files)
    if not target_encodings:
        print("无有效目标人脸，退出")
        exit(1)
    
    jpg_files = get_jpg_files(INPUT_FOLDER)
    if not jpg_files:
        print("输入文件夹无.jpg文件，退出")
        exit(1)
    
    process_images(jpg_files, target_encodings)
    print("处理完成！")