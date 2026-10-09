# 第十三批来源记录：训练 NPU 供电散热观测补齐（T01-02）

研究日期：2026-10-08。研究者：探索子代理（非 gpt-6.1-sol）。目标正文：`knowledge/01-hardware/power-thermal-evidence.md`（reference，revise，验收标准见 plans/full-coverage-backlog.yaml T01-02）。背景：该文 NPU 侧此前只有边缘/推理产品线（Atlas 200I A2/500 A2 智能边缘硬件 24.1.RC1）npu-smi 证据，训练型号受阻（evidence_blocker）。**本批突破：训练产品线版本化 npu-smi 文档定位在 HDK 26.1.x 文档树，不在 Atlas 800T A2 产品树。** 未在任何真实设备执行 npu-smi；除本文件外未改动仓库其他文件。

修订日期：2026-10-09，主执行者按补充审阅 B13-R01 修订正文及本记录，加入同版本 DCMI 路径。上述研究者和“仅改本文件”是首次取证的历史声明。本次仍未查询真实设备；故障定义 xlsx 为编写者取得的证据，独立审阅者未重新取得。

## 获取路径与边界

- 训练线 npu-smi 命令参考落点：`doc_center/source/zh/HDK/2610/A2/A2npu/`（《Atlas A2 npu-smi命令参考》，产品线「Atlas A2 推理和训练系列产品」）；A3 线在 `HDK/2610/A3/A3npu/`。CANN 文档树下无独立 npu-smi 参考。
- `doc_center/source/zh/...` 为静态 HTML 可直接抓取；`document/detail/zh/...` 形态 curl 只得 JS 壳（早期批次受阻原因即只尝试了该形态）。不存在页返回 403 而非 404；`latest` 路径 403，必须带版本号（2610）。
- 训练线未找到 npu-smi PDF；健康管理故障定义为可下载 xlsx（约 264KB，5 sheet，故障描述表 144 行）。

## 主张—证据表（训练机型 = 支持矩阵显式含 Atlas 800T A2 / Atlas 900 A2 PoD）

| 主张 | 来源与定位 | 版本/日期 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| 温度查询 `npu-smi info -t temp -i id [-c chip_id]`：NPU Temperature (C)（°C）；MCU 芯片另有 LM75A_TE/LM75B_TE (C)（进/出风口温度） | [npusmi_0023](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0023.html)、[npusmi_0024](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0024.html) | HDK 26.1.x（URL 2610），2026-10-08 核对 | 训练机型 | 高温门限具体 °C 值文档未给 |
| 功耗查询 `npu-smi info -t power -i id [-c chip_id]`：NPU Real-time Power(W)（W）；不支持指定 MCU 芯片 | [npusmi_0025](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0025.html)、[npusmi_0026](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0026.html) | 同上 | 训练机型 | 无功率上限/封顶类设置命令 |
| 电压查询 `npu-smi info -t volt -i id`：Voltage(V)；训练服务器不支持查 MCU 电压 | [npusmi_0027](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0027.html) | 同上 | 训练机型 | — |
| 频率字段成对：Aicore Freq(MHZ)（输出说明仅称「Aicore频率」）与 Aicore curFreq(MHZ)（「Aicore当前频率」）；同屏含 Aicore Usage Rate(%)、Temperature(C)、NPU Real-time Power(W) | [npusmi_0016](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0016.html) 使用示例与输出说明 | 同上 | 训练机型 | 页面未把 Freq 定义为标称值或降频判定阈值；示例本身为 利用率 0、Freq 1850、curFreq 800——空闲时 curFreq 同样走低，差异不能单独判定节流（B13-C06 修订） |
| 周期监测 `npu-smi info watch [-i id]`：Pwr(W)、Temp(C)、AI Core(%)、AI Cpu(%)、Ctrl Cpu(%)、Memory(%)、Memory BW(%)、NPU Util(%)、AI Cube(%) | [npusmi_0012](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0012.html) | 同上 | 训练机型 | 开 profiling 时 AI Core(%) 返回 0（页内注明） |
| 传感器明细 `npu-smi info -t sensors -i id -c chip_id`：Soc Max/SFP/NDIE/HBM Temperature (C) | [npusmi_0039](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0039.html) | 同上 | 训练机型 | — |
| 内存信息含 HBM Temperature(C)、HBM Clock Speed(MHz)（当前值）、DDR Clock Speed(MHz)；800T A2/200T A2 HBM 64G | [npusmi_0019](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0019.html) | 同上 | 训练机型 | — |
| 健康查询 `npu-smi info -t health`：OK/Warning/Alarm/Critical/UNKNOWN 五态；指定芯片显示 Error Code/Error Information，页面指引查《健康管理故障定义》《黑匣子错误码信息列表》 | [npusmi_0029](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0029.html)、[npusmi_0030](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0030.html) | 同上 | 训练机型 | — |
| 高温事件 0x80E20207「SOC非致命高温异常告警（不含DDR/HBM颗粒）」：LPM 10ms 轮询 SOC Tsensor；自处理含「系统调节AIcore频率进行温控」；迟滞 5°C（降到阈值下 5°C 才恢复/再报）；业务影响「通常业务性能受损」；建议可继续训练或存 ckpt 复位 | [hma2_01.html](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2healthmanagement/hma2_01.html) 附件 xlsx 故障描述表 row 64 | 文档版本 02（2026-08-19；01：2026-07-30） | 训练机型（事件级） | 阈值数值未公开；这是机制描述，不是实时可查询字段 |
| 过流事件 0x80E21007「主电源过流告警」（通知事件）：「SOC ACG（或者POWERBRAKE，以产品分表为准）模块触发快速降频」；瞬态过流无需处理 | 同 xlsx row 65 | 同上 | 训练机型（事件级） | ACG 与 POWERBRAKE 的产品分表未随附 |
| 关联事件：0x80E21008 电源过流控制异常（EDP 降电流手段用完仍失控）、0x80E24E00 LPM 心跳异常（温保/EDP/AVS/PMU 全失效）、0x80E39200 Tsensor 异常、0x80E3A201 调频调压（DVFS）功能异常 | 同 xlsx rows 66–69 | 同上 | 训练机型（事件级） | — |
| 事件获取途径：msnpureport 收集 device-os slog 搜 event_id；`npu-smi info -t health -i id -c chip_id` 最多查最近 8 次 RAS Event ID | 同 xlsx「如何获取EventID」sheet | 同上 | 通用工具 | — |
| 降P启动：仅服务器形态（HCCS 款和 PCIe 款）支持，推理卡/训练卡（标卡）暂不支持；查询方法 1 为 msnpureport 收集 Device 侧日志，方法 2 为 iBMC `ipmcget -d npustatus`；**HCCS 款两种方法均有效，PCIe 款只支持方法 1（方法 2 查询无效）**；设置经 iBMC `ipmcset -d npuisolation -v <id> 1`；降P NPU 支持单 NPU 复位，正常启动的不支持 | [npusmi_0177](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0177.html)、[npusmi_0178](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0178.html)、[npusmi_0099](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0099.html) | HDK 26.1.x | 训练机型（HCCS 款服务器） | 降P是管理性隔离/降额启动，文档未称其为温度/供电异常的自保动作；「iBMC 查不到」不等于「没有降P」（B13-C08 修订） |
| **npu-smi 限定扫描结论**：编写者扫描 npusmi_0002–0181 存在页未找到当前原因位图；该结论只覆盖这组命令页。npusmi_0008 的 `info -h` 含 pwm-mode/pwm-duty-ratio/cpu-freq-up，但无逐类型支持矩阵，各类型命令页矩阵未逐条核对 | 原扫描记录及 [npusmi_0008](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0008.html)（2026-10-08） | HDK 26.1.x | 命令页范围的负面证据 | 不能据此否定平台其他接口；同版本 DCMI 当前原因路径见下一行 |
| DCMI 当前 AI Core 原因：`dcmi_get_device_info`，main `DCMI_MAIN_CMD_LP`、sub `DCMI_LP_SUB_CMD_AICORE_FREQREDUC_CAUSE`，返回 8Byte / 64 位位图，100ms 更新，无历史查询；IDLE bit 0、THERMAL 2、SW_EDP 3、HW_EDP 4、POWER_BREAK 5、SVFD 8、POWERCAPPING 10 | [dcmi_077 约束、表 1–3](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2DCMI/dcmi_077.html)，2026-10-08 独立审阅取得，2026-10-09 主执行者重取 | HDK 26.1.x A2 | 官方接口与支持矩阵 | IDLE 为空闲节能，不等于故障；可多位同时置位，不与 NVIDIA 逐位等价。800T A2/900 A2 PoD 的裸机 root、运行用户组非 root、普通容器 root、AVI 容器 root 均列 Y；VM 等未列场景及现场版本/权限未知，未调用接口 |
| A3 线同构：npusmia3_0023 等同名命令；产品含 Atlas 9000 A3 SuperPoD、Atlas 900 A3 SuperPoD 超节点、Atlas 800T A3 超节点；A3 故障定义 xlsx 02 存在 | [npusmia3_0023](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A3/A3npu/npusmia3_0023.html)、[hma3_01.html](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A3/A3healthmanagement/hma3_01.html) | HDK 26.1.x | 训练机型（A3） | A3 xlsx 未逐行核对 |

## 设施/BMC/设备关联证据（验收要求的最小关联）

- 设备侧：上述 npu-smi 温度/功耗/电压/频率/传感器字段与健康五态；事件侧经 `npu-smi info -t health`（最近 8 个 RAS Event ID）与 msnpureport 的 device-os slog。
- 当前原因侧：DCMI LP 位图查询与同窗口频率、负载分开记录；一次当前查询不能追溯历史原因，也不能用任意置位直接定位设施故障。该能力不自动意味着 MindCluster exporter 已导出对应指标。
- BMC/设施侧：iBMC `ipmcget -d npustatus`（仅 HCCS 款有效，PCIe 款方法 2 无效）、`ipmcset -d npuisolation`（npusmi_0177/0178/0099）；MCU 进/出风口温度 LM75A_TE/LM75B_TE（npusmi_0023）。
- 机制侧：故障定义 xlsx 把高温（0x80E20207）与过流（0x80E21007）分别关联到 AIcore 频率温控与 ACG/POWERBRAKE 快速降频——这是「设施/供电异常 → 设备自保 → 性能退化」链条的官方事件级证据，但阈值与分表数值未公开。
- 边界：以上均为网页/附件证据，未在真实设备执行；不能虚构现场告警时间线，正文的关联表标为「方法+官方事件定义」，不给虚构案例。

## 候选新来源登记

- `src.huawei.hdk-26.1x-a2-npu-smi-2026-10-08`：Atlas A2 npu-smi命令参考（HDK 26.1.x），逐页核对 npusmi_0002–0181 中的存在页；许可 status unknown（华为版权页禁止摘抄复制，仅链接+原创归纳）。
- `src.huawei.hdk-26.1x-a2-dcmi-low-power-2026-10-08`：A2 DCMI LP 当前原因接口；2026-10-08 已补登，2026-10-09 修订正文引用。
- `src.huawei.hdk-26.1x-a2-health-fault-def-02-2026-10-08`：健康管理故障定义 02 xlsx（hma2_01.html 附件）。
- `src.huawei.hdk-26.1x-a3-npu-smi-2026-10-08`：A3 线同构文档（抽查 npusmia3_0023）。
- `src.huawei.hdk-26.1x-a3-health-fault-def-02-2026-10-08`：存在性核对，未逐行解析（如正文不逐条引用可不登记，本轮登记以备后续批次）。

## 残留未知（不补写）

- 高温门限与 ACG/POWERBRAKE 产品分表的具体数值未公开。
- npusmi_0016 未将 Freq 定义为标称值或判定阈值，不能单凭 Freq/curFreq 差异判定故障节流；平台“无当前原因位图”的旧表述已撤回，DCMI 已有文档接口。本地支持组合、未列部署场景及 exporter 与 DCMI 的对应关系仍未知。
- HDK 26.1.x 之前版本（25.x/24.x）的训练线对应文档未追溯。
- A3 故障定义 xlsx 未逐行核对；A3 超节点（800T A3）的整机供电散热规格未取证。
- 边缘线 24.1.RC1 文档（已登记 src.huawei.npu-smi-atlas-a2-edge-24.1.rc1-pdf）与 HDK 26.1.x 训练线文档的字段差异未逐条比对；边缘证据仍不可外推训练型号。
