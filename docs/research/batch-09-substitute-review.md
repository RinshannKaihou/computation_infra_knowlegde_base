# 第九批复查记录（替代性复查，非 astra/xhigh）

复查日期：2026-09-30。**限制声明同 batch 08：用户约定每轮由 gpt-6-astra / xhigh 独立审阅；当前环境没有该模型派发能力，本轮未能完成约定模型的独立审阅。** 本记录是同环境只读子代理的定向复查，审阅独立性不等同于跨模型外部审阅。

## 范围与实际核查

完整复读三篇新增正文（ascend-inference-oom-triage、bandwidth-degradation-triage、silent-errors-and-integrity）与三份第九批来源记录；实际核对：vLLM `b17039bc`、vLLM Ascend `52d4acfa`、nccl-tests `b4d5beeb` 固定 commit 的 17 处源码锚点（全部命中，含关键疑点——"GPU KV cache size"/"Maximum concurrency" 日志确在 kv_cache_utils.py 而非 core.py）；NCCL 2.27.5 归档（ras.html 实际路径与顶层 404、env.html 变量语义）；CANN 9.1.X HCCL Test 五个页面（cookie jar + __NUXT_DATA__ 提取）；PyTorch 2.6 三页；arXiv v1 ar5iv 全文、SuperBench PDF 全文、OCP 白皮书 p.1–19；两条 Issue 的 gh API 状态与评论。复查者另运行 `make check`（PASS）。

## 发现与关闭

| 发现 | 级别 | 状态 | 关闭依据 |
|---|---|---|---|
| 静默错误篇 DUE 展开写成 "detected uncorrectable error"，所引 OCP 白皮书原文为 "detected unrecoverable error" | P2 | 关闭 | 正文改为随来源的 "detected unrecoverable error"，并补齐图 1 的四种结局（benign/fault corrected/DUE/SDC） |
| 静默错误篇"冗余/重试使静默计算错误没有报错通道"误锚到 §5/p.15（该处是检测分类与磨损案例）；对应原文在执行摘要 p.3 与 §3.3 p.10 的 fault-masking 表述 | P2 | 关闭 | 正文改锚 p.3/§3.3 并按 fault-masking 原文改写 |
| 故障结局三分遗漏 fault corrected 一类 | P3 | 关闭 | 随 P2 第一行一并改为四种结局 |
| "实测证据"措辞偏强：OCP §3.2.1 是机制性陈述 | P3 | 关闭 | 改为"机制性陈述（非新实测）" |
| 带宽篇"显著增加耗时"超出 HCCL 0005 原文（只说增加） | P3 | 关闭 | 删去"显著" |
| OOM 篇 block_size 强制 128 省略 qwen3_next 例外 | P3 | 关闭 | 补上例外与 TODO 说明 |
| 静默错误研究记录把 22.61× 仿真误标 §5.1，实际在 §5.2 | P3 | 关闭 | 研究记录已改（正文未引用节号，无需改） |
| 两篇 procedure 的 evidence_refs 未覆盖已核对来源（两条 Issue / cann-hccl 快照） | P3 | 关闭 | evidence_refs 已对齐并同步 notes |
| 昇腾平台路径未收带宽退化篇 | P3 | 关闭 | ascend.md 的 HCCL/性能退化条目已补链，related_ids 同步 |

## 已排除的疑点（核对为正确）

- 全部抽查源码锚点（kv_cache_utils、exceptions、troubleshooting、conserving_memory、worker.py、platform.py、utils.py、faqs.md、release_notes、model_runner_v1.py、common.cu、util.cu、all_reduce.cu）行号与内容一致。
- 版本/平台边界：两快照未拼配套；Issue 归因未采信；HCCL/NCCL 口径未互比；CUDA/NPU 语义未混淆；Meta CPU 结论未外推 GPU/NPU；SuperBench 22.61× 如实标为仿真。
- 元数据符合 schema；导航与 README 与实际文件一致；无 YAML 截断；无虚构命令或阈值。

## 未覆盖

- cann-hccl gitee 快照未重抓（仅作定性机制提示）；OCP 白皮书 p.19 之后正文（文章已声明未读）；未复核存量 57 篇内容；未运行 `make build` 之外的验证，未执行任何训练/推理/通信/硬件操作。
