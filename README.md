<div align="center">
<!-- <h1>SUMix: Mixup with Semantic and Uncertain Information</h1> -->
<h2><a href="https://arxiv.org/abs/2312.11954">SUMix: Mixup with Semantic and Uncertain Information (ECCV 2024)</a></h2>

[Huafeng Qin](https://scholar.google.com/citations?user=5jvXcJ0AAAAJ&hl=zh-CN)<sup>1,2,5\*,†</sup>, [Xin Jin](https://scholar.google.com/citations?user=v3OwxWIAAAAJ&hl=zh-CN)<sup>1,2,\*</sup>, [Hongyu Zhu](https://scholar.google.com/citations?user=P-QctiYAAAAJ&hl=zh-CN)<sup>1,2,\*</sup>, Hongchao Liao<sup>1,2</sup>, [Mounim A. El-Yacoubi](https://scholar.google.com/citations?user=ObFYefYAAAAJ&hl=zh-CN)<sup>3</sup>, [Xinbo Gao](https://scholar.google.com/citations?user=VZVTOOIAAAAJ&hl=zh-CN&oi=sra)<sup>4</sup>

<sup>1</sup>[Chongqing Technology and Business University](https://www.ctbu.edu.cn/)

<sup>2</sup>[National Research base of Intelligent Manufacturing Service](https://ghjd.ctbu.edu.cn/)

<sup>3</sup>[Telecom SudParis, Institut Polytechnique de Paris](https://www.ip-paris.fr/telecom-sudparis)

<sup>4</sup>[Chongqing University of Posts and Telecommunications](https://www.cqupt.edu.cn/)

<sup>5</sup>Chongqing Micro-Vein Intelligent Technology Co.

<sup>*</sup> Equal Contribution <sup>†</sup> Corresponding Author
</div>

<p align="center">
<a href="https://arxiv.org/abs/2312.11954" alt="arXiv">
    <img src="https://img.shields.io/badge/arXiv-2312.11954-b31b1b.svg?style=flat" /></a>
<a href="https://github.com/JinXins/Adversarial-AutoMixup/blob/main/LICENSE" alt="license">
    <img src="https://img.shields.io/badge/license-Apache--2.0-%23B7A800" /></a>
<a herf="" alt="Github stars">
    <img src="https://img.shields.io/github/stars/JinXins/SUMix?color=blue" /></a>
</p>

<p align="center">
<img src="https://github.com/JinXins/SUMix/assets/124172716/1725dfb7-ab1e-4429-a34b-0dfdd3bc2a6f" width=75% height=75% 
class="center">
</p>

We propose **SUMix**, which consists of a mix ratio learning module and an uncertain estimation module. The former focuses on computing the proportion of two images and the latter aims to learn the uncertainty information of mixed samples. Firstly, we design a function to compute the semantic distance between the mixed and original samples to determine the ratio lambda. Secondly, we present a method to learn the uncertainty of the mixed. This adapted feature vector effectively mitigates issues related to computing the loss function caused by discrepancies in semantic and uncertainty aspects. 

### 📬 You can contact me by email: 158398730@qq.com or WeChat: *xinxinxinxin_j*.
**If you are interested in *palm or finger vein research*, please contact us!**
___
## 🛠 Installation
***💥News! ! !💥***  
***2024-07-8:*** **Please Wait for a while, we will release the code and checkpoints.**

***🔧How to install?🔧***  
*In fact, you can add our python file in **OpenMixup***.  
*There, you can see how to use it and the environment required. What you need to do is add or replace our files by folder inside OpenMixup, and then add the function names of the files in the `__init__.py` file*.   
*You also can download or find other Mixup methods in **OpenMixup("https://github.com/Westlake-AI/openmixup")***  
*Thanks contributors: **Siyuan Li[(@Lupin1998)](https://github.com/Lupin1998), Zichen Liu[(@pon7)](https://github.com/pone7) and Zedong Wang[(@Jacky1128)](https://github.com/Jacky1128)***.  
___
**Here are the commands to install OpenMixup**
```markdown
conda create -n openmixup python=3.8 pytorch=1.12 cudatoolkit=11.3 torchvision -c pytorch -y
conda activate openmixup
pip install openmim
mim install mmcv-full
git clone https://github.com/Westlake-AI/openmixup.git
cd openmixup
python setup.py develop
```
**Here are the commands to git clone SUMix**
```markdown
git clone https://github.com/JinXins/SUMix.git
```
___

## 📊 Experiments

### CIFAR-100
| Name             | alpha | Conference | ResNet18 | ResNeXt50 | Wide-ResNet28 | DeiT-Small | Swin-Tiny |
|------------------|-------|------------|----------|-----------|-----------|-----------|-----------|
| [CutMix](https://arxiv.org/abs/1905.04899)           | 0.2   | ICCV2019   | 78.17   | 78.32    | 84.45 | 74.12    | 80.64 |
| [SaliencyMix](https://arxiv.org/abs/2006.01791)      | 0.2   | ICLR2021   | 79.12   | 78.77    | 84.35 | 69.78    | 80.40 |
| [FMix](https://arxiv.org/abs/2002.12047)             | 0.2   | ArXiv      | 79.69   | 79.02    | 84.21 | 70.41    | 80.72 |
| [ResizeMix](https://arxiv.org/abs/2012.11101)        | 1.0   | CVMJ2023   | 80.01   | 80.35    | 84.87 | 68.45    | 80.16 |
| CutMix+SUMix           | 0.2   | -   | 79.78    | 79.91     | 84.56    | 75.26    | 80.32 |
| SaliencyMix+SUMix      | 0.2   | -   | 79.91    | 79.32     | 84.58    | 70.32    | 84.71 |
| FMix+SUMix             | 0.2   | -   | 80.20    | 80.79     | 84.32    | 70.69    | 80.73 |
| ResizeMix+SUMix        | 1.0   | -   | 80.38    | 80.72     | 84.91    | 68.78    | 80.59 |
___
### Tiny-ImageNet & ImageNet-1K(denote *)
| Name             | alpha | Conference | ResNet18 | ResNeXt50 | ResNet18 |
|------------------|-------|------------|----------|-----------|----------|
| CutMix           | 0.2   | ICCV2019   | 65.53    | 66.47     | 68.95    |
| SaliencyMix      | 0.2   | ICLR2021   | 64.60    | 66.55     | 69.16    |
| FMix             | 0.2   | ArXiv      | 63.47    | 65.08     | 69.96    |
| ResizeMix        | 1.0   | CVMJ2023   | 63.74    | 65.87     | 69.50    |
| CutMix+SUMix     | 0.2   | -   | 65.71    | 68.74     | 69.71    |
| SaliencyMix+SUMix| 0.2   | -   | 65.68    | 68.92     | 69.52    |
| FMix+SUMix       | 0.2   | -   | 63.69    | 67.12     | 70.48    |
| ResizeMix+SUMix  | 1.0   | -   | 65.30    | 67.49     | 69.76    |
___
### CUB-200, FGVC-Aircraft and Standford Cars
| Name             | alpha | Confrence  | CUB R18 | CUB RX50 | FGVC R18 | FGVC RX50 |
|------------------|-------|------------|---------|---------|---------|------------|
| CutMix           | 0.2   | ICCV2019   | 77.70   | 83.67   | 78.84   | 84.55   |
| SaliencyMix      | 0.2   | ICLR2021   | 75.77   | 82.83   | 79.78   | 84.31   |
| FMix             | 0.2   | ArXiv      | 77.28   | 84.06   | 79.36   | 84.10   | 
| ResizeMix        | 1.0   | CVMJ2023   | 78.50   | 84.16   | 78.10   | 84.08   |
| CutMix+SUMix     | 0.2   | -   | 78.20   | 83.71   | 79.72   | 85.84   |
| SaliencyMix+SUMix| 0.2   | -   | 76.98   | 82.84   | 79.90   | 84.49   |
| FMix+SUMix       | 0.2   | -   | 79.24   | 84.33   | 79.48   | 84.64   | 
| ResizeMix+SUMix  | 1.0   | -   | 78.56   | 84.23   | 80.29   | 85.12   |

___

## 😉 Citation
**If you feel that our work has contributed to your research, please cite it, 🥰 and please don`t forget to cite OpenMixup if you use this project ! 🤗 Thanks.**  
```markdown
@article{qin2024sumix,
  title={SUMix: Mixup with Semantic and Uncertain Information},
  author={Qin, Huafeng and Jin, Xin and Zhu, Hongyu and Liao, Hongchao and El-Yacoubi, Moun{\^\i}m A and Gao, Xinbo},
  journal={arXiv preprint arXiv:2407.07805},
  year={2024}
}
