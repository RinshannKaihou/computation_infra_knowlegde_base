# 第三批 F08 来源核查与证据提取

本记录对应 `communication.bandwidth-baselines`。它保存固定来源、实际读取位置、正文可以采用的结论、不能外推的范围，以及供主任务合并到 `sources/registry.yaml` 的完整来源登记建议。它不是本地通信测试报告、硬件验收结论或运行手册。

## 核查结论

F08 采用两个官方仓库的固定 commit。NVIDIA `nccl-tests` 快照能支持其自身的 `time`、`algbw`、`busbw` 公式、消息 size 处理、rank 数、in/out-of-place、warm-up/iterations、同步、逐次 CUDA event 计时和结果检查。Ascend `cann-hccl` 快照只支持 HCCL Test 示例中 `data_size`、`aveg_time`、`alg_bandwidth` 与 `check_result` 的文字语义，以及 HCCL README 的 α–β 模型；它没有在该位置给出与 NCCL-tests 完全相同的带宽公式或计时实现。

因此正文把 NCCL 公式限定在 `nccl-tests` 固定版本内，没有将 `busbw` 等同物理链路采样，也没有把 NCCL 系数套给 HCCL。未知的 NPU 链路、工具默认参数和目标性能保持未知。

## 固定引用解析

2026-09-29 对两个官方远端执行只读引用查询，未克隆仓库：

```text
git ls-remote https://github.com/NVIDIA/nccl-tests.git refs/heads/master
b4d5beebca8a76cf01335f724d154b9b9d394d96  refs/heads/master

git ls-remote https://gitee.com/ascend/cann-hccl.git refs/heads/master
2d685b084a60366b47ad8e50a563ee5c4dbef7fe  refs/heads/master
```

正文链接固定到完整 commit，不依赖分支继续移动。这里记录的是当次解析结果，不保证远端分支或引用以后不变，也不表示这两个 commit 彼此配套。cann-hccl README 明确要求选择与 CANN 软件版本配套的 tag，并警告 master 可能版本不匹配；本次只将固定 master commit 当作可复核的文档快照，不把它当成可部署组合。

## NVIDIA nccl-tests：实际读取和证据提取

### 读取位置

| 文件 | 固定位置 | 提取范围 |
|---|---|---|
| README | <https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/README.md> | 多进程/线程/GPU 的 rank 计算；二进制 size 后缀；默认与可配置 warm-up、iters、aggregate、rank 聚合、blocking、逐次 event timing、correctness check；split group 的每组带宽语义 |
| Performance | <https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/doc/PERFORMANCE.md> | 小/大消息的时间解释；`algbw=S/t`；AllReduce、ReduceScatter、AllGather、Broadcast、Reduce、AlltoAll 的 bus factor 和 `S` 说明 |
| common.cu | <https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/common.cu> | `K/M/G` 解析为 1024 进制；warm-up 完成后 barrier；性能循环、同步、rank 聚合、CUDA event timing；out-of-place 后 in-place；数据正确性汇总 |
| all_reduce.cu | <https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/all_reduce.cu> | `baseBw=count*typesize/1e9/sec` 与 `2(n-1)/n` 系数 |
| all_gather.cu | <https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/all_gather.cu> | send/recv count、in-place offset、`baseBw=count*typesize*n/1e9/sec` 与 `(n-1)/n` |
| alltoall.cu | <https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/alltoall.cu> | 每 rank 总 send/recv 与单 peer param count 的关系；`(n-1)/n`；in-place AlltoAll correctness 不支持 |
| LICENSE.txt | <https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/LICENSE.txt> | 三条款 BSD 文本；README 同时称源码和 accompanying documentation 使用 BSD license |

以上文件均直接打开并读取正文。没有用搜索摘要替代目标文件，也没有执行其中的构建或测试命令。

### 可支持的正文陈述

1. `nccl-tests` 的总 rank 数等于进程数 × 每进程线程数 × 每线程 GPU 数；MPI 进程数不是测试二进制参数。
2. 大小参数的 `K/M/G` 是 KiB/MiB/GiB 倍数；实现计算带宽时除以 `1e9`，结果列为十进制 GB/s。
3. 固定 `PERFORMANCE.md` 定义 `algbw=S/t`，bus factor 为：AllReduce `2(n-1)/n`；ReduceScatter、AllGather 和 AlltoAll `(n-1)/n`；Broadcast 与 Reduce 为 1。
4. ReduceScatter 的 `S` 是每 rank 总输入，AllGather 的 `S` 是每 rank 总输出；两者均含 rank 数因子。
5. 默认 warm-up 1 次、timed iterations 20 次、aggregate 1 次；warm-up 完成后同步，再进入 timed loop。主表 getBw 始终用 deltaSec；-C 1 只切换显示为 cputimeSec，不能用它反算带宽。Graph 的 deltaSec 另按 launch 次数归一化；-I 逐次 event 摘要及 -K 跳过样本不改变主表带宽，逐次汇总取跨 GPU/线程/进程最大值。
6. 每个 size 都跑 out-of-place 和 in-place；AlltoAll 实现明确不支持 in-place correctness reporting。
7. correctness check 在性能计时之外执行并汇总 wrong elements；它只能覆盖该工具生成的数据和检查迭代。
8. split communicator 的报告带宽是每组值；组数乘积是逻辑并发总量，不是共享物理链路计数器。

### 不能外推的范围

- `busbw` 是操作模型换算，不是 NIC、NVLink、PCIe 或交换机端口的字节采样；不能直接算作链路利用率。
- PERFORMANCE 文档的模型不证明本次选择了 ring、tree、NVLS、CollNet 或任意特定算法，也不描述层次化路径各层的真实流量。
- 本轮没有固定与该 commit 配套的 NCCL、CUDA、驱动或 GPU 机型组合；不提供硬件峰值和期望效率。
- 默认参数只属于该固定 commit；其他 nccl-tests 版本需重新读取 README 和实现。
- 工具 correctness 通过不证明训练模型数值、未检查的 timed iterations 或更广的数据分布正确。

## Ascend cann-hccl：实际读取和证据提取

### 读取位置

| 文件 | 固定位置 | 提取范围 |
|---|---|---|
| README | <https://gitee.com/ascend/cann-hccl/blob/2d685b084a60366b47ad8e50a563ee5c4dbef7fe/README.md> | HCCL α–β 模型；版本配套警告；HCCL Test 单节点 8 NPU AllReduce 示例及输出字段 |
| LICENSE | <https://gitee.com/ascend/cann-hccl/blob/2d685b084a60366b47ad8e50a563ee5c4dbef7fe/LICENSE> | `CANN Open Software License Agreement Version 1.0`；定义包含可许可的 API、源码、二进制和相关文档，并限制为 Ascend processors 用途 |

Gitee 固定 blob 页面无法由静态网页读取工具获取正文，因此本轮通过固定 raw URL 直接读取了 README 和根 LICENSE 的完整文本；固定 blob URL 作为正文与登记的人工可复核定位。`docs/LICENSE` 在该 commit 返回 404，未发现独立文档许可文件。根 LICENSE 的定义包含 related documents，但发行 CANN 包、HCCL Test 二进制和第三方组件是否完全由同一许可覆盖，本轮未取得制品内容和 notices，保持未知。

### 可支持的正文陈述

1. README 的 HCCL Test 示例使用单节点 8 NPU、AllReduce、fp32、sum，并扫描 8 KiB 到 64 MiB；示例不是本地结果或推荐阈值。
2. README 明确把 `data_size` 解释为单个 NPU 参与集合通信的数据量（byte），`aveg_time` 为算子耗时（μs），`alg_bandwidth` 单位 GB/s，`check_result=success` 表示示例 AllReduce 功能结果正确。
3. README 的 α–β 模型定义 α 为节点间固定时延、β 为每 byte 传输时间、γ 为每 byte 规约计算时间，单步为 `D=α+nβ+nγ`，该处 n 是通信 byte 数而非 rank 数，节点个数另用 p；正文为避免冲突改用 m 表示 byte 数。
4. README 明确要求使用与 CANN 配套的 tag，并警告 master 可能版本不匹配。

### 保持未知的内容

- 该 README 没有在输出说明中给出 `alg_bandwidth` 精确公式、bus bandwidth 或各集合算子的换算系数；不能与 NCCL-tests 同名字段直接等价。
- 未取得固定、配套版本的 HCCL Test 工具指南或源码，因此默认 warm-up、iterations、rank 聚合、同步边界、in/out-of-place 及 correctness 覆盖范围未知。
- 未取得目标 Ascend NPU 型号、HCCS/PCIe/网络端口数量和速率、端口聚合、协议开销或物理遥测口径。
- 未核验 HCCL Test 所在 CANN 发行包、第三方 notices 和二进制再分发许可；仓库根协议不能自动替代发行包许可审计。

## 与 F07 的衔接

F08 正文通过稳定 ID `communication.collectives-and-rank-progress` 关联同轮 F07。F07 负责集合语义、rank 参与和进度边界；F08 只在这些语义固定后解释性能分子、分母与换算。F07 选用的 NCCL 2.27.5 用户指南和 HCCL API 文档可支持集合调用语义，但不是本文 `nccl-tests` 或 HCCL Test 性能统计实现的替代来源，因此 F08 没有用 API 文档补写工具公式。

## 完整来源登记建议

以下条目符合 `schemas/sources.schema.json`，供主任务合入共享 `sources/registry.yaml`。F08 作者按任务约束不直接修改 registry。

```yaml
- id: src.nvidia.nccl-tests-b4d5beeb
  title: NVIDIA nccl-tests 固定源码与文档快照 b4d5beeb
  url: https://github.com/NVIDIA/nccl-tests/tree/b4d5beebca8a76cf01335f724d154b9b9d394d96
  kind: repository
  registered_at: "2026-09-29"
  revision: b4d5beebca8a76cf01335f724d154b9b9d394d96
  license:
    status: identified
    scopes:
      - scope: 固定 commit 的仓库源码与随附文档；第三方依赖和外部链接材料另计
        identifier: BSD-3-Clause
        url: https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/LICENSE.txt
    notes: 根 LICENSE.txt 的三条款 BSD 文本已直接打开核对；README 明确称源码和 accompanying documentation 使用 BSD license。未核验任何构建产物、容器、NCCL/CUDA 包或第三方依赖的许可。
  notes: 2026-09-29 只读解析官方 master 得到此 commit。已核对 README、doc/PERFORMANCE.md、common.cu、all_reduce.cu、all_gather.cu、alltoall.cu 和 LICENSE.txt；仅用于工具自身的 rank、size、计时、正确性及 algbw/busbw 口径，不构成硬件峰值或环境配套推荐，未构建或运行。
```

```yaml
- id: src.ascend.cann-hccl-2d685b08
  title: Ascend cann-hccl 固定源码与文档快照 2d685b08
  url: https://gitee.com/ascend/cann-hccl/tree/2d685b084a60366b47ad8e50a563ee5c4dbef7fe
  kind: repository
  registered_at: "2026-09-29"
  revision: 2d685b084a60366b47ad8e50a563ee5c4dbef7fe
  license:
    status: partial
    scopes:
      - scope: 固定 commit 根 LICENSE 所定义的可许可 API、源码、二进制与相关文档；仅限协议允许的 Ascend processors 用途
        identifier: CANN Open Software License Agreement Version 1.0
        url: https://gitee.com/ascend/cann-hccl/blob/2d685b084a60366b47ad8e50a563ee5c4dbef7fe/LICENSE
    notes: 根协议全文已通过固定 raw URL读取；docs/LICENSE 在该 commit 不存在。仓库协议含用途和分发限制。未取得 CANN/HCCL Test 发行包及第三方 notices，不能用本登记覆盖其制品许可。
  notes: 2026-09-29 只读解析官方 master 得到此 commit。已核对 README 的 α–β 模型、版本配套警告和 HCCL Test 示例字段；该快照不是与特定 CANN 版本配套的 tag，不构成部署建议。未构建、安装或运行，HCCL Test 精确公式与默认统计参数仍未知。
```

## 执行与验证边界

本轮没有克隆仓库、下载发行包、安装依赖、构建源码或运行任何上游命令；没有访问 GPU/NPU、NIC、交换机或真实集群；没有生成 latency、algbw、busbw、alg_bandwidth、链路利用率或 correctness 结果。执行的远端动作只有读取网页/raw 文本和 `git ls-remote` 固定引用。

正文的 `source_checked` 只覆盖上述固定文件与论断。结构校验、链接可达性、固定源码阅读都不能替代目标环境的工具配套核验、物理拓扑确认、重复性能实验和数据正确性验证。

## 轮末定位修订

按 astra/xhigh 审阅和主任务直接读取固定 raw 文件，纠正正文源码锚点：common.cu 的大小解析 240–274、warm-up 720–733、分母 795–811、getBw 823–824、显示选择 886–887、event 666–683、逐次摘要 889–914、检查迭代 828–883、两种 buffer 模式 952–960；算子公式分别为 all_reduce.cu 59–65、all_gather.cu 38–44、alltoall.cu 48–54。以固定文件的实际函数与上述行号为定位，不沿用初稿误差。
