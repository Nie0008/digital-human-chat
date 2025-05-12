# 数字人对话系统

基于阿里云百炼的数字人对话系统，支持语音识别、大语言模型对话、语音合成和数字人生成。

## 功能特点

- 支持多种数字人形象
- 支持语音输入和文本输入
- 支持音色克隆
- 支持知识库检索增强
- 支持单轮对话和互动对话模式
- 支持模型参数调整

## 安装说明

1. 克隆仓库
```bash
git clone https://github.com/Nie0008/digital-human-chat.git
cd digital-human-chat
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置阿里云百炼API
在`config.yaml`文件中填入您的阿里云百炼API密钥

4. 运行应用
```bash
python app.py
```

## 使用说明

1. 访问 http://localhost:7860 打开Web界面
2. 选择数字人形象、对话模式和TTS音色
3. 可以通过麦克风录制音频或直接输入文本进行对话
4. 可以上传知识库文件增强对话能力
5. 可以调整模型参数以获得不同的对话效果

## 依赖说明

本项目依赖已经更新，支持Python 3.8-3.12版本。主要依赖包括：

- gradio: Web界面
- modelscope_studio: 模型服务
- torch: 深度学习框架
- diffusers: 扩散模型
- funasr: 语音识别
- dashscope: 阿里云百炼API

## 许可证

MIT