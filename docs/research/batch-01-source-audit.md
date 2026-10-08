# 第一批内容来源核查记录

本文件记录第一批正文使用的来源定位、核查结果和缺口。它是研究审计记录，不是兼容矩阵、部署手册或本地实验结果。

2026-09-30 补审：用户授权 Codex 主助手替代 astra，已完成[第一批审阅](batch-01-codex-review.md)，本批未发现需要修改的问题；没有实际派发 astra/xhigh 或执行硬件验证。四批总体状态见[补审汇总](batch-01-02-08-09-codex-review-summary.md)。下文保留原来源审计结果。

## E01：昇腾软件栈文档配套档案

### 选定基线

- 官方仓库：`Ascend/pytorch`。
- 发行 tag：`v7.2.0-pytorch2.6.0`。
- 2026-09-29 查询官方远端得到 annotated tag 对象 `d5b59de96811e24be9f580ff3b85c8ef6c608f23`，解引用 commit 为 `bc51ab84cc6f35c77aab1c59886e0ea43681a317`。
- 内容引用固定到 commit；不依赖 tag 或分支以后仍指向同一对象。
- README 声明的组合：PyTorch 2.6.0、`torch_npu` 安装包 2.6.0.post3、CANN 8.3.RC1、Python 3.9.x/3.10.x/3.11.x；源码分支名为 `v2.6.0-7.2.0`。
- `version.txt` 为 `2.6.0.post3`。该一致性只说明文件声明相符，没有核验发布 wheel 的构建来源。

### 已核查文件和页面

| 对象 | 固定定位 | 结果 |
|---|---|---|
| 英文 README | <https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/README.md> | 可访问；二进制安装段、Python 表和 CANN 配套表可相互核对。 |
| 版本文件 | <https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/version.txt> | 可访问；内容为 `2.6.0.post3`。 |
| 根许可证 | <https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/LICENSE> | 可访问；包含 BSD 3-Clause 条款。只登记根代码范围。 |
| 中文 README | <https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/README.zh.md> | 可访问，但文件残留 `<<<<<<<`/`=======`/`>>>>>>>` 合并冲突标记；未作为 tuple 的主要证据。 |
| `COMPATIBILITY.md` / `.en.md` | 同一固定 commit | 不存在；该版本的配套矩阵在 README 中。不能引用 `master` 的同名文件冒充历史快照证据。 |
| `docs/LICENSE` | 同一固定 commit | 请求返回 404；该快照的文档许可状态保持未知。 |
| CANN commercial 8.3.RC1 `instg_0033.html` | <https://www.hiascend.com/document/detail/zh/canncommercial/83RC1/softwareinst/instg/instg_0033.html> | 纠错记录：直接打开后标题为“卸载驱动和固件”，内容是卸载命令。先前采用的检索片段与精确页面不符，不能支持安装前置或 Python 范围；相关断言和 source ref 已撤回。 |
| CANN community 入口 | <https://www.hiascend.com/zh/software/cann/community> | 直接读取只返回需要 JavaScript 的页面外壳，未取得固定 8.3.RC1 配套内容。 |
| 候选 commercial 8.3.RC1 `instg_0001.html` | <https://www.hiascend.com/document/detail/zh/canncommercial/83RC1/softwareinst/instg/instg_0001.html> | 当前读取工具报告不可访问，未用作证据。 |
| 候选 commercial 8.3.RC1 `instg_0002.html` | <https://www.hiascend.com/document/detail/zh/canncommercial/83RC1/softwareinst/instg/instg_0002.html> | 当前读取超时，未用作证据。 |

### 没有执行的动作

没有克隆或运行上游脚本，没有安装 PyTorch、TorchNPU、CANN 或 HDK，没有下载 wheel/安装包，没有访问真实 NPU，也没有运行算子、通信或性能测试。

### 保持未知的条件

- 具体硬件对应的 firmware/driver 版本和补丁；
- 操作系统、内核、glibc、主机架构及容器镜像；
- CANN 子包和算子包的完整安装集合；
- wheel 的摘要、内含 `METADATA`、构建 commit 及二进制许可/notice；
- MindCluster、MindSpeed/MindSpeed-LLM、vLLM Ascend 与本基线的同版本官方交集。

### 固定 tag 的复核方式

2026-09-29 对[官方远端仓库](https://github.com/Ascend/pytorch)执行只读引用查询，未克隆仓库：

```bash
git ls-remote https://github.com/Ascend/pytorch.git 'refs/tags/v7.2.0-pytorch2.6.0*'
```

本次返回：

```text
d5b59de96811e24be9f580ff3b85c8ef6c608f23  refs/tags/v7.2.0-pytorch2.6.0
bc51ab84cc6f35c77aab1c59886e0ea43681a317  refs/tags/v7.2.0-pytorch2.6.0^{}
```

这是本次引用解析结果，不保证远端 tag 永久不变。主审另行读取固定 commit 的英文 README、version.txt 与根 LICENSE，核对了组合、版本字段和许可条款。

## F05/F06：概念与判断方法的来源

| 已登记来源 ID | 定位与范围 | 未覆盖的判断 |
|---|---|---|
| `src.nvidia.cuda-toolkit-12-8` | [CUDA 12.8.0 归档入口](https://docs.nvidia.com/cuda/archive/12.8.0/)及[安装指南元包表](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-installation-guide-linux/#meta-packages)：核对 Toolkit 所列组件与驱动包边界 | 当前部署版本推荐、GPU 环境实测 |
| `src.kubernetes.device-plugins-v1-32` | [Kubernetes v1.32 Device Plugins](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/)：核对注册、健康上报与 Allocate 职责 | Ascend 或 NVIDIA 某个厂商插件实现的具体能力 |
| `src.vllm.plugin-system-v0-14` | [vLLM v0.14.0 Plugin System](https://docs.vllm.ai/en/v0.14.0/design/plugin_system/)：核对引擎 platform plugin 扩展点 | 任意 vLLM Ascend 与引擎版本的兼容关系 |
| `src.ascend.torch-npu-v7.2.0-pytorch2.6.0` | 上述固定快照；F05 使用角色和 CANN 依赖，F06 使用发行包、源码身份与配套声明的区别 | 具体 wheel 与源码二进制同一性、HDK 配套或整栈实测 |

以上四项已写入[来源表](../../sources/registry.yaml)，与初始八个发现入口分开。表中版本化文档页面不等同于固定 Git commit；本批未核对完整上游项目的全部能力。F06 的两轴判定、字段清单和故障归属提示属于本库整理方法，不表述为上游标准。

## 入库审读记录

三位作者与一位独立审读子代理均使用 `gpt-5.6-sol`、`high` 推理；主审负责整合和交叉核查。实质修正包括：

- 撤回 CANN 错链及其不能支持的安装条件。
- 将 TorchNPU README 能支持的关系限于 PyTorch 适配与 CANN 依赖，不把驱动/固件描述归给未包含该说明的 README。
- 将源码身份移出兼容判定表，不用 `supported` 表示版本文件存在或值一致。
- 将缺少具体来源的厂商插件职责改为通用 Kubernetes 接口描述。

三篇正文保持 `draft`，核对范围内使用 `source_checked`。结构校验和目录构建不替代技术审核或硬件实验；未知项保留在 E01 正文，后续有新证据时逐项更新。
