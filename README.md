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

1. 完成初始化后可以在项目的根目录找到config文件夹。**注意：config_example文件中保存的是配置文件的示例，如果配置文件出现了错误，可以按照config_example对应的文件进行恢复。请不要删除config_example文件夹。**

    ```
    config
    ├── command.json
    ├── lang.json
    └── stage.json
    ```

2. **必须**配置lang.json，该文件包括开发语言信息。`"programming language"`中配置开发语言，目前测评机支持Java(`"java"`)。若开发语言为Java，需要在`"java"`中的`"jar_path"`配置生成的编译程序的JAR文件的**绝对路径**。**注意：请先使用IDEA等开发工具生成JAR之后再配置，测评机启动时会检测JAR文件是否存在**

   ```json
   {
     "programming language": "java", // Java -> java
     "java": {
       "jar_path": "PATH_TO_JAR"
       // 示例："jar_path": "/Users/ap0stader/Compiler/artifacts/Compiler.jar"
       // 示例："jar_path": "D:\Compiler\artifacts\Compiler.jar"
     }
   }
   ```

3. **可选**配置stage.json，该文件包括实验各阶段的运行和测评信息。以词法分析(`lexical_analysis`)为例，`"args"`表示评测机运行JAR文件时传入的参数，建议自行设计编译程序的传入参数体系~~以防止被判为抄袭~~ ***（提示：课程平台运行时的传入参数以课程平台公布为准，可能无参数）***。`"testfile_path"`为测试用例存放的文件夹。在初始化时已经在项目的根目录生成好了testfile的目录结构。`"sourcecode_prefix"`为测试用例的源代码文件名称前缀，`"answer_prefix"`为测试用例的答案文件名称前缀，在代码生成阶段还需要指定`"input_prefix"`即输测试用例的入数据文件名称前缀。*（具体见**数据导入**部分）*

   ```json
   {
     "lexical_analysis": {
       "args": "-LEX",
       "testfile_path": "./testfile/lexical_analysis/",
       "sourcecode_prefix": "testfile",
       "answer_prefix": "output"
     },
   	............
   }
   ```

4. command.json文件包括评测LLVM IR时需要用到的指令信息。*（具体见**代码生成**评测部分，待开发上线）*