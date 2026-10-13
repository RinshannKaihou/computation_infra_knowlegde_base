---
id: data-storage.artifact-transfer-and-publication
title: 模型制品与 Checkpoint 的传输、发布和读回
type: procedure
domain: data-storage
status: draft
platforms: [generic]
source_refs:
  - src.hf.huggingface-hub-v0.33.0
  - src.hf.safetensors-v0.7.0
  - src.ceph.docs-rgw-s3-squid
  - src.linux-man-pages.fsync-6.19
  - src.linux-man-pages.rename-6.19
updated_at: "2026-10-14"
summary: 从制品清单身份到暂存、传输、提交、读回验证的持久化发布协议；制品格式以 safetensors v0.7.0、传输实现以 huggingface_hub v0.33.0 固定代码为样板，后端承诺复用 T04-02/03。
related_ids:
  - data-storage.local-and-shared-storage
  - data-storage.object-and-parallel-storage
  - data-storage.checkpoint-durability
  - data-storage.checkpoint-integrity-evidence
  - data-storage.training-data-path
applicability:
  environment_refs: []
  notes: "流程以 safetensors v0.7.0 与 huggingface_hub v0.33.0（commit d5dff4ef）为证据样板；目标环境的制品格式版本、后端类型与版本、网络与中断条件需另行固定。"
verification:
  status: source_checked
  evidence_refs:
    - src.hf.huggingface-hub-v0.33.0
    - src.hf.safetensors-v0.7.0
  notes: "已核对两仓库 tag/commit、Apache-2.0 许可、safetensors README 格式节与 tensor.rs 错误枚举、hub v0.33.0 版下载指南、file_download/_snapshot_download/测试行号；传输中断测试除所列行外未定位；safetensors 读写测试未定位；未做任何下载/发布实测。"
---

# 模型制品与 Checkpoint 的传输、发布和读回

> 范围：文件/对象层发布协议（清单→暂存→传输→提交→读回验证）。**下载成功不等于版本一致或模型 ready**：hub 下载完成判据只有长度（plain HTTP 路径；无内容哈希），见 §2。`generic` 仅为导航聚合。

## 1. 制品清单（发布前必须固定）

| 字段 | 含义 | 来源 |
|---|---|---|
| 集合成员 | 全部张量文件＋非张量文件（config、tokenizer 等）；每文件记长度与 SHA-256 | 本库清单要求；成员完整性由发布方保证 |
| 内容身份 | 每文件 SHA-256 | 同上（端到端哈希约定见 [T04-03 §5](object-and-parallel-storage.md)） |
| 版本 | hub 制品记**解析出的 40 位 commit**（并记录请求的 revision）；对象制品按 [T04-03 身份分支](object-and-parallel-storage.md) | hub 实现先 `repo_info(revision)` 取 sha 再按 commit 下载全部文件（[file L283/L305](https://github.com/huggingface/huggingface_hub/blob/d5dff4efd9187cc5c56246f416d666ea1f808cb0/src/huggingface_hub/_snapshot_download.py)）；50 000 文件以上时列表按原 revision 取，存在列表与内容跨 commit 窗口 |
| 长度与分片关联 | 文件长度；safetensors `data_offsets` 为**单文件内**张量区间（"relative to the beginning of the byte buffer"），只用于格式检查；跨文件的张量→分片索引关联未取源（unknown，或本库设计约定另行声明） | [safetensors README §Format](https://github.com/safetensors/safetensors/blob/v0.7.0/README.md) |
| 来源与配置 | 仓库/路径＋下载参数（revision、缓存目录） | [hub v0.33.0 下载指南](https://huggingface.co/docs/huggingface_hub/v0.33.0/en/guides/download)（snapshot_download/revision/缓存） |

safetensors header 字段只有 dtype、shape、`data_offsets` 与可选 `__metadata__`（字符串到字符串），**格式本身没有校验和字段**；库实现或外部工具是否另有校验仍 unknown。选 v0.33.0/0.7.0 为固定样板，不追 latest（取证时 latest 为 hub 2.2.0/safetensors 0.8.0），结论不外推到 1.x/2.x。

## 2. 分支步骤（本地 ext4 / NFSv4.1 / RGW 三栏）

| 步骤 | 本地文件暂存 | NFS 文件暂存 | Ceph RGW 对象发布 |
|---|---|---|---|
| 暂存写 | 写临时名 → fsync(文件) → rename → fsync(目录)：目录 fsync 必须在 rename **之后**，新目录项才落盘（[fsync(2)](https://man7.org/linux/man-pages/man2/fsync.2.html)/[rename(2)](https://man7.org/linux/man-pages/man2/rename.2.html)） | 同左栏次序，另加 NFS 条件（下行） | multipart 上传（中断后可按 upload-id 列举已传分片续传；文档未用"续传"字样，RGW 上传续传语义 unknown）；完成前可见性/列举一致性 unknown（见 [T04-03 §2](object-and-parallel-storage.md)） |
| NFS 追加条件 | — | UNSTABLE WRITE 须 COMMIT 并比对 write verifier；可见性≠持久性；`hard` 挂载、导出 `sync`、close/fsync 查错、rename 后复核重传误报（见[本地与共享存储 §3](local-and-shared-storage.md) 提交链/锁行与 [§4 选型表发布行](local-and-shared-storage.md)） | — |
| 传输 | hub 下载（plain HTTP 路径；Xet 例外见下行）：`.incomplete` 追加写＋`Range` 续传（默认总是续传；仅 force_download/hf_transfer 从头下）；网络错误最多续传 5 次；完成判据只有**长度**（plain HTTP 路径；全文无 `hashlib`）；LFS ETag 为 sha256 但本地不重算 | 同左（NFS 栏除外） | RGW 上传续传语义 unknown（续传仅 hub 下载实现行为，不外推上传；中断后可按 upload-id 列举已传分片续传，文档未用"续传"字样）：multipart 按对象与并行存储 §2 条件（见[对象与并行存储 §2](object-and-parallel-storage.md)） |
| Xet 路径例外 | setup.py 默认安装 hf-xet（x86_64/amd64/arm64/aarch64）；有 Xet 元数据且可用时走 `xet_get`（哈希交外部包 L600–603，下载 L627–633），无 `resume_size`、跳过 5 次重试与长度检查 | 以上续传/长度结论仅 plain HTTP 路径；Xet 路径行为未核对（unknown） | [setup.py L17](https://github.com/huggingface/huggingface_hub/blob/d5dff4efd9187cc5c56246f416d666ea1f808cb0/setup.py)/[file_download.py L530/L600–603/L627–633/L1708–1710](https://github.com/huggingface/huggingface_hub/blob/d5dff4efd9187cc5c56246f416d666ea1f808cb0/src/huggingface_hub/file_download.py) |
| 提交 | rename 即单文件提交点；**集合级提交点（本库设计，非上游保证）**：先写全部成员，最后发布清单/指针（文件侧 rename 指针文件或目录，要求同文件系统、目标不存在或为空目录，以[rename(2)](https://man7.org/linux/man-pages/man2/rename.2.html)为准）；读者先读清单再按清单取成员，哈希不符即失败 | 同左 | Complete 即单对象提交点（见[对象与并行存储 §2](object-and-parallel-storage.md) multipart 行）；**集合级提交点（本库设计）**：先完成全部对象，最后 PUT 清单对象；读者协议同左；对象侧无多对象原子性（Squid 文档未写明，unknown） |
| hub 落地边界 | hub 缓存落盘为 `shutil.move`（无 fsync；跨卷退化为复制，非原子 rename），故 hub 缓存目录本身**不是**已持久发布位置；发布须另行 fsync/提交 | 同左 | — |
| 读回验证 | 内容哈希比对＋应用格式检查＋正确性门（见 §3） | 同左 | 同左；ETag 不作内容哈希 |

实现行号（v0.33.0 commit d5dff4ef）：续传 [file_download.py L406–407/L500–517](https://github.com/huggingface/huggingface_hub/blob/d5dff4efd9187cc5c56246f416d666ea1f808cb0/src/huggingface_hub/file_download.py)；长度检查 L444–445/L485/L522；`resume_download` 已弃用（"总是续传" L942–947）；`.incomplete` 写入 L1160–1163；move L1684–1693/L1735/L1776。版本字段与 T04-03 L84 身份分支一致（Enabled 且可获得 versionId / 其他用 key＋SHA-256）。

## 3. 中断、部分发布与恢复

| 现象 | 处理 | 残留物发现与清理 |
|---|---|---|
| 传输中断 | hub 按上表续传/重试；续传语义以实现行为为准 | 文件侧：`.incomplete` 残留（force_download 删除）；发现方法：缓存目录扫描（方法设计，未执行） |
| 部分发布 | 未 Complete 的 multipart 按 List uploads 找残留再 Abort（见 [T04-03 §2/§5](object-and-parallel-storage.md)） | 对象侧：in-progress uploads 列表 |
| 读到旧/混合版本 | 按版本化三态判定：Enabled 用 versionId（可获得时）＋清单；Suspended/从未设置以内容哈希为准；revision 制品用解析 commit（>50k 窗口除外）；判定方法见 [T04-03 §5](object-and-parallel-storage.md) | — |
| 重试与清理（方法设计，未执行） | 幂等重试；文件侧残留：`.incomplete`、临时名、锁文件（删除仍被并发下载持有的锁文件的安全条件未核对，unknown），发现方法为缓存/暂存目录扫描后按清单比对清理；对象侧残留：in-progress multipart（按 List 查再 Abort）；不以对象 API 200 或 Future 完成证明全部持久 | — |
| 端到端校验 | 清单 SHA-256 比对（下载后本地重算；LFS ETag 只作远端声称值） | — |
| 应用格式检查 | 门槛：首字符 `{`、header ≤100MB（`MAX_HEADER_SIZE`）、offset 合法、字节区完整无空洞（`MetadataIncompleteBuffer`）、键不重复（[README L89](https://github.com/safetensors/safetensors/blob/v0.7.0/README.md)；解析器未必遵守）；通过≠数值有效（NaN/±Inf 可存在于文件，[README L94](https://github.com/safetensors/safetensors/blob/v0.7.0/README.md)） | [tensor.rs L10/L20–45/L73–91/L389](https://github.com/safetensors/safetensors/blob/fa27fa835a466cb50d07696ec20b94f46aed0e31/safetensors/src/tensor.rs) |
| 正确性门 | 最低形式：固定输入下与参考输出比对，容差由负责任务定；归属 T07-01（batch 26，未交付）；本页不设通过条件 | 缺失部分 unknown |

## 4. 上游实现/测试的阶段计时与失败点（只定位不执行）

| 阶段 | 上游锚点 | 可观测计时起止 | 失败信号 |
|---|---|---|---|
| 解析 revision | _snapshot_download.py L283/L305 | repo_info 返回→commit 确定 | revision 不可解析（实现报错，未逐条列举，unknown） |
| 下载/续传 | file_download.py L406–407/L500–517/L1160–1163 | http_get 开始→长度检查通过 | 超过 5 次重试；ConnectionError/ReadTimeout（续传语义） |
| 长度检查 | L444–445/L485/L522（测试 L514/L536 断言报错） | 检查点 | "Consistency check failed" |
| 落地 move | L1684–1693/L1735/L1776 | move 开始→返回 | 空间不足为**警告非失败点**（`warnings.warn` 在 L799，检查在下载前；L784–786 仅函数签名，特此纠正） |
| 本库 SHA-256 校验 | 本库约定（发布方写入清单，读回方重算） | 校验开始→比对完成 | 不一致即失败 |
| 格式检查 | tensor.rs 错误枚举 | 解析开始→元数据完整确认 | HeaderTooLarge/InvalidHeaderStart/InvalidOffset/MetadataIncompleteBuffer |
| 提交/读回 | §2 提交点；[T04-03 §5](object-and-parallel-storage.md) | 提交→读回哈希比对完成 | 见 §3 |

计时值一律未执行。上游测试 L798–806（续传/force 不续传）为行为样例：注意 L804 为裸比较表达式（缺 `assert`），不能证明续传内容正确。safetensors 读写测试检索范围为仓库 tests 目录浏览，未定位到可用例，保留 unknown。

## 5. 链接

- [Checkpoint 写入与持久化边界](checkpoint-durability.md)（提交/持久化语义，"文件同步与目录记录是两个层面"节）、[Checkpoint 完整性与校验证据](checkpoint-integrity-evidence.md)（"四层校验机制与各自边界"节）、[本地与共享文件存储 §4](local-and-shared-storage.md)（NFS 发布行）、[对象与并行存储 §2/§5](object-and-parallel-storage.md)（multipart/版本化/验证设计）。
- 推理加载归 T07-01（batch 26，未交付），暂链[07 推理与服务系统](../07-inference/index.md)，缺失部分 unknown。

## 来源与更新范围

- 上表各入口（两仓库 tag、v0.33.0 版指南、tensor.rs、T04-02/03）。
- 待确认：传输/commit 中断官方测试（除所列行外）；safetensors 读写测试；hub 续传之外的中断语义；推理加载实现；全部实测（未执行）。
