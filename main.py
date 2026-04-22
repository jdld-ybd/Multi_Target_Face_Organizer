import face_recognition
import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import threading

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

# 步骤2: 读取输入文件夹内的图片文件名
def get_files(folder):
    files = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    return files

# 步骤3: 处理每张图片，匹配并移动
def process_images(files, target_encodings, output_folder, tolerance, log_callback):
    # 创建输出文件夹结构
    os.makedirs(output_folder, exist_ok=True)
    for target in target_encodings.keys():
        os.makedirs(os.path.join(output_folder, f"{os.path.splitext(target)[0]}_folder"), exist_ok=True)
    os.makedirs(os.path.join(output_folder, "else"), exist_ok=True)
    
    for file in files:
        input_path = os.path.join(INPUT_FOLDER, file)
        try:
            image = face_recognition.load_image_file(input_path)
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            if not face_encodings:
                # 无脸，移到else
                output_path = os.path.join(output_folder, "else", file)
                shutil.move(input_path, output_path)
                log_message = f"{file}：无人脸，已移动到 else 文件夹"
                print(log_message)
                log_callback(log_message)
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
            
            if min_distance < tolerance:
                # 匹配，移到对应文件夹
                folder_name = f"{os.path.splitext(best_match)[0]}_folder"
                output_path = os.path.join(output_folder, folder_name, file)
                shutil.move(input_path, output_path)
                log_message = f"{file}：匹配 {best_match} (距离: {min_distance:.2f})，已移动到 {folder_name}"
                print(log_message)
                log_callback(log_message)
            else:
                # 不匹配，移到else
                output_path = os.path.join(output_folder, "else", file)
                shutil.move(input_path, output_path)
                log_message = f"{file}：不匹配任何目标 (最小距离: {min_distance:.2f})，已移动到 else 文件夹"
                print(log_message)
                log_callback(log_message)
        
        except Exception as e:
            log_message = f"处理 {file} 出错：{e}"
            print(log_message)
            log_callback(log_message)

# GUI类
class FaceOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("多目标人脸整理工具")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        # 设置窗口最小尺寸，防止内容变形
        self.root.minsize(800, 700)
        
        # 设置科技风黑灰主题
        self.root.configure(bg='#1a1a1a')
        
        # 设置样式
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # 自定义样式 - 科技风黑灰主题
        self.style.configure('TLabelFrame', 
                            font=('Consolas', 10, 'bold'), 
                            foreground='#ffffff', 
                            background='#2d2d2d',
                            borderwidth=2,
                            relief='groove',
                            lightcolor='#3d3d3d',
                            darkcolor='#1a1a1a',
                            bordercolor='#3d3d3d')
        self.style.configure('TButton', 
                            font=('Consolas', 9), 
                            padding=5,
                            background='#3d3d3d',
                            foreground='#ffffff',
                            lightcolor='#4d4d4d',
                            darkcolor='#2d2d2d',
                            bordercolor='#3d3d3d')
        self.style.configure('Accent.TButton', 
                            background='#4d4d4d', 
                            foreground='#ffffff', 
                            font=('Consolas', 9, 'bold'),
                            borderwidth=1,
                            relief='ridge',
                            lightcolor='#5d5d5d',
                            darkcolor='#3d3d3d',
                            bordercolor='#4d4d4d')
        self.style.map('Accent.TButton', 
                      background=[('active', '#5d5d5d')],
                      foreground=[('active', '#ffffff')])
        self.style.configure('TEntry', 
                            font=('Consolas', 9),
                            fieldbackground='#3d3d3d',
                            foreground='#ffffff',
                            insertcolor='#ffffff',
                            lightcolor='#4d4d4d',
                            darkcolor='#2d2d2d',
                            bordercolor='#3d3d3d')
        self.style.configure('TLabel', 
                            font=('Consolas', 9),
                            background='#2d2d2d',
                            foreground='#ffffff')
        self.style.configure('TScale', 
                            background='#2d2d2d',
                            foreground='#ffffff',
                            troughcolor='#3d3d3d',
                            bordercolor='#3d3d3d')
        self.style.configure('TScrollbar', 
                            background='#3d3d3d',
                            foreground='#ffffff',
                            troughcolor='#1a1a1a',
                            lightcolor='#4d4d4d',
                            darkcolor='#2d2d2d',
                            bordercolor='#3d3d3d')
        # 为框架设置统一的背景色
        self.style.configure('TLabelframe', background='#2d2d2d')
        self.style.configure('TLabelframe.Label', background='#2d2d2d', foreground='#ffffff')
        
        # 主框架
        self.main_frame = ttk.Frame(self.root, padding="10", style='TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 为所有ttk框架设置统一的背景色
        self.style.configure('TFrame', background='#1a1a1a')
        
        # 顶部框架 - 配置区域
        self.config_frame = ttk.LabelFrame(self.main_frame, text="配置", padding="10")
        self.config_frame.pack(fill=tk.X, pady=5)
        
        # 文件夹选择
        folder_frame = ttk.Frame(self.config_frame, style='TFrame')
        folder_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(folder_frame, text="输入文件夹:", width=12, font=('Consolas', 9)).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.input_folder_var = tk.StringVar(value=INPUT_FOLDER)
        input_entry = ttk.Entry(folder_frame, textvariable=self.input_folder_var, width=50, font=('Consolas', 9))
        input_entry.grid(row=0, column=1, padx=5, pady=5)
        input_entry.bind('<FocusIn>', lambda e: input_entry.select_range(0, tk.END))
        browse_button = ttk.Button(folder_frame, text="浏览", command=self.browse_input_folder)
        browse_button.grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(folder_frame, text="输出文件夹:", width=12, font=('Consolas', 9)).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.output_folder_var = tk.StringVar(value=OUTPUT_FOLDER)
        output_entry = ttk.Entry(folder_frame, textvariable=self.output_folder_var, width=50, font=('Consolas', 9))
        output_entry.grid(row=1, column=1, padx=5, pady=5)
        output_entry.bind('<FocusIn>', lambda e: output_entry.select_range(0, tk.END))
        browse_button = ttk.Button(folder_frame, text="浏览", command=self.browse_output_folder)
        browse_button.grid(row=1, column=2, padx=5, pady=5)
        
        # 阈值设置
        threshold_frame = ttk.Frame(self.config_frame, style='TFrame')
        threshold_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(threshold_frame, text="匹配阈值:", width=12, font=('Consolas', 9)).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.tolerance_var = tk.DoubleVar(value=TOLERANCE)
        tolerance_scale = ttk.Scale(threshold_frame, from_=0.1, to=1.0, orient=tk.HORIZONTAL, variable=self.tolerance_var, length=400)
        tolerance_scale.grid(row=0, column=1, padx=5, pady=5)
        self.tolerance_label = ttk.Label(threshold_frame, text=f"{TOLERANCE:.2f}", font=('Consolas', 9, 'bold'), width=5, foreground='#ffffff')
        self.tolerance_label.grid(row=0, column=2, padx=5, pady=5)
        self.tolerance_var.trace_add("write", self.update_tolerance_label)
        
        # 添加阈值说明
        ttk.Label(threshold_frame, text="(值越小，匹配越严格)", font=('Consolas', 9, 'italic'), foreground='#ffffff').grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        # 中间框架 - 目标人脸显示
        self.target_frame = ttk.LabelFrame(self.main_frame, text="目标人脸", padding="10")
        self.target_frame.pack(fill=tk.X, pady=5)
        
        self.target_canvas = tk.Canvas(self.target_frame, height=180, bg='#2d2d2d', highlightbackground='#3d3d3d', highlightthickness=1)
        self.target_canvas.pack(fill=tk.X, expand=True)
        
        self.target_scrollbar = ttk.Scrollbar(self.target_frame, orient=tk.HORIZONTAL, command=self.target_canvas.xview)
        self.target_scrollbar.pack(fill=tk.X, side=tk.BOTTOM)
        self.target_canvas.config(xscrollcommand=self.target_scrollbar.set)
        
        self.target_inner_frame = ttk.Frame(self.target_canvas, style='TFrame')
        self.target_canvas.create_window((0, 0), window=self.target_inner_frame, anchor=tk.NW, tags="inner_frame")
        
        # 加载目标人脸
        self.load_target_faces()
        
        # 底部框架 - 控制和日志
        self.control_frame = ttk.Frame(self.main_frame, style='TFrame')
        self.control_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 左侧 - 控制按钮
        control_left = ttk.Frame(self.control_frame, width=200, relief=tk.RAISED, borderwidth=2, style='TFrame')
        control_left.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # 添加标题
        ttk.Label(control_left, text="控制", font=('Consolas', 10, 'bold'), padding=5, foreground='#ffffff').pack()
        
        self.process_button = ttk.Button(control_left, text="开始处理", command=self.start_process, style="Accent.TButton")
        self.process_button.pack(fill=tk.X, pady=5, padx=10)
        
        # 添加状态信息
        status_frame = ttk.Frame(control_left, padding=5, style='TFrame')
        status_frame.pack(fill=tk.X, pady=2)
        ttk.Label(status_frame, text="状态:", font=('Consolas', 9)).pack(anchor=tk.W)
        self.status_label = ttk.Label(status_frame, text="就绪", foreground="#ffffff", font=('Consolas', 9, 'bold'))
        self.status_label.pack(anchor=tk.W, pady=2)
        
        # 添加统计信息
        ttk.Label(control_left, text="统计", font=('Consolas', 10, 'bold'), padding=5, foreground='#ffffff').pack()
        self.stats_frame = ttk.Frame(control_left, padding=5, style='TFrame')
        self.stats_frame.pack(fill=tk.X, pady=2)
        ttk.Label(self.stats_frame, text="目标人脸: 0", font=('Consolas', 9)).pack(anchor=tk.W, pady=2)
        ttk.Label(self.stats_frame, text="输入图片: 0", font=('Consolas', 9)).pack(anchor=tk.W, pady=2)
        
        # 右侧 - 日志显示
        log_frame = ttk.LabelFrame(self.control_frame, text="处理日志", padding="10")
        log_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        log_scrollbar = ttk.Scrollbar(log_frame)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(log_frame, 
                               wrap=tk.WORD, 
                               yscrollcommand=log_scrollbar.set, 
                               height=15, 
                               font=('Consolas', 9), 
                               bg='#2d2d2d', 
                               fg='#ffffff', 
                               relief=tk.FLAT, 
                               borderwidth=1, 
                               insertbackground='#ffffff')
        self.log_text.pack(fill=tk.BOTH, expand=True)
        log_scrollbar.config(command=self.log_text.yview)
        
        # 禁用文本编辑
        self.log_text.config(state=tk.DISABLED)
        
        # 添加日志说明
        ttk.Label(log_frame, text="处理过程中的详细信息将显示在这里", font=('Consolas', 8, 'italic'), foreground='#009900').pack(anchor=tk.W, pady=2)
        
        # 绑定窗口大小变化
        self.root.bind('<Configure>', self.on_configure)
        
        # 初始化统计信息
        self.update_stats()
    
    def update_stats(self):
        """更新统计信息"""
        # 统计目标人脸数量
        target_files = [f for f in os.listdir(TARGET_FOLDER) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        target_count = len(target_files)
        
        # 统计输入图片数量
        input_folder = self.input_folder_var.get()
        input_count = 0
        if os.path.exists(input_folder):
            input_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
            input_count = len(input_files)
        
        # 更新统计信息
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        ttk.Label(self.stats_frame, text=f"目标人脸: {target_count}", font=('Consolas', 9), foreground='#ffffff').pack(anchor=tk.W, pady=2)
        ttk.Label(self.stats_frame, text=f"输入图片: {input_count}", font=('Consolas', 9), foreground='#ffffff').pack(anchor=tk.W, pady=2)
    
    def on_configure(self, event):
        """窗口大小变化时调整布局"""
        self.target_inner_frame.update_idletasks()
        self.target_canvas.config(scrollregion=self.target_canvas.bbox('all'))
    
    def update_tolerance_label(self, *args):
        self.tolerance_label.config(text=f"{self.tolerance_var.get():.2f}")
    
    def browse_input_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_folder_var.set(folder)
            self.update_stats()
    
    def browse_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder_var.set(folder)
    
    def load_target_faces(self):
        # 清空现有内容
        for widget in self.target_inner_frame.winfo_children():
            widget.destroy()
        
        # 加载目标人脸
        target_files = [f for f in os.listdir(TARGET_FOLDER) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        
        for i, target_file in enumerate(target_files):
            frame = ttk.Frame(self.target_inner_frame, padding="5", style='TFrame')
            frame.grid(row=0, column=i, padx=10, pady=5)
            
            # 加载并显示图片
            try:
                image = Image.open(os.path.join(TARGET_FOLDER, target_file))
                image = image.resize((100, 100), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                label = ttk.Label(frame, image=photo, style='TLabel')
                label.image = photo  # 保持引用
                label.pack()
                
                # 显示文件名
                name_label = ttk.Label(frame, text=os.path.splitext(target_file)[0], font=('Consolas', 10), foreground='#ffffff')
                name_label.pack()
            except Exception as e:
                ttk.Label(frame, text=f"加载失败", font=('Consolas', 10), foreground='#ff6666').pack()
        
        # 更新画布大小
        self.target_inner_frame.update_idletasks()
        self.target_canvas.config(scrollregion=self.target_canvas.bbox('all'))
    
    def log(self, message):
        """添加日志信息"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def start_process(self):
        """开始处理图片"""
        # 检查输入文件夹
        input_folder = self.input_folder_var.get()
        if not os.path.exists(input_folder):
            messagebox.showerror("错误", "输入文件夹不存在！")
            return
        
        # 检查目标人脸
        target_files = [f for f in os.listdir(TARGET_FOLDER) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        if not target_files:
            messagebox.showerror("错误", "目标人脸文件夹为空！")
            return
        
        # 检查输入文件
        files = get_files(input_folder)
        if not files:
            messagebox.showerror("错误", "输入文件夹中没有图片文件！")
            return
        
        # 禁用按钮
        self.process_button.config(state=tk.DISABLED)
        self.status_label.config(text="处理中...", foreground="orange")
        
        # 清空日志
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # 启动处理线程
        def process_thread():
            try:
                # 加载目标人脸编码
                self.log("正在加载目标人脸...")
                target_encodings = load_target_encodings(target_files)
                
                if not target_encodings:
                    self.log("无有效目标人脸，处理终止")
                    return
                
                # 处理图片
                self.log(f"开始处理 {len(files)} 张图片...")
                process_images(files, target_encodings, self.output_folder_var.get(), self.tolerance_var.get(), self.log)
                
                self.log("处理完成！")
                messagebox.showinfo("完成", "图片处理完成！")
            except Exception as e:
                error_message = f"处理过程出错：{e}"
                self.log(error_message)
                messagebox.showerror("错误", error_message)
            finally:
                # 恢复按钮状态
                self.process_button.config(state=tk.NORMAL)
                self.status_label.config(text="就绪", foreground="green")
        
        thread = threading.Thread(target=process_thread)
        thread.daemon = True
        thread.start()
    
    def on_configure(self, event):
        """窗口大小变化时调整布局"""
        self.target_inner_frame.update_idletasks()
        self.target_canvas.config(scrollregion=self.target_canvas.bbox('all'))

# 主函数
if __name__ == "__main__":
    root = tk.Tk()
    app = FaceOrganizerApp(root)
    root.mainloop()