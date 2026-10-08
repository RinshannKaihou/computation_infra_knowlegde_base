# 第五批 NVIDIA 配套档案候选

2026-09-29，主任务预查；不是 E02 正文或部署推荐。

已实际打开 [NVIDIA PyTorch Release 25.01](https://docs.nvidia.com/deeplearning/frameworks/pytorch-release-notes/rel-25-01.html)。它可作为一个有发行编号的容器文档样板，但仍需取镜像 tag/digest、支持矩阵、对应许可和设备环境。

候选明确字段：容器 release 25.01、PyTorch `2.6.0a0+ecf3bae40a`、CUDA `12.8.0.038`、cuDNN `9.7.0.66`、NCCL `2.25.1`。这不是现有 F10 的上游 PyTorch v2.6.0 固定源码，也不是 F07 的 PyTorch 2.8/NCCL 2.27.5 样板；不得合并成已验证环境。

页面含需保留的冲突：

- Driver Requirements 首段把部分 R545 列为数据中心 GPU 的例外驱动，紧接段落又把 R545 列为应升级的非 forward-compatible 分支。不要按第一段写“R545 已支持”；应另查当期 compatibility 资料，证据不足时该例外保持 unresolved。
- Contents 中列 Ubuntu 24.04/Python 3.12，但正文另处安装路径写 `python3.10/dist-packages`。只能记录文档所列版本与路径存在差异，实际解释器和包身份需取制品证据。
- 容器里的 Ubuntu 版本不是宿主机 OS 支持声明；目录出现 CUDA 也不等于宿主机驱动已兼容。

正式作者可选择更一致的发行样板，但不能为了表格完整而略去实际发现的冲突。此处没有拉取镜像、执行容器、读取本地主机 GPU 状态或确认完整部署组合。
