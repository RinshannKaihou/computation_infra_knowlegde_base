# 第一批审阅记录（用户授权由 Codex 替代 astra）

审阅日期：2026-09-30。审阅者：本会话 Codex 主助手。用户明确要求由本助手替代 astra 审阅 batch 01、02、08、09；本次没有派发 gpt-6-astra/xhigh，也没有使用子代理。此授权仅覆盖这四批补审，不自动修改后续批次的审阅约定。

**结论：本次来源与内容审阅未发现需要修改的问题。** 三篇正文保持 `draft`；没有硬件、安装或整栈兼容性验证。原来源审计中的历史核查和未知项继续保留。

## 审阅对象

| 任务 | 正文 | 核查重点 |
|---|---|---|
| F05 | [主机到模型执行的软件栈分层](../../knowledge/02-software-stack/layers-and-boundaries.md) | 驱动、平台软件、框架后端、引擎插件和设备插件的职责边界 |
| F06 | [如何判断版本配套是否有依据](../../knowledge/02-software-stack/compatibility-evidence.md) | 官方声明与本地验证的两轴；源码、wheel、分支与版本文件的身份 |
| E01 | [昇腾软件栈的文档配套档案](../../knowledge/02-software-stack/ascend-documented-profile.md) | 固定 TorchNPU 配套声明；CANN 补充页的范围；整栈与 HDK 缺口 |

同时读取[第一批来源审计](batch-01-source-audit.md)、来源登记、元数据与导航；E01 的第二批补充核查见[第二批审阅](batch-02-codex-review.md)。正文版本由[四批汇总](batch-01-02-08-09-codex-review-summary.md)的 SHA-256 清单固定。

## 独立核对结果

| 主张或边界 | 本次重新读取的直接来源 | 判断 |
|---|---|---|
| TorchNPU 文档列出扩展 `2.6.0.post3`、PyTorch `2.6.0`、CANN `8.3.RC1`、源码分支 `v2.6.0-7.2.0`，Python 表列出 3.9–3.11 | 固定 commit `bc51ab84cc6f35c77aab1c59886e0ea43681a317` 的 [README](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/README.md) 安装段与配套表；[version.txt](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/version.txt) | 与正文一致；文件值一致不证明某个 wheel 与本地构建等价 |
| CUDA Toolkit 元包与驱动包不能混称 | [CUDA 12.8 Linux Installation Guide：Meta Packages](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-installation-guide-linux/#meta-packages) | `cuda-toolkit-12-8` 与包含运行依赖/驱动的元包边界支持正文的区分 |
| Kubernetes 设备插件属于资源发现/分配链，不能替代框架设备后端 | [Kubernetes v1.32 Device Plugins](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/) 的注册、ListAndWatch 与 Allocate 段 | 正文没有将通用接口扩张为厂商插件的完整能力 |
| vLLM 具有平台插件扩展点，但这不证明某 Ascend 插件与引擎配套 | [vLLM v0.14.0 Plugin System](https://docs.vllm.ai/en/v0.14.0/design/plugin_system/) | 支持角色区分；正文未作传递兼容性断言 |
| 根代码许可不等于文档、第三方材料和发行包许可 | 同一固定 TorchNPU commit 的 [LICENSE](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/LICENSE) 及[来源登记](../../sources/registry.yaml) | BSD 三条款与登记范围一致；未扩大为全栈再分发许可 |

上述来源均已有登记。本次按正文所引用的 commit 读取文件，没有重新解析远端 tag；缺少独立 COMPATIBILITY 文件、中文 README 冲突标记和曾引用错误卸载页等历史记录没有被冒称为本次新检查结果。

## 仍保留的证据边界

- 精确 HDK、硬件、OS、CANN 子包、wheel 摘要与上层组件的同版本交集仍未知；正文明确保留这些缺口，不构成审阅缺陷。
- E01 当前 CANN 安装页的 URL `83RC1` 与页头 `8.3.RCX` 差异仍存在；它只支持当前页面的安装职责，不能补成不可变历史配套矩阵。
- 没有下载发行包、安装组件、运行算子或访问 GPU/NPU。此结论只覆盖本次所列来源和正文边界。

## 最终状态

本批没有新增 P1/P2/P3 发现。审阅工作完成，正文技术正确性仍受以上来源范围和未知条件限制。结构检查、构建及元数据核对的实际结果统一记在[四批汇总](batch-01-02-08-09-codex-review-summary.md)。
