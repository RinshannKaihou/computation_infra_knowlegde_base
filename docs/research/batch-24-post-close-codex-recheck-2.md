# Batch 24 交付后复查：第二次 Codex 定向复核

日期：2026-10-19（Asia/Shanghai）。基线：`bbdc0a4ed02a6ec69bd8840c74a61570e12060c8` 加本轮开始时已有的未提交修订。

## 1. 结论与范围

**通过。** 第一次报告仍开放的 **B24-PC-04、B24-PC-R01、B24-PC-R02 全部 CLOSED**；本次定向范围内没有新增 OPEN P1/P2，也没有新增 P3。通过仅指本次交付后复查的指定问题，不是重做 Batch 24 全量审阅，更不代表硬件、分布式训练或恢复验证通过。

| 编号 | 原优先级 | 本轮判定 | 关闭依据 |
|---|---|---|---|
| B24-PC-04 | P2 | **CLOSED** | 正文三情形表分别列出 PyTorch 2.6 与 Megatron core_v0.19.2 scaler，后者明确限于 fp16、未设显式 `--loss-scale` 的动态分支；hysteresis 状态机、bf16 无 scaler、常量 scaler 边界与源码一致。见第 3 节。 |
| B24-PC-R01 | P2 | **CLOSED** | 已删除“必须连续 overflow”和无条件“单次不缩小”的错误概括；增长窗口 reset、backoff 后不自动 reset、min_scale 下界及 ConstantGradScaler 均说明。三类指定轨迹以及下界、常量分支均实际执行断言，全部通过。见第 4 节。 |
| B24-PC-R02 | P3 | **CLOSED** | 正文、复查记录、T06-01 来源补充与登记 notes 的对应坐标均与原文件一致，包含真实放大赋值 L153、无 scaler 返回 L774、QKV 交错 L1840–1841。见第 5 节。 |

PC-04 与 R01 是同一修订链上的问题，不重复计作两个独立的新 P2。原已 CLOSED 的 PC-01/02/03/05/06 不重开、不重新全审；仅对本轮改动的相邻边界作回归抽查。依据为[第一次定向复核报告](batch-24-post-close-codex-recheck.md)第 5.2、6.2 节的关闭条件，以及[修订轮二记录](batch-24-post-close-review.md#修订轮二第一次定向复核发现处理)。

本轮只新增本报告，不改写正文、来源登记、修订记录、历史审阅报告或原工作区构建产物。

## 2. 角色、模型与证据取得

### 2.1 模型身份的可核验边界

本轮承担与第一次相同的 Codex 技术审阅角色，未派发子代理，也未启动另一轮模型调用。用户指定的审阅模型/档位为 `gpt-6.1-sol / xhigh`。本轮实际读取的本地 CLI 会话记录为：

```text
~/.codex/sessions/2026/10/19/rollout-2026-10-19T09-42-49-01a151d3-5df8-73b2-a560-8214ab4d0a33.jsonl
```

其中 `session_meta.originator=codex_exec`、`cli_version=0.157.1`、cwd 为本仓库；`turn_context.model=gpt-6.1-sol`、`effort=xhigh`、`approval_policy=never`，sandbox 为 workspace-write、`network_access=false`。provider 记录为 `custom`。

**能独立核对的是本地 CLI 所记录的请求配置与指定模型/档位一致；不能独立核验自定义服务端最终实际使用的模型权重、路由或推理档位。** 本轮没有能进一步证明服务端执行身份的返回元数据，不作超出本地记录的身份保证，也不重新认证历史审阅模型。

### 2.2 原文件身份与网络限制

已重新阅读 `README.md`、`docs/authoring-guide.md`、`content-outline.md`、metadata schema、第一次报告、修订轮二、来源补充、登记 notes 以及相关工作区 diff；仓库中仅有根级 `AGENTS.md`，无本轮目标的更深层指令。

本轮重新打开下表五个精确 raw URL，均指向 `core_v0.19.2`，不使用 main/latest。网页工具对 `grad_scaler.py` 返回 `Internal Error / Cache miss`；其他四个返回经过网页工具解析的文本，不能据此重建原文件字节或使用其网页行号。对 `grad_scaler.py` 额外执行一次保留默认 TLS 校验的下载尝试：

```bash
curl -fLSs --connect-timeout 10 --max-time 30 'https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/optimizer/grad_scaler.py' -o /private/tmp/b24-recheck2.8DYmjy/grad_scaler.raw.py
```

结果 exit 7，`Couldn't connect to server`。这不是上游文件缺失的证据；没有关闭 TLS、提权或绕过网络限制。

因此沿用第一次报告的交叉取证方法：通过已连接 GitHub 工具，**本轮重新读取** `NVIDIA/Megatron-LM`、`ref=core_v0.19.2` 的这五个精确路径及相关行，取得远端完整 Git blob SHA；再读取既有 `/private/tmp/b24src/` 原件，对每份完整字节独立计算 `SHA1(b"blob " + 十进制字节数 + b"\0" + 原文件字节)`，全部等于本轮远端返回的 blob SHA。随后重新计算完整 SHA-256，与第一次报告及登记/来源记录比对，全部一致。核验后的字节另复制到本轮隔离目录 `upstream/`，再以 `nl -ba` 核对原文件坐标。

**没有把本轮未成功取得的完整 raw 下载写成成功，也不是仅因缓存文件名相同就信任缓存。** 本轮采用的是“新取得远端 blob 身份＋本地完整字节匹配＋SHA-256 复算”的证据链。Git blob SHA 与 SHA-256 是两种不同摘要。

| 编号 | 固定 tag 原文件/raw 入口 | 字节数 / 行数 | 本轮复算 SHA-256 | 本轮远端 Git blob SHA，已与本地重算匹配 |
|---|---|---|---|---|
| S1 | [optimizer/grad_scaler.py](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/optimizer/grad_scaler.py) | 6263 / 165 | `81402e800476fce96b70d91ff2b799d889ac6ed9407fe74be7cd73d32449c2a7` | `036564889825ef6a5b3f27fc0e39386730f17e36` |
| S2 | [optimizer/optimizer.py](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/optimizer/optimizer.py) | 87339 / 2022 | `24609822f7c165c9be9f6e95945c873bf474cdce3ca06600b00b52c5d23b31e4` | `dac16f4a2eeff10325dfcb7e28738e3d76f1ae88` |
| S3 | [optimizer/__init__.py](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/optimizer/__init__.py) | 57172 / 1224 | `5a657e3f3ad88d1ea6bf3600258cd1e391921b55d88ba055134e958db300ea20` | `70f757f2889ba5834ad3b046132354bf7f9e8e43` |
| S4 | [training/arguments.py](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/training/arguments.py) | 207996 / 3655 | `f7fad20bc0e0cd9ba4b9ba7e70fa1a1b77030dfd020a7edb50b1d3b3aa41ebf6` | `fd30984b38ae64e1207a948c71ef04dbaf5925da` |
| S5 | [transformer/attention.py](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/transformer/attention.py) | 89030 / 2159 | `a019cd00a708a22237383456a7ba85bf522201c14a5b7cb0c1e4f0f12eac9837` | `3a5876bc0fe69f9c4a467cd3d74ecd303513af25` |

表内短路径相对于 `megatron/core/`，但 S4 的完整路径为 `megatron/training/arguments.py`。S1/S2/S3/S5 的完整 SHA-256 与 `sources/registry.yaml:4707` 的本次补充一致；S4 与第一次报告 E06、T06-01 初审 U07 一致，[来源补充](batch-24-t06-01-sources.md)第 140 行也注明它沿用 U07。

## 3. B24-PC-04：CLOSED

目标位置为 `knowledge/06-training/parallelism-and-state.md:212`、`:214`、`:216`–`:224`。已重读引导句、完整表格及表后说明，而非只检查关键词。

- **不再跨实现拼接。** 第 214 行明确两列对应两个实现；第 216 行将 Megatron 列限定为“动态 grad scaler（fp16，未设 `--loss-scale`）”，scheduler/成功更新计数限定为 Megatron。PyTorch 列和第 224 行仍明确使用 PyTorch GradScaler 语义，没有把它的逐次 overflow backoff 写成 Megatron 的通用行为。本轮不重新全审原已接受的 PyTorch 证据链。
- **更新位置与跳步含义一致。** [S2](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/optimizer/optimizer.py#L741-L774) L741–774 的 `prepare_grads` 只在 scaler 存在时 unscale/check，并于 L770 调用 `update(found_inf_flag)`；无 scaler 的返回在 L774。[同文件 L816–822](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/optimizer/optimizer.py#L816-L822) 先调用 `prepare_grads`，发现非有限值即返回 `(False, None, None)`，其首元素才是 `update_successful=False`。所以跳过参数更新并不取决于这一次 scale 数值是否下降。
- **动态与常量的分支边界一致。** [S3 L638–662](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/optimizer/__init__.py#L638-L662) 在有效显式 loss_scale 下选 ConstantGradScaler；没有该显式设置且 fp16 时选 DynamicGradScaler，growth/backoff 为 2.0/0.5；bf16 且未设该值时不创建 scaler。正文第 222 行仅排除“由 loss scaling 引起”的 overflow 跳步，没有宣称 bf16 不可能出现非有限值，也没有宣称常量 scaler 不会检查非有限值或跳步。
- **三情形的动态规则正确。** 第 219、220 行已改为真实 tracker 状态机，详细断言见第 4 节；第 222 行说明 [S1 L43–52](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/optimizer/grad_scaler.py#L43-L52) 的常量 `update()` 不调整 scale，动态规则不适用。没有再将“fp16”本身等同于动态 scaler。

PC-04 的分列、适用条件和动态状态机要求均满足，因此关闭；关闭不是仅依据表格已拆列。

## 4. B24-PC-R01：CLOSED

### 4.1 按第一次报告的关闭条件逐项核对

| 第一次报告的条件 | 修订后位置 | 本轮原文件证据与判定 |
|---|---|---|
| 删除“必须连续 overflow”及无条件“单次不缩小” | 正文第 220 行；复查记录第 26、36 行 | [S1 L138–143](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/optimizer/grad_scaler.py#L138-L143)：overflow 清零 growth，hysteresis 减 1，`<=0` 时 backoff；普通 finite 步不会恢复 hysteresis。已明确“不必连续”。满足。 |
| 明确增长窗口完成才 reset | 正文第 219、220 行；复查记录第 36 行 | [S1 L144–153](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/optimizer/grad_scaler.py#L144-L153)：growth 加 1，等于 interval 时 growth 归零、hysteresis 恢复配置值、scale 乘 growth_factor。满足。 |
| backoff 后不自动恢复门槛 | 正文第 220 行 | S1 L138–153：backoff 分支没有给 hysteresis 恢复配置值的赋值；修订稿说明门槛耗尽后直到下一增长窗口才恢复。满足。 |
| min_scale 下界 | 正文第 220 行；复查记录第 36 行 | S1 L143 是 `max(scale × backoff_factor, min_scale)`；[S4 L2913](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/training/arguments.py#L2913) 默认 1.0。正文已给出下界；“每次都缩小”应在这同一单元格已声明的下界内理解，触发 backoff 不保证处于下界时数值仍下降。满足。 |
| ConstantGradScaler 不套动态规则 | 正文第 216、222 行 | S3 L638–662 以及 S1 L43–52。满足。 |
| 至少执行三类指定轨迹 | 本节 4.2 | 非连续 overflow、门槛耗尽后的孤立 overflow、完整连续有限窗口后的恢复均执行，断言通过。满足。 |

[S4 L2907–2917](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/training/arguments.py#L2907-L2917) 同时核对了 loss-scale 默认 None、initial scale 默认 `2**32`、min 默认 1.0、window 默认 1000、hysteresis 默认 2。下面测试的初始 scale=1024 是**合成测试值**，不是冒称 CLI 默认值。

### 4.2 实际执行的控制流复核

本轮以原工作区 `.venv/bin/python`（Python 3.11.15）执行隔离脚本 `audit.py control-flow`：从经摘要核验的 S1 AST 中抽出 `DynamicGradScaler.update`、`state_dict` 和 `ConstantGradScaler.update`；**没有改写方法 AST**。使用普通标量字段的 `SimpleNamespace` 承载状态，唯一 tensor 运算 `torch.max` 由提供同名属性的替身映射为 Python `max`。没有 import 整个 Megatron 或 torch，没有调用 scaler 的 CUDA 构造函数。

初始合成状态：scale=1024、minimum=1、growth_factor=2、backoff_factor=0.5、growth_interval=1000、hysteresis=2、growth tracker=0、hysteresis tracker=2。直接运行原方法控制流并断言如下结果；不是手抄伪代码计算后宣称运行了原实现。

| 轨迹/检查点 | 本次输入 | scale | growth tracker | hysteresis tracker |
|---|---|---|---|---|
| 初始 | — | 1024 | 0 | 2 |
| 非连续轨迹第 1 步 | True | 1024 | 0 | 1 |
| 非连续轨迹第 2 步 | False | 1024 | 1 | 1 |
| 非连续轨迹第 3 步 | True | 512 | 0 | 0 |
| 门槛耗尽后的有限步 | False | 512 | 1 | 0 |
| 夹在有限步之间的孤立 overflow | True | 256 | 0 | -1 |
| 孤立 overflow 后的有限步 | False | 256 | 1 | -1 |
| 继续有限更新，到连续第 999 步 | 再执行 998 次 False | 256 | 999 | -1 |
| 连续有限更新满 1000 步 | 再执行 1 次 False | 512 | 0 | 2 |
| 恢复门槛后的首次 overflow | True | 512 | 0 | 1 |
| 恢复后的普通有限步 | False | 512 | 1 | 1 |
| 恢复后的第二次 overflow | True | 256 | 0 | 0 |

三类必需轨迹均覆盖：`True, False, True` 的两个 overflow 不连续仍发生 backoff；门槛耗尽后，`False, True, False` 中的孤立 overflow 仍发生 backoff；增长窗口前第 999 个 finite 步尚未 reset，第 1000 个 finite 步才同时放大 scale、清零 growth、恢复 hysteresis，之后首次 overflow 不 backoff。

另实际执行了两项边界：

- **minimum 边界**：另起 scale=1、minimum=1 的状态执行 `True, False, True, False, True`，每次 scale 都保持 1，最终 growth=0、hysteresis=-1；证明命中 backoff 分支与实际数值下降不同。
- **常量分支**：对标量状态执行原 `ConstantGradScaler.update` 的 `True, False, True`，前后状态一致，scale 仍为 1024。这里只执行该 no-op 方法，没有构造真实 ConstantGradScaler 或优化器。

所有断言通过，进程 exit 0。S1 的原 `state_dict` 在标量状态上确实返回 `scale`、`growth_tracker`、`hysteresis_tracker` 三项；[L155–165](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/optimizer/grad_scaler.py#L155-L165) 保存/加载这三项的静态证据也与正文第 222 行一致。**没有执行含 `.cuda()` 的 `load_state_dict`，没有进行 checkpoint 保存/加载、数值精度验证、真实梯度检测或 optimizer 参数更新。** 本测试只覆盖所述标量控制流及计数器轨迹。

## 5. B24-PC-R02：CLOSED

坐标均来自第 2 节确认身份后的原文件，已执行 `nl -ba`；不采用网页工具重排或删除空行后的行号。以下逐一核对正文与三处记录，历史审阅报告不倒填。

| 应纠正的证据 | 原文件实际位置 | 正文位置 | 复查记录位置 | T06-01 来源补充位置 | 登记 notes 位置 |
|---|---|---|---|---|---|
| QKV 按 query group 交错 | S5 L1840–1841 是交错注释；L1861–1867 按 group 维 view；L1887–1903 是常规组内 Q/K/V 拆分 | `parallelism-and-state.md:100` 三组坐标均正确 | `batch-24-post-close-review.md:27`、`:37` 已改为 L1840–1841，后者补齐 view/split 坐标 | `batch-24-t06-01-sources.md:141` 三组坐标正确；`:142` 记录本轮更正 | `sources/registry.yaml:4707` 三组坐标正确 |
| 无 scaler 的 `return False` | S2 L774；L775 是空行 | 正文第 218 行范围止于 L774；第 222 行明确 L774 | 记录第 26 行范围 L741–774；第 37 行明确 L774 | 来源补充第 140 行 `prepare_grads L741–774`，覆盖真实返回 | notes 第 4707 行 `prepare_grads L741–774`，覆盖真实返回 |
| 成功增长时乘 growth_factor 的赋值 | S1 L153；L152 只是注释 | 正文第 219 行 L144–153，包含赋值 | 记录第 26、36 行 L131–153；第 37 行明确 L153 | 来源补充第 140 行 `DynamicGradScaler.update L131–153`，包含赋值 | notes 第 4707 行同为 L131–153，包含赋值 |

来源补充和 notes 对后两项采用的是包含目标语句的正确函数区间，不要求每处都重复写成单行 L774/L153，不能把正确范围误判为未同步。复查记录第 27、36 行保留“首轮误写”的历史说明，明确标作旧错误，不是继续把旧坐标或旧状态机作为当前依据。

补核结果：S5 L1828–1829 确实仍是有无 output gate 的 shape 注释，不是交错注释；当前“参数身份示例”已不再将交错锚定到这两行。原文的**合成 MHA**、`[3×hidden, hidden]`、TP=2、dim-0 offset=`3×hidden/2` 以及存储布局边界未因引用修订而改变。常量 scaler L43–52、保存/加载 L155–165、S3 L638–662，以及 S4 L2913/L2915/L2917 也均与新增记录相符。

## 6. 回归抽查与新问题

额外只做与本次修改耦合的有限抽查：

- 与第一次报告保留的隔离副本 `/private/tmp/b24-post-close-recheck.hzN5Fw/isolated-repo` 比较当前目标正文：差异限于“参数身份示例”的引用坐标，以及三情形表和紧随其后的说明；没有再次改变 expert grid 的轴序、组员、专家编号或 offset 算术。该旧副本只辅助界定变化，不作为本轮远端源码的替代证据。
- 第 100 行仍限定合成 MHA 和 query-group 存储布局；没有将这些 shape 推广成任意 GQA/MQA/output gate 的通用 shape。PC-05 只因坐标更正而抽查，原技术关闭状态不撤销。
- 第 161–172 行的状态责任矩阵、第 193–197、224–226 行的 step 边界/mid-step 契约仍保留；第 222 行新增 tracker 恢复要求与其一致，没有引入“跳步就不保存 scaler”或“任何 checkpoint 都必须保存梯度”。
- 第 212、214 行仍区分尝试迭代、成功更新、scheduler 进度与 consumed samples；本轮 scaler 修订没有改写该已接受的计数边界。没有重开 PC-01/02 的账面、PC-03 的完整构组或 PC-06 的导航审阅。
- frontmatter 仍为 `status: draft`、`verification.status: source_checked`，没有升级为真实环境已验证。

**新问题清单：无。** 本轮不分配 `B24-PC-R2-xx`，因为没有发现需要修订并设关闭条件的新问题；不将网络下载限制或未做硬件验证伪装成技术正文缺陷。无新增 OPEN P1/P2/P3。

## 7. 隔离结构检查与工作区保护

隔离副本：`/private/tmp/b24-recheck2.8DYmjy/repo`。复制的是当前工作区内容，包含原有未提交改动及两份已有复查记录；排除 `.git`、`.venv`、`.agents`、`.codex` 和无关 Python 缓存。沿用第一次报告已明确的装配要求，把原工作区现有 `build/catalog.json`、`build/catalog.md` 作为副本起始文件一并复制，以满足正文已有本地链接；随后 `make build` 只重写**隔离副本**的 build 文件。

解释器为原工作区 `/Users/ywang2397/work/AI_reliability_knowledge_base/.venv/bin/python`，实际版本 Python 3.11.15。没有安装或升级依赖。实际以隔离目录为 cwd 执行：

```bash
make check PYTHON=/Users/ywang2397/work/AI_reliability_knowledge_base/.venv/bin/python
make build PYTHON=/Users/ywang2397/work/AI_reliability_knowledge_base/.venv/bin/python
```

该副本没有 `.venv`，Makefile 因而使用上面的绝对 `PYTHON`；命令输出也确认执行该原工作区解释器，而不是另一个系统 Python。

| 检查 | 报告写入前的隔离执行 | 含本报告的最终隔离执行 | 输出 |
|---|---|---|---|
| `make check` | PASS，exit 0 | PASS，exit 0 | `103 content entries; 493 sources.` |
| `make build` | PASS，exit 0 | PASS，exit 0 | 同为 103 / 493；生成副本 `build/catalog.json` 与 `build/catalog.md`。 |

本报告落盘后再复制进入同一隔离副本、执行同样两条命令，因此本报告的本地链接也包含在最终检查中。日志分别为本轮隔离目录下的 `make-check-before-report.log`、`make-build-before-report.log`、`make-check-with-report.log`、`make-build-with-report.log`。控制流脚本、摘要核验与结果保留在同目录 `audit.py`、`source-identities.json`、`control-flow-results.json`、`validation-results.json`；这些临时材料不进入仓库。

报告写入前记录既有工作区文件 SHA-256，最终逐项比较：**既有文件内容变更 0、删除 0，仓库唯一新增为本报告**；原工作区两个 build 文件也纳入字节比较且未变。没有修改或提交已有未提交修订，没有创建分支。文件保护不把 `.git`、`.venv` 或 Python 缓存当作知识源内容；没有在原工作区运行 make build。

本轮没有改 `src/kb/`，未运行 `make test`，未执行训练、GPU/NPU、进程组初始化、集群或 checkpoint 操作。结构检查只验证格式、登记与本地链接，**不验证远程链接、技术正确性或真实环境效果**；技术关闭依据是第 2–5 节的固定来源与受限控制流复核，而非 make 的 PASS。
