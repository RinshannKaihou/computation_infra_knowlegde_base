---
id: data-storage.checkpoint-integrity-evidence
title: Checkpoint 完整性与校验证据
type: concept
domain: data-storage
status: draft
platforms: [generic]
source_refs:
  - src.pytorch.dcp-2.6
  - src.ascend.mindio-acp-v26.1.1
  - src.ceph.docs-scrubbing-latest-2026-10-08
  - src.ceph.repo-caf3def
  - src.python.zipfile-docs-2026-10-08
updated_at: "2026-10-08"
summary: "checkpoint 的完整性证据分四层：容器格式、框架元数据、存储 scrub、应用自检；所查 DCP 2.6 FileSystem 路径未见独立内容摘要，文件按配置分桶，形状断言不证明字节完整；MindIO checker 校验文件个数，Ceph 默认不自动修复；分别限定证据范围。"
related_ids:
  - data-storage.checkpoint-durability
  - data-storage.checkpoint-slow-io-triage
  - training.checkpoint-state-consistency
  - reliability.silent-errors-and-integrity
verification:
  status: source_checked
  evidence_refs:
    - src.pytorch.dcp-2.6
    - src.ascend.mindio-acp-v26.1.1
    - src.ceph.docs-scrubbing-latest-2026-10-08
  notes: "已核对 PyTorch v2.6.0 DCP 写/读路径与全包校验和关键词扫描、serialization.py 的 CRC32 语义、MindIO ACP register_checker 接口与调用方、Ceph latest 的 scrub/health-check 文档与 ceph/ceph 固定 commit 的 man page；未执行任何保存、损坏注入或修复操作。"
---

# Checkpoint 完整性与校验证据

## 定义与要解决的问题

"checkpoint 文件还在"不等于"字节还是写出的那些字节"。本文回答：从写入到读回之间，**哪一层机制能发现哪一类损坏**。结论先行：固定来源下没有哪一层单独覆盖全部损坏模式，完整性结论必须分层给出。写入/提交的完成语义见[Checkpoint 写入与持久化边界](checkpoint-durability.md)，恢复后状态正确性属 [06 的恢复一致性](../06-training/checkpoint-state-consistency.md)；本文只管"字节/文件是否损坏"这一层证据。

## 四层校验机制与各自边界

### 1. 容器格式层：torch.save 的 zip CRC32 存在但 torch.load 不依赖它

`torch.save` 的 zip 容器**写时默认对每条 record 计算并写入 CRC32**（`_compute_crc32` 默认 True，[serialization.py L184](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/serialization.py#L184)），可用 `set_crc32_options(False)` 关闭；其文档字符串明示：关闭后"unzipping … may fail or warn due to corrupted CRC32. **However torch.load will be able to load the file**"（[L196–209](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/serialization.py#L196-L209)）。zip 格式的成员级 CRC-32 与 `testzip()` 校验行为见 [Python zipfile 文档](https://docs.python.org/3/library/zipfile.html)。要点：CRC32 对**外部工具/生态**（unzip、testzip）有效，但 torch.load 走自研 C++ reader，2.6 的文档字符串表明它不依赖 CRC32——"zip 有 CRC"不等于"torch.load 读回时能发现损坏"。

### 2. 框架元数据层：所查 DCP FileSystem 路径未见独立内容摘要

PyTorch 2.6 的 DCP（固定 v2.6.0 源码）：

- `FileSystemWriter` 的 `.distcp` 布局取决于参数：默认 `single_file_per_rank=True`、`thread_count=1` 时一个本地保存计划的多个 write item 进入同一桶文件；多线程按大小/类型分桶；`single_file_per_rank=False` 才按 item 建文件（[参数 L447–463](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/filesystem.py#L447-L463)、[分桶 L225–246](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/filesystem.py#L225-L246)、[write_data L507–534](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/filesystem.py#L507-L534)）。实际数据文件集以配置、保存计划与 metadata 为准，不能由 tensor/request 个数直接推出。
- 另有 `.metadata`，是 **pickle 序列化的 `Metadata` 对象（不是 JSON）**，写时先写 `.tmp` 再 rename（[L582–595](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/filesystem.py#L582-L595)）。`Metadata` 字段为 `state_dict_metadata/planner_data/storage_data/storage_meta`（[metadata.py L136–147](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/metadata.py#L136-L147)），所查 FileSystem 的 `storage_data` 记 `(relative_path, offset, length)`，未见独立内容摘要。此前全包关键词扫描未命中是检索记录，不能单独证明所有后端/扩展路径均无校验。
- 读取按 offset/length 定位记录，tensor 项经 `torch.load` 与切片后有**形状匹配断言**（[L666–668](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/filesystem.py#L666-L668)）。形状检查不验证内容；某些损坏可在解析时失败，另一些保持可解析与相同形状的损坏可能逃过此断言，不能将所有同长度损坏都判为可检测或不可检测。
- 细节差异：`.distcp` 中 tensor 项内嵌 `torch.save`（带容器 CRC32，但见第 1 层边界）；BYTE_IO 项是裸字节写入，连容器 CRC 都没有（[filesystem.py L249–270](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/filesystem.py#L249-L270)）。

**MindIO ACP（昇腾，MindCluster v26.1.1）的"完整性校验"是文件个数完备性**：`register_checker` 的 check_dict 语义是"校验指定 path 下的文件个数是否符合要求"（[register_checker接口.md L39](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/mindio/acp/doc/Interface_description/register_checker%E6%8E%A5%E5%8F%A3.md#L39)）；调用方在异步保存完成后注册 `{目录: 文件个数}`，回调成功才写 tracker 文件、失败记 "watching checkpoint failed" 且不写 tracker（[framework_acp.py L111–136](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/mindio/acp/python_whl/mindio_acp/mindio_acp/acc_checkpoint/framework_acp.py#L111-L136)）。它能发现"异步写未完成/少文件"，不能发现字节级损坏。

### 3. 存储层：Ceph scrub 校验 at-rest 数据，默认不自动修复

以 Ceph 为存储层实现例子（latest 文档，对应 main 开发主线；仅作例子，不套用到其他存储系统）：

- **Light scrub** 查对象大小与属性，通常每日；**deep scrub** 读数据并用 checksum 校验，通常每周（`osd_deep_scrub_interval` 默认 7 天）（[osd-config-ref Scrubbing 节](https://docs.ceph.com/en/latest/rados/configuration/osd-config-ref/)）。
- 发现问题后以 **PG_DAMAGED**（"Data scrubbing has discovered problems with data consistency"）与 **OSD_SCRUB_ERRORS** 报警；注意 latest 文档**没有名为 PG_INCONSISTENT 的健康检查**，`inconsistent` 是 PG 状态标志（[health-checks 页](https://docs.ceph.com/en/latest/rados/operations/health-checks/)）。
- **默认不自动修复**：`osd_scrub_auto_repair` 默认 false；手动入口 `ceph pg repair <pgid>`（[ceph(8) man page，固定 commit](https://github.com/ceph/ceph/blob/caf3def8088a17706021a8fd68ee40f62beda519/doc/man/8/ceph.rst#L1633-L1637)）。
- 覆盖边界：scrub 只管 at-rest 数据的副本一致性；读路径上的错误在有可用副本时立即修复（OSD_TOO_MANY_REPAIRS 节）。**"写入前已损坏"的数据会被忠实地多副本保存**——存储层校验发现不了应用层写错的字节。

### 4. 应用自检层：语义级正确性只能自查

前三层都不覆盖"字节完整但数值语义错误"（如写错了 tensor 内容、恢复错位置）。应用层的可行做法是加载后自检（自算摘要、数值合理性如 loss/grad norm 量级对照）。本批来源中没有可引用的现成应用层实现，此层是实践建议而非来源事实；数值层面的判定纪律见[静默错误与计算完整性判定](../08-reliability/silent-errors-and-integrity.md)。

## 适用边界

- DCP 结论按 PyTorch v2.6.0 固定源码；其他版本（含更新的 DCP）是否引入校验和需逐版核对，本文不推断。
- MindIO 结论按 MindCluster v26.1.1 固定 commit；memfs 的 C++ 实现是否有传输级校验未查。
- Ceph 仅作存储层实现例子；其他文件系统/对象存储的 scrub、校验与修复语义需各自的版本化文档，不沿用本节结论。
- torch.load 的 C++ reader 是否在任何路径验证 CRC32 未逐行核对；本库证据是 2.6 的 Python 层文档字符串。

## 常见误解

- **"保存返回成功 = 数据完整"**：`save`/`flush` 的返回语义是完成性（见[持久化边界](checkpoint-durability.md)），不是字节校验；所查 DCP FileSystem 路径未见独立内容摘要，不能据此替所有后端作保证。
- **"torch.save 有 CRC，读回就能发现损坏"**：torch.load 不依赖 CRC32（2.6 文档字符串明示 CRC 损坏仍可加载）；CRC 只对外部 zip 工具有效。
- **"文件个数对 = 字节对"**：MindIO checker 是文件个数完备性门控，不校验内容。
- **"存储 scrub 会自动修好"**：Ceph 默认 `osd_scrub_auto_repair=false`，报警后需手动 `ceph pg repair`；且 scrub 发现不了"写入前已损坏"。
- **"形状对 = 内容对"**：DCP 的形状断言不能排除保持形状与可解析性的内容损坏；语义错误要靠应用自检与[恢复一致性](../06-training/checkpoint-state-consistency.md)训练侧验证。

## 例子与相关知识

- 写入路径各阶段的耗时与故障定位：[Checkpoint 慢写与恢复 I/O 诊断](checkpoint-slow-io-triage.md)；提交与原子性语义：[Checkpoint 写入与持久化边界](checkpoint-durability.md)。
- 字节损坏在训练中的下游表现与检测方法分层：[静默错误与计算完整性判定](../08-reliability/silent-errors-and-integrity.md)。

## 来源与待确认问题

- [PyTorch v2.6.0 filesystem.py](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/filesystem.py)、[metadata.py](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/metadata.py)、[serialization.py](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/serialization.py)；[Python zipfile 文档](https://docs.python.org/3/library/zipfile.html)（2026-10-08 观察）。
- [MindIO ACP register_checker 接口文档（MindCluster v26.1.1）](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/mindio/acp/doc/Interface_description/register_checker%E6%8E%A5%E5%8F%A3.md)与 [framework_acp.py](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/mindio/acp/python_whl/mindio_acp/mindio_acp/acc_checkpoint/framework_acp.py)。
- [Ceph osd-config-ref Scrubbing 节](https://docs.ceph.com/en/latest/rados/configuration/osd-config-ref/)与[health-checks 页](https://docs.ceph.com/en/latest/rados/operations/health-checks/)（latest，2026-10-08 观察；文档许可 CC BY-SA 3.0 见 [doc/conf.py](https://github.com/ceph/ceph/blob/caf3def8088a17706021a8fd68ee40f62beda519/doc/conf.py#L58-L61)）。
- 逐条主张与证据定位见[第十二批 checkpoint 完整性来源记录](../../docs/research/batch-12-checkpoint-integrity-sources.md)。
- 待确认：torch.load C++ reader 的 CRC32 验证路径；DCP 更新版本的校验语义变化；MindIO memfs 实现层校验；其他存储系统的 scrub 等价物与版本化文档；应用层自检的可引用实现。
