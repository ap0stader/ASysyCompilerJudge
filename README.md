# ASysyCompilerJudge

**A** **S**ysy Compiler Judge

By [@**a**p0stader](https://github.com/ap0stader) & [@**s**wkfk](https://github.com/swkfk)

## 简介

这是为BUAA编译技术课程实验设计的测评机。覆盖词法分析、语法分析、语义分析、代码生成等实验阶段，提供自动拉取评测、自定义评测模式等多种功能。

**若有疑问，欢迎Issue。若有好点子，欢迎PR！**

## 当前进度

开发语言：

- [x] Java (@ap0stader)
- [ ] C++

实验阶段：

- [x] 词法分析（已完成）(@ap0stader)
- [x] 语法分析（已完成）(@ap0stader)
- [ ] 语义分析（待开发）(@ap0stader)
- [x] 代码生成(LLVM)（已完成开发，待上线）(@swkfk)
- [ ] 代码生成(MIPS)（开发中）(@swkfk)

评测功能：

- [x] JAR文件自动拉取评测（已完成）(@ap0stader)
- [x] GUI（已完成开发，待上线）(@swkfk)
- [x] 自定义评测（已完成开发，待上线）(@ap0stader)
- [x] MARS执行周期统计（已完成开发，待上线）(@swkfk)
- [ ] VSCode打开与比较文件指令
- [ ] 测试文件持续监控评测

## 如何更新

*Author: @ap0stader*

1. 本项目仍在快速迭代中，稳定的分支为**main分支**，

2. 更新时，请先拉取，然后运行**update.py**。

   ```shell
   $ git pull
   $ python update.py
   ```

3. update.py将引导完成有冲突的升级工作。

   ```shell
   $ python update.py
   =======   ASysyCompilerJudge Update   =======
   >>>>>  Update dependencies
   ......
   >>>>> Update custom_judge.py
   A new version of custom_judge.py is prepared. Do you want to replace? [Y/N] 
   ......
   ```

## 如何使用

*Author: @ap0stader*

### 说明

1. 本项目暂未进行Python最低可运行版本的测试，**但是应至少运行在Python3.10及以上版本。**可通过以下指令查看Python版本。如果有多Python环境需求，可以考虑使用[Miniconda](https://docs.anaconda.com/miniconda/)或[Anaconda](https://docs.anaconda.com/anaconda/)。

   ```shell
   $ python --version
   Python 3.11.9
   ```

2. 本项目需安装第三方依赖库，若下载过程缓慢，可能需要[更换PyPI镜像源](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/)。

### 快速开始

1. 克隆本仓库至本地。本项目仍处于快速迭代阶段，**建议克隆本仓库**而非直接下载ZIP压缩包以方便通过`git pull`获得更新。

   ```shell
   $ git clone https://github.com/ap0stader/ASysyCompilerJudge.git
   ```

2. 安装依赖库与初始化文件目录。**注意，初始化时将会清空runtime、testfile和config三个文件夹中的所有文件。若之前已建立这些文件夹，请先行备份其中数据再进行初始化。**

   ```shell
   $ python init.py
   ```

   执行到此处即为成功

   ```
   ......
   =======           Initialization End          =======
   Please configure the judge.
   See README.md for more details.
   ```

3. 完成初始化后可以在项目的根目录找到config文件夹。**注意：config_example文件中保存的是配置文件的示例，如果配置文件出现了错误，可以按照config_example对应的文件进行恢复。请不要删除config_example文件夹。**

   ```
   config
   ├── command.json
   ├── custom_judge.py
   ├── lang.json
   └── stage.json
   ```

4. 配置lang.json，该文件包括开发语言信息。`"programming language"`中配置开发语言，目前测评机支持Java(`"java"`)。若开发语言为Java，需要在`"java"`中的`"jar_path"`配置生成的编译程序的JAR文件的**绝对路径**（路径支持包含中文字符），建议填写IDEA等开发工具生成JAR的路径，这样后续有新版本JAR生成了，测评机可以**自动监测到并且拉起评测**。**注意：配置文件请保存为UTF-8编码，否则可能导致解析或运行时的编码错误。请先生成JAR之后再配置，测评机启动时会检测JAR文件是否存在。**

   ```javascript
   {
     "programming language": "java", // Java -> java
     "java": {
       "jar_path": "PATH_TO_JAR"
       // 路径支持包含中文字符
       // Linux/macOS示例："jar_path": "/Users/ap0stader/编译/artifacts/Compiler.jar"
       // Windows示例："jar_path": "D:\\编译器\\artifacts\\Compiler.jar"
       // Windows注意反斜杠需要转义！
     }
   }
   ```

5. 在平台的课程信息下教学资料中下载公共测试程序库，并且解压到testfile文件夹中的**对应阶段的文件夹中**。

   ```
   testfile
   ├── code_generation
   ├── lexical_analysis
   │   ├── A
   │   │   ├── testcase1
   │   │   │   ├── ans.txt
   │   │   │   ├── in.txt
   │   │   │   └── testfile.txt
   │   │   └── ...
   │   ├── B
   │   │   ├── testcase1
   │   │   └── ...
   │   └── C
   │       ├── testcase1
   │       └── ...
   ├── semantic_analysis
   └── syntax_analysis
   ```
   
6. 启动测评机，选择需要评测的阶段，**确认启动测评机**。启动测评机后，将自动进行第一次测评。

   ```shell
   $ python main.py
   >>> Parsing configurations...
   [1] Lexical Analysis
   [2] Syntax Analysis
   [C] Custom
   Please select the stage_input of your project [1-2 or C] 1
   >>> Executor is ready!
   
   - Programming language: Java
   - JAR file path: PATH_TO_JAR
   Start observing JAR file? [Y/N] Y
   
   >>> Creating Java Observer...
   >>> All Observer Started!
   >>> Press Ctrl+C to exit.
   >>> Starting Executor...
   No. 1  ......
   ```
   
7. 若开发语言为Java，在使用IDEA等开发工具生成新的JAR之后，评测机将**自动拉取新生成的JAR并自动进行测评**。

   ```
   ...
   Results folder: results/...
   >>> Judge finished! Continuing... 
   New Compiler.jar has been detected and copied.
   >>> Starting Executor...
   No. 67  ......
   ```

8. 测评完成后，可在results文件中查看生成的测评结果。其中的文件夹以测评开始的时间的命名。每个文件夹中的summary.txt为**测评信息摘要**。其他部分按照导入的测试程序文件结构组织。与每个测试点testfile.txt同级的info.txt为该**测试点运行和评测的信息**。

   ```
   ...
   ├── A
   │   ├── testcase1
   │   │   ├── info.txt
   │   │   ├── lexer.txt
   │   │   └── testfile.txt
   │   └── ...
   ├── B
   │   └── ...
   ├── C
   │   └── ...
   └── summary.txt
   ```