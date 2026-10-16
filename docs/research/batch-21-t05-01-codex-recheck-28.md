# Batch 21 补交 T05-01 第二十八次定向复核

## 1. 结论、角色与范围

- 日期：2026-10-16（Asia/Shanghai）。执行者：当前本地 Codex CLI 会话，以独立审阅角色核对作者第二十八轮修订，与正文作者角色分开；未派发子代理或其他模型。
- 模型核验：读取当前会话 `01a142dc-ed0c-75b3-a17a-0e741cfbf674` 的本地执行记录。`turn_context`（`2026-10-16T03:59:13.967Z`）报告 `model=gpt-6.1-sol`、`effort=xhigh`，`collaboration_mode.settings` 的模型与档位同样为 `gpt-6.1-sol / xhigh`；本轮所见执行元数据为单一约定模型，已输出的审阅者消息未检出 fallback 标记。核验依据是本地 CLI 提供的执行元数据，不冒充独立服务端路由证明，也不追改历史报告的模型记录。核验摘录保存在仓库外审计目录。
- 唯一复核范围为 **B21-C32、B21-C33、B21-C34**。权威关闭条件分别为[第二十六次复核](batch-21-t05-01-codex-recheck-26.md) L91、L106、L121；具体子项编号沿用[第二十七次复核](batch-21-t05-01-codex-recheck-27.md) §4 的各项顺序。**C30/C31 已 CLOSED，范围外，不重审。** [初审](batch-21-t05-01-codex-review.md)仅用于继承原发现 ID、优先级和职责边界。
- **0 CLOSED / 3 OPEN（1 P1、2 P2）；第二十八次定向复核不通过。** 本轮认可 worker 七项的条件与生成算法已补；不再将其描述为只有组数/函数名。其余扫描与稳定映射方法、公共分类、完整 Ascend 记录关联、旧挂载判据与宽口径清理、无矛盾的两端消费配置、资源更新设计仍未闭合。R1 公共阶段连接规则继续沿用前轮认可，不重新索取。
- 只新增本报告，不修改、删除其他仓库文件，不提交 Git、不创建分支。修订映射和作者验收准备材料仅作位置索引，不沿用其关闭判断；本轮不新增发现 ID。
- **未执行实测，不构成硬件验证。** 未安装、拉取/构建镜像、生成 SBOM、运行容器、查询设备、接入集群、执行上游脚本或进行访问、负向、资源更新、回退、恢复测试；来源读取和结构校验均不建立目标环境兼容性或硬件结论。

| 原发现 | 优先级 | 本轮状态 | 核心位置与剩余项 |
|---|---|---|---|
| B21-C32 | P2 | OPEN | 正文 L60、L72、L78、L82–84、L109–114、L118、L131–138：扫描/逐库连接、稳定映射方法及共同缺项分类仍缺 |
| B21-C33 | P2 | OPEN | 正文 L90、L92；作者来源记录 L12、L17：worker 生成规则认可；完整对象记录、旧挂载判据、逐库取证关联与宽口径仍未闭合 |
| B21-C34 | P1 | OPEN | 正文 L127、L132、L137：R1 保留认可；两端设计矛盾未清，资源更新接口/字段仍未选，另依赖 C32 |

优先级口径不变：P1 为核心验收主干缺失、阻断通过；P2 为必须补齐的证据、机制或版本边界，不是对生产漏洞或事故严重性的评级。

## 2. 输入身份与定位

SHA-256 对完整文件原始字节独立计算。开始读取与写报告前的七份指定输入摘要一致；仓库物理行号均对应下列快照，正文 L90、L132 等长行另以精确短语定位。来源登记的结构校验计数为 **444 项**，不套用前轮的 440 项计数。

| 输入 | 本轮 SHA-256 | 审阅定位 |
|---|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md) | `57cfdff61222fd4980a71ae40741d85baddbd12048e9d8acc678f7798420c69f` | L60、L72、L78、L90、L98–142；保持 `reference / draft / source_checked` |
| [修订映射](batch-21-review-fixes.md) | `8c996021a27ce9f717f4cd26f358010def6e222d5454186ee2302e25d5f53d8c` | “T05-01 第二十八轮修订”L324–327，仅列 worker/默认设备与分类同步改动 |
| [第二十六次复核](batch-21-t05-01-codex-recheck-26.md) | `ade616897c367afb566c3076ffc8b36f2dbf6c95af8558d74af8d537ed3402b0` | 权威关闭条件 L91、L106、L121 |
| [初审报告](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` | 原 C32–C34 的职责、优先级和验收边界 |
| [任务计划](../../plans/full-coverage-backlog.yaml) | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` | T05-01 L5386–5430；acceptance L5403–5406 |
| [来源登记](../../sources/registry.yaml) | `b9cdbedf73379dd24d704e0363e1fcbcc550f3c8f9581b93659a32a1e39a6b0f` | 相关 GPU/Ascend/containerd/Syft/PyTorch 登记；Ascend 边界 L5424、L5446、L5457、L5462 |
| [作者来源记录](batch-21-t05-01-sources.md) | `3719c44a87798ef001541fa241877decc3f0817483cea3408c2f609a8d888235` | L12 已读范围与三分口径；L17 旧 unknown 总项 |
| 补充：[第二十七次复核](batch-21-t05-01-codex-recheck-27.md) | `ffca98e72193c673d2231404a45cb9297e234916777ecaf22156bb7ec9ad77b8` | §4 编号、worker 待补项、R1 已认可项 |
| 补充：[作者验收准备](batch-21-t05-01-acceptance-gap-check.md) | `a23cacedc78fef53a9198020f933a15b14ad3055377f0854557b6b1faa12355a` | 仅作正文位置索引，不作为关闭证据 |

另从 `README.md`、`docs/authoring-guide.md` 开始读取规则，并核对 `content-outline.md` 的归属边界、元数据 schema 和适用目录指令；不把这些材料或前轮摘录当作上游实现证据。

## 3. 一次源取证与方法限制

### 3.1 实际通道与限制

本轮直接使用用户允许的 **GitHub 原文件只读连接器 `fetch_file`** 和 **Web 阅读工具 `open` / `find`**，不是只检查 URL 可达性，也不是只读搜索摘要。GitHub 读取均显式传入下表的固定 ref/path；默认分支代码搜索只用于定位路径，相关常量和函数随后重新读取了指定 commit，不将搜索结果中的其他 commit 混作证据。失败的网页原文件请求返回 `Cache miss`，不作为文件不存在或实现缺失的证明；成功取证位置以下表为准。

**本轮没有运行本机 curl**，不借用前轮的 curl 退出码、HTTP 状态或 DNS 错误充作本轮测量，也不宣称已用 curl 取回原始正文或完成本机 TLS 校验。这里是按授权使用的替代读取通道；**curl DNS 失败不判技术不通过**。网页通道可能使用缓存/文本提取：Toolkit CDI 页标示两日前抓取，排障页五日前，PyTorch/Syft 页当日；这些标记不是本机实时下载保证。

GitHub 返回的 Git blob SHA 是文件身份，不是本机 HTTP 下载的 SHA-256；对 tag 来源只记录本轮指定 ref 返回的文件身份，不额外宣称独立完成 tag 对象解引用。源码行号以连接器请求的原文件范围为准；网页阅读器行号不充作 GitHub 源码行锚。未执行取回的脚本/命令，不以取证成功推导配套支持交集、实际注入或恢复成功。

### 3.2 一次源实读表

下列编号仅为本报告的抽查点，不是新增发现或登记 ID。Ascend 文件统一固定 commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e`；没有换用最新分支代替。

| 抽查点 | 精确来源 / 本轮实读位置 | 已核对的文字与有限支持范围 |
|---|---|---|
| 01 | [device-plugin common.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go)，L85–170、L171–350 | `SetAscendRuntimeEnv` 的 ID 拼接/options/310B allow-link、七个 worker 键及 `localRankStr`；`GetDefaultDevices` 的存在性/产品条件。worker 算法可核对，不等于现场环境输出已采集 |
| 02 | [api/consts.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/api/consts.go)，L1–210 的 Env 段；[api/default_name.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/api/default_name.go)，L140–240 的 docker-runtime 段 | 前者定义七个 worker 环境键的字符串，后者定义 ASCEND 控制键和配置目录；不能把两类常量的定义位置混成同一段 |
| 03 | [device-plugin plugin.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go)，L1080–1175 | 原生路径直接返回 `DeviceSpec` / `rw`；`UseAscendDocker=true` 调环境辅助函数。新增默认设备索引不把未选路径 A 变成路径 B 的下一跳 |
| 04 | [runtime/process/process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go)，L206–430、L485–840 | `LD_LIBRARY_PATH` 仅改 env；VIRTUAL 与条件化 poststop 分开；14 辅助项警告继续、manager 回退/目标重命名；UB 目录跳过子目录；作业/UB/manager 错误返回和 `rwm` 节点许可链 |
| 05 | [hook/process/process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/hook/process/process.go)，L1–70、L85–225、L237–440 | 默认 base、逐列表行数限制、stat 后文件/目录分类、CLI 参数与 exec；`addUBMount` 的 rootinfo/topo 是文件/目录挂载，与 runtime UB 设备节点不同 |
| 06 | [base.list](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/scripts/base.list)，完整五项 | driver lib64/include、dcmi、npu-smi、queue_schedule 是宿主候选，不提供逐子库来源、版本或实际挂载证明 |
| 07 | [run_main.sh](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/scripts/run_main.sh)，L278–315 | 五产品分支与默认复制分支、两个 add_so、部署配置 base.list 与 chmod 440；不把源码列表当作现场部署产物 |
| 08 | [cli/src/u_mount.c](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/cli/src/u_mount.c)，L45–240 | 源 stat 失败可返回 0；NODRV 可直接返回 0；实际执行 bind 后 remount 只读。成功返回与目标可达不能单独证明来源—目标挂载 |
| 09 | [NVIDIA README@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/README.md)，L194–315 | 文件入口为 `flags.plugin.deviceListStrategy` / `passDeviceSpecs`；支持保留 false 设计值，不由插件策略推定消费执行器和 Toolkit mode |
| 10 | [NVIDIA server.go@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go)，L280–438 | `CdiDevices`、CDI 提前返回、envvar/volume-mounts/DeviceSpecs 条件分开；这些输出链不替代框架 ordinal→稳定物理身份方法 |
| 11 | [containerd CRI config@v2.4.1](https://github.com/containerd/containerd/blob/v2.4.1/docs/cri/config.md)，L1–160、L270–385 | RuntimeClass/handler、runtimes 同名项、`runtime_type`、`options.BinaryName`、默认 runc 空 BinaryName 和 CDI 目录；是选定两端设计的依据，不是正文已完成选择的证明 |
| 12 | [Toolkit 1.20.0 CDI 页](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html)，Running a Workload / Non-CDI-Enabled Runtimes / Setting the CDI Mode Explicitly | 原生消费与 NVIDIA runtime 的 cdi mode 分开；显式 cdi mode 仍可使用 `NVIDIA_VISIBLE_DEVICES`，所以 envvar 单策略不足以证明 legacy |
| 13 | [Toolkit 1.20.0 排障页](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html#containers-losing-access-to-gpus-with-error-failed-to-initialize-nvml-unknown-error)，访问丢失与 Affected Environments | hook/legacy 更新丢失访问的条件，CPU/内存限制调整与特定 systemd reload 场景有别；该段不替本文选择资源更新接口/字段，不证明本库恢复成功 |
| 14 | [Syft README@v1.54.1](https://raw.githubusercontent.com/anchore/syft/v1.54.1/README.md)，Features / The basics / 配置与 schema 入口 | 支持镜像/文件系统扫描及多种输出格式；工具入口不代替本文选定范围、路径/层字段及逐库连接设计 |
| 15 | [PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html)，Device-agnostic code 的 CUDA_VISIBLE_DEVICES 段 | 可用 GPU 范围管理不等于本文完整 ordinal→分配/CDI→节点→UUID 关联方法；不据此断言其他身份接口不存在 |

本轮连接器返回的 Git blob SHA：`common.go=6cd038e9f1d67a8a913aa4bb1301692f177b3dbe`；`api/consts.go=ea68039808d6e034363936c2c4cc4dff9e941b3e`；`api/default_name.go=4bc4f25f076ff992542b3032fe785fd4de4d6ef7`；`plugin.go=b7692611b12884854d973fa2a3da18e381353f10`；runtime `process.go=acbd7a1ec0703498abfcfcb6ce1aa493069091b1`；hook `process.go=816212afa5f69b8edfb1554d3935af2ebcd28f06`；`base.list=4ea1b223fdeed19fed7fdf1a3b4457b8ddd747b3`；`run_main.sh=9be36636ff13c480c57342b81c78f4b74e95675b`；`u_mount.c=d85fd8155a1805edaf509b047c6441bcdc603e12`；NVIDIA `README.md=44594d4343967a313ff268223c8f638de005062c`、`server.go=9281b48ef52f9eda9cbed6d98491729da85b5a75`；containerd `config.md=3a206263f4f9e76b6ca14110461b8661a03b1619`。这些值均不是本机 curl 下载摘要。

## 4. 逐项复核与剩余关闭条件

以下“C32-1”等仅指前轮 §4 下的条目顺序，不新增发现 ID。子条件得到认可不等于其所属发现整体 CLOSED。

### B21-C32 — P2 / OPEN

**权威条件：** 第二十六次复核 L91。**位置：** 正文 L60、L72、L78、L82–84、L109–114、L118、L127、L131–138；第二十八轮映射 L327。

**保留认可：** 宿主内核驱动/注入用户态组件/镜像库的分层、Allocate/CDI/OCI 连接、节点与许可分开；L112 的缺方法/缺采样区分、L118 的缺规则优先无法确定，以及前轮已认可的 R1 规则均保留。不把诚实 unknown 或现场值未采本身判为事实错误。

1. **C32-1 / OPEN：扫描范围、字段与逐库连接仍未交付。** L60 仍以“所选扫描配置实际扫描的成分记录”为对象，未选定范围；比对字段仍只列包名/版本/来源层。L72 仍写“包名/版本/路径/来源层字段，以实际输出为准”，没有包/文件路径与层的解析/连接键。digest→层清单→SBOM→宿主来源→挂载→目标的串联方向正确，但不能替代所选逐库关联规则。抽查 14 只证工具入口，不由审阅者代选范围或补作者设计。
2. **C32-2 / OPEN：逐 ordinal 稳定映射仍明确未交付。** L78 原文仍为“稳定物理标识映射方法（未交付，unknown）”，后文是待完成需求；L82–84 是待填表。缺可见集快照→实际分配 ID/CDI 名或传递字段→完整节点（类型、major/minor、路径及来源）→稳定身份的来源支持连接方法。抽查 10、15 不替代这一方法；数量或编号文本一致仍不能证明同一设备。
3. **C32-3 / OPEN：分类同步未贯通。** L109 仍为“未记录即缺失”，L110“无法确定写 unknown”，L111“同上”；没有共同携带缺方法/缺采样原因、具体缺项、证据定位。L114 和 L131–138 的比较也未统一引用该分类。L112 的局部规则及 L127 的阶段对象关联有价值，但不自动补出其他记录的缺项分类。映射 L327 的“分类同步（诚实边界）”不是正文已落实的关闭证据。

**剩余关闭条件：** 按固定来源交付所选扫描范围、必要字段、包/文件/层解析与逐库来源连接，以及完整逐 ordinal 稳定映射；将缺方法/缺采样原因、具体缺项和证据定位的公共规则同步到核对表、最小清单及 C34 比较/判定。**现场值可 unknown；不要求拉镜像、生成 SBOM、审全部 cataloger、采设备或实测，不重开 C30/C31。**

### B21-C33 — P2 / OPEN

**权威条件：** 第二十六次复核 L106。**位置：** 正文 L90、L92；作者来源记录 L12、L17；登记 L5446、L5457、L5462；第二十八轮映射 L326。

**本轮新增认可：worker 七项生成规则子条件已满足。** L90 已逐名写出七个 API 常量，六个计数字段取 `Itoa(len(devices))`，`PtLocalRankEnv` 取 local-rank 逗号串，且保留 `!PresetVDevice` 条件。抽查 01 实际使用 `len(deviceStr)`，该数组由输入 devices 逐项生成，与此计数等价；对所选非空输入，`localRankStr(n)` 生成 `0` 至 `n-1`、无尾逗号。这不是框架标准语义或真实环境输出已验证的结论，不再索取同一生成算法。ID 逗号拼接、options、310B allow-link 条件亦继续认可。

为精确区分证据位置，抽查 02 核到 worker 字符串实际定义在同 commit 的 `api/consts.go` Env 段：`MS_LOCAL_WORKER`、`MS_WORKER_NUM`、`WORLD_SIZE`、`LOCAL_WORLD_SIZE`、`LOCAL_RANK`、`CM_WORKER_SIZE`、`CM_LOCAL_WORKER`；ASCEND 控制键在 `api/default_name.go`。L90 将环境字符串定义笼统指向 default_name.go 的旧表述尚未区分两者；这属于本项原有 worker/控制键证据定位，不另立发现。新增 `GetDefaultDevices` 产品/存在性索引可以保留，但不把未选原生路径 A 的默认设备配置当成所选路径 B 的完整输出。

1. **C33-1 / OPEN：worker 部分已补，完整对象记录关联仍未完成。** L90 的机制链已细化，不再判为只有组名；但称为“完整节点/许可/环境逐段对应表”的部分仍未把所选对象的条件、宿主来源/容器目标、节点/许可/环境结果、失败/跳过和可定位证据接到共同的可复用记录规则。尤其同一 UB 集合仍把 `uburma/ummu` 与 `hccl_rootinfo.json/topo` 合列；应分别将前者连到 runtime `addUBDevice/addDevicesInDir` 的设备节点/许可，将后者连到 hook `addUBMount` 的文件/目录挂载与 CLI 目标（抽查 04、05），并各自记录状态及证据位置。不是要求机械重写 14 行或填真实设备号，而是补齐已有机制如何落成同一所选对象记录。
2. **C33-2 / OPEN：旧挂载成功判据仍残留，逐库取证关联不足。** L90 前部已有“CLI 成功返回＋目标可达均不单独证明挂载，须来源-目标关联记录”，但默认 base 第①项仍逐字保留“挂载成功以 CLI 返回＋目标可达为准，未执行”；②③⑤又写“同①规则”。该旧判据没有真正替换，与新增原则直接冲突。抽查 08 中源 stat 失败或 NODRV 可返回 0 而不挂载，所以 CLI 返回及目标存在不是来源证明。逐库仍只列“库文件名/版本/CLI 目标路径/挂载结果”，缺父候选＋子库相对路径→宿主子库完整来源、采样证据与实际挂载证据的可定位关联，以及缺项/原因；仅“三方同路径”连接的是路径文本。缺项一概“注缺采样”也不能覆盖方法尚未交付。
3. **C33-3 / OPEN：正文与作者清单旧宽口径未清。** L90 仍两处出现“runtime 库注入语义未核对，unknown”，而同一行已写默认白名单/hook/CLI 和 env 改写机制；应区分已读机制与尚缺方法/记录、未读变体、现场结果未采。作者来源记录 L12 的机制已读说明认可，但“所选记录 filled 值未交付”不能掩盖 C33-1/C33-2 的设计缺项；L17 仍把“实际库挂载/白名单/hook 可执行/dcmi 完整实现”合列 unknown。登记 L5462 既有源码/部署产物限定继续保留，不重复要求新增同一登记。

**剩余关闭条件：** 保留已补的 worker 生成算法、辅助候选集合、manager 重命名与准确错误传播；补所选节点/许可/环境、UB 挂载、条件化 vdevice/poststop 的共同记录关联，并准确定位 worker/控制键来源；真正删除/改正旧挂载成功判据，落实逐库来源—实际挂载证据—缺项原因连接；清除正文与作者清单旧宽口径，区分机制已读、方法/记录设计缺项和现场未采。**支持交集、现场文件/设备号、库版本和结果可 unknown；不要求安装、执行脚本、实测、完整 DCMI、全部产品白名单或 CLI 审计。**

### B21-C34 — P1 / OPEN

**权威条件：** 第二十六次复核 L121。**位置：** 正文 L127、L131–138，关联 L109–114、L118–125、L140–142；第二十八轮映射 L327。

**保留前轮已认可项：** `flags.plugin.passDeviceSpecs=false` 的所选假设、原生 CDI 基线空 BinaryName/默认 runc 与 NVIDIA runtime 不参与的边界声明、单逻辑策略/旁路排除、S1/R1、负向独立授权、更新/回退/重建拆分、NPU 独立未知继续认可。**L127 的 R1 已提供每阶段主体、新旧 ID、完整目标节点、稳定身份、时间窗、正负访问结果或未执行原因和可定位证据的公共连接规则；该子条件不重开，不再以各行没有重复整套字段为由要求补写。** 无负向授权只记未执行，不要求执行。

1. **C34-1 / OPEN：L132 两端设计矛盾仍未清。** 前半已选“Toolkit mode 不适用（CDI 原生直达低层 runtime，NVIDIA runtime 不参与）”，同一行后半仍为“Toolkit mode 取 CDI 模式设计值，待填”；已选 `options.BinaryName` 默认空，链内仍写“执行器，值待填”。legacy 端仍写“Toolkit 对应 legacy 模式（设计值待填）”，没有一致固定该端的消费执行器、`runtime_type/options.BinaryName` 及对应 Toolkit 配置键/取值。抽查 09–12 支持区分插件传递、CRI 执行器和包装器 mode；`envvar` 与 `NVIDIA_VISIBLE_DEVICES` 本身不能证明 legacy。缺口是清理冲突并完成来源支持的配置对，不是再补策略名称或要求现场 handler/安装路径/配置输出。
2. **C34-2 / OPEN：L137 资源更新接口/字段仍未选。** 原文仍为“CPU 限制（接口/字段未选定，unknown；内存限制另立变体）”，证据栏仍承诺“接口选定后绑定同一次更新前后采样”。没有已选接口、完整字段、单位/语义、旧→新记录格式及同次更新前后采样关联。抽查 13 提供场景依据，不能替作者选接口；回退或重建不是这一更新变体的交付。
3. **C34-3 / OPEN：C32 方法依赖未闭合。** L131 的三单基线与 L132–138 的比较仍依赖未交付的稳定映射与缺项分类。此部分归 C32 原缺口，不新增/重复计数，也不拿依赖问题掩盖本项前两条独立设计缺项。R1 关联框架认可与 C32 方法仍缺可以同时成立。

**剩余关闭条件：** 保留已选 false、原生 CDI/不适用边界及 R1 公共规则；清除同行旧矛盾，交付完整无歧义的两端配置键/设计取值、消费执行器、Toolkit mode/不适用说明与旁路排除；选定资源更新接口、完整字段、单位/语义、旧新记录格式和同次采样关联；引用 C32 已交付方法并贯通缺方法/缺采样分类。**保留 NPU 独立未知、S1/R1、负向授权和回退拆分；不要求实测、现场值、扩大生产权限或制造结果。**

## 5. Acceptance 与结论

| T05-01 acceptance | 本轮判定 | 原发现对应 |
|---|---|---|
| L5403：镜像身份、层、构建输入、SBOM/签名、拉取策略 | 沿用此前完整通过，不重审；不据此宣称已有供应链系统 | C30 CLOSED，范围外 |
| L5404：固定运行时/NVIDIA 版本与层间职责 | 部分满足，未完整通过；扫描/逐库连接、稳定映射方法与分类仍缺 | C31 CLOSED，范围外；C32 OPEN |
| L5405：Ascend 独立实现与目标组合 | 部分满足，未完整通过；worker 算法进展认可，完整记录、旧挂载判据/逐库关联和宽口径仍缺 | C33 OPEN |
| L5406：最小清单、异常/隔离、对照与源案例 | 部分满足，未完整通过；R1 保留认可，但两端设计与资源更新方案未完成，另依赖 C32 | C34 OPEN |

四条 acceptance：**1 沿用既有完整通过 / 3 未完整通过**。本轮 **0 CLOSED / 3 OPEN（1 P1、2 P2）**，**第二十八次定向复核不通过**；无新增发现 ID，不修改计划或正文审核状态。阻断来自方法/记录设计缺项、旧判据与分类/配置不一致，**不是 DNS 失败、现场值 unknown、缺少实测或未证明整栈兼容**。审阅者本轮补读和解释上游不代替作者把方法落到正文。

## 6. 结构校验与写入审计

- 为只新增本报告，原仓库不执行会更新生成文件的构建。审计目录为 `/private/tmp/b21-t05-01-recheck28-nLAtf6`；校验在其中的独立 `validation` 副本进行，复制既有 `build/`，排除 `.git`、虚拟环境与工具缓存；原仓库生成文件保持不动。
- 写入前，副本使用原仓库虚拟环境 Python，禁写 Python 字节码，执行 `make check` 与 `make build` 均 **PASS，96 content entries / 444 sources**；仅副本重建 `build/catalog.json` / `build/catalog.md`。这些结果只说明结构和本地链接，不验证远程正文或技术正确性。
- 报告写入并同步副本后，禁写字节码执行 `make check` / `make build` 均 **PASS，96 content entries / 444 sources**；日志保存在审计目录的 `validation-after.log`，仍仅副本更新生成文件。
- 文件摘要审计覆盖 **424 个**既有文件（排除 `.git`、虚拟环境与工具缓存，包含原仓库 `build/`）：无修改、无删除，唯一新增为本报告；七份指定输入及两份补充输入摘要均与 §2 一致。剔除本报告后的 Git 状态与开始时一致；再次核验的本地执行模型/档位仍为单一 `gpt-6.1-sol / xhigh`，未检出审阅者输出 fallback 标记。审计结果保存在 `audit-result.json`，本段仅在实际检查完成后补记。
- 未运行 `make test`：本轮未修改 `src/kb/` 或测试代码；不安装或执行上游组件。临时审计材料不是永久来源，也不是环境实测证据。

**最终结论：B21-C32 OPEN、B21-C33 OPEN、B21-C34 OPEN；0/3 关闭，本次不通过。仅继续上述剩余条件，不重开 C30/C31，不重复索取已认可的 worker 算法和 R1 公共规则。未执行实测，不构成硬件验证。**
