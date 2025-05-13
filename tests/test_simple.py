import os
import sys
import time

# 添加src目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tts import CosyVoice_API

def test_cosyvoice():
    """
    测试CosyVoice API功能
    """
    print("开始测试CosyVoice API...")
    
    # 创建输出目录
    output_dir = "test_output"
    os.makedirs(output_dir, exist_ok=True)
    
    # 初始化CosyVoice API
    tts = CosyVoice_API()
    print(f"当前音色: {tts.voice}")
    print(f"API密钥状态: {'已设置' if tts.api_key else '未设置'}")
    
    # 设置音色
    tts.set_voice("longcheng")
    print(f"已更改音色为: {tts.voice}")
    
    # 测试语音合成
    test_text = "这是一段测试文本，用于验证语音合成功能是否正常工作。"
    print(f"\n开始合成文本: {test_text}")
    
    start_time = time.time()
    output_file = tts.infer(output_dir, test_text)
    elapsed_time = time.time() - start_time
    
    print(f"语音合成耗时: {round(elapsed_time, 2)}秒")
    
    if output_file and os.path.exists(output_file):
        print(f"语音合成成功，输出文件: {output_file}")
        file_size = os.path.getsize(output_file)
        print(f"文件大小: {file_size} 字节")
        
        if file_size == 0:
            print("警告: 输出文件为空，可能是API密钥未设置或API调用失败")
    else:
        print("语音合成失败，未生成输出文件")
    
    print("\n测试完成!")
    print("提示: 如需正常使用API，请在config.yaml中设置有效的dashscope_api_key")

if __name__ == "__main__":
    test_cosyvoice()
