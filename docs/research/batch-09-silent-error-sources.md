# 第九批来源记录：静默错误与计算完整性（R2-06）

研究日期：2026-09-30。目标正文：`knowledge/08-reliability/silent-errors-and-integrity.md`（concept）。主任务对 OCP 白皮书未做独立抽查（PDF 提取），正文引用保持节级粗定位并注明读取范围；arXiv/PyTorch 证据由研究子代理按页核对。

## 主张—证据表

### Silent Data Corruptions at Scale（arXiv:2102.11245v1，Facebook/Meta）

| 主张 | 证据位置 | 类型 | 反证/未知 |
|---|---|---|---|
| SDC 定义：计算结果错误但无任何系统事件/错误日志指示（"2x3 得 5" 示例）；错误沿栈向上传播为应用层问题 | 摘要；§1（ar5iv HTML，节号定位；无印刷页码） | 一手（fleet 运营方） | 定义针对数据中心 CPU |
| 日志/健康检查覆盖不到：肇事机器系统事件日志、内核日志全部干净 | §5 开头；§6 | 一手实证（单案例） | 单案例，作者声明代表数百颗 CPU 之一 |
| fleet 级：数十万机器上检出数百颗 CPU，跨多代平台，监测超 18 个月；CPU SDC 比软错误 FIT 仿真高 orders of magnitude；可复现、非瞬态、数据依赖（Core 59 上 Int(1.1^53)=0 可复现） | 摘要；§1；§5；§3.4 | 一手实证 | 未给具体发生率/FIT 数值；"applicable to special function accelerators" 是外推非实测 |
| 温度/电压/频率依赖：v1 未给实测数据，仅在 §6.1 列为待研究方向 | §6.1 | 研究方向声明 | 不能引 v1 支持"随温度/频率变化" |
| 检测：目标化 reproducer（60 行汇编，从 43 万行 JIT 缩减）；fleet 三类检测 Opportunistic/Periodic/Production-friendly；容错：冗余+多检查点校验（成本随冗余度增长）、容错库（点名 PyTorch）。**§7 Detection Mechanisms 明确用特定计算与已知参考值比较来发现 SDC——主动结果校验可以检出部分 SDC，不能按"静默"定义宣称主动测试一概无效**（Codex 代审 B09-C02 修订点） | §5、§5.3；§7.1–7.3；§8.1–8.2 | 一手方法描述 | §1 明确不含性能-成本权衡细节 |
| ECC 局限：主要护 SRAM，CPU 内并非所有数据通路有同等保护 | §1、§2 | 一手陈述 | 未量化覆盖率 |
| 范围限制：单案例研究、无故障注入、不含代价权衡、CPU 为主 | §1 | 作者自述 | — |
| 版本：abs 页 Submission history 仅 [v1] 2021-02-22，无 v2+；检测量化数据的后续论文是 arXiv:2203.08989（未读，不登记不引用） | abs 页 | 版本核对 | — |

### SuperBench（USENIX ATC 2024，印刷页 835–850；已读 835–844，PDF 文件页=印刷页−834）

| 主张 | 证据位置（印刷页） | 类型 | 反证/未知 |
|---|---|---|---|
| 灰色退化定义：硬件冗余引入 hidden degradation / fail-slow，渐进性能退化而非二元状态 | 摘要；§1（p.835） | 一手（Azure 生产观察） | 性能域概念，不是计算错误 |
| 冗余掩盖实证：24 节点、192 张 InfiniBand NIC 的特定测试床中，ToR 配置 25% 冗余上行；部分 ToR 超过一半的冗余链路失效时，多组双节点对同时通信的 all-reduce 带宽显著下降（图 3；不是全部上行链路的半数或通用阈值）；HBM 行重映射 >10 次的 GPU 端到端回归概率高 77.8%（表 1）；节点事故间隔从 719.4h 降至 151.7h（图 4） | §2.2（p.837–838） | 一手实证 | Azure 特定集群；77.8% 为相对风险 |
| 验证分类：组件级 micro-benchmarks + pattern-wise + 端到端 benchmarks；单节点→多节点两阶段 | §3.2（p.840–841）、表 2（p.843） | 系统设计 | — |
| 代价—覆盖率：Comprehensive/Clear-cut/Cost-efficient；贪心子集选择；覆盖率 C 为历史检出缺陷节点占比 | §1（p.836）；§2.3（p.839）；§3.3（p.841–842） | 方法+成本数据 | 成本数字为 2024 年 Azure 挂牌价 |
| MTBI 提升最高 22.61× 来自 1k 节点 4 个月事故 trace 的仿真，非 A/B 生产对照 | 摘要；§5.2 Benchmark Selection Evaluation（仿真） | 仿真 | 不写成生产实测 |
| 某些 A100 回归仅在计算与通信并发时出现（L2 cache 干扰），单独 GEMM 或 NCCL 测试测不出 | §2.1（p.837） | 一手案例 | 性能回归非数值错误 |

### OCP 白皮书 Silent Data Corruption in AI（2025-08-27，CC BY-SA 4.0；已读 p.1–19/29）

| 主张 | 证据位置（印刷页） | 类型 | 反证/未知 |
|---|---|---|---|
| 故障结局分类 benign / fault corrected / DUE（detected unrecoverable error）/ SDC 四类（图 1；DUE 展开随来源原文，不写 uncorrectable） | p.8 | 多厂商白皮书 | Codex 代审 B09 修订点：早期记录误写三类且 DUE 展开不一致 |
| 小延迟缺陷随电压骤降/温度/开关活动间歇激活；AI 加速器激进 DVFS 缩小裕量 | §3.2.1（p.9） | 一手综述 | — |
| Meta 案例：同一计算检查运行六个月后才失败，指向磨损 | §5.0（p.15） | 一手运营事实 | — |
| fleet 检测：Fleetscanner 周期筛查（45–60 天覆盖、分钟级）+ 与负载共置的毫秒–秒级测试（数天覆盖全 fleet）；两者 70% 重叠覆盖；分析法（按核心统计应用异常）比测试法多检出 41% | §5.1（p.15–16） | 一手运营事实 | 41% 为特定 fleet 观察 |
| 训练侧两种发散模式：NaN 传播与梯度方差污染 | §5.1.1（p.16–17） | 一手 | — |
| Google Gemini：该规模下 SDC 每 1–2 周影响一次训练；定位手段=确定性重放+空闲机主动 SDC 扫描+热备 | §5.1.4.1（p.19） | 一手运营事实 | 规模相关频率，不作通用发生率 |
| 检测分类法：空间/时间/信息冗余、端到端完整性校验、复制+一致性检查、整数剩余校验、ABFT | §5.2/§5.3（目录 p.4–5；正文未读） | 目录级 | p.19 之后未读，细节不引用 |

### PyTorch 2.6 文档（区分 SDC 与正常数值噪声的背景）

| 主张 | 证据位置 | 类型 | 反证/未知 |
|---|---|---|---|
| 浮点加法/乘法不满足结合律；不保证数学等价计算逐位相同，不保证跨 release/commit/平台一致；CPU 与 GPU 同输入同种子结果仍可能不同 | numerical_accuracy.html 开篇 | 官方声明 | 跨平台比对必须带容差 |
| batched 与逐元素、整张量与切片不保证逐位一致；linalg 对病态输入可能静默返回错误结果（软件/算法层，非硬件 SDC）；TF32/FP16/BF16 降精度累加等开关改变数值结果 | #batched-computations-or-slice-computations；#extremal-values-in-linalg；#tensorfloat-32-tf32-on-nvidia-ampere-and-later-devices 等 | 官方声明 | 比对前须固定这些开关 |
| 完全可复现不保证（跨 release/commit/平台，即使同 seed） | randomness.html 开篇 | 官方声明 | — |
| 确定性控制：manual_seed、cudnn.benchmark=False、use_deterministic_algorithms(True)、CUBLAS_WORKSPACE_CONFIG（CUDA≥10.2）等；确定性≠跨平台一致，且常更慢 | randomness.html 各小节 | 官方声明 | — |
| assert_close：|actual−expected| ≤ atol + rtol·|expected|；rtol/atol 成对；省略按 dtype 默认（float32: 1.3e-6/1e-5；float16: 1e-3/1e-5；bfloat16: 1.6e-2/1e-5；float64: 1e-7/1e-7）；非有限值仅相等才 close；NaN 仅 equal_nan=True 互等；默认检查 device/dtype/layout | testing.html #torch.testing.assert_close（generated 页在 2.6 为 404） | 官方 API 文档 | 默认容差是经验值非硬件保证 |

## 未解决与抓取失败

- pytorch testing.html 的 generated 单页 404，文档位于 testing.html。
- SuperBench 印刷页 845–850 未读；OCP 白皮书 p.19 之后（§5.2 细节、§6、§7）未读。
- arXiv HTML 锚点 ID（#S7 等）按惯例推断，未逐一验证；正文引用保持节级。
- arXiv:2203.08989、2502.12340、2608.30769 仅确认存在性，未读全文，不登记不引用。
- 网络二手转述（Meta 每月 25 亿次硬件测试等）未找到一手出处，不可引用。
