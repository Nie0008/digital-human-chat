import os
import time
import subprocess
import requests
import json
from typing import Optional

class GPT_SoVits_TTS:
    """
    GPT-SoVits语音合成模块
    使用GPT-SoVits进行文本到语音转换
    """
    def __init__(self):
        """
        初始化GPT-SoVits语音合成模块
        """
        print("初始化GPT-SoVits语音合成模块...")
        self.initialized = False
        self.reference_audio = None
        self.reference_text = None
        
        # 创建音频目录
        os.makedirs("data/audio", exist_ok=True)
        
        # 检查预设音频文件是否存在
        self.check_preset_audio_files()
    
    def check_preset_audio_files(self):
        """
        检查预设音频文件是否存在
        """
        preset_voices = ["少女", "女性", "青年", "男性"]
        for voice in preset_voices:
            voice_path = f"data/audio/{voice}.wav"
            if not os.path.exists(voice_path):
                print(f"警告: 预设音频文件不存在: {voice_path}")
                # 在实际项目中，可以从网络下载预设音频文件
    
    def init_infer(self, reference_audio: str, reference_text: str):
        """
        初始化推理参数
        
        参数:
            reference_audio: 参考音频文件路径
            reference_text: 参考音频对应的文本
        """
        if not os.path.exists(reference_audio):
            print(f"参考音频文件不存在: {reference_audio}")
            return
            
        self.reference_audio = reference_audio
        self.reference_text = reference_text
        self.initialized = True
        print(f"GPT-SoVits初始化完成，参考音频: {reference_audio}")
    
    def infer(self, project_path: str, text: str, index: int = 0) -> str:
        """
        进行语音合成
        
        参数:
            project_path: 项目路径
            text: 要合成的文本
            index: 音频索引
            
        返回:
            合成的音频文件路径
        """
        if not self.initialized:
            print("GPT-SoVits未初始化，无法进行语音合成")
            return ""
            
        try:
            start_time = time.time()
            
            # 创建音频输出目录
            os.makedirs(project_path, exist_ok=True)
            output_audio = os.path.join(project_path, f"audio_{index}.wav")
            
            # 在实际项目中，这里应该调用GPT-SoVits的API或本地模型
            # 这里使用模拟实现，实际项目中需要替换为真实实现
            print(f"[模拟] 使用GPT-SoVits合成音频: {text}")
            
            # 模拟合成过程，复制参考音频作为输出
            if self.reference_audio and os.path.exists(self.reference_audio):
                import shutil
                shutil.copy2(self.reference_audio, output_audio)
            else:
                # 如果没有参考音频，创建一个空音频文件
                with open(output_audio, "wb") as f:
                    f.write(b"")
            
            print(f"语音合成耗时: {round(time.time()-start_time, 2)}秒")
            return output_audio
            
        except Exception as e:
            print(f"语音合成失败: {str(e)}")
            return ""


class CosyVoice_API:
    """
    CosyVoice语音合成API
    使用CosyVoice在线API进行文本到语音转换
    """
    def __init__(self):
        """
        初始化CosyVoice语音合成API
        """
        print("初始化CosyVoice语音合成API...")
        self.voice = "longwan"  # 默认音色
        self.api_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2audio/generation"
        self.api_key = None
        self.api_id = None
        
        # 从配置文件读取API密钥和ID
        self._load_config()
    
    def _load_config(self):
        """
        从配置文件加载API密钥和ID
        """
        try:
            import yaml
            config_path = "config.yaml"
            
            if os.path.exists(config_path):
                with open(config_path, "r", encoding="utf-8") as f:
                    config = yaml.safe_load(f)
                
                if config and "api" in config:
                    self.api_key = config["api"].get("dashscope_api_key")
                    self.api_id = config["api"].get("dashscope_api_id")
                    
                    if not self.api_key:
                        print("警告: 配置文件中未设置阿里云百炼API密钥")
                    else:
                        print("成功从配置文件加载阿里云百炼API密钥")
            else:
                print(f"警告: 配置文件不存在: {config_path}")
        except Exception as e:
            print(f"加载配置文件失败: {str(e)}")
    
    def set_voice(self, voice: str):
        """
        设置语音合成的音色
        
        参数:
            voice: 音色名称
        """
        self.voice = voice
        print(f"已设置音色: {voice}")
    
    def infer(self, project_path: str, text: str, index: int = 0) -> str:
        """
        进行语音合成
        
        参数:
            project_path: 项目路径
            text: 要合成的文本
            index: 音频索引
            
        返回:
            合成的音频文件路径
        """
        if not self.api_key:
            print("未设置阿里云百炼API密钥，无法使用CosyVoice API")
            return ""
            
        try:
            start_time = time.time()
            
            # 创建音频输出目录
            os.makedirs(project_path, exist_ok=True)
            output_audio = os.path.join(project_path, f"audio_{index}.wav")
            
            # 准备API请求
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # 构建请求负载
            payload = {
                "model": "cosyvoice-v1",
                "input": {
                    "text": text
                },
                "parameters": {
                    "voice": self.voice
                }
            }
            
            # 如果有API ID，添加到请求中
            if self.api_id:
                payload["api_id"] = self.api_id
            
            # 发送API请求
            print(f"[CosyVoice] 发送请求: {text}")
            try:
                response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
                
                if response.status_code == 200:
                    # 尝试解析响应内容
                    try:
                        # 检查响应是否为JSON格式
                        if response.headers.get('Content-Type', '').startswith('application/json'):
                            result = response.json()
                            # 检查是否有音频数据URL
                            if 'output' in result and 'audio_file' in result['output']:
                                audio_url = result['output']['audio_file']
                                # 下载音频文件
                                audio_response = requests.get(audio_url, timeout=30)
                                if audio_response.status_code == 200:
                                    with open(output_audio, "wb") as f:
                                        f.write(audio_response.content)
                                    print(f"语音合成成功，保存到: {output_audio}")
                                else:
                                    raise Exception(f"下载音频文件失败: {audio_response.status_code}")
                            else:
                                # 直接保存响应内容为音频文件
                                with open(output_audio, "wb") as f:
                                    f.write(response.content)
                                print(f"语音合成成功，保存到: {output_audio}")
                        else:
                            # 直接保存响应内容为音频文件
                            with open(output_audio, "wb") as f:
                                f.write(response.content)
                            print(f"语音合成成功，保存到: {output_audio}")
                    except Exception as e:
                        print(f"处理API响应失败: {str(e)}")
                        # 尝试直接保存响应内容
                        with open(output_audio, "wb") as f:
                            f.write(response.content)
                        print(f"已保存原始响应内容到: {output_audio}")
                elif response.status_code == 401:
                    print(f"API认证失败: 请检查API密钥是否正确")
                    # 创建一个空音频文件作为替代
                    with open(output_audio, "wb") as f:
                        f.write(b"")
                elif response.status_code == 429:
                    print(f"API请求超过限制: 请稍后再试")
                    # 创建一个空音频文件作为替代
                    with open(output_audio, "wb") as f:
                        f.write(b"")
                else:
                    error_msg = ""
                    try:
                        error_data = response.json()
                        if 'message' in error_data:
                            error_msg = error_data['message']
                    except:
                        error_msg = response.text
                    
                    print(f"API请求失败: 状态码 {response.status_code}, 错误信息: {error_msg}")
                    # 创建一个空音频文件作为替代
                    with open(output_audio, "wb") as f:
                        f.write(b"")
            except requests.exceptions.Timeout:
                print("API请求超时，请检查网络连接")
                # 创建一个空音频文件作为替代
                with open(output_audio, "wb") as f:
                    f.write(b"")
            except requests.exceptions.ConnectionError:
                print("API连接错误，请检查网络连接")
                # 创建一个空音频文件作为替代
                with open(output_audio, "wb") as f:
                    f.write(b"")
            
            print(f"语音合成耗时: {round(time.time()-start_time, 2)}秒")
            return output_audio
            
        except Exception as e:
            print(f"语音合成失败: {str(e)}")
            # 创建一个空音频文件作为替代
            try:
                with open(output_audio, "wb") as f:
                    f.write(b"")
                return output_audio
            except:
                return ""