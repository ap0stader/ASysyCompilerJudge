# ASysyCompilerJudge

**A** **S**ysy Compiler Judge

By [@**A**p0stader](https://github.com/ap0stader) & [@**s**wkfk](https://github.com/swkfk)

## 简介

这是为BUAA编译技术课程实验设计的测评机。覆盖词法分析、语法分析、错误处理、代码生成等实验阶段，提供自动拉取评测、自定义评测模式等多种功能。

**若有疑问，欢迎Issue。若有好点子，欢迎PR！**

## 当前进度

开发语言：

- [x] Java (@Ap0stader)
- [ ] C++

实验阶段：

- [x] 词法分析（已完成）(@Ap0stader)
- [x] 语法分析（已完成开发，待上线）(@Ap0stader)
- [ ] 错误处理（待开发）(@Ap0stader)
- [x] 代码生成(LLVM)（已完成开发，待上线）(@swkfk)
- [ ] 代码生成(MIPS)（开发中）（@swkfk)

评测功能：

- [x] JAR文件自动拉取评测（已完成）(@Ap0stader)
- [x] MARS执行周期统计（已完成）(@swkfk)

- [ ] VSCode中打开与比较文件指令
- [ ] 代码生成阶段自定义评测

## 如何使用

### 说明

1. **本项目暂未进行Python最低可运行版本的测试，建议运行在Python3.10及以上版本。**可通过以下指令查看Python版本。如果有多Python环境需求，可以考虑使用[Miniconda](https://docs.anaconda.com/miniconda/)或[Anaconda](https://docs.anaconda.com/anaconda/)。

   ```shell
   $ python3 --version
   ```

2. 本项目需安装第三方依赖库，若下载过程缓慢，可能需要[更换PyPI镜像源](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/)。

### 下载与初始化

1. 克隆本仓库至本地。本项目仍处于快速迭代阶段，建议克隆本仓库而非直接下载ZIP压缩包以方便通过克隆获得更新。

   ```shell
   $ git clone https://github.com/ap0stader/ASysyCompilerJudge.git
   ```

2. 安装依赖库与初始化文件目录。**注意，初始化时将会清空runtime、testfile和config三个文件夹中的所有文件。若之前已建立这些文件夹，请先行备份其中数据再进行初始化。**

   ```shell
   $ python3 init.py
   ```

   执行到此处即为成功

   ```
   ............
   =======           Initialization End          =======
   Please configure the judge.
   See README.md for more details.
   ```

### 配置评测机

