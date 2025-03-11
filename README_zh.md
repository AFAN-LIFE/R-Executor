# R-Executor

**其他语言版本: [English](README.md), [中文](README_zh.md).**

**作者：AFAN（微信：afan-life）**   

R-Executor 是一个基于 Docker 的 R 语言执行环境，集成了 R 语言运行时和 Python 的 Flask 服务。通过 HTTP 请求，用户可以将 R 代码发送到 r-executor 容器中执行，并获取结果。该项目旨在提供一个跨平台的 R 语言调用解决方案，简化 R 代码的远程执行和结果获取。

## 项目特色
- Flask 集成：将 Flask 服务嵌入 R 的 Docker 环境中，构建一个可远程调用的 R 执行服务。
- 数据类型转换：利用 rpy2 将 R 的数据类型转换为 Python 的常规数据类型，支持通过 HTTP 解析返回结果。

## 目录说明

```
- app.py               # Flask 服务入口
- config.py            # 全局配置文件
- Dockerfile           # Docker 镜像构建文件
- requirements.txt     # Python 依赖列表，用于构建镜像
- r_packages.txt       # R 依赖列表，用于构建镜像
- compose.yaml         # Docker Compose 配置文件
- test/                # 测试用例
  - test0_local.py     # 测试容器内 R 代码执行
  - test1_basic.py     # 测试客户端请求获取 R 的不同数据类型结果
  - test2_lrm.py       # 测试客户端请求调用 rms 包的 lrm 进行逻辑回归
  - test3_plot.py      # 测试客户端请求绘制 nomogram 图表并保存
- train.csv            # 测试用例所用的数据集
- nom.png              # test3_plot.py 的输出结果（nomogram 图表）
```

## 使用方法

### 获取镜像

#### 直接从dockerhub拉取镜像

r-executor 镜像已发布到 Docker Hub，你可以通过以下命令直接拉取：

```bash
docker pull afanlife/r-executor
```

镜像地址：https://hub.docker.com/r/afanlife/r-executor

r-executor 镜像预装了 `Python 3.13.2` 和 `R 4.4.2`，并按照 `requirements.txt` 和 `r_packages.txt` 安装了默认的 Python 和 R 依赖。如果当前版本满足需求，可以直接从 Docker Hub 拉取镜像：

注意：r-executor的`app.py`是以挂载形式在容器内执行，可以直接更改无需重新构建镜像


#### 重新构建镜像

如果默认版本不满足需求，可以根据需要重新构建镜像：
- 如果需要更改 Python 或 R 的版本，可以修改 `Dockerfile`。
- 如果需要调整 Python 或 R 的依赖包，可以修改 `requirements.txt` 和 `r_packages.txt`。

```bash
docker build -t r-executor:1.0 .
```

镜像导出和加载相关指令：

```bash
docker save -o r_executor.tar r_executor
docker load -i r_executor.tar
```

### 容器启动

将当前目录的所有文件映射到容器内的 `/app` 目录，并启动服务。

手动启动：

```bash
docker run -it -p 5000:5000 -v .:/app r_executor /bin/bash
python app.py
```

或使用 Docker Compose 启动：

```bash
docker compose up 
```

## 测试用例

启动：`app.py`：

```
root@9f2585313bab:/app# Python app.py
3.5.17
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.17.0.2:5000
Press CTRL+C to quit
 * Restarting with stat
```

执行：`test1_basic.py`，测试基本数据类型：

```
{
  "data": {
    "dataframe": {
      "a": [
        1.0,
        2.0
      ],
      "b": [
        "x",
        "y"
      ]
    },
    "matrix": [
      1,
      2,
      3,
      4
    ],
    "vector": [
      1.0,
      2.0,
      3.0
    ]
  },
  "message": "R code run success",
  "status": "success"
}
```

执行：`test2_lrm.py`，测试导包使用逻辑回归模型：

```
{
  "data": {
    "accuracy": [
      0.991
    ],
    "model_summary": [
      "Logistic Regression Model",
      "",
      "lrm(formula = Heart_Disease ~ ., data = r_df)",
      "",
      "                       Model Likelihood     Discrimination    Rank Discrim.    ",
      "                             Ratio Test            Indexes          Indexes    ",
      "Obs          1000    LR chi2     238.07     R2       0.859    C       0.997    ",
      " 0            968    d.f.             4    R2(4,1000)0.209    Dxy     0.994    ",
      " 1             32    Pr(> chi2) <0.0001    R2(4,92.9)0.919    gamma   0.994    ",
      "max |deriv| 2e-05                           Brier    0.007    tau-a   0.062    ",
      "",
      "               Coef      S.E.    Wald Z Pr(>|Z|)",
      "Intercept      -109.6707 24.8000 -4.42  <0.0001 ",
      "Age               0.4953  0.1116  4.44  <0.0001 ",
      "Blood_Sugar       0.5558  0.1228  4.52  <0.0001 ",
      "Blood_Pressure    0.0135  0.0213  0.63  0.5270  ",
      "Weight            0.0647  0.0307  2.11  0.0352  ",
      ""
    ]
  },
  "message": "R code run success",
  "status": "success"
}
```

执行：`test3_plot.py`，测试图表生成和保存：

![](nom.png)

## 参考链接

- [r-base镜像构建](https://github.com/rocker-org/rocker/tree/master/r-base)