# 介绍
本项目融合了语音识别，VLM(视觉语言)模型，目标跟踪模型，机器人控制算法等多个AI领域。用语音控制玩原神，只需要动嘴就可以玩原神。
通过构建怪物目标检测数据集，用半监督方法学习(标注5%)，为整个数据集标注伪标签。
根据目标检测伪标签构建VLM伪标签，学习根据语言描述定位图中物体。

# 安装
首先安装基本依赖
```bash
pip install -r requirements.txt
```

安装mmcv-full
```bash
pip install openmim
mim install mmcv-full
```

安装vs2019或以上。

## 安装mmtracking
安装方法参考[mmtracking](https://github.com/open-mmlab/mmtracking)

## 安装wenet
```bash
pip install wenet
```

## 运行程序
```bash
python voice_play.py
```