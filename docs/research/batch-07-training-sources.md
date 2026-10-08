# 第七批 T05 精度差异场景来源准备

> 调研记录，不是知识库正式正文，也不是训练、迁移或恢复操作授权。

- 调研范围：T05-P/C/X（GPU 到 NPU 的精度差异）。
- 核对日期：2026-09-30。
- 执行边界：只读取公开官方文档、固定 commit 和 Issue/PR/commit；未安装或运行 msprobe、PyTorch、CANN/torch_npu，未下载模型/数据，未执行训练、dump、保存、加载、恢复或硬件测试。
- 证据边界：P/C 的 `source_checked` 只表示正文与来源对照；X 保持 `not_verified`，不填写测量或复现结果。

## 可写判定

- T05-P 可采用固定 msprobe commit `7783f6b2d0cbae0e2f6200b05e604a09d7820c50` 的“前置对齐、平台内重复、缩小范围、寻找首差异”流程，并用 PyTorch 2.6 numerical accuracy 限定跨平台不保证 bitwise identical。相同 seed 不是相同随机张量的跨设备保证，工具阈值不是本库的通用验收线。
- T05-C 可用 Ascend/pytorch #17 作为真实但未闭环的公开案例。环境、症状、比较对象和怀疑点足够；GPU 软件栈、模型/数据/随机性/容差缺失，DDP stride warning 只自述“may impair performance”，不能写成精度根因。GitHub connector 取得一条评论：评论者否认已知功能问题，并要求固定输入、随机种子和确定性后逐 step 比较 loss；这进一步说明原报告尚未形成因果闭环。
- T05-X 可写成不执行的双层实验：先分别验证 GPU/NPU 平台内重复性，再加载同一输入/权重字节做跨平台比较；保留未插桩对照，预注册结构检查、非有限值、逐层首差异和下游任务判据。

## T05：GPU 到 NPU 的精度差异

### 固定 msprobe 来源

固定仓库 commit 为 `7783f6b2d0cbae0e2f6200b05e604a09d7820c50`。实际读取：

- [训练精度定位指南](https://github.com/Ascend/msprobe/blob/7783f6b2d0cbae0e2f6200b05e604a09d7820c50/docs/zh/best_practices/train_debug_guide.md)：第 15 行把有限字长、计算序、通信序和数学表达式差异列为数值差异来源，并明确不能把计算差异直接等同收敛问题；第 65 行起为 checklist；第 88 行起固定随机性；第 153 行起缩小规模；第 209、234、275 行起区分首 step、长稳和不稳定复现；第 836 行起单算子验证。
- 同一指南第 321–325 行明确：相同 seed 在不同硬件上仍可能生成不同随机张量；需要相同输入时，应直接固定张量内容/字节或在统一位置生成后搬运。正文不把该文档中的具体规避动作提升为所有模型的默认方案。
- [PyTorch 场景精度比对](https://github.com/Ascend/msprobe/blob/7783f6b2d0cbae0e2f6200b05e604a09d7820c50/docs/zh/user_guide/accuracy_compare/pytorch_accuracy_compare_instruct.md)：第 21–32 行说明自研 API 可能无对应项、误差累积会使后续输入不再可比、调用次数可造成错误匹配；第 142 行起说明首差异节点；第 353 行起说明输出与 Result；第 467 行起给工具指标解释。
- 工具文档里的 Loss 1%、Cosine 0.99、MaxAbsErr 0.001 等是该指南/工具的筛选或解释规则。正式 T05 不把它们登记为任意模型、dtype、算子或下游质量的通过阈值。
- dump、同步、hook、异步 dump 和关闭融合/重叠都可能改变时序、内存、I/O 或实现路径。现象随插桩消失只能推动“观测干扰/时序依赖”假设，不能独立证明内存踩踏或唯一根因。

许可：固定 `docs/LICENSE` 是 CC-BY-4.0；固定 `docs/zh/legal/LICENSE` 是 MulanPSL-2.0 文本，许可说明将文档与产品范围分开。外链图片、用户日志、wheel、安装分发形态、第三方依赖和 EULA 另计。

### PyTorch 数值边界

复用 `src.pytorch.numerical-verification-2.6`。PyTorch 2.6 [Numerical accuracy](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html)说明：浮点加/乘非结合，数学等价计算、不同 release/commit/platform 即使输入 bitwise identical 且控制随机性，也不保证 bitwise identical。批处理与逐 slice、不同后端和低精度路径可能产生不同结果；非有限值和病态输入需要独立检查。

因此 T05 需要分开：

1. 结构/语义是否相同：模型、输入、权重、shape、dtype、layout、训练 step、并行/规约和更新规则。
2. 各平台内部是否可重复：同平台多次运行的自然波动。
3. 跨平台差异是否超过有依据的容差：容差按比较对象、参考、dtype、任务和风险预注册。
4. 局部差异是否传播为梯度/优化器/收敛或质量问题：不能从单算子差异直接外推。

CPU/FP64 只在操作、输入、dtype 转换和参考误差有定义时作为第三方参考；PyTorch 文档也说明 float64 常常有帮助但不能解决所有病态数值问题，不能写成绝对真值。

### T05-C：Ascend/pytorch #17

来源：[Ascend/pytorch #17](https://github.com/Ascend/pytorch/issues/17)，2023-12-19 打开；2026-09-30 观察为 `Open`，无关联 branch/PR。

报告者比较 V100 与 Ascend 910B 的大模型 SFT：称 V100 loss 从 1.3 在半个 epoch 内降至 0.3，而 910B 在 5 epochs 后仍约 0.8；使用 PEFT、TRL 和 `accelerate launch`，声称除 `cuda`/`npu` 部分外训练脚本和参数相同。

已给 NPU 环境：Ubuntu 20.04、kernel `4.19.90-vhulk2211.3.0.h1543.eulerosv2r10.aarch64`、CANN 7.0.RC1、Python 3.9、torch 2.1.0、torch_npu 2.1.0rc1.post20231013。未给 GPU OS/driver/CUDA/cuDNN/NCCL/PyTorch、PEFT/TRL/Accelerate 版本、模型/数据身份、输入/权重字节、seed/RNG、dtype/autocast/loss scale、batch/token 顺序、并行映射或重复样本。

报告中的 DDP warning 明说 gradient stride 与 bucket view stride 不匹配，“not an error, but may impair performance”。报告者又比较 torch 与 torch_npu reducer 代码，怀疑 stride matching。公开正文没有数值因果对照、单变量修改、梯度内容对比、修复或复验。故正式案例只能写“报告者怀疑 DDP reducer 差异；根因未定”，不能把 warning 当作梯度值错误。

静态页面没有渲染评论；2026-09-30 改用 GitHub connector 取得[一条评论](https://github.com/Ascend/pytorch/issues/17#issuecomment-2029286848)。评论者称 NPU/GPU 的计算能力、私有格式、bucket 与传输实现不同，但“当前功能上没有问题”，并询问是否已固定输入和随机种子、开启确定性后逐 step 比较 loss。该评论没有给修复或独立复现，也没有证明 stride warning 与收敛差异无关；它把缺少的控制实验说得更具体。

## 三篇正文写作边界

| 条目 | 主来源 | 必须保留 |
| --- | --- | --- |
| T05-P | 固定 msprobe 指南；PyTorch 2.6 numerical accuracy | 平台内重复→跨平台；固定输入/权重/shape/dtype/layout；阈值有依据；插桩干扰 |
| T05-C | Ascend/pytorch #17 | Open、GPU 栈缺失、DDP warning 非根因、评论要求的控制实验未见结果 |
| T05-X | 固定 msprobe 归因流程 | 未插桩对照、单变量、资源/隐私/停止恢复、无结果 |

## 未知与待办

- T05 #17 的 GPU 软件栈、模型/数据/随机性/dtype/布局/并行、重复性、评论后续、修复和根因未知。
- msprobe 固定文档提供的阈值没有被本库验证为任何目标任务的容差；正式实验需预注册自己的依据。
- 三篇都没有本地 GPU/NPU 执行证据；X 保持 `not_verified`。

## 可复用的现有登记

- `src.pytorch.numerical-verification-2.6`
- `src.pytorch.parallel-training-state-2.6`

## 待合并来源 YAML

下面是符合 `schemas/sources.schema.json` 的完整独立 YAML。本文件不修改 `sources/registry.yaml`。

```yaml
schema_version: 1
sources:
  - id: src.ascend.msprobe-training-guide-2026-09-30
    title: Ascend msprobe 固定训练精度定位与比对文档
    url: https://github.com/Ascend/msprobe/tree/7783f6b2d0cbae0e2f6200b05e604a09d7820c50/docs/zh
    kind: repository
    registered_at: '2026-09-30'
    revision: commit 7783f6b2d0cbae0e2f6200b05e604a09d7820c50; observed 2026-09-30
    license:
      status: partial
      scopes:
        - scope: 固定 commit 的 docs 自有文档；外链图片、用户日志与第三方内容另计
          identifier: CC-BY-4.0
          url: https://github.com/Ascend/msprobe/blob/7783f6b2d0cbae0e2f6200b05e604a09d7820c50/docs/LICENSE
        - scope: 固定文档法律目录所声明的 msprobe 产品代码范围；wheel、安装分发、EULA 与第三方依赖另计
          identifier: MulanPSL-2.0
          url: https://github.com/Ascend/msprobe/blob/7783f6b2d0cbae0e2f6200b05e604a09d7820c50/docs/zh/legal/LICENSE
      notes: 固定 license_notice 将文档与产品许可分开；没有把 CC-BY-4.0 扩张到产品代码，也没有把 MulanPSL-2.0 扩张到所有制品、外链或依赖。
    notes: T05-P/X 的固定来源；核对 train_debug_guide、accuracy_compare、安装与许可页面。只支持版本内定位流程和工具字段，文档中的 1%/0.99 等规则不是通用验收阈值；未安装或运行工具。
  - id: src.ascend.pytorch-issue-17
    title: "Ascend PyTorch #17：V100 与 910B SFT 收敛差异报告"
    url: https://github.com/Ascend/pytorch/issues/17
    kind: issue
    registered_at: '2026-09-30'
    revision: opened 2023-12-19; observed Open 2026-09-30; no linked branch or pull request visible
    license:
      status: unknown
      scopes: []
      notes: Issue、评论、代码片段与日志的再分发范围未核验；仓库源码许可不自动覆盖用户提交内容。本库只链接并作有限原创归纳。
    notes: T05-C 主案例；报告 NPU 环境和 loss 轨迹，但 GPU 栈、模型/数据/随机性/容差与复验不足。DDP stride warning 只支持性能怀疑，不证明数值根因；connector 取得一条要求固定输入/随机性并逐 step 对比的评论，没有修复或根因确认。
```
