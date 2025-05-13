import os
import sys
import unittest

# 添加src目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tts import GPT_SoVits_TTS, CosyVoice_API

class TestTTS(unittest.TestCase):
    """
    测试TTS模块功能
    """
    
    def setUp(self):
        """
        测试前的准备工作
        """
        # 确保输出目录存在
        self.output_dir = "test_output"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 确保音频目录存在
        self.audio_dir = "data/audio"
        os.makedirs(self.audio_dir, exist_ok=True)
    
    def test_gpt_sovits_initialization(self):
        """
        测试GPT-SoVits初始化
        """
        tts = GPT_SoVits_TTS()
        self.assertFalse(tts.initialized)
        self.assertIsNone(tts.reference_audio)
        self.assertIsNone(tts.reference_text)
        
        # 创建测试音频文件
        test_audio = os.path.join(self.audio_dir, "test.wav")
        with open(test_audio, "wb") as f:
            f.write(b"")
        
        # 测试初始化
        tts.init_infer(test_audio, "测试文本")
        self.assertTrue(tts.initialized)
        self.assertEqual(tts.reference_audio, test_audio)
        self.assertEqual(tts.reference_text, "测试文本")
    
    def test_gpt_sovits_infer(self):
        """
        测试GPT-SoVits推理
        """
        tts = GPT_SoVits_TTS()
        
        # 未初始化时的推理
        result = tts.infer(self.output_dir, "测试文本")
        self.assertEqual(result, "")
        
        # 创建测试音频文件
        test_audio = os.path.join(self.audio_dir, "test.wav")
        with open(test_audio, "wb") as f:
            f.write(b"")
        
        # 初始化后的推理
        tts.init_infer(test_audio, "测试文本")
        result = tts.infer(self.output_dir, "测试文本")
        self.assertTrue(os.path.exists(result))
    
    def test_cosyvoice_initialization(self):
        """
        测试CosyVoice初始化
        """
        tts = CosyVoice_API()
        self.assertEqual(tts.voice, "longwan")
        self.assertIsNone(tts.api_key)
        self.assertIsNone(tts.api_id)
    
    def test_cosyvoice_set_voice(self):
        """
        测试CosyVoice设置音色
        """
        tts = CosyVoice_API()
        tts.set_voice("longcheng")
        self.assertEqual(tts.voice, "longcheng")
    
    def test_cosyvoice_infer_without_api_key(self):
        """
        测试CosyVoice在没有API密钥的情况下推理
        """
        tts = CosyVoice_API()
        result = tts.infer(self.output_dir, "测试文本")
        self.assertEqual(result, "")
    
    def tearDown(self):
        """
        测试后的清理工作
        """
        # 清理测试生成的文件
        import shutil
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        
        # 清理测试音频文件
        test_audio = os.path.join(self.audio_dir, "test.wav")
        if os.path.exists(test_audio):
            os.remove(test_audio)

if __name__ == "__main__":
    unittest.main()
