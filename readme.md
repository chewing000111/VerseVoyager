<div align=center>
<h1 aligh="center">
梅宿莺 (VerseVoyager)
</h1>
</div>

**梅宿莺: 一个中日双语诗词向量数据库搜索引擎**
**如果喜欢这个项目，请给它一个Star**

VerseVoyager: A Chinese-Japanese Bilingual Poetic Vector Database Search Engine
If you like this project, please give it a Star.

> [!NOTE]
> 1.本项目使用国内中文大语言模型智谱GLM，如希望使用其他大语言模型，请修改`src/glm.py`文件
>
> 2.本项目可以存在多个数据集，可以使用`编译数据库.py`对json格式的文件编译为需要的项目文件，所有的数据集文件都存放在`data/sentence_embeddings`文件夹内，以`[朝代]_[id].pt`的格式存在。
>
> 2.本项目提供了几个已经编译好的数据集文件放在[release](https://github.com/chewing000111/VerseVoyager/releases/tag/dataset)里，下载其中的sentence_embeddings.zip解压至./data/sentence_embeddings目录中。文件结构如下
> ```
> data
>   - sentence_embeddings
>       - 平安_0.pt
>       - 唐_300.pt
> ```

| 功能         | 描述                                                         |
| ------------ | ------------------------------------------------------------ |
| 中日双语搜索 | 支持用自然语言对诗词数据库进行检索，支持中日双语             |
| 诗词展示     | GUI内中日显示随意切换，可以直接拷贝完整诗词，标注符合条件的语句，展示其来源诗词和作者朝代信息 |
| 快速跳转     | 提供速览目录，可方便快速跳转到指定诗词                       |
| 历史搜索     | 保留历史搜索记录，双击记录可直接跳转至对应记录               |

- **GUI**

![GUI](data/pics/show1.png)

- **日文搜索**

![JP](data/pics/show2.png)

# Installation

1. 下载项目

    ```sh
    git clone --depth=1 https://github.com/binary-husky/gpt_academic.git
    cd gpt_academic
    ```

2. 安装conda环境

    - 选择I:  (bat自动安装) win系统可直接运行`运行 - 初始创建环境.bat`或者`运行 - 初始创建环境cpu版本.bat`
    - 选择II: (conda手动安装)

    ```sh
    call conda create -n poetry python=3.10   # 创建anaconda环境
    conda activate poetry                     # 激活anaconda环境
    # 自行选择CPU还是GPU版本
    python -m pip install -r requirements.txt
    python -m pip install -r requirements_cpu.txt
    ```
    - 选择III: (python安装) python推荐版本 3.9 ~ 3.11

    ```sh
    # 自行选择CPU还是GPU版本
    python -m pip install -r requirements.txt
    python -m pip install -r requirements_cpu.txt
    ```

3. 配置API_KEY等变量

    在`data/settings.yaml`中，配置API KEY等变量。

4. 下载BERT-CCPoem

    在[BERT-CCPoem](https://github.com/THUNLP-AIPoet/BERT-CCPoem)项目中下载BERT_CCPoem_v1的模型文件，放入BERT_CCPoem_v1文件夹中。


# Usage

win系统可直接运行`运行.bat`

其它系统：

```sh
conda activate poetry
python .\app.py
```

编译新的数据库：

准备json格式的数据集文件并修改`编译数据库.py`里的对应文件路径

json文件格式(可参考`data/poet.song.test.json`)：

```json
[
    {
        "title": "日诗",
        "author": "宋太祖",
        "paragraphs": [
            "欲出未出光辣达，千山万山如火发。",
            "须臾走向天上来，逐却残星赶却月。"
        ],
        "paragraphs_tr": [
            "出でんと欲して未だ出づ光辣の达，千山万山火の如く発き。",
            "须臾にして天上に向って上る，逐却する残星は月を赶却す。"
        ]
    },
    ...
]
```

直接运行`运行 - 编译数据库.bat` 或

```sh
conda activate poetry
python .\编译数据库.py
```

# 参考与学习

```
项目开发过程中使用了很多项目

[GUI]NiceGUI
https://github.com/zauberzeug/nicegui

[向量数据库]faiss
https://github.com/facebookresearch/faiss

[Bert]BERT-CCPoem
https://github.com/THUNLP-AIPoet/BERT-CCPoem

[数据集]chinese-poetry
https://github.com/chinese-poetry/chinese-poetry

[翻译]Kanbun-LM
https://github.com/nlp-waseda/Kanbun-LM
```
## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->