# 第十七批第五次定向复核记录

**最新进展（2026-10-09）：[第六次定向复核](batch-17-codex-sixth-recheck.md)已完成，本报告的三项修订要求均已满足，无新增修改项。** 累加精度与固定实现关联仍缺证，C08 继续 OPEN（P2），累计 12 项关闭/1 项开放。以下保留第五次输入与当时判定，已修复项不再列为待办。

复核日期：2026-10-09（Asia/Shanghai）。**结论：B17-C08 继续 OPEN（P2）；累计 12 项 CLOSED、1 项 OPEN，Batch 17 暂不通过。** 新取得的官方页确实补入 Add/Matmul 支持条件与 Cube 计算逻辑，但当前摘要仍有来源范围错误和适用条件遗漏；累加精度及关联实现证据仍缺。第四次已通过的两处限定不重新打开，本轮不新增发现 ID。

依据：[第四次定向复核及剩余关闭条件](batch-17-codex-fourth-recheck.md)、[第五轮修订](batch-17-review-fixes.md)、[路线图](../full-coverage-roadmap.md)、[T02-10 验收清单](../../plans/full-coverage-backlog.yaml)及[批次审阅约定](../authoring-guide.md#7-批次审阅约定)。执行者为初审及前四次复核的同一 Codex 主助手，与正文编写者分开，未派发子代理。用户约定配置为 `gpt-6.1-sol / xhigh`；沿用此前披露，没有可独立核验的实际运行标识，不把约定写成已确认的执行元数据。

## 输入与独立取证

| 输入 | 第五次复核 SHA-256 |
|---|---|
| [精度正文](../../knowledge/02-software-stack/dtype-layout-and-precision-semantics.md) | `dc3770e7e81d23d9d4b3bdc39a28abbea67a5261195ccd2ac7852c23b368dd11` |
| [精度研究记录](batch-17-dtype-precision-sources.md) | `c7f3378876481068c955a7c3b05ddcaa09671bc2a9d4203484cfa99c04390d5d` |
| [修订记录](batch-17-review-fixes.md)（追加本次结果前） | `fb3778a8f670fc5964f2c39dc0bf6fc3710a104cc8fb1e549339163e8f327356` |
| [来源登记](../../sources/registry.yaml)（340 项，本轮不改） | `2eb12f2ad55d288648c6c4fc64628ace2aca446cd5b99ba12c0f6a9b10752445` |

重新读取精度正文 L44、L61、L102–117、相关登记及第五轮附录。其他三篇正文、领域索引、其他三份研究记录与 backlog 的摘要和第四次输入一致，不重新验收已关闭项。

网页工具未能读取四个精确 `doc_center` 地址，改用 curl 独立取得同一登记 URL（均 HTTP 200），完整读取静态 Markdown，包括算子页样例；没有执行这些样例。以下行号按本次原文件逻辑行计数（含未以换行结束的末行），不是网页阅读器坐标。CANN 版本路径与本次内容摘要共同记录观察身份，不把版本路径视为不可变 commit。

| 已登记来源 | 本次逻辑行数 | 原始响应 SHA-256 |
|---|---|---|
| `src.huawei.cann-82rc1alpha001-acl-datatype` | 30 | `31024e3939fa672a92af6d35f9fc5d06c6c3b85f311d70790312f72da5558420` |
| `src.huawei.cann-82rc1alpha001-acl-promotion` | 39 | `410648a0f52e58e01c45ae6b9ccf30a4d6caa09f64891898ef57864f945539af` |
| `src.huawei.cann-82rc1alpha001-aclnn-add` | 317 | `a0098e281fbd383e2219d26fdbc32031e3fac763e4e11a233108ceb40f5cdaca` |
| `src.huawei.cann-82rc1alpha001-aclnn-matmul` | 224 | `c4fa0ef483cade0d51a84ba489d43a8d3bceb469fbaed115ccb12a03b4d7d235` |

复用前轮固定 TorchNPU AutoCastOps.cpp 的核对结果，仅采信 matmul 族 autocast 注册；不把它充作 Cube 选项透传或内核计算实现。未定位到实现不等于证明整个仓库不存在该实现。

## 本轮判定

| 新增内容 | 判定与范围 |
|---|---|
| 内部 dtype 互推导 | 精度 L105 的存在性说明符合官方页：部分类型可推导，表中另有不允许组合，逐算子限制另计。不证明与 PyTorch promotion 全部相同 |
| aclnnAdd | 精度 L106 的产品差异、参数 dtype、ND、broadcast 与错误条件入口得到支持；这是有限的 API 支持/推导样板，不作为累加精度证据 |
| aclnnMatmul | 精度 L107 的降精度选项与产品差异有官方依据，计算逻辑契约已取得；但缺少关键限制，尚不能采信当前四选项摘要为完整适用条件 |
| aclDataType 全量/torch 对应列 | 精度 L104 及登记的来源范围不成立，见下文。本次收到的是 19 行简写表，不是所称 21 项官方类型加 torch 列 |
| 累加精度与固定实现关联 | 精度 L117 继续 unknown / OPEN 合理。本次所取 Matmul 页未陈述累加数据类型；普通 autocast 注册不能建立 TorchNPU 到 cubeMathType 的实现关系 |

## B17-C08 — P2，OPEN：仍需修订的新增主张

### 1. 数据类型页被误作完整枚举和 torch 映射

位置：精度 L104、L61；`src.huawei.cann-82rc1alpha001-acl-datatype` 的 title/notes；精度研究第五轮附录 L68 与修订记录第五轮的“全量”概括。

本次取得的[数据类型页](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/aolapi/context/common/%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B.md) L3 将完整类型引向另一份 AscendCL `aclDataType` 文档；该页 L7–27 是原始名/简写名两列表，19 项含 ACL_STRING。没有 torch dtype 对应列。正文列举 18 项并漏掉 STRING，也不能称为完整枚举。用户提交说明的“21 项”与本次登记 URL 的正文不符，不以提交说明替代来源。

修订要求：按此页实际角色改为有限简写表；若列完整表，须补 STRING 并按实际 19 行核对。删除该来源的 torch 对应列主张。若作者另有真正的完整枚举/torch 映射页，应登记和引用那个精确正文，分别说明来源范围，不能从本次简写表补推。本轮未取得其链接所指完整枚举正文，不宣称已验收。

### 2. cubeMathType 摘要遗漏会改变适用性的条件

位置：精度 L107；`src.huawei.cann-82rc1alpha001-aclnn-matmul` notes；第五轮研究/修订附录的“逐产品条件”概括。

独立取得的[aclnnMatmul 页](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/aolapi/context/aclnnMatmul.md) 中，L30–49、L78–80 明确限制当前摘要：

- L41：Atlas 训练/推理系列的 FLOAT32 输入不支持 `KEEP_DTYPE`；不能无条件写成保持输入类型计算。
- L45–46：`USE_FP16` 的计算逻辑及 A2 的 BFLOAT16 排除条件需写全，不能只列选项名。
- L39：有互推导关系时，选项处理的是推导后的类型；L36 要求 out 与推导后的类型一致。降计算精度不等于输出存储 dtype 也随之降低。
- L80：self 与 mat2 均为一维时，cubeMathType 不生效。正文同时声明 1–6 维，必须保留这一排除项。

正文已有 `ALLOW_FP32_DOWN_PRECISION` 的产品差异、`USE_HF32` 的 A2/FLOAT32 条件以及 BFLOAT16 混合输入排除项，继续采信，不要求重写。框架侧 `lower_precision_fp` 只证明输入 autocast 注册策略；“方向对照”可以作为明确的概念比较，不能把标题中的“官方正文 + 框架实现侧”理解为已取得该计算选项的实现链。

修订要求：补齐上述精度选项、推导/输出和一维例外，同步正文、登记及附录；把 SDK 官方计算逻辑契约与 TorchNPU 注册/未定位实现分别记录。

### 3. verification notes 的取得范围仍有矛盾

精度 L44、L61 前半与 L106–107 都说 Add/Matmul 逐算子正文已取得，但 L61 末尾仍无条件写“CANN 逐算子表未取得”。应改为两算子正文已取得、其余未核对范围和累加精度/关联实现仍未知。保留历史研究前段不构成新发现，但当前元数据需与新增取证一致。

## 剩余关闭条件及累计状态

先纠正上述新增来源范围和支持条件，并同步记录；官方 Matmul 的计算逻辑契约已取得这一进展保留，不再将全部算子计算精度正文概括为未取得。仍沿用前次强制证据边界：累加精度缺证继续单列未验收；固定实现关联也不能由普通 autocast 注册代替。作者继续将这两项记 unknown / OPEN 正确，不因新增四项登记关闭 C08。第四次通过的候选门控与第五种 autocast 策略限定不重复列为修改项。

累计 CLOSED：C01、C02、C03、C04、C05、C06、C07、C09、C10、C11、C12、C13（12 项）；OPEN：C08（P2）。T02-10 继续暂不通过，不解锁依赖其完成的任务；其他任务保持原验收边界。条目仍为 `draft / source_checked`，backlog 与主题覆盖状态不调整。

独立 `make check` / `make build` 均 PASS：83 content entries / 340 sources。本轮只新增第五次复核报告、同步审阅状态并追加结果；未改正文、四份作者研究记录、来源登记或 `src/kb/`，未新增代码测试、未执行设备/集群或数值实验。响应只在临时目录读取，未镜像全文入库；沿用网站许可 unknown 的登记，不推断再分发权。结构检查不证明技术正确性、远程内容不可变或硬件验证。
