# 第十九批第三次定向复核

复核日期：2026-10-12（Asia/Shanghai）。作者文件中的 `2026-10-14` 保留为输入标签，不作为本轮执行日期。

**结论：C03、C09 转 CLOSED，累计 9 CLOSED / 0 OPEN。T03-05 在原定有限内容/来源范围内通过，T04-01 的既有通过范围保持；T03-06 对 T03-05 的审阅等待门已解除。** 本次只复核[第二次复核](batch-19-codex-rerecheck.md)的两个剩余要求及其同步影响，无新增发现 ID，不重开此前七项。T03-06/T03-07/T03-08 未在本轮审阅，不能据此声明整个 Batch 19 已验收。

约定模型 / effort 为 `gpt-6.1-sol / xhigh`，本会话 Codex 主助手执行，与作者修订角色分开；未派发子代理。实际运行标识无可独立核验元数据，沿用[初审说明](batch-19-codex-review.md)。依据[写作指南](../authoring-guide.md#7-批次审阅约定)、[原任务验收](../../plans/full-coverage-backlog.yaml)及 [AGENTS](../../AGENTS.md)，本轮通过不构成硬件验证或完整部署组合声明。

## 输入与变更范围

| 输入 | SHA-256 |
|---|---|
| [T03-05 正文](../../knowledge/03-communication/rccl-runtime-and-verification.md) | `69e84c033cb8b993bf6a823fbbfff98e9fb65d51c265f2bf92aba526de70316c` |
| [T04-01 正文](../../knowledge/04-data-storage/training-data-path.md) | `f703eba9a49f545e7e62ec3864c3e0b176b313f9fcdcbdfffc565200c2cbcb81` |
| [RCCL 来源记录](batch-19-rccl-sources.md) | `891c737e94dcfc4d1c40e5a7ed9cf6f96847ba56fdecb46482a8c3394b8b50c2` |
| [修订映射](batch-19-review-fixes.md) | `2d5873a7c5cb8c4680b1b51707ae2dc0fce922d8c9e87b350730e047edd44851` |
| [第二次复核](batch-19-codex-rerecheck.md) | `96fcf1a6b8515dcbeca05d5fd855ee706c9979f2d03489762c6c830e2dd0de44` |
| [来源审计](batch-19-source-audit.md) | `9b9d7953e58b8921d0d4dbb5b9f1e49ae31dc0984742eb6dc8181234f6f6971a` |
| [来源登记](../../sources/registry.yaml)（386 项） | `e84c3b6eb61a83a46dbbfd371e5de4112def120131e0c374181e8e5acbf8f51f` |

T04-01 正文、RCCL 来源记录及登记与第二次复核输入身份相同；本轮读取 RCCL L75/L77/L95–96 和第三轮修订映射。设计命令与最终命令的参数序列独立解析核对一致，均无 `-O` 选项；timer href 已含 `src/`。Batch 17/18 研究输入对照第二次复核未变；本轮写入保护另覆盖全部既有正文、研究记录、修订映射、索引、登记和计划。

## 一次源复验

默认 TLS 校验 curl 重抓五个精确地址，全部 HTTP 200：固定 commit `7da43026e4f2ef7600433c38c820732f7a205d22` 的 common.cu、README、src/timer.cc，及正文所用 `therock-10.1` 的 src/timer.cc blob/raw。三个固定原文件 SHA 与第二次复核相同；tag timer 原文字节与固定 commit 一致。本轮未运行或编译 rccl-tests，不重做其余已关闭范围的取证；临时原文和日志未镜像入库，无新增登记。

| 固定原文件 | 字节数 | SHA-256 |
|---|---:|---|
| rccl-tests common.cu | 107420 | `1339f9535d68b748677bd817e88d02002a71ff27b7f2b7ce41fcaccaa505f9d7` |
| rccl-tests README | 14309 | `7b2dbdab28a619a47c8ac685704fc6a1432fc7d42ce4c87c71ab82a7b905e2cc` |
| rccl-tests src/timer.cc | 615 | `c1e4e76679cc56c62b84633035a07ae563e7c6d47d769324c978b12c229d436f` |

## C03 — CLOSED

T03-05 L77 与 L95 均省略 `-O`，采用相同的 Float/Sum、20 次迭代、1 次 warmup、`-m 1`、8 B–1G 倍增扫描、每进程一 GPU 和 `-c 1`；L77 保留 0/1 只选择一种 placement 的注记，不再把 `both` 当作可传取值。源码默认两个 enable 标记均为 1，省略 `-O` 不会进入反置其中一个标记的解析分支。[common.cu L174–179](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/common.cu#L174-L179)、[L2092–2095](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/common.cu#L2092-L2095)、[README L187–190](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/README.md#L187-L190)。

L77/L96 的完整覆盖、校验开启、零 wrong、N/A/缺行/提前停止不判 P1，以及正确性通过与性能无基线时未判定的条件保持。两种 placement 按每个消息尺寸输出中的两组列核对，沿用[第二次复核的输出形态说明](batch-19-codex-rerecheck.md)，不以正文“输出行”的简写要求将同尺寸拆成两行。修订已消除命令与预期覆盖的不一致，无需执行 benchmark 关闭本项。

## C09 — CLOSED

T03-05 L75 已改为 [therock-10.1 的 projects/rccl-tests/src/timer.cc](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl-tests/src/timer.cc)，本轮精确 blob 请求 HTTP 200；[同路径 raw](https://raw.githubusercontent.com/ROCm/rocm-systems/therock-10.1/projects/rccl-tests/src/timer.cc) 也 HTTP 200，615 B，SHA 与[固定 commit 文件](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/timer.cc)一致。原文件中的 steady_clock / 秒换算实现与所引用的默认主机计时描述相符。其余来源链按第二次复核已接受范围保持，原错误路径仅作为历史记录保留。

## 状态与通过范围

| 状态 | ID |
|---|---|
| CLOSED（9） | C01、C02、C03、C04、C05、C06、C07、C08、C09 |
| OPEN（0） | 无 |

- T03-05：独立 RCCL 文档/源码样板、接口与返回/错误边界、日志、测试口径、来源案例和两节点待执行设计，在原定有限文档范围内通过；并非整栈已测组合或 AMD 硬件复现。
- T04-01：第二次复核通过的数据身份/游标、缓存/对照、选定 NPU 源码语义和来源范围保持，不重做验收。
- T03-06：对 T03-05 的审阅等待已解除，可按原任务前置及来源要求继续填 RCCL 列；本轮没有启动其写作，也未关闭 HCCL Test 组合等尚待交付子项。
- T03-07/T03-08：按原顺序和具体前置推进，本轮未审阅。两个已审条目的通过不能替代整个 Batch 19 的后续验收。

正文仍为 draft/source_checked，尚无实机验证；环境档案、整栈组合、latest/别名 diff、PR 最早入版及底层挂起机理等既有 unknown 保留。T02-10 按 [B17-C08 例外清单](batch-17-t02-10-exception.md)条件满足，未证累加精度/cubeMathType 不关闭；T02-11 草稿仍只作边界材料，不因本轮通过转为已验收前置。任务计划/主题覆盖未由审阅者改为完成。

本轮仅新增本报告并更新既有三份审阅报告及来源审计的最新状态/入口，作者正文、研究记录、修订映射、索引、登记和其他批次材料保持本轮输入。历史初审与前两次复核判定保留，不改写为当前结果。

`make check` / `make build` 均 PASS（87 篇内容 / 386 项来源），报告本地链接、状态集合和受保护输入身份核对完成。结构检查不证明技术正确性、全部远端链接或硬件验证。未修改 `src/kb/`，无新增内容镜像测试，未执行 `make test`；无真实 GPU/NPU、MPI/RCCL、存储、配置变更或故障注入。
