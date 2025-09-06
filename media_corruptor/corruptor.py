import os
import random
import argparse
import sys

def corrupt_media_file(input_path, output_path=None, corruption_level=0.01):
    """
    部分损坏媒体文件，使其仍可播放但会出现错误
    
    :param input_path: 输入文件路径
    :param output_path: 输出文件路径（默认为输入文件加_corrupted后缀）
    :param corruption_level: 损坏程度（0.01-0.1，默认0.01）
    :return: 输出文件路径，如果出错则返回None
    """
    try:
        # 验证输入文件是否存在
        if not os.path.isfile(input_path):
            print(f"错误: 文件 '{input_path}' 不存在")
            return None
        
        # 设置输出路径
        if output_path is None:
            dir_name, file_name = os.path.split(input_path)
            name, ext = os.path.splitext(file_name)
            output_path = os.path.join(dir_name, f"{name}_corrupted{ext}")
        
        # 验证损坏程度
        corruption_level = max(0.001, min(0.1, corruption_level))
        
        # 读取文件
        print(f"正在读取文件: {input_path}")
        with open(input_path, 'rb') as f:
            data = bytearray(f.read())
        
        file_size = len(data)
        num_corruptions = int(file_size * corruption_level)
        
        print(f"文件大小: {file_size} 字节")
        print(f"将损坏约 {num_corruptions} 字节 ({corruption_level*100:.2f}%)")
        
        # 选择要损坏的位置（避免文件头，以免完全无法读取）
        start_pos = min(1024, file_size // 10)  # 至少跳过前1024字节或10%的文件
        
        if start_pos >= file_size:
            print("错误: 文件太小，无法损坏")
            return None
            
        positions = random.sample(range(start_pos, file_size), min(num_corruptions, file_size - start_pos))
        
        # 损坏数据
        print("正在损坏文件数据...")
        for i, pos in enumerate(positions):
            # 随机修改字节（翻转一些位）
            data[pos] ^= random.randint(1, 255)
            
            # 每处理1000个字节显示一次进度
            if i % 1000 == 0 and i > 0:
                print(f"已处理 {i}/{len(positions)} 字节")
        
        # 写入输出文件
        print(f"正在写入输出文件: {output_path}")
        with open(output_path, 'wb') as f:
            f.write(data)
        
        print(f"成功创建部分损坏的文件: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"处理文件时出错: {str(e)}")
        return None

def corrupt_media_file_safe(input_path, output_path=None, corruption_level=0.01):
    """更安全的版本，确保不会损坏原始文件"""
    try:
        # 确保输入文件存在
        if not os.path.isfile(input_path):
            raise FileNotFoundError(f"输入文件不存在: {input_path}")
        
        # 确保输出路径与输入路径不同
        if output_path is None:
            dir_name, file_name = os.path.split(input_path)
            name, ext = os.path.splitext(file_name)
            output_path = os.path.join(dir_name, f"{name}_corrupted{ext}")
        
        if os.path.abspath(input_path) == os.path.abspath(output_path):
            raise ValueError("输出路径不能与输入路径相同")
        
        return corrupt_media_file(input_path, output_path, corruption_level)
    except Exception as e:
        print(f"错误: {str(e)}")
        return None
