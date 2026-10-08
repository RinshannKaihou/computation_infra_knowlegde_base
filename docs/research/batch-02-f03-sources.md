# 第二批 F03 来源提取记录

本文件记录 `hardware.resource-topology` 使用的页面、可支持的陈述、未采用的候选资料和来源登记建议。它是来源审计记录，不是目标环境资产清单、机型兼容矩阵或硬件实测报告。

## 核对结论

F03 采用两份可直接打开并看到目标正文的厂商资料：Huawei Atlas 800T A2 产品页和 NVIDIA DGX H100/H200 用户指南。前者支持 NPU 服务器的明确机型及主机侧整机规格，但没有公开 NPU 数量、设备内存或节点内互联；后者支持 DGX H100 的整机组件、端口映射和拓扑图入口。正文保留这种证据粒度差异，没有把 GPU 拓扑类推成 NPU 拓扑。

### Huawei Atlas 800T A2

| 核对对象 | 精确定位 | 实际打开结果 |
|---|---|---|
| 产品页 | <https://e.huawei.com/cn/products/computing/ascend/atlas-800t-a2> | 页面标题为“Atlas 800T A2训练服务器”；“技术规格”可见 4U、4×鲲鹏 920、32 个 DDR4 槽及单条容量、三组 SATA/NVMe 组合、8×200GE QSFP 直出/RoCE、最多 3 个 PCIe 4.0 扩展槽、2+2 电源和 N+1 风扇等字段。 |
| 页面关联白皮书落地页 | <https://e.huawei.com/cn/documents/products/computing/b0b253c4d5da4e05ba80a39e3dc65fd2> | 标题为“Atlas 800T A2 训练服务器 技术白皮书 16”，页面明确显示文件无法预览且下载区域要求提交信息。本轮未取得白皮书正文，因此版本 16 不作为任何规格、容量或拓扑证据，也不写入产品页的 `revision`。 |
| 产品文档入口 | 产品页“相关资源”中的“Atlas 800 A2 训练服务器（型号 3010）产品文档” | 当前读取返回 403；浏览器访问跳到华为技术支持入口，没有显示目标机型正文。未作为证据。 |
| 网站法律声明 | <https://www.huawei.com/cn/legal> | 第 212–214 行附近的“著作权说明”声明网站材料受版权保护，未经许可不得复制等；本库仅保存链接和原创归纳，不镜像页面或图片。 |

产品页没有显示 NPU 数量、单 NPU 设备内存、NPU 到 CPU/PCIe 的映射或 HCCS/其他节点内互联。以下推断均被排除：

- 从 8 个 200GE 端口推断 NPU 数量或端口与 NPU 一对一；
- 从训练任务常见的 8 卡配置推断该产品页所代表的每个 BOM 都有相同设备布局；
- 从其他 Atlas A2 机型或系列文档移植内存容量和互联拓扑；
- 把“最多 3 个 PCIe 4.0 扩展槽”解释为 NPU 的完整主机连接路径。

### NVIDIA DGX H100/H200

| 核对对象 | 精确定位 | 实际打开结果 |
|---|---|---|
| 用户指南入口 | <https://docs.nvidia.com/dgx/dgxh100-user-guide/> | 标题为“NVIDIA DGX H100/H200 System User Guide”，目录包含 Hardware Overview、Network Connections 和 System Topology，页面标注最后更新于 2026-01-26。 |
| 组件、网络与拓扑页 | <https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html> | “Component Descriptions”可见 H100/H200 分列的 GPU 与总 GPU 内存、CPU、系统内存、系统盘、数据缓存盘及网络；“Network Modules”给出 OSFP 端口到 network module/CPU 和 GPU 的映射；同页有 System Topology 图入口。 |
| Notices | <https://docs.nvidia.com/dgx/dgxh100-user-guide/notices.html> | 页面标注最后更新于 2026-01-26；第 37–39 行附近说明文档不授予许可，复制需要事先书面批准且须满足条件。本库仅保存链接和原创归纳，不复制图。 |

正文只使用组件表中语义清楚的字段。组件表的 `NVSwitch` 行使用“4 x 4th generation NVLinks”这一措辞，本轮没有把它解释为 NVSwitch 数量、NVLink 条数或拓扑边；节点内互联只引用官方系统拓扑图入口，避免自行改写厂商结构。

## 没有采用的候选资料

- 搜索结果曾返回 `Ascend/mind-cluster` 的旧 `docs/en/scheduling/...` 路径。2026-09-29 只读查询官方远端得到 `master` 为 `d0cf08dada17ea0c16026ebbd3e5c29ed5ac85c6`，但在该固定 commit 请求候选文件返回 404；搜索摘要不能代替正文，因此未引用。
- 华为 `Atlas A2 中心推理和训练硬件 25.2.0 npu-smi 命令参考 02` 的检索结果含内存、拓扑和 HCCS 目录项，但精确 URL 在直接打开时返回 403/跳转，没有取得目标页面正文。本轮没有用目录或摘要补齐 Atlas 800T A2 拓扑，也没有写入任何命令。
- 不使用社区论坛、模型训练 README、第三方规格表或经销商页面支持整机拓扑事实。

## 来源登记建议

以下条目按 `schemas/sources.schema.json` 填写，供主审合并进 `sources/registry.yaml`。F03 作者不直接修改共享来源表。

```yaml
- id: src.huawei.atlas-800t-a2-product-2026-09-29
  title: Atlas 800T A2训练服务器产品页（2026-09-29核对）
  url: https://e.huawei.com/cn/products/computing/ascend/atlas-800t-a2
  kind: documentation
  registered_at: "2026-09-29"
  revision: "page observed 2026-09-29"
  license:
    status: unknown
    scopes: []
    notes: 华为网站法律声明称网站材料受版权保护且未经许可不得复制等；本库仅登记链接并作原创归纳，未取得产品页内容的再分发许可。
  notes: 已打开并核对技术规格区；支持 Atlas 800T A2 的主机、内存槽、本地存储组合、网络、PCIe扩展槽、电源与风扇规格。页面未给 NPU 数量、设备内存或节点内互联，不能据此补写。
```

```yaml
- id: src.nvidia.dgx-h100-h200-user-guide-2026-01-26
  title: NVIDIA DGX H100/H200 System User Guide（2026-01-26）
  url: https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html
  kind: documentation
  registered_at: "2026-09-29"
  revision: "last updated 2026-01-26"
  license:
    status: unknown
    scopes: []
    notes: 官方 Notices 称文档不授予知识产权许可，复制需事先书面批准并满足条件；本库仅登记链接并作原创归纳，未复制官方拓扑图。
  notes: 已核对 DGX H100/H200 组件表、网络端口与 GPU/CPU 映射、系统拓扑图入口和电源冗余说明；具体数值按 H100/H200 分列，不把 H200 数值写入 H100 示例。
```

## 验证与执行边界

本轮没有安装或运行上游工具，没有克隆厂商仓库，没有访问真实 GPU/NPU 设备，也没有执行枚举、通信、存储、链路或性能测试。`source_checked` 只表示上表所列页面和正文引用范围已经核对；具体机型资料不代表用户环境的实际 BOM、拓扑、容量或健康状态。
