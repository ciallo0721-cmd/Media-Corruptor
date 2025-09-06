import os
import sys
from .corruptor import corrupt_media_file_safe

def main():
    parser = argparse.ArgumentParser(description='部分损坏媒体文件')
    parser.add_argument('input', help='输入文件路径')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('-l', '--level', type=float, default=0.01, 
                       help='损坏程度 (0.001-0.1，默认0.01)')
    
    args = parser.parse_args()
    
    # 获取当前工作目录的绝对路径
    current_dir = os.getcwd()
    print(f"当前工作目录: {current_dir}")
    
    # 处理输入路径，如果是相对路径，则转换为绝对路径
    input_path = args.input
    if not os.path.isabs(input_path):
        input_path = os.path.join(current_dir, input_path)
    
    print(f"输入文件路径: {input_path}")
    
    # 处理输出路径
    output_path = args.output
    if output_path and not os.path.isabs(output_path):
        output_path = os.path.join(current_dir, output_path)
    
    result = corrupt_media_file_safe(input_path, output_path, args.level)
    
    if result:
        print(f"处理成功，输出文件: {result}")
        sys.exit(0)
    else:
        print("处理失败")
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    main()
