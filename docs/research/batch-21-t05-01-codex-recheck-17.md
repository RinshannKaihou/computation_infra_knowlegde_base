# Batch 21 补交 T05-01 第十七次定向复核

## 1. 结论、角色与范围

- 日期：2026-10-14（Asia/Shanghai）。执行者：当前 Codex 会话，以独立审阅角色核对作者第十七轮修订，与作者修订角色分开；未修改作者材料，未派发其他模型或子代理。
- `gpt-6.1-sol / xhigh` **仅为用户约定**，不是本会话已独立确认的执行元数据。未取得可独立核验的实际模型、推理档位或路由信息，不宣称实际模型一致性或无 fallback 已获独立确认。
- 唯一复核范围为 **B21-C32–C34**；剩余关闭条件以[第十六次复核](batch-21-t05-01-codex-recheck-16.md) L84、L105、L120 为权威。[初审报告](batch-21-t05-01-codex-review.md)仅用于原 ID、优先级和职责核对。C30/C31 保持此前 CLOSED、范围外，不重审。
- **0 CLOSED / 3 OPEN（1 P1、2 P2）；第十七次定向复核不通过。** `constants.go` 的别名首跳属实，但作者所称的 vendored 包归属不是固定源码中的模块连接：同提交 `go.mod` 指向兄弟目录 `../ascend-common`，该目录 `api/default_name.go` 已有环境键字符串定义。审阅者已读到定义，不再将其表述为一次源无法定位；作者正文/记录/登记尚未交付这一完整链及所选条件对应。
- 没有新增发现 ID。上述别名链归属错误及已读/未读口径继续归入 **C33**；C32 的方法缺口和 C34 的设计缺口仍按原 ID 记录。
- 未安装组件、拉取或构建镜像、运行容器、生成 SBOM、采集设备、接入集群、修改运行配置或执行访问/负向/恢复实测。知识库结构检查与目录构建不构成容器或硬件验证。

| 原 ID | 原优先级 | 本轮状态 | 主要位置与剩余问题 |
|---|---|---|---|
| B21-C32 | P2 | OPEN | 正文 L71、L77、L81–83、L108–113、L117、L130–137：所选扫描归层及逐 ordinal 稳定映射方法未交付，缺方法/缺采样尚未统一记录 |
| B21-C33 | P2 | OPEN | 正文 L30、L41、L89、L91、L146；作者记录 L12、L17；登记 L5335、L5446：别名首跳已确认，但模块/定义链、完整所选节点/许可/环境表、必要库来源/目标及口径同步未闭合 |
| B21-C34 | P1 | OPEN | 正文 L126、L131–137：完整模式配置对、资源更新接口/字段、受控成功访问和负向恢复的逐变体关联仍缺，并依赖 C32 未交付方法 |

## 2. 输入身份与写入边界

用户提供的 **4 个 SHA-256 前缀全部吻合**。以下为本轮读取的完整摘要；仓库位置使用输入原文件行号。

| 输入 | SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md)，146 行 | `81671c99377212951413cd37c89708e5fbf82a1e035ae7204b751ae18b84cb7e` |
| [作者来源记录](batch-21-t05-01-sources.md)，28 行 | `cd3d9b30f499345d140b3e6335b9e8ec7068103275ccbe6afe9f0545fa2f51c2` |
| [修订映射](batch-21-review-fixes.md)，262 行 | `05d6ca11f84e6f675e7cc6fbea0f4909917d9e04494abe2d5f47fe46883f2de4` |
| [第十六次复核](batch-21-t05-01-codex-recheck-16.md) | `de42ff0fc79fa0385d48fd7ed4ea52e0135480e25368c3218d0dd43012b1ac82` |
| [初审报告](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` |
| [任务计划](../../plans/full-coverage-backlog.yaml)，T05-01 acceptance L5403–5406 | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml)，439 项 | `c6006d3f9fd8ff1a32ac8749721c7e781f1be0bda3f7885348adbedb7c87bd77` |

仅采用修订映射的 **T05-01 第十七轮节 L259–262** 作为作者落盘改动索引，不把自述作为通过证据。本轮正文摘要与第十六次复核输入表 L24 **完全相同**；正文没有新的落盘字节变化。作者记录及 common 登记虽有变化，仍需按实际支持范围判断，不能据映射中的“分类同步”认定正文已同步。

已读取 README、编写指南、内容总目录和 metadata schema。正文主归属仍为 05.1/05.5，状态仍为 `draft / source_checked`；不修改编辑、验证或任务状态。起始工作区已有修改和未跟踪文件，均保留、不回滚。原仓库唯一写入目标为本报告；结构构建副本位于 `/private/tmp/b21-t05-01-recheck-17.xO0WXC/validation/`，不作为知识内容或永久来源附件。

## 3. 一次源文字抽查与方法限制

### 3.1 curl 实际请求

本机 curl **8.7.1**，对下表 01–11 各执行一次只读 GET。源码请求使用相同仓库/ref/路径的 `raw.githubusercontent.com` 地址；文档使用表列固定版本 URL。调用形态为：

```bash
curl --disable --location --silent --show-error --connect-timeout 8 --max-time 20 \
  --write-out '\nHTTP=%{http_code}\n' "$url"
```

保留默认 TLS 校验，未使用 `-k`，未改 DNS/证书、提权或绕过沙箱。**11/11 退出码 6、HTTP `000`，均为 `Could not resolve host`。** 未取得 curl 响应正文，TLS 握手未发生；不声称 curl 成功、HTTP 200 或本机完成证书验证。请求 URL、错误和退出码已在本会话工具记录输出；登记 L5330 的历史“curl 200”不是本轮结果。

### 3.2 允许的只读替代通道与实际文字

使用 `web.run` 读取版本化厂商/PyTorch 页面和 syft README 的支持段落；使用 GitHub 只读连接器读取固定 ref 源码及目录/模块连接，核对文字和控制流，**不是仅判断可达性**。网页通道可能使用缓存或归一化文本，不等于本机即时 GET；版本 URL 不自动构成不可变快照。以下源码行号来自连接器按原文件区间读取，网页以章节定位，不将网页阅读器坐标拼成 GitHub 行号。所有 Ascend 源码点均使用 commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e`。

| curl 点 | 实际读取的一次源 / 位置 | 核对文字及有限支持范围 |
|---|---|---|
| 01 | [device-plugin/common/constants.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/constants.go#L85)，L85–100；import L18–23 | 三个本地常量分别引用 `api.AscendVisibleDevicesEnv`、`api.AscendRuntimeOptionsEnv`、`api.AscendAllowLinkEnv`。确认别名首跳，不由 import 名推定 vendored 目录。 |
| 02 | [device-plugin/common/common.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go#L90)，L90–130 | 有效响应下写 ID 逗号串/options；allow-link 仅 310B；worker 组仅 `!PresetVDevice`。这些条件不能由 `UseAscendDocker=true` 单独替代。 |
| 03 | [hook/process/process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/hook/process/process.go)，L18–文件末分段读取 | 核对 env 别名/configDir、stdin state/bundle/rootfs、mount group、每份 `.list` 的 128 扫描行限制、UB 候选、options/allow-link、CLI 路径/参数和 `syscall.Exec`。是候选与调用构造证据，不是 CLI 库目标/实际挂载成功证据。 |
| 04 | [runtime/process/process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go)，L60–130、L243–291、L330–405、L455–810、L850–910 | 核对库搜索 env、VIRTUAL 提前返回/独立设备选择、节点与 `rwm`、manager/产品/UB、设备非空分支及独立 env/DP-mount 处理。 |
| 05 | [Toolkit 1.20.0 CDI support](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html)，Running a Workload / Non-CDI-Enabled Runtimes / Setting the CDI Mode Explicitly | 区分原生 CDI、NVIDIA runtime CDI 模式与独立 Runtime Hook；CDI 模式可使用 `NVIDIA_VISIBLE_DEVICES`，变量存在本身不能证明 legacy。 |
| 06 | [Toolkit 1.20.0 troubleshooting](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html)，NVML / Containers losing access / Affected Environments / Mitigations | 核对权限与 SELinux 分离、hook/legacy 访问丢失、显式 CPU/内存更新、重建及 CDI 条件；不能替本文选定更新接口/字段或证明恢复结果。 |
| 07 | [NVIDIA server.go@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go#L305)，L280–481 | 请求校验→ID 转换去重→qualified 名/`CdiDevices`；CDI 与非 CDI 策略可以并选；全 CDI 时提前返回，非全 CDI 时按条件另添 env/volume/DeviceSpecs。 |
| 08 | [syft README@v1.54.1](https://github.com/anchore/syft/blob/v1.54.1/README.md)，Features / The basics | 支持镜像/文件系统等扫描及输出格式入口；该 README 不能替正文选择扫描范围、必要字段与逐库归层规则。不重开 C30。 |
| 09 | [PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html)，Device-agnostic code 的 `CUDA_VISIBLE_DEVICES` 段 | 支持管理 PyTorch 可见集；该段没有交付本文逐 ordinal→分配/注入对象→完整节点→稳定身份的连接规则，不据此否定其他身份接口。 |
| 10 | [ascend-common/api/default_name.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/api/default_name.go#L143)，L143–176 | 同提交直接定义 `ASCEND_VISIBLE_DEVICES`、`ASCEND_RUNTIME_OPTIONS`、`ASCEND_RUNTIME_MOUNTS`、`ASCEND_ALLOW_LINK` 和 `/etc/ascend-docker-runtime.d`，不是字符串无法定位。 |
| 11 | [device-plugin/go.mod](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/go.mod#L112)，L1–112，尤其 replace | `replace ascend-common => ../ascend-common`；模块连接落到同仓库兄弟目录，不是本次所称的 device-plugin 内 vendored 包。 |

另读同提交 [hook/main.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/hook/main.go) 的 `main()`、[runtime/go.mod](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/go.mod) 的 require/replace、[plugin.go L1087–1174](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go#L1087)、[api/consts.go L6–26](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/api/consts.go#L6)。runtime 模块也 replace 至 `../ascend-common`；worker 环境组的字符串定义亦可在该 api 包读取。hook 入口在日志/参数检查后调用 `DoPrestartHook`；插件 A/B 仍互斥，不能拼其原生 `rw` 与 wrapper `rwm`。

按作者 vendored 说法尝试的 `component/ascend-device-plugin/vendor/ascend-common/api` 固定 ref 目录请求返回 404。**本报告不以该 404 推断符号或固定源码不存在**；归属及定义判断基于随后的正向目录记录、go.mod replace 和 `default_name.go` 原文。

未审计完整 dcmi、全部 cataloger/白名单、CLI 库挂载目标实现，也未取得执行或现场配置。正文/记录的未交付方法不能由审阅者读到源码后自动视为作者已经交付。

## 4. 逐项定向判定

### B21-C32 — P2 / OPEN

**权威条件：** 第十六次复核 L84。**位置证据：** 正文 L71、L77、L81–83、L108–113、L117、L130–137；第十七轮映射 L262。

**认可/保留：** 已有 Allocate/CDI/edits/最终 OCI 连接、节点与许可/LSM 分离、不以数量或编号文本证明同一设备的边界继续认可。L111 对“缺方法/缺采样”的区分及 L117 的缺规则优先门槛保留；不重开 C30/C31。

**仍未满足：**

1. **所选扫描归层方法未交付。** L71 仍为“所选扫描配置”“字段以实际输出为准”“缺项逐项记 unknown”；没有确定扫描范围、必要字段、成分/路径到镜像来源层的解析规则，以及镜像库与宿主注入来源、最终挂载、容器目标路径各段连接键。层清单/diff_ids/annotations 和抽查 08 的工具入口不等于逐库归属方法。
2. **逐 ordinal 稳定映射未交付。** L77 明写“未交付，unknown”，L81–83 是空表。抽查 09 的可见集管理段不能补成框架 ordinal/可见集快照→分配 ID/CDI 名或传递字段→完整节点（类型、major/minor、路径/来源）→稳定身份的来源支持方法。
3. **缺失分类尚未全量同步。** L108 仍“未记录即缺失”，L109 “无法确定写 unknown”，L110 “同上”；L113 用“按已取证映射对应”，而实际方法尚未交付。L130–137 的依赖比较也没有统一引用已交付规则及缺方法/缺采样原因、缺项与记录格式。映射 L262 的“分类同步”不能改变这些正文事实。

**剩余关闭条件：** 在固定来源上交付所选扫描范围、必要字段和逐库归层/宿主注入来源→最终挂载→目标路径连接规则；交付逐 ordinal 完整稳定映射规则。将缺方法/缺采样的原因、缺项和记录格式同步至核对表、清单与 C34 依赖比较/判断。**现场值可 unknown；不要求拉取镜像、生成 SBOM、采集设备、审计全部 cataloger 或实测；不重开 C30。**

### B21-C33 — P2 / OPEN

**权威条件：** 第十六次复核 L105。**位置证据：** 正文 L30、L41、L89、L91、L146；作者记录 L12、L17；第十七轮映射 L261；登记 L5335、L5446、L5451。

**独立确认的完成部分：** 抽查 01/02 确认 `constants.go` 别名首跳及 common 输出条件。抽查 03 和补充 main 入口再次确认 hook 的流程、白名单读取机制与 CLI 参数构造；此子条件已在第十六次复核 L90 获认可，**本轮不重开，也不把重复描述计成整项新关闭**。VIRTUAL 提前返回与独立 vdavinci 选择、非提前返回后的 CreateVDevice/poststop 条件、env 搜索路径不当库挂载等既有修正继续认可。

**本轮别名链追记（仍属 C33，不新增 ID）：**

- `common.go` 写输出键→`pkg/common/constants.go` L90/L92/L94 引 `api.*`→`device-plugin/go.mod` L112 replace 至 `../ascend-common`→同提交 `component/ascend-common/api/default_name.go` L156/L158/L162 给出实际字符串；L160/L176 分别给出 mount 选择键与配置目录。
- 因此实际定义为 `AscendVisibleDevicesEnv`→`ASCEND_VISIBLE_DEVICES`，`AscendRuntimeOptionsEnv`→`ASCEND_RUNTIME_OPTIONS`，`AscendAllowLinkEnv`→`ASCEND_ALLOW_LINK`；hook 另消费 `AscendRuntimeMountsEnv`→`ASCEND_RUNTIME_MOUNTS`，配置目录为 `/etc/ascend-docker-runtime.d`。这些是**只读取证的源码常量**，不是现场环境值或挂载结果。
- 作者记录 L12 和登记 L5335 所称“vendored”归属与该 replace 链不符；“device-plugin 子树内无字符串定义”的局部边界不能替代读取同提交兄弟模块，更不能证明固定 mind-cluster 树无法定位。作者可以记录“当时未读定义”，但不能把它写成依赖归属已确认或一次源缺失。本轮审阅者已经定位并读取，后续应按这一精确链同步；不继续将定义本身列为审阅者 unknown。

**仍未满足：**

1. **完整所选条件对应表仍缺。** L89 虽称“条件固定”，仍只列芯片/产品/VIRTUAL 分支摘要，没有选定产品、输入 ID/options、PresetVDevice、mount group 等必要设计条件，也没有将实际环境键连接到完整节点/许可/环境输出。抽查 04 还显示 manager 受芯片及产品分支影响，UB 受目录及目录项影响；`devType` 非空且非 910A5 时另有尝试添加 `dvpp_cmdlist` 的分支。列出 310B/default 等简称不能代替所选完整节点表；相关 stat、可选失败与现场设备号可保持待采，不虚构结果。
2. **必要库来源/目标与所选白名单仍缺。** 抽查 03 取得的是 `.list` 候选路径及 `--mount-file/--mount-dir/--rootfs` 参数；正文未选定 mount group/必要列表内容并交付库来源→CLI 消费规则→容器目标路径。L89 将实际库来源/目标/白名单未取合列 unknown，未完成只读取证设计条件；不把 `LD_LIBRARY_PATH` 或 hook 调用构造当作库挂载。
3. **白名单及条件参数摘要仍需精确化。** L89、登记 L5446 的“≤128 条”应写成**每份 `.list` 的扫描行数上限**：计数发生在路径/stat/分类之前，不是合并所有列表及 UB 后的 mount 总项数上限。`--options` 仅 parsedOptions 非空才加入；候选构造与 CLI 挂载目标/执行结果分别记录，不把它们合称全流程已验证。
4. **已读/未读/未执行口径尚未同步。** L30/L41 仍概括“白名单未取”；L89 后半仍称环境变量/白名单未取源、api 包未定位；作者记录 L17 仍把白名单/hook 可执行与 dcmi 合列 unknown，L12 又将实际结果放入“未读”栏；正文 L146 的复核范围未清楚纳入 hook 机制和完整定义链。新增记录不能替代正文同步。应区分机制/常量已读、所选具体列表及 CLI 源/目标未读、实际结果未执行或未采。

**剩余关闭条件：** 保留已确认 hook/common/VIRTUAL 条件；纠正 vendored 归属并将 go.mod→兄弟 api 定义→输出/消费实际环境键完整落入正文、作者记录和登记。为所选 `UseAscendDocker=true` 样板确定必要产品、输入 ID/options、PresetVDevice、mount group 等设计条件，交付完整节点/许可/环境对应表，按所选条件覆盖 manager/产品/UB 等实际分支，明确虚拟/poststop 纳入或排除。补必要库来源/目标与所选白名单依据，精确化每列表 128 行及条件参数，统一“机制/定义已读、所选源/目标未读、结果未执行”边界。**现场值、未选原生路径真正消费端及支持交集可 unknown；不要求安装、试运行、完整 dcmi/全部白名单审计或实测。**

### B21-C34 — P1 / OPEN

**权威条件：** 第十六次复核 L120。**位置证据：** 正文 L108–113、L117–124、L126、L130–137、L139–141；第十七轮映射 L262。

**认可/保留：** 策略可多选、CDI 自身 hooks 与独立 legacy 区分、有序完整许可比较、S1/R1、旧新主体/时间窗、镜像/驱动回退与更新/重建拆分、replicas 解释收窄、NPU 独立对照 unknown 及授权/安全边界继续认可。L126 已有公共证据对象格式，不再说完全没有对象，也不要求每行机械复制公共规则。

**仍未满足：**

1. **模式配置对未固定。** L131 基线仍仅“含 cdi-cri”，变体仍“envvar 或 volume-mounts”；未选定两端完整策略集合、runtime 模式/handler 消费组合、传递字段及并行 DeviceSpec/其他路径排除。抽查 07 的 `AnyCDIEnabled`/`AllCDIEnabled` 与非 CDI 分支说明组合策略可另产其他字段；抽查 05 说明选择变量可由 CDI 模式消费。“混合路径→无法确定”是判据，不是受控两端的完整配置选型；现场 handler 名和旧新值仍可待填。
2. **资源更新接口/字段未选定。** L136 明写候选为 CRI 更新对象/OCI `linux.resources.cpu`、“固定字段未取，unknown”。抽查 06 支持 CPU/内存更新场景，不替本文选择接口、完整字段、单位/语义和旧新记录格式。需连接同一更新生命周期前后采样；镜像/驱动回退和重建记录不能替代。
3. **R1 仍缺受控成功访问/原负向边界记录及逐变体绑定。** L126 有 audit/AVC、进程/设备/时间与恢复后配置摘要/主体窗，但未选定成功访问操作和结果记录、单独授权的负向拒绝记录，也未给出它们与每个变体更新/重建前后和恢复后主体、目标节点、时间窗的连接键。L132 等仍主要是拒绝事件/注入集；未见拒绝、配置摘要和可见性不等于成功访问或负向边界已恢复。公共格式可复用，“同上”仍须指向能覆盖各生命周期的绑定规则。
4. **C32 映射依赖未闭合。** 三单物理对应仍依赖未交付的稳定映射规则，缺方法/缺采样也未统一同步。按 C32 同一缺口引用，不另立 ID；不混淆设备映射方法与对照/恢复设计。

**剩余关闭条件：** 固定两端完整设备传递策略集合和 runtime 模式/handler 消费组合、字段及旁路排除，保留 CDI 自身 hooks/独立 legacy 区分。保留已补许可比较字段，选定资源更新接口、完整字段、单位/语义和旧新记录格式。完善 R1 的受控成功访问及原负向边界恢复记录，将主体/目标节点/时间窗按各变体更新或重建生命周期绑定至可定位证据；公共规则可统一引用。统一引用 C32 已交付方法，缺方法时优先无法确定并区分缺采样。保留 NPU 独立对照未知、S1/R1、回退拆分及全部授权/安全边界。**不要求执行试验、取得现场值、扩大生产权限或制造结果。**

## 5. Acceptance 与最终计数

| T05-01 acceptance / 原文件位置 | 本轮判断 | 原 ID |
|---|---|---|
| 镜像身份、构建输入、SBOM/签名、拉取策略 / L5403 | 沿用此前完整通过；范围外，不重审供应链 | C30 CLOSED |
| 固定 runtime/Toolkit/CDI、各层与映射分离 / L5404 | 部分满足，未完整通过：扫描归层、稳定映射及分类同步仍缺 | C31 CLOSED（范围外）；C32 OPEN |
| Ascend 独立实现与目标组合 / L5405 | 部分满足，未完整通过：别名首跳及 hook 已确认，完整定义链落盘、所选条件/必要库源目标仍缺 | C33 OPEN |
| 清单、异常/隔离、对照与源案例 / L5406 | 部分满足，未完整通过：配置对、更新字段、访问/恢复关联及映射依赖未闭合 | C34 OPEN |

四条 acceptance 汇总：**1 沿用既有完整通过 / 3 未完整通过**。本轮范围 **0 CLOSED / 3 OPEN（1 P1、2 P2）**，**第十七次定向复核不通过**，没有新增发现 ID。阻断依据是正文未交付的具体方法、条件对应与证据关联，以及 C33 的模块归属/已读范围未同步；**不是 curl DNS 失败、现场值 unknown、没有实测或未证明整栈兼容**。不变更正文或任务验收状态。

## 6. 结构校验与写入审计

- 写入前原仓库 `PYTHONDONTWRITEBYTECODE=1 make check` **PASS：96 content entries / 439 sources**，仅验证结构和本地文件链接。
- 写入后原仓库 `PYTHONDONTWRITEBYTECODE=1 make check` **PASS：96 content entries / 439 sources**。
- 为遵守单文件边界，在上述临时副本复制既有非忽略源文件、build 链接目标及本报告，用原仓库虚拟环境 Python、禁写字节码执行 `make check` / `make build`，均 **PASS：96 content entries / 439 sources**。仅在副本重新生成 `build/catalog.json` 和 `build/catalog.md`，未改原仓库生成文件；本节补记后同步最终报告并复跑同样检查。
- 摘要审计覆盖 **400 个**起始 Git 所列 tracked/untracked 非忽略文件及两份 build 文件：既有文件摘要不变，唯一新增为本报告，无删除；原 Git 状态去除本报告后与起始状态相同。七个输入保持 §2 摘要。报告仅含 C32/C33/C34 三个原发现标题，优先级/OPEN 状态吻合，行尾空白检查通过。
- 本会话未修改作者正文、作者来源记录、修订映射、来源登记、任务计划或其他既有文件；结构与构建 PASS 不改变 §4 技术状态。
- 原仓库唯一授权写入为本报告；未修改 `src/kb/` 或测试，不需要 `make test`。不执行容器/硬件实测。

**最终技术结论：B21-C32、B21-C33、B21-C34 均 OPEN；0 CLOSED / 3 OPEN，第十七次定向复核不通过。C30/C31 保持此前 CLOSED、范围外；用户约定配置不作为已独立确认的执行元数据。**
