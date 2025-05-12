import os
import gradio as gr
import yaml
from tts import GPT_SoVits_TTS, CosyVoice_API

# 加载配置
def load_config():
    try:
        with open("config.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"加载配置文件失败: {str(e)}")
        return {}

config = load_config()

# 创建TTS实例
def create_tts_instance(tts_type, voice=None):
    if tts_type == "GPT-SoVits":
        tts = GPT_SoVits_TTS()
        # 如果有参考音频，初始化GPT-SoVits
        voice_name = voice.split(" ")[0] if voice else "少女"
        reference_audio = f"data/audio/{voice_name}.wav"
        if os.path.exists(reference_audio):
            tts.init_infer(reference_audio, "这是一段参考音频")
        return tts
    else:  # CosyVoice
        tts = CosyVoice_API()
        if voice:
            voice_name = voice.split(" ")[0] if " " in voice else voice
            tts.set_voice(voice_name)
        return tts

# 获取TTS选项
def get_tts_options():
    if config and "tts" in config:
        return config["tts"].get("options", ["GPT-SoVits", "CosyVoice"])
    return ["GPT-SoVits", "CosyVoice"]

# 获取音色选项
def get_voice_options():
    if config and "tts" in config:
        return config["tts"].get("voices", [])
    return ["longwan (CosyVoice)", "少女 (GPT-SoVits)"]

# 获取默认TTS模块
def get_default_tts():
    if config and "tts" in config:
        return config["tts"].get("default_module", "CosyVoice")
    return "CosyVoice"

# 文本转语音
def text_to_speech(text, tts_type, voice):
    if not text:
        return None, "请输入要合成的文本"
    
    # 创建输出目录
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建TTS实例
    tts = create_tts_instance(tts_type, voice)
    
    # 合成语音
    audio_path = tts.infer(output_dir, text)
    
    if not audio_path or not os.path.exists(audio_path):
        return None, "语音合成失败"
    
    return audio_path, f"已使用 {tts_type} 合成语音，音色: {voice}"

# 创建Gradio界面
def create_ui():
    with gr.Blocks(title="数字人对话系统 - TTS模块") as demo:
        gr.Markdown("# 数字人对话系统 - TTS模块")
        
        with gr.Row():
            with gr.Column(scale=3):
                text_input = gr.Textbox(label="输入文本", placeholder="请输入要合成的文本...", lines=5)
                
                with gr.Row():
                    tts_type = gr.Dropdown(
                        label="TTS引擎",
                        choices=get_tts_options(),
                        value=get_default_tts()
                    )
                    
                    voice = gr.Dropdown(
                        label="音色",
                        choices=get_voice_options(),
                        value=get_voice_options()[0] if get_voice_options() else None
                    )
                
                submit_btn = gr.Button("合成语音")
                
            with gr.Column(scale=2):
                audio_output = gr.Audio(label="合成结果")
                status_output = gr.Textbox(label="状态信息", interactive=False)
        
        # 更新音色选项
        def update_voice_options(tts_type):
            if tts_type == "GPT-SoVits":
                return gr.Dropdown.update(
                    choices=[v for v in get_voice_options() if "GPT-SoVits" in v],
                    value=[v for v in get_voice_options() if "GPT-SoVits" in v][0] if [v for v in get_voice_options() if "GPT-SoVits" in v] else None
                )
            else:  # CosyVoice
                return gr.Dropdown.update(
                    choices=[v for v in get_voice_options() if "CosyVoice" in v],
                    value=[v for v in get_voice_options() if "CosyVoice" in v][0] if [v for v in get_voice_options() if "CosyVoice" in v] else None
                )
        
        tts_type.change(update_voice_options, inputs=[tts_type], outputs=[voice])
        
        # 提交按钮事件
        submit_btn.click(
            text_to_speech,
            inputs=[text_input, tts_type, voice],
            outputs=[audio_output, status_output]
        )
    
    return demo

# 主函数
def main():
    demo = create_ui()
    demo.launch(share=False)

if __name__ == "__main__":
    main()