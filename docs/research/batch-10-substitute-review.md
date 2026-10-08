# 第十批复查记录（替代性复查，非 astra/xhigh）

**历史记录提示（2026-10-08）：** 本文保留当时实际执行与关闭结论。当前 `gpt-6.1-sol / xhigh` 的[新审阅](batch-10-codex-review.md)及[修订/定向复核](batch-10-11-12-codex-recheck.md)已完成，2 项 P2 全部关闭，本批在原审阅范围内通过；以新报告和[汇总](batch-10-11-12-codex-review-summary.md)为当前状态。

复查日期：2026-09-30。**限制声明同前：用户约定每轮由 gpt-6-astra / xhigh 独立审阅；当前环境没有该模型派发能力，本轮未能完成约定模型的独立审阅。** 本记录是同环境只读子代理的定向复查，审阅独立性不等同于跨模型外部审阅。

## 范围与实际核查

完整复读三篇新增正文（slow-rank-triage、power-thermal-evidence、checkpoint-slow-io-triage）与三份来源记录；实际打开 14 处固定 commit 源码锚点（PyTorch v2.8.0/v2.6.0、DCGM v3.3.9、kernel v6.16、MindCluster v26.1.1、MLPerf v2.0）与 17 个外部页面/PDF（NCCL RAS、PyTorch 文档、DCGM 系列页、nvidia-smi、DGX 指南、Atlas 产品页、SuperBench PDF）。复查者另运行 `make check`（PASS，63/76）。

## 发现与关闭

| 发现 | 级别 | 状态 | 关闭依据 |
|---|---|---|---|
| 供电文把「测试通过不排除窗口外环境问题」写成页面原文 | P2 | 关闭 | 改为显式标注「这是本库的推论，不是页面原文」 |
| README 计数滞后（60/71，实际 63/76） | P2 | 关闭 | README 已更新为 63 content entries / 76 sources |
| 位图表 CLOCKS_SETTING 的「同上」注释归属错误（移除说明只在 GPU_IDLE 与 HW_SLOWDOWN） | P2 | 关闭 | 该行改为头文件原意「时钟受应用时钟设置限制」，研究记录同步 |
| DISPLAY_CLOCKS「仅部分型号」超出所引头文件 | P3 | 关闭 | 改为引用 nvidia-smi 文档的「仅 Volta 设备支持」 |
| checkpoint 文引文与源码拼写不一致（degredation 为上游原文） | P3 | 关闭 | 保留原文拼写并注明「原文拼写如此」，研究记录同步 |
| npu-exporter「help 字符串不含单位」过度概括（aicore_current_freq 有 MHz、process_info 有 MB） | P3 | 关闭 | 收窄为温度/功耗/电压无单位口径，研究记录同步 |
| desync 三类报告误挂文档页（三类文本仅在 TraceUtils.h） | P3 | 关闭 | 类别描述改挂固定源码，文档页只引其用途说明 |
| desync 与 ASYNC_ERROR_HANDLING 的强制方向含糊（实为强制把 async error handling 改回开启） | P3 | 关闭 | 正文与研究记录写明方向 |
| 昇腾平台路径未收本批 NPU 相关正文 | P3 | 关闭 | ascend.md 增加供电散热与 checkpoint 慢写入口及相关 related_ids |

## 已排除的疑点（核对为正确）

- PyTorch v2.8.0 的 desync 触发与字段、heartbeat 默认 480s、WAIT_TIMEOUT_DUMP_MILSEC 默认 15000ms、`TORCH_NCCL_HEARTBEAT_MONITOR` 全文零命中；flight recorder 时间戳为 CPU 侧发现时刻。
- PyTorch v2.6.0 的主线程 staging、后台单线程、CPU 后端 assert、两次集合点、sync_files 默认与 L466 一致性提醒、FileSystemReader 串行。
- DCGM v3.3.9 的位图/字段/violation（usec）与 watch 判定（一分钟增量、30s）；Healthy 官方限定逐字一致；DGX/Atlas 规格吻合；MLPerf 清缓存与强制 fsync 吻合；MindIO flush 语义吻合。
- kernel vm.rst 的写者节流原文逐字在案；SuperBench 35× 为缺陷链路数量的表述正确；教程页 2.9 内容未被当作 2.6 功能引用。
- 元数据、导航、YAML、版本边界（2.6/2.8 未混用、动态页带观察日期、NPU 缺口如实标注）均通过。

## 未覆盖

- 未复核存量 60 篇内容；RAS 判读阈值、flight recorder 默认值冲突、NPU 慢 rank 观测、MindIO memfs 实现、网络存储传输等原文标注的缺口保持开放；未执行任何环境验证。
