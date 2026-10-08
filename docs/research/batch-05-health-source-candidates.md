# 第五批设备健康资料候选

2026-09-29，主任务预查；不是 F04 正文，也未完成来源登记。正式写作前需选择版本、核对许可范围并逐项复查。

## 已打开的原始资料

- [DCGM Diagnostics 当前模块说明](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/dcgm-diagnostics.html)：区分被动健康遥测与主动诊断；主动测试可消耗计算、内存、互联、电源和散热资源。测试失败还可能涉及主机环境、权限、软件和干扰，不能直接定位为 GPU 硬件故障。该页为 `latest`，只能登记观察日期，不能伪称固定发行版。
- [DCGM 当前功能概览](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/feature-overview.html)：给出后台健康检查、作业前后检查与较长验证的用途；在线诊断仍处于已安装环境中。旧 user-guide 与新 learn 导航同时存在，应避免混用套件列表、参数或支持表。
- [MindX DL 6.0.RC2 ascend-dmi 故障诊断](https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0020.html)：已读约束、前提和参数表。多个诊断/压测项会影响训练推理；AICore 诊断及压测各有后续重启说明。不同检查项的产品、权限和环境支持不同，PRBS 另有 6.0.RC2.1 起的版本条件。不能把它与 E01 的 CANN/TorchNPU 配套档案组成一个已验证环境。

## 仍待获取

补充发现：[DCGM 3.0 路径下的 Feature Overview](https://docs.nvidia.com/datacenter/dcgm/3.0/user-guide/feature-overview.html)可读，但页面标题仍显示 `latest documentation`；不能仅凭 URL 认定全文等于不可变的 3.0 发布快照。后续可用固定仓库源码交叉核对，或如实登记 URL 与观察日期的区别。

1. NVIDIA 固定版本的诊断和健康字段说明；优先固定源码或已验证可访问的归档，记录计数器生命周期、聚合窗口及 unsupported/blank 的语义。
2. NPU health 查询的精确工具版本、型号、字段解释，区别状态摘要、错误码、采样失败与未覆盖项。搜索片段中的五种健康状态尚未作为正文证据。
3. 独立的真实型号/软件支持表与许可页。不能用仓库代码 LICENSE 自动覆盖厂商网站文档。
4. F04 仅说明如何解读证据；主动压测的执行设计需要单独记录对象、隔离条件、停止条件和恢复验证。

## 获取限制

对猜测的 DCGM 3.3 `user-guide/feature-overview.html` 和当前 `learn/modules/health.html` URL 的读取失败；这不表示相应版本或健康监控能力不存在。后续应从实际页面链接发现地址，不把失败地址登记为已核验来源。
