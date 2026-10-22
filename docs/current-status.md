# 当前状态与使用方式

更新：2026-10-22。本页是当前使用与维护入口；历史批次、规划和审阅模型记录见[归档索引](archive/README.md)。

## 当前定位

知识库主要服务昇腾用户，供人和 Agent 学习系统关系、查找技术依据、分析问题与准备方案。其他平台内容保留为比较和按需参考，不以平台篇数均衡驱动扩写。

批量内容建设已结束：三轮共 141 项内容任务均已交付，内容批次止于 Batch 32；其中既有条件验收的证据缺口仍保留。下一步由实际问题与资料变化决定，不从历史计划自动领取任务。正文的 `draft` 是编辑状态，不代表仍有一个待继续执行的写作批次。

当前可用的是 Markdown 正文、阅读路径和本地构建的静态目录。网站、向量检索、知识 API、现场适配器及自动评测系统仍属于未实现的早期设想。

## 怎样使用

| 目的 | 入口与使用方式 |
|---|---|
| 认识昇腾系统 | 从[昇腾路径](../paths/platforms/ascend.md)进入；先读[术语与责任边界](../knowledge/00-overview/terms-and-system-boundaries.md)、[软件栈分层](../knowledge/02-software-stack/layers-and-boundaries.md)，再选训练或推理全流程 |
| 查一个具体问题 | 沿[训练问题路径](../paths/tasks/training-triage.md)或[推理问题路径](../paths/tasks/inference-triage.md)找到正文，核对版本、原始来源和未知条件 |
| 准备方案或讨论 | 从 README 的任务与角色入口组织阅读；输出有依据的条件、权衡和待确认项，具体环境未知就保留未知 |
| 使用 Agent 查证 | 要求回答给出正文位置与原始来源，区分事实、推断和未知；本地 `make build` 可生成 `build/catalog.md` 与 `build/catalog.json` |

没有现场环境时也可以学习、查询和做纸面分析。排障指南描述一类现象及调查方法，不表示当前存在一个必须修复的 bug。操作有效性仍需在具体环境取得证据。

## 当前证据边界

- 尚无本地实测、故障注入或原事件复现证据。既有七份实验仍为设计，执行数为 0/7；19 个准备实例仍未就绪。没有实测环境不阻止知识库日常使用。
- `source_checked` 表示正文声明范围内的来源核对；编辑审阅与 `reproduced` 分别维护。归档不升级任何正文的编辑或验证状态。
- 公开教学题组可用于学习与检索回归，尚无独立诊断效果评测结果；独立评测集仍未取得。

以下限制继续影响具体主张，不因历史任务归档而关闭：

| 待确认项 | 对使用的影响与依据 |
|---|---|
| 逐算子累加精度与 TorchNPU `cubeMathType` 透传契约缺证（B17-C08） | 相关平台精度判断保持 unknown；见[精度语义正文](../knowledge/02-software-stack/dtype-layout-and-precision-semantics.md)及[原例外记录](research/batch-17-t02-10-exception.md) |
| HCCL Test 与目标 CANN/HDK/机型的官方配套交集未建立（03.5-G3 / BLOCKED-1） | 不将不同版本的 API、测试指南拼成可执行环境；见[通信库档案](../knowledge/03-communication/communication-library-profiles.md)及[原例外记录](research/batch-19-blocked-1-exception.md) |
| 真实环境、验证结果与独立评测证据缺失 | 选用流程或形成现场结论前按具体目标补证；[原验证计划](../plans/validation-backlog.yaml)与[准备骨架](../plans/v00-preparation-instances.yaml)仅供将来按需取用 |

完整覆盖基线见[主题盘点](topic-coverage-audit.md)及[机器清单](../plans/topic-coverage.yaml)。62 个主题达到所列基础范围、1 个部分覆盖；覆盖程度不代表技术主张或平台组合全部验证通过。

## 怎样维护

围绕使用中发现的错误、解释不清、查找断点和新来源做定向修订。新增或改动正文时遵守[维护规则](../AGENTS.md)与[编写指南](authoring-guide.md)，保留稳定 ID、单一主归属、精确来源、版本条件和未知项；修改后运行相应结构检查。

当前不固定审阅模型、推理档位或 CLI。保留查证、记录发现、修订后复核和说明验证范围的原则；历史模型及实际审阅过程在原报告中保留，不作为新的执行约束。

旧批次计划、候选来源包与交接提示词原地冻结；验证方案休眠保留。需要开展新工作时，按当次具体目标选择资料与范围，不默认恢复整套旧计划。
