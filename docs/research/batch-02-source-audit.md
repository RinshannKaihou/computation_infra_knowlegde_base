# 第二批来源核查与集成记录

日期：2026-09-29。范围：F03、F09、F11 三篇正文，以及 E01 的 CANN 安装文档补充。研究、写作与独立复核子代理均使用用户指定的 `gpt-5.6-sol`、`high` reasoning；主任务负责整合来源、交叉检查、导航和构建。

2026-09-30 补审：用户授权 Codex 主助手替代 astra，已完成[第二批审阅](batch-02-codex-review.md)及[修订定向复核](batch-02-08-09-codex-recheck.md)，新增 P2 B02-C01 与 batch 08 的共享影响均已关闭。本批在原审阅范围内通过；没有实际派发 astra/xhigh 或硬件验证，正文仍为 draft。四批总体状态见[补审汇总](batch-01-02-08-09-codex-review-summary.md)；下文原来源审计和复核结论保留为历史。

## 交付与证据范围

| 任务 | 正文 | 采用的证据 | 保留的缺口 |
|---|---|---|---|
| F03 | [计算节点资源与拓扑参考](../../knowledge/01-hardware/resource-topology.md) | Atlas 800T A2 产品页；DGX H100/H200 用户指南中的组件、端口映射和拓扑入口 | Atlas 产品页未给出的 NPU 数量、设备内存和互联；任何具体节点的 BOM、现场枚举与故障影响 |
| F09 | [训练数据供给路径与等待](../../knowledge/04-data-storage/training-data-path.md) | PyTorch 2.6 DataLoader/CUDA 语义；MLPerf Storage v2.0 规则 | TorchNPU/CANN 的对应传输语义；真实数据集、缓存、队列、指标和 GPU/NPU 性能 |
| F11 | [从物理设备到容器资源的状态链](../../knowledge/05-cluster-platform/device-resource-chain.md) | Kubernetes v1.32 Device Plugins；MindCluster v26.1.1 固定组件说明及注册、上报、分配实现 | 目标集群部署与时间线；运行时实际应用结果；与 TorchNPU/CANN 的整栈配套 |
| E01 补充 | [昇腾软件栈的文档配套档案](../../knowledge/02-software-stack/ascend-documented-profile.md) | 当前 CANN community 安装正文中的驱动/固件前提和物理机职责 | 不可变的 CANN 8.3.RC1 历史安装条件、精确 HDK 与具体制品身份 |

逐条来源、可支持的论断、许可范围和未采用候选见 [F03 记录](batch-02-f03-sources.md)、[F09 记录](batch-02-f09-sources.md)、[F11 记录](batch-02-f11-sources.md)。本批新增七项来源登记，沿用已有 Kubernetes 来源；全库目前为六篇正文、十三个导航/路径条目和十九项来源记录。来源记录包括发现入口和具体版本，数量不等于已完成十九个来源的全部核查。

## 固定快照与可变页面

| 来源 | 本次定位方式 | 引用约束 |
|---|---|---|
| MindCluster | tag `v26.1.1` 解引用为 `44385c13d7b1d87def35f1604e8be4d16de6ca4e` | 正文引用完整 commit；不使用 master 补写旧快照，不声明该 tag 的维护期或整栈兼容 |
| MLCommons Storage | release `v2.0` 对应 `7e71ca162d8f9e7ae4b5b698d7d79b0883817f25` | 主任务补读固定 commit 的规则与根 `LICENSE.md`；最终正文和登记使用完整 commit |
| PyTorch | 2.6 版本化文档；关联 release v2.6.0 commit `1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340` | 区分生成文档与源码身份；不声称文档站点不可变，也不把 CUDA 页面外推为 TorchNPU 语义 |
| DGX 指南 | 页面标注最后更新于 2026-01-26 | 日期标识而非不可变快照；厂商机型资料不代表用户实际配置 |
| Atlas 产品页 | 2026-09-29 实际读取 | `revision` 仅登记访问日期，不把未取得正文的白皮书版本号移作页面版本 |
| CANN 安装页 | 2026-09-29 浏览器渲染正文 | URL 含 `83RC1`、页头显示 `8.3.RCX`；保留差异，不将 URL 当成内容版本证明 |

## CANN 补充核查

静态网页读取曾只返回导航外壳；随后使用浏览器实际加载正文，核对页面标题、版本选择器和目标章节。没有执行页面里的安装、查询、卸载或配置命令，没有下载软件包或接受软件包协议。

### 采用的精确页面

1. [快速安装](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/83RC1/softwareinst/instg/instg_quick.html?Mode=PmIns&InstallType=netconda&OS=openEuler&Software=cannToolKit#ZH-CN_TOPIC_0000002474377814__zh-cn_topic_0000002473322892_section574172816522)：当次页面选择为物理机、在线 Conda、openEuler、Toolkit；“安装前准备”将 NPU 驱动和固件已经安装列为 CANN 安装前提。页面标题和版本选择器显示 `8.3.RCX`。
2. [安装 NPU 驱动和固件](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/83RC1/softwareinst/instg/instg_0005.html?Mode=PmIns&InstallType=netconda&OS=openEuler&Software=cannToolKit#ZH-CN_TOPIC_0000002474537728)：从文档目录进入该页并确认实际导航后的 URL；正文说明物理机和容器部署场景均在物理机安装驱动、固件。它不能证明容器设备映射、用户态软件和框架已经可用。

连续阅读模式还加载了邻近的软件包和环境章节；那些相邻正文没有被当成上述两个精确页面的独立证据。未将页面示例中的 Python 范围、安装顺序、软件包组合或硬件选择补入 E01 的历史配套矩阵。

固定 TorchNPU README 的配套行仍是 E01 中 `torch-npu 2.6.0.post3 / PyTorch 2.6.0 / CANN 8.3.RC1` 的来源。当前 CANN 页面不提供本基线完整的、同版本的 HDK 配套证明。这次补充也不改变[第一批记录](batch-01-source-audit.md)对错误引用卸载页的纠正。

## 审阅修正

三篇初稿完成后安排独立只读复核，主任务完成以下修正：

- 将新来源合入统一 registry，消除初稿交付时尚未登记的引用。
- 修正硬件关系图：分开主机 NIC 与可选加速器直出端口，移除本地盘直接指向共享存储的路径；说明网络节点是抽象入口，不能推断网络共用。
- 修正数据路径图：索引采样作为读取前的控制关系，读取后的 `collate` 单列；明确 map-style 与 iterable-style 的差异。
- 将 F09 的协作待办替换为已入库文章的普通链接和稳定 ID 关系。
- 将 MLPerf 规则和许可引用固定到完整 commit，补充实际读取许可正文的结果。

独立复核确认上述问题已解决，并检查了 E01 的 `8.3.RC1` 固定声明与 `8.3.RCX` 当前补充范围一致，未发现新的实质性问题。该次复核不改变正文 `draft` 状态，也不是硬件或整栈兼容性验证。

## 集成与后续

正文接入所属章节、两条平台路径和训练/推理任务入口；README、填充计划、来源获取包与任务清单同步更新。F03/F09/F11 的 `done` 只表示本批草稿和来源核对已交付。人通过 Markdown 阅读，Agent 通过 `make build` 生成的内容清单查找相同条目；没有新增网站、检索服务或执行接口。

本批按仓库约定运行 `make check` 与 `make build`。两者只检查结构、引用和生成流程，技术结论仍以正文中的来源范围与未知项为准。本批没有修改 `src/kb/`，也没有执行真实 GPU/NPU、存储或集群实验。

下一内容批次为 F07 集合通信与 rank 进度、F08 通信性能口径、F17 可靠性维度与故障域、F18 证据与假设。精确 HDK 配套、Atlas 设备拓扑、TorchNPU 数据传输以及实际制品身份继续作为有来源后再补的缺口。
