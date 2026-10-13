# 第二十批 T04-04 第五次定向复核（作者第五轮修订后）

复核日期：2026-10-13（实际取证日）。审阅模型 `claude-opus-5-5`，由用户本次明确要求。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定；推理等级等运行元数据没有可核验记录，不补造。审阅者角色独立于作者修订角色。

**结论：T04-04 第五次定向复核通过。本轮范围 1 项（C24）：CLOSED 1，OPEN 0。连同此前已关闭、本轮不重开的 C22、C23、C25、C26、C27、C28、C29、C30、C31，B20-C22–C31 合计 CLOSED 10 / OPEN 0。** 前次两项剩余条件都已满足：L55 RGW"传输"栏已删除否定断言，改为与 L53 一致的 unknown 写法；L56 来源栏已补回 L530 和 L1708–1710，且不含 L618。不新增发现 ID，也没有新的事实错误需要按原 ID 追记。

本轮只做只读核对：未改作者正文、来源记录、修订映射、登记或计划；未下载模型，未上传或发布对象，未执行读写、中断或计时试验。模型审阅不构成硬件或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 | 与任务给定前缀 |
|---|---|---|
| T04-04 正文 `knowledge/04-data-storage/artifact-transfer-and-publication.md`（97 行，procedure / draft） | `03fe46aad2e9df6e…` | 一致 |
| 修订映射 `docs/research/batch-20-review-fixes.md`（T04-04 第五轮节 L137–140） | `135334a13346d5cb…` | 一致 |
| 前次复核报告 `docs/research/batch-20-t04-04-claude-recheck-4.md`（C24 剩余关闭条件权威来源） | `cc3a985b14dca82c…` | 任务未给前缀 |
| 任务计划 `plans/full-coverage-backlog.yaml`（T04-04 acceptance 4 条） | 本轮未重算 | 沿用前次判定表 |

`make check`：`PASS: 91 content entries; 409 sources.` 只校验结构与本地链接，不校验技术正确性和远端链接。

## 源重取（审阅者独立获取）

用 `curl` 默认 TLS 只读获取，原文只存放在 `/tmp/`，未入库。

| 来源 | SHA-256 | 核对结果 |
|---|---|---|
| hub `file_download.py`@d5dff4ef（1803 行） | `a973d1986453bf5a…` | 与前四轮一致。L530 `def xet_get(`；L600–603 `xet_download_info = [PyXetDownloadInfo(..., hash=xet_file_data.file_hash, file_size=expected_size)]`；L627–633 `download_files(xet_download_info, endpoint=..., token_info=..., token_refresher=..., progress_updater=[...])`；L1708 `if xet_file_data is not None and is_xet_available():`，L1710 `xet_get(`。 |
| hub `setup.py`@d5dff4ef | 未记 | L17 为 `hf-xet>=1.1.2,<2.0.0; platform_machine=='x86_64' or ... 'amd64' or ... 'arm64' or ... 'aarch64'`，与 L56 正文平台列表一致。 |
| Ceph Squid objectops 页 | `14f5689f8f03a427…` | 与前次一致。去标签后 "Multipart Upload Part"、"List Multipart Upload Parts"、"Complete Multipart Upload" 各出现一次；全页无 "resume"。 |

取证限制：hf_xet 外部包实现未核对（unknown）；未克隆仓库、未跑测试、未经 GitHub API 重做 tag→commit 解析；Ceph 页为动态站点，按文字核对。

## 逐项复核

### B20-C24 — P1 / **CLOSED**

- 条件 1（L55 RGW 栏措辞）：已满足。
  - L55 RGW"传输"栏现为"RGW 上传续传语义 unknown（续传仅 hub 下载实现行为，不外推上传；中断后可按 upload-id 列举已传分片续传，文档未用'续传'字样）"，后接 multipart 条件和 T04-03 §2 链接。
  - 全文检索"无续传"零命中；"续传语义"只出现在 L53、L55（均为 unknown）以及 L67、L80（指 hub 下载侧实现行为，不涉及 RGW）。L53 和 L55 的 RGW 栏不再互相矛盾。
- 条件 2（L56 Xet 证据列锚点）：已满足。
  - L56 来源栏链接文字为 `file_download.py L530/L600–603/L627–633/L1708–1710`，不含 L618，链接固定在 commit d5dff4ef。
  - 四段锚点逐一对上重取原文：L530 是 `xet_get` 定义；L600–603 把哈希交给外部包（支持"哈希交外部包"）；L627–633 是下载调用（支持"下载 L627–633"）；L1708–1710 是分支条件和 `xet_get` 调用（支持"有 Xet 元数据且可用时走 `xet_get`"）。"无 `resume_size`、跳过 5 次重试与长度检查"这个判断依赖 L530 的函数签名和 L1708 的分支位置，前几轮已在同一份原文上核对过，本轮不重开。
- 不阻断（沿用前次，不计数）：L53 和 L55 都保留了肯定式前半句"中断后可按 upload-id 列举已传分片续传"。Squid 文档只列出 Upload Part 和 List Parts 两个接口，没有写明中断后 upload-id 是否仍然有效。由于同一括号已标 unknown，这句话不构成无据断言。前次给的措辞建议（"接口有 List Parts/Upload Part；中断后能否在同一 upload-id 下补传，文档未写明"）作者没有采用，可留给后续编辑处理。

## 不阻断追记（不新增 ID，不改变计数）

- 修订映射：第五轮节写"L55 RGW 栏改 unknown 措辞（与 L53 一致）；Xet 证据列补 L530/L1708-1710"，与正文实际改动一致。前次指出的映射与正文不对应问题已经消除。
- 行数：正文从前次的 98 行变为 97 行。修订映射只写"L57 正文去词重复"，没有说明为什么少了一行。本轮核对的 L53/L55/L56 行号与任务描述一致，其余行的变化不在本轮范围内，没有逐行比对。
- 范围外（沿用前次）：正文 `updated_at` 仍为 2026-10-14，晚于取证日 2026-10-13，留给作者核查。

## 对照 acceptance

| acceptance | 判定 | 未关闭 |
|---|---|---|
| 1 清单字段；下载成功≠版本一致/ready | 满足 | — |
| 2 本地/NFS/RGW 提交条件逐实现核对 | 满足（RGW 续传语义统一为 unknown；Xet 分支有行锚点） | — |
| 3 中断/部分/旧/混合/重试/清理；三类门槛 | 满足 | — |
| 4 阶段计时与失败点；链接 durability/integrity/推理加载 | 满足 | — |

## 结论

**第五次定向复核通过：本轮 1 项 CLOSED 1 / OPEN 0；C22–C31 合计 CLOSED 10 / OPEN 0。T04-04 的编辑与来源审阅可以声明通过。**

正文仍为 `draft`。本次通过只说明编辑与来源层面已经闭环，不构成硬件、部署或现场验证，也不代表已经完成实验核验。状态升级按仓库流程另行处理。
