# Codex 代审发现的修订记录（batch 02/08/09）

修订日期：2026-09-30。修订者：Opus（主任务）。针对[四批代审汇总](batch-01-02-08-09-codex-review-summary.md)的 9 项开放发现（5 P2、4 P3）。修订前主任务对最关键的源码断言做了独立抽查（Ascend `bc51ab84` 的 alloc_block L2692–2694 / setMemoryFraction L1717–1724 / OOM allowed 分支 L1391–1409 / GC 条件 L1353–1369 与门槛 L2624–2629；vLLM `b17039bc` 的 core.py L927–943 与 core_client.py L425–428；PyTorch `1eba9b3a` 的 dataloader.py L1449–1480），确认审阅方引证全部属实，故 9 项均按建议修订，无反驳项。

## 逐项关闭依据

| 发现 | 级别 | 修订内容 | 关闭状态 |
|---|---|---|---|
| B02-C01 队列空满归因缺“可按序消费”限定 | P2 | [training-data-path](../../knowledge/04-data-storage/training-data-path.md)：队列证据行改为“下一顺位 batch 是否就绪”，新增“队列深度不等于可交付 batch”段（按序返回、`_task_info` 队首等待、四类缓冲点、in_order=False 不作通用修复）；候选瓶颈表同步。[data-starvation-triage](../../knowledge/04-data-storage/data-starvation-triage.md)：证据表与步骤 5 同步，补 dataloader.py L1449–1480 引用 | 已关闭（Codex 定向复核） |
| B08-C01 进程额度也产生同一 OOM 错误码 | P2 | [ascend-memory-oom-evidence](../../knowledge/02-software-stack/ascend-memory-oom-evidence.md)：新增“同一个错误码有两个来源”段（alloc_block 额度分支、setMemoryFraction、文案 allowed 字段、observer 容量参数为额度）；OOM 文案补齐可选项。[ascend-inference-oom-triage](../../knowledge/07-inference/ascend-inference-oom-triage.md)：步骤 5 张量分配器分支改为先查进程额度，证据表补 set_per_process_memory_fraction | 已关闭（Codex 定向复核） |
| B08-C02 GC 阈值缺生效条件 | P3 | ascend-memory-oom-evidence 的选项表：补充须同时设置 fraction、发生在缓存搜索失败后申请新块之前、门槛 = 阈值 × allowed_memory_maximum；明确不代表其他释放缓存路径 | 已关闭（Codex 定向复核） |
| B08-C03 空 conditions 反推 StrictFIFO | P3 | [idle-resource-job-waiting-triage](../../knowledge/05-cluster-platform/idle-resource-job-waiting-triage.md)：步骤 2 改为“空 conditions 不能单独反推”，需先核 queueingStrategy、对象创建时间与控制器接管，只有空列表时保持 unknown；证据表同步 | 已关闭（Codex 定向复核） |
| B09-C01 EngineDeadError 被误判为启动期失败 | P2 | ascend-inference-oom-triage 步骤 1：改为“引擎不可恢复退出的传播信号”，区分构造失败日志与 run_busy_loop 后 fatal + ENGINE_CORE_DEAD；后者可传播该异常，不按异常名单独判断阶段；阶段判断改用启动完成证据、最后成功请求与 EngineCore 原始日志；无法确定时保持 unknown | 已关闭（Codex 定向复核） |
| B09-C02 主动校验被整体排除在 SDC 检测外 | P2 | [silent-errors-and-integrity](../../knowledge/08-reliability/silent-errors-and-integrity.md)：章节改为“被动监控的盲区与主动校验的覆盖边界”，分三层（被动不覆盖 / 主动结果校验可检出，引论文 §7 / 一次 PASS 不排除全部）；frontmatter summary 与“健康检查全绿”误解条同步 | 已关闭（Codex 定向复核） |
| B09-C03 稳定复现被设为 SDC 入口条件 | P2 | silent-errors-and-integrity 判定流程：改为“排除已知数值语义后即可进入候选”，复现/重放/迁移/冗余/设备关联用于增强或削弱假设而非门槛；补 OCP §3.2.1 间歇性限定；超容差不自动等于硬件故障；容差按任务约定，整数/不变量/校验和按各自契约 | 已关闭（Codex 定向复核） |
| B09-C04 RAS MISMATCH 缺正常瞬态限定 | P3 | [bandwidth-degradation-triage](../../knowledge/03-communication/bandwidth-degradation-triage.md) 步骤 6：补官方示例的正常瞬态与初始化/销毁过渡限定、连续查询不推进才值得调查、持续停滞不直接证明链路退化 | 已关闭（Codex 定向复核） |
| B09-C05 SuperBench 链路分母被扩大 | P3 | silent-errors-and-integrity：改为“特定测试床、ToR 有 25% 冗余上行、部分交换机超过一半的**冗余**链路失效”示例表述，删去泛化的“才” | 已关闭（Codex 定向复核） |

## 同步修订的研究记录与登记

- [batch-08-memory-sources.md](batch-08-memory-sources.md)：OOM 行补错误码双来源与 allowed 字段；alloc conf 行补 GC 生效条件。
- [batch-08-kueue-pending-sources.md](batch-08-kueue-pending-sources.md)：StrictFIFO 行补“空列表不证明控制器已处理”边界。
- [batch-09-inference-oom-sources.md](batch-09-inference-oom-sources.md)：EngineDeadError 行区分构造失败日志与运行期死亡传播；不按异常名判断阶段或 OOM。
- [batch-09-bandwidth-sources.md](batch-09-bandwidth-sources.md)：RAS 行补正常瞬态限定。
- [batch-09-silent-error-sources.md](batch-09-silent-error-sources.md)：OCP 结局分类改四类并随来源写 DUE 展开；Meta 检测行补 §7 主动校验说明。
- registry：`src.ascend.torch-npu-v7.2.0-pytorch2.6.0`、`src.pytorch.dataloader-source-v2.6.0`、`src.ocp.sdc-in-ai-2025` 的 notes 同步修订范围。

## 复核前提交的文件身份（SHA-256）

以下摘要已由 Codex 在补正前独立核对，7 项全部一致。复核时有少量补正，最终身份见[定向复核记录](batch-02-08-09-codex-recheck.md)，本表保留提交历史。

| 正文 | SHA-256 |
|---|---|
| training-data-path.md | `4c2c6299cfc4e603f0b212e97be18c4053df22206ed38888cc0bee5de56a145c` |
| data-starvation-triage.md | `4a165fe1643f0b89d1709b1a35d8a4d493c581ccc23b480b9b032f3aac71a990` |
| ascend-memory-oom-evidence.md | `3494d91dbda5eb8dfabe451cd26875e8592339dc8bdafde7669ea9d8655e00e7` |
| idle-resource-job-waiting-triage.md | `f7abbecd3b15462a9a3f67409db3faea9c9c26051ec9626c2de2d34ffb6522d7` |
| ascend-inference-oom-triage.md | `e7b5d4a61b733f459a18880ad91fe60e6b8f1aacf633e5dfce9719db4afc9a86` |
| bandwidth-degradation-triage.md | `3759b142642e4af3344f4a7b3ba990c9d6a5ac8f0b6af0e2b1263adb7e240b8b` |
| silent-errors-and-integrity.md | `15f7fa5f1e88eed1682b30b2caeefb446139b790397e70899c797c4619cedfd1` |

## 检查与最终状态

- 修订后 `make check` / `make build` 通过：60 content entries / 71 sources（数量不变，本次为修订非新增）。
- 全部正文仍 `draft`；本次只关闭文档缺陷，不新增 `reproduced`，未执行任何环境验证。
- **最终状态：原审阅者 Codex 已完成[定向复核](batch-02-08-09-codex-recheck.md)，9 项全部正式关闭。** 复核时一并补正 DataLoader 函数名、Kueue 队首证据、EngineCore 来源记录、RAS 查询范围和 SuperBench 并发条件；最终文件身份保留于复核记录。
