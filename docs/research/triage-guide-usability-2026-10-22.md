# 三篇高频排障指南的可用性整理与文档使用检查

日期：2026-10-22（Asia/Shanghai）。本轮落实用户优先项 1：先整理示范页，重点检查是否能找到下一步。公开闭环案例（优先 AMD）的搜集仍为后续工作；本轮的小规模读者检查仅服务这三页修订，不替代后续更广的文档使用检查、独立效果评测或现场验证。

开始本轮时工作区已有 [IQ-01–IQ-08 修订](independent-quality-audit-2026-10-22-fixes.md)，本轮保留这些改动。没有新增知识条目、来源、实际环境档案、实验结果或工作包完成声明；三篇仍为 `draft` / `source_checked`。

## 示范页的两层结构

这里的“首屏”指去除 YAML 元数据后的正文首段，不保证任意屏幕尺寸都在一屏内完整显示。它先给出最小适用范围与身份字段，再用四列列出“现象→所需证据→判断分支→下一项检查”，最后指向停止与完成边界。

| 页面 | 快速层 | 详细层与本轮重点 |
|---|---|---|
| [NCCL 超时](../../knowledge/03-communication/nccl-timeout-triage.md#快速分流先找下一项检查) | 6 个入口：缺 rank 日志、对齐后的契约分歧、设备事件、transport 事件、入队不完成、等待预算 | 保留完整证据表、逐 rank 分支、NCCL/PyTorch 观测条件与来源；强调同 group、对齐轨迹、入队/完成区别。瞬时序号差和 0% 利用率不足以确认根因 |
| [GPU 推理 OOM](../../knowledge/07-inference/gpu-inference-oom-triage.md#快速分流先找下一项检查) | 7 个入口，NVIDIA/AMD 适用范围及昇腾入口明确分开 | 将原长表格的启动链、KV 自动/显式预算、profile 断言、单因素对照、恢复顺序展开成小节；启动预算与 KV 容量检查的建议方向分开。一次单变量后不报错改为支持因素影响，不能单独确认因果或根因 |
| [Checkpoint 恢复](../../knowledge/06-training/checkpoint-state-recovery-triage.md#快速分流先找下一项检查) | 6 个入口：存储身份、schema、对象应用、optimizer 缺失、应用状态、布局变化 | 保留普通 dict/Stateful、strict 固定提交、重分片与 rank-local 映射的详细机制；分流完成与恢复正确的判据分开，首步成功不足以证明长期续接正确 |

既有详细节名保留，仅调整标题层级，因此原有节名锚可继续使用。README 新增三页直达入口，训练路径的 NCCL/checkpoint 行改为直达指南；推理路径明确昇腾行的范围并直达 GPU 快速层，避免泛化 OOM 入口先把读者带到 NPU 字段。

## 必要条件、反例与证据支持范围

快速层是既有正文的有条件摘要，不新增平台支持声明。本轮重新读取：

- [PyTorch 2.8 init_process_group](https://docs.pytorch.org/docs/2.8/distributed.html#torch.distributed.init_process_group)：NCCL 10 分钟、其他后端 30 分钟的默认值及显式覆盖边界；没有把 IB local-ack timeout 视为进程组预算。
- [PyTorch 2.6 DCP](https://docs.pytorch.org/docs/2.6/distributed.checkpoint.html)：目标 tensor 预分配、普通值与 Stateful 的对象应用区别、跨版本兼容限制。后续 optimizer 修复仍单独引用原固定提交，不猜首个发行版本。
- vLLM `b17039bccc17b94a2ea107272ad7bc93508708df` 的 [kv_cache_utils.py L609–645](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/kv_cache_utils.py#L609-L645) 与 [gpu_worker.py L295–339](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py#L295-L339)：无可用 KV、单请求需求超预算、显式字节值和 profile 断言分别核对。通过断言也可能仍有他进程占用变化，不以单一成功信号排除共享干扰。

上述读取通过 web 与 GitHub 连接器，只读原文；来源已登记，未添加镜像。其他详细来源沿用正文既有核对范围，没有将本次整理写成全篇重新技术验收。

## 独立读者检查协议

使用本地 Codex CLI 的独立会话，模型按仓库约定指定 `gpt-6.1-sol / xhigh`，执行沙箱为 `read-only`。[冻结提示词与 9 道题](triage-guide-usability-2026-10-22-reader-prompt.md)完整保存：从 README 开始，仅凭库内正文作答，记录找到的页面/依据、候选、下一项检查、缺失信息与首段是否够用；禁止外网、历史审阅与作者答案。

题目由本轮作者构造，全部是合成输入，检查前固定。读者没有获得作者答案，但读者模型与作者可能共享模型家族和训练资料；这不是人类读者研究或独立 holdout，没有未改版的对照组，也不测查找时间或现场诊断能力。题目与回答入库后仅供公开文档回归。

## 读者结果与作者核对

[独立读者原始回答](triage-guide-usability-2026-10-22-reader.md)保留逐题引用、候选与缺失项，仅把绝对路径链接转换为仓库相对链接。读者报告均从 README 的三页直达入口找到主页；这是文本查找路径，未做浏览器点击或人工读者计时。

| 题号 | 找到的页面与依据 | 是否找到下一项检查 | 作者核对及边界 |
|---|---|---|---|
| U01 缺 rank 日志 | NCCL 快速层、证据表、步骤 1–4C | 是：补缺失 rank 前序日志、栈/位置、最后完成点，再对齐全 rank | 回答保留故障数量与根因未知，未把 7 条日志化为 1/7 个确定首因 |
| U02 同号与瞬时序号差 | NCCL 身份前提、快速层、步骤 1–4A | 是：先核 group/attempt，再对齐同一逻辑操作的调用轨迹 | 回答区分不同 group、暂时进度差与实际契约分歧；未把快照差异当成错序证明 |
| U03 两层 timeout | NCCL 快速层与版本化观测边界 | 是：实际后端、初始化 timeout、watchdog 与 IB 配置、耗时基线 | 默认值与显式值分开，未把 IB 参数作为框架超时的同一预算；默认数字需下钻详细层 |
| U04 启动显存预算 | GPU OOM 快速层与启动阶段① | 是：初始 free、gmu 预算、同卡进程/实例边界 | 回答没有照搬 KV 的增大 gmu 方向；下一项是读证据，不是立即变更 |
| U05 自动/显式 KV | GPU OOM 快速层与 KV 小节 | 是：报错全文、实际预算路径、所需/可用字节与初始 free | 三个预算分支和实际分配边界均区分；承认题面尚未给具体错误，未断言任一参数必修复 |
| U06 AMD 死亡信号与接流 | GPU OOM 首错入口、取证差异、恢复顺序与接流判据 | 是：先补 EngineCore 首错，再核实际 HIP backend/字段与同窗记录 | 未由 SMI/reserved 单值诊断碎片；未将 ready 或重启当成接流充分条件 |
| U07 DCP load 返回 | Checkpoint 快速层与 DCP 责任边界 | 是：传入值类型、显式装载或 Stateful 回调记录 | 回答区分读取、对象应用与训练正确性，未用 None 返回值证明全部恢复 |
| U08 optimizer 缺失 | Checkpoint 快速层与 strict 小节 | 是：逐 FQN 核对真实 update、算法惰性 state 与保存契约 | 回答保留发行版本/backport unknown，未把 strict=False 当成安全续训保证 |
| U09 8→4 与 rank-local | Checkpoint 快速层、去重机制、布局变化及恢复一致性正文 | 是：实际保存表示/metadata、旧 rank 覆盖、新 rank 映射及恢复目标 | 回答区分保存覆盖、映射和持续窗口；同名 rng/cursor、load/首步成功均未被当作充分判据 |

本轮 9 题均找到相应下一项检查；需要具体默认值、KV 分支、HIP 条件或状态映射机制时，读者使用了第二层。这个观察只覆盖本轮题目、页面与模型；没有对未整理指南、人工阅读成本、诊断准确率或现场恢复效果作出推论。

### 仍开放的资料问题

| 编号 | 读者指出的位置 | 性质与本轮处置 |
|---|---|---|
| DU-01 | Checkpoint strict 小节与 `src.pytorch.dcp-fix-edd8d35` | 既有资料缺口：缺固定修复到首个发行版本/backport 的映射。本轮保留 unknown；未来可用源码/发行证据补齐，不按版本号猜测，不因本次文档检查关闭 |
| DU-02 | GPU OOM 的 HIP 字段与构建范围 | 既有条件未知：目标 HIP backend、统计细项及实际构建组合不明。本轮保留按实际构建核对/不支持字段不得当 0 的边界；不能把一个文档样板替代未指定的目标构建 |

缺 rank 日志、首错、实际配置、旧状态内容和恢复对照是题面未给的现场证据；读者已与上述资料缺口分开。没有因“尚不能下根因结论”反向认定导航失败，也不以本次无导航阻碍宣告技术全面审阅通过。

## 执行身份与冻结范围

- 本地 CLI `codex-cli 0.163.0`；只读会话 `01a1628c-4f44-7680-985f-2986d88983a8`，进程退出码 0。
- 调用方读取该会话的 `turn_context`：实际 model 唯一为 `gpt-6.1-sol`、effort 唯一为 `xhigh`、sandbox 为 `read-only`。最终回答与 stderr 均没有 fallback 标记；事件流中同词仅来自只读打开编写指南中的规则原文，不是路由降级信号。
- 检查结束后比对冻结时的 README、两条任务路径、三篇正文、来源登记，共 7 个输入的 SHA-256，全部一致；独立读者没有修改文件。作者的结果核对没有改变本轮被读输入，因此无需针对新正文再跑一次。
- 冻结提示词 SHA-256：`4779a5cc33c682c302a3a8ebba24e302081a37b283674253664c44e86e4949bd`。
- 原始 CLI 最终回答 SHA-256：`387644c7439768708b729e82de581525bb730e192c484853e718bbb78829c36c`。归档文件添加说明并转换本地链接后的 SHA-256 为 `99425dc6ed3e7d5d55e9550916437e6e0bf6b7e628486798ec3621fa6c9c9e92`。未把整份工具事件流或本地日志加入仓库。

三篇正文在读者检查时的输入摘要：

| 文件 | SHA-256 |
|---|---|
| `knowledge/03-communication/nccl-timeout-triage.md` | `3d83f03127af7d0c03ee16ee79675e9a4c8ae11dba1becb3e0d2475e5f7602b7` |
| `knowledge/07-inference/gpu-inference-oom-triage.md` | `8f01f648255e7a70821be97f30f0aec2be66a51b80f99f42d4b811008e7bafea` |
| `knowledge/06-training/checkpoint-state-recovery-triage.md` | `3cbef6a159444b924077a078ceb8e94896aa1960ba9696672f00bb3e4c8fdd57` |

## 仓库检查

- `make check` / `make build`：PASS，135 个条目 / 578 项来源；结构与本地文件链接符合检查范围。
- 本轮涉及的三篇正文、README 与两条任务路径共 47 处本地标题片段补查，未发现缺失目标；使用近似 GitHub 标题 slug 的静态核对，未声称任意渲染器的锚点均已验证。
- 三篇既有详细节名均保留。NCCL 与 checkpoint 的原精确远程链接全部保留；OOM 启动检查从同一固定文件的 L262–270 引用扩大为 L253–273，仍覆盖原范围，其他旧精确远程链接保留。
- `git diff --check`：PASS。内容与导航整理没有修改 `src/kb/`，未运行工具回归测试或目标应用。

构建通过、模型作答与静态跳转检查均不替代技术全篇验收、现场兼容性、实测或故障注入。后续公开 AMD 闭环案例仍须逐一具备明确环境、根因证据、修复与复验反馈，不能用 Issue 关闭或补丁合入代替复验。
