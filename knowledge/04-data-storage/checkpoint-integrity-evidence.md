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
  - src.google.sre-data-integrity
  - src.ceph.docs-rgw-s3-squid
  - src.lustre.ops-manual-2x
  - src.hf.safetensors-v0.7.0
  - src.hf.huggingface-hub-v0.33.0
  - src.nfs-utils.nfs-5-man7
  - src.ietf.rfc-8881
  - src.ceph.docs-bluestore-squid
updated_at: '2026-10-22'
summary: "checkpoint 与制品的完整性证据分四层，外加校验原语对照、选定后端读路径责任、清单到结果的验证链与官方反例；DCP 2.6 FileSystem 路径未见独立内容摘要，MindIO checker 只数文件个数，Ceph 默认不自动修复，RADOS scrub 不等于 RGW 端到端校验；分别限定证据范围。"
related_ids:
  - data-storage.checkpoint-durability
  - data-storage.checkpoint-slow-io-triage
  - data-storage.artifact-transfer-and-publication
  - data-storage.object-and-parallel-storage
  - data-storage.local-and-shared-storage
  - training.checkpoint-state-consistency
  - training.checkpoint-state-recovery-triage
  - reliability.silent-errors-and-integrity
verification:
  status: source_checked
  evidence_refs:
    - src.pytorch.dcp-2.6
    - src.ascend.mindio-acp-v26.1.1
    - src.ceph.docs-scrubbing-latest-2026-10-08
    - src.google.sre-data-integrity
    - src.ceph.docs-rgw-s3-squid
    - src.lustre.ops-manual-2x
    - src.hf.safetensors-v0.7.0
    - src.hf.huggingface-hub-v0.33.0
    - src.nfs-utils.nfs-5-man7
    - src.ietf.rfc-8881
    - src.ceph.docs-bluestore-squid
  notes: "最终核对范围（T04-05 已完成修订与定向复核；记录见 docs/research/batch-20-t04-05-claude-recheck-3.md）：既有四层来源不变，新增 SRE 章（validator/恢复原则/两案例）、Squid RGW/BlueStore（ETag/版本化/读修复/32-bit 漏检量级）、Lustre §23.5.1 全文（两类 checksum/重试/EIO/adler32）、nfs(5) 传输损坏与 krb5i、safetensors/hub 行号；签名机制未取（unknown）；未执行任何保存、损坏注入或修复操作。"
---

# Checkpoint 完整性与校验证据

## 定义与要解决的问题

"checkpoint 文件还在"不等于"字节还是写出的那些字节"，版本对也不等于内容对、真实性另需证据。本文回答：从写入到读回之间，**哪一层机制能发现哪一类损坏**（字节损坏、版本错误、真实性缺失、训练状态错误分开判定）。结论先行：固定来源下没有哪一层单独覆盖全部损坏模式，完整性结论必须分层给出。写入/提交的完成语义见[Checkpoint 写入与持久化边界](checkpoint-durability.md)，恢复后状态正确性属 [06 的恢复一致性](../06-training/checkpoint-state-consistency.md)；字节/版本/真实性/状态四类证据的划分见下文新增节。

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
- Ceph 存储层结论以 Squid 版（BlueStore/health-checks）为准，旧 latest 引用处已核对两版一致；其他文件系统/对象存储的 scrub、校验与修复语义需各自的版本化文档，不沿用本节结论。
- NFS 结论以 nfs(5) 手册页与 T04-02（CTO 仅 v3 有原文）为准；RGW 结论以 Squid 分支文档为准（点版本 unknown）；Lustre 结论以 2.x 手册为准（稳定锚 LTS 2.15.x）；hub/safetensors 结论以 v0.33.0/0.7.0 固定代码为准。
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
- [Ceph osd-config-ref Scrubbing 节](https://docs.ceph.com/en/latest/rados/configuration/osd-config-ref/)与[health-checks 页](https://docs.ceph.com/en/latest/rados/operations/health-checks/)（latest，2026-10-08 观察；Squid 版同句已核对；文档许可 CC BY-SA 3.0 见 [doc/conf.py](https://github.com/ceph/ceph/blob/caf3def8088a17706021a8fd68ee40f62beda519/doc/conf.py#L58-L61)）。
- 逐条主张与证据定位见[第十二批 checkpoint 完整性来源记录](../../docs/research/batch-12-checkpoint-integrity-sources.md)。
- T04-05 新增节来源：[SRE 数据完整性章](https://sre.google/sre-book/data-integrity/)（已登记 src.google.sre-data-integrity）；RGW/Lustre/safetensors/hub 明细见[制品传输](artifact-transfer-and-publication.md)与[对象存储](object-and-parallel-storage.md)（登记见两页 frontmatter）。
- 待确认：torch.load C++ reader 的 CRC32 验证路径；DCP 更新版本的校验语义变化；MindIO memfs 实现层校验；签名机制；safetensors 读写测试；hub Xet 路径细节；目标现场配置；应用层自检的可引用实现；全部实测（未执行）。

## 校验原语对照（T04-05 新增）

| 原语 | 发现什么 | 发现不了什么 | 证据位置 |
|---|---|---|---|
| CRC32（zip/容器） | 外部工具解包损坏 | torch.load 不依赖它；碰撞与语义错误 | 前文 §1；Python zipfile 文档（已登记） |
| 内容哈希（SHA-256 清单） | 字节级 silent 改动（下载后本地重算比对） | 写入前已错的字节；碰撞边界见下文 | [制品传输 §3](artifact-transfer-and-publication.md)；[T04-03 §5](object-and-parallel-storage.md) |
| 文件/对象版本 | 哪个版本被读到（hub 解析 commit；RGW versionId；Lustre 路径＋布局） | 版本机制本身不校验内容 | [制品传输 §1](artifact-transfer-and-publication.md)；[对象存储 §2/§3](object-and-parallel-storage.md) |
| ETag | RGW 实体标签（List 显示 MD-5 措辞）；hub LFS ETag 为 sha256（远端声称值） | 不作内容哈希；两处 ETag 语义不同，不互推 | [对象存储 §2](object-and-parallel-storage.md)；[制品传输 §2](artifact-transfer-and-publication.md) |
| 真实性 | 签名机制（未取，unknown） | 所选格式内无签名字段；无签名则真实性不可证 | safetensors README §Format（见制品传输登记注） |
| 应用自检 | 数值语义（自算摘要、loss/grad 量级） | 无现成可引用实现（实践建议） | 前文 §4 |

边界：碰撞分两类——随机错误漏检（校验设计目标；BlueStore 文档给出 32-bit 约四十亿分之一量级，见 [BlueStore Checksums](https://docs.ceph.com/en/squid/rados/configuration/bluestore-config-ref/)）与对抗性碰撞（构造攻击，不在本库来源覆盖内，unknown；选型按威胁模型另行评估）。真实性：所选 safetensors 格式内无签名字段（README §Format 字段清单为证），hub/RGW 签名机制未取（unknown），无签名则真实性不可证。可信清单：须可信来源＋版本固定；清单与数据经同一信道获取时（如 hub LFS ETag 由同一服务端声称），哈希比对只证明"与该信道声称值一致"，清单本身的独立获取与保护方式 unknown（本库约定为发布方写入、读回方重算，见 [T04-03 §5](object-and-parallel-storage.md)）。数据语义：字节对≠数值对，见恢复一致性主文。

## 选定后端的读路径与校验责任（T04-05 新增）

| 后端 | 读路径校验 | 持久化/修复 | 不能发现 | 证据位置 |
|---|---|---|---|---|
| NFS（v4.1） | 读路径校验：传输层 checksum 细节未在已登记来源覆盖（nfs(5) 只述 UDP 16-bit checksum 与 65536 误匹配概率；TCP 侧 unknown）；`sec=krb5i` 提供每 RPC 完整性保证；`soft` 超时可致静默损坏；NFS 协议层端到端内容校验未见对应机制（unknown，不作"没有"断言） | 持久化判据：UNSTABLE WRITE 须 COMMIT＋write verifier；服务器重启 grace/reclaim（协议层）；服务器后端文件系统校验 unknown；实现细节 unknown | 不能发现：未启用 krb5i 的传输损坏、`soft` 静默损坏、写入前已错的字节、缓存窗口内陈旧读（预期行为） | [nfs(5)](https://man7.org/linux/man-pages/man5/nfs.5.html)；[本地与共享存储 §3](local-and-shared-storage.md)（CTO 仅 v3 有原文，v4 unknown） |
| RGW S3（Squid） | 读路径（RADOS 层）：BlueStore 对落盘全元数据＋全数据做 checksum（默认 crc32c），有其他副本时读错误立即修复；读路径（RGW 层）：GET 无端到端内容校验，ETag 不作内容哈希 | 持久化：版本化三态；Abort 残留清理 | **RADOS scrub 不能当 RGW 端到端校验**：scrub 与 BlueStore checksum 在 OSD 收到数据后才起作用，到达 OSD 前已错的字节会被正确算 checksum 并多副本保存（本库推论） | [BlueStore Checksums](https://docs.ceph.com/en/squid/rados/configuration/bluestore-config-ref/)；[health-checks](https://docs.ceph.com/en/squid/rados/operations/health-checks/)（读修复）；[对象存储 §2](object-and-parallel-storage.md) |
| Lustre（2.x） | §23.5.1 两类 checksum：in-memory 与 wire，覆盖读写两向，默认开启（默认算法 adler32，可改）；失配重读/重写最多五次，仍失败返回 I/O error（`BAD WRITE CHECKSUM` 为写方向日志） | 持久化/修复：e2fsck（ldiskfs）、ZFS scrub（ZFS OST）、LFSCK（组件间一致性，非内容校验） | 不能发现（限 ldiskfs OST）：持久化内容损坏；ZFS OST 手册称有 ZFS 完整性特性，具体行为未核（unknown） | [手册 §23.5.1](https://doc.lustre.org/lustre_manual.xhtml)；登记 src.lustre.ops-manual-2x 已补 §23.5.1 |

## 验证链（T04-05 新增，只设计不执行）

版本清单（commit/versionId/布局固定）→ 完整读回（全文件/全对象读出；注意 DCP 按 offset 读取不等于完整读回，见下）→ 应用结构检查（格式门，见制品传输 §3）→ 同输入结果（正确性门：训练 checkpoint 见恢复一致性"恢复后验证"；推理加载见[权重加载与就绪诊断](../07-inference/model-loading-and-readiness.md)，结果质量见[输出质量评估](../07-inference/output-quality-evaluation.md)，现场结果仍未验证）。四类错误区分：

- 缺片/缺成员（清单有、读回无）：发布/传输失败，见制品传输 §3；
- 错版（revision/versionId 与清单不符）：版本机制判定，见对象存储 §5；
- 静默内容改动（版本对、哈希错）：内容哈希判据，见制品传输 §3；
- 训练状态错误（字节对、语义错）：应用自检＋[恢复一致性](../06-training/checkpoint-state-consistency.md)（"恢复后验证"节）。

DCP 实例化：清单对应 `.metadata` 中 `storage_data` 列出的 `.distcp` 文件集合；完整读回须覆盖每个 `(relative_path, offset, length)`；结构检查为形状断言（不验证内容）；MindIO 文件个数检查只覆盖"缺片"的一部分。错误×步骤对照：错版在第 1 步按清单判定；静默改动须第 2 步全文件哈希（DCP 按 offset 读回不等同全文件哈希，缺失处 unknown）；训练状态错误只在第 4 步可判定。

## 官方反例与证据保留（T04-05 新增）

- hub 测试 `test_resume_from_incomplete`（L798–806）：测试期望值为 `"XXXXent"` 但 L804 缺 `assert`（测试未强制）；实现以长度为完成判据（见制品传输 §4）。反例含义以此为限。
- 检测信号（非反例，列于此供对照）：Ceph PG_DAMAGED/OSD_SCRUB_ERRORS 报警（见前文 §3）；Lustre `BAD WRITE CHECKSUM` 日志（见上表）。
- SRE 章官方支撑（不外推到 AI checkpoint）：Gmail out-of-band validator 在生产中发现过真实完整性问题；"data recovery plans should not rely upon replication"（与"写入前已错的字节会被多副本忠实保存"同义）；"the only test that should let you sleep at night is a full end-to-end test"；案例 Gmail 2011 磁带恢复、Google Music 2012 误删数周后发现（见 [SRE 数据完整性章](https://sre.google/sre-book/data-integrity/)）。
- 修复/repair 前保留损坏证据的顺序为**本库设计约定**（文件＋清单＋日志快照 → 隔离 → 选恢复点 → 复验；Ceph repair 前的不一致对象清单无官方原文，unknown）：训练状态恢复按[恢复诊断指南](../06-training/checkpoint-state-recovery-triage.md)（[适用范围与前置条件](../06-training/checkpoint-state-recovery-triage.md)、[停止条件与恢复安排](../06-training/checkpoint-state-recovery-triage.md)、[完成判据](../06-training/checkpoint-state-recovery-triage.md)）；存储侧 repair/隔离与恢复验证见[存储客户端、后端异常与恢复验证](storage-client-backend-recovery.md)，未核对机制与实际执行缺口继续以该流程正文为准，不以 concept 页代替。
