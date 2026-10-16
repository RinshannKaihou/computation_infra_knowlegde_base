# Batch 21 补交 T05-01 第二十七次定向复核

## 1. 结论、角色与范围

- 日期：2026-10-14（Asia/Shanghai）。执行者：当前 Codex 会话，以独立审阅角色核对作者第二十七轮修订，与作者修订角色分开；未派发其他模型或子代理。
- `gpt-6.1-sol / xhigh` **仅为用户约定，不是已独立确认的执行元数据**。没有可独立核验的底层实际模型、推理档位或路由证据，不宣称已确认模型一致性或无 fallback。
- 唯一复核范围为 **B21-C32–C34**；剩余关闭条件以[第二十六次复核](batch-21-t05-01-codex-recheck-26.md) L91、L106、L121 为权威。[初审报告](batch-21-t05-01-codex-review.md)用于核对原 ID、优先级和职责边界。**C30/C31 沿用此前 CLOSED，范围外，不重审。** 第二十七轮修订映射只列落盘改动，不代替关闭证据。
- **0 CLOSED / 3 OPEN（1 P1、2 P2）；第二十七次定向复核不通过。** 本轮认可 310B 辅助项展开、manager 目标重命名、作业/UB/manager 错误传播的精确化、`passDeviceSpecs=false` 设计取值、原生 CDI 基线的执行器/mode 边界声明，以及 R1 的每阶段公共连接规则；但扫描/稳定映射方法、完整环境/逐库记录、旧判据与旧口径清理、无矛盾的两端消费配置及资源更新设计仍未闭合。
- 只新增本报告，不修改作者正文、修订映射、作者来源记录、来源登记、计划或原仓库生成文件；保留开始时已有工作区改动，不提交、不创建分支。所有问题归原 ID，**不新增发现 ID**。
- 未安装组件、拉取/构建镜像、生成 SBOM、运行容器、查询设备、接入集群、修改运行配置或执行访问、负向、资源更新、回退、恢复实测。上游脚本/源码只读，不执行；知识目录结构检查/构建不代表技术或硬件验证。

| 原 ID | 原优先级 | 本轮状态 | 位置证据与主要剩余项 |
|---|---|---|---|
| B21-C32 | P2 | OPEN | 正文 L60、L72、L78、L82–84、L109–114、L118、L131–138：扫描范围/字段与逐库连接、逐 ordinal 稳定映射仍未交付，缺方法/缺采样分类未贯通 |
| B21-C33 | P2 | OPEN | 正文 L90、L92；作者来源记录 L12、L17：辅助集合与错误传播有进展，worker 键/生成规则及完整记录关联仍缺；旧挂载成功判据和宽口径仍在 |
| B21-C34 | P1 | OPEN | 正文 L127、L132、L137：R1 公共连接规则认可；两端消费配置仍有矛盾/待选字段，资源更新接口与字段仍未选；另依赖 C32 方法 |

## 2. 输入身份与审阅边界

用户给出的 **2 个 SHA-256 前缀均与当前整文件吻合**。修订映射本轮仅审 L318–322，不将旧轮次清单当作本轮新增交付。来源登记经 YAML 解析为 **440 项**。补充只读作者来源记录，因为前次 C33 剩余条件明确包含该清单的口径同步，不扩展为新项目。

| 输入 | 本轮独立计算的完整 SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md)，指定前缀 `7936cc9ec110680a` | `7936cc9ec110680a2e4df06730e34083958068619c7db8f11ff5341fa808108b` |
| [修订映射](batch-21-review-fixes.md)，指定前缀 `9fd1604ae2db82b0` | `9fd1604ae2db82b0549be104b0d0eb515364c3d9b65d2f756919045526cfb880` |
| [第二十六次复核](batch-21-t05-01-codex-recheck-26.md) | `ade616897c367afb566c3076ffc8b36f2dbf6c95af8558d74af8d537ed3402b0` |
| [初审报告](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` |
| [任务验收](../../plans/full-coverage-backlog.yaml)，T05-01 acceptance L5403–5406 | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml) | `af8d7441ba9fb3da5413475200b8a75278586877e06dc004d70a89ef4453d4b8` |
| 补充只读：[作者来源记录](batch-21-t05-01-sources.md)，L12、L17 | `3719c44a87798ef001541fa241877decc3f0817483cea3408c2f609a8d888235` |

仓库位置证据均为上述文件的物理行号。正文 L90、L127、L132 是长行，下文用精确短语区别新增与残留内容。已从 `README.md`、`docs/authoring-guide.md` 开始核对规则，并读取 `content-outline.md` 的归属边界及元数据 schema；不以作者映射或前次报告摘录代替本轮一次源实读。

## 3. 一次源抽查方法与结果

### 3.1 curl 尝试、替代通道与限制

对下表 01–14 分别实际发起只读 HTTPS GET。GitHub 文件使用同 ref/path 的 `raw.githubusercontent.com` 地址；厂商文档使用表列精确地址。命令形态：

```sh
curl --proto '=https' --proto-redir '=https' \
  --location --fail --silent --show-error \
  --connect-timeout 10 --max-time 25 \
  --output /private/tmp/b21-t05-01-recheck27-fI1Ouq/curl/NN.body \
  --write-out 'http=%{http_code} bytes=%{size_download}\n' "$url"
```

保留 curl 默认 TLS 证书校验，未使用 `-k`、证书绕过、IP 替换或代理改写。**14 次均在 DNS 阶段失败：exit 6、HTTP 000、下载 0 字节**，分别为 `raw.githubusercontent.com`、`docs.nvidia.com`、`docs.pytorch.org` 无法解析；因此本机 curl 没有取得正文，也没有完成 TLS 握手，不能写成 curl 已核对文字或 TLS 已验证。

随后使用允许的只读通道完成文字核对：**GitHub 连接器 `fetch_file`** 按精确 ref/path 读取下表源码区间；**Web 阅读工具 `open`/`find`** 打开 Toolkit 两页和 PyTorch 指定版本页，定位到下列章节/段落并读正文。不是只判可达性，不只读标题/搜索摘要；未改用最新版本替代指定版本。连接器返回的 Git blob SHA 是服务返回的文件身份，不是本机 curl 下载摘要；Web 返回页面可能经提取/缓存，不能据此声称独立验证了网络原始字节或 TLS。Web 阅读行号不拼成 GitHub 原文件行锚。

### 3.2 实读证据表

编号只标抽查点，不是新发现 ID。Ascend 各文件均固定 commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e`。

| 抽查点 | 精确一次源与本轮读取位置 | 文字核对结果及用途 |
|---|---|---|
| 01 | [runtime/process/process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go)，L1–135、L206–430、L485–840 | `addDeviceToSpec` 取节点信息失败返回错误；310B 14 辅助项失败警告继续；manager 回退源映射到容器 `/dev/davinci_manager`；作业 davinci 失败直接返回，UB/manager 失败由上层 Errorf 后返回。UB 目录遍历跳过子目录；VIRTUAL 提前返回与后续 CreateVDevice/poststop 条件分开。支持认可本轮已改部分，不等于完整记录已交付 |
| 02 | [device-plugin/pkg/common/common.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go)，L85–160 | `SetAscendRuntimeEnv` 写 ID 串/options、按卡写 allow-link，`!PresetVDevice` 时逐项写 7 个 worker 环境键；计数取输入长度，`localRankStr` 给出具体拼接算法。正文仅写组数/“有生成函数”，仍未落实这些输出键与生成规则 |
| 03 | [ascend-common/api/default_name.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/api/default_name.go)，L1–240 的 docker runtime 常量段 | 核到 ASCEND 可见设备/options/mounts/allow-link 等控制键和配置目录定义；本轮读取区间不冒充该文件全部常量审计 |
| 04 | [hook/process/process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/hook/process/process.go)，L1–70、L85–225、L237–440 | 默认 base；每份列表扫描行数计数后 stat/分类；文件/目录列表转 CLI 参数并 exec。`addUBMount` 的 `/etc/hccl_rootinfo.json` 与 `/usr/local/Ascend/driver/topo` 是文件/目录挂载候选，区别于 runtime 的 UB 设备节点。父目录入选不是逐子库来源证据 |
| 05 | [build/scripts/base.list](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/scripts/base.list)，完整五行 | 五个宿主候选路径已核；列表不提供逐库身份、版本或已挂载证明 |
| 06 | [build/scripts/run_main.sh](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/scripts/run_main.sh)，L278–315 | 五产品分支/默认复制、两分支 add_so、目标 base.list 和 chmod 440 已核；源码列表与部署产物有别，不证明现场安装或组合配套 |
| 07 | [cli/src/u_mount.c](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/cli/src/u_mount.c)，L45–240 | 目标拼接 rootfs＋源路径，bind 后只读 remount；源 stat 失败可返回 0，NODRV 可直接返回 0 而不挂载。故 CLI 成功返回＋已有目标可达不足以证明目标来自所选宿主源 |
| 08 | [NVIDIA README@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/README.md)，L190–315 | 文件配置入口是 `flags.plugin.deviceListStrategy` / `flags.plugin.passDeviceSpecs`，支持本轮 false 设计值；策略传递与消费端执行器是不同层 |
| 09 | [NVIDIA server.go@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go)，L280–438、L448–507 | CDI 响应、全 CDI 提前返回、非 CDI 的 envvar/volume-mounts/PassDeviceSpecs 条件不同；ID 转换与去重不交付框架 ordinal→物理身份规则 |
| 10 | [containerd CRI config@v2.4.1](https://github.com/containerd/containerd/blob/v2.4.1/docs/cri/config.md)，L1–155、L270–385 | RuntimeClass/handler→同名 runtimes 项，runtime_type 与 BinaryName 有具体配置；默认 runc 项及空 BinaryName、cdi_spec_dirs 已核。认可作者开始选择原生基线，但不能以文档默认项代替正文尚待选的完整两端配置 |
| 11 | [Toolkit 1.20.0 CDI support](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html)，Running a Workload / Non-CDI-Enabled Runtimes / Setting the CDI Mode Explicitly | 原生 engine 消费与 NVIDIA 包装器 cdi mode 分开；显式 cdi mode 仍使用 NVIDIA_VISIBLE_DEVICES，故 envvar 单策略不自动证明 legacy；hook/CDI 冲突需排除 |
| 12 | [Toolkit 1.20.0 troubleshooting](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html)，访问丢失 / Affected Environments | hook/legacy 更新可丢失访问，CPU/内存限制调整与特定 systemd reload 条件有别；该段提供场景，不替作者选择更新接口、完整字段、单位和旧新记录格式 |
| 13 | [Syft README@v1.54.1](https://github.com/anchore/syft/blob/v1.54.1/README.md)，L1–110 的 Features / The basics | 核到镜像/文件系统扫描、输出格式和配置/schema 入口；README 入口不替正文确定扫描范围、逐库路径/层字段与连接规则，不要求审全部 cataloger 或生成 SBOM |
| 14 | [PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html)，Device-agnostic code 的 CUDA_VISIBLE_DEVICES 段 | 核到可用 GPU 范围管理；该段不交付本文逐 ordinal→分配/CDI→完整节点→UUID 关联规则。不据此断言不存在其他身份接口 |

GitHub 连接器返回的文件身份（Git blob SHA）：runtime `process.go=acbd7a1ec0703498abfcfcb6ce1aa493069091b1`；`common.go=6cd038e9f1d67a8a913aa4bb1301692f177b3dbe`；`default_name.go=4bc4f25f076ff992542b3032fe785fd4de4d6ef7`；hook `process.go=816212afa5f69b8edfb1554d3935af2ebcd28f06`；`base.list=4ea1b223fdeed19fed7fdf1a3b4457b8ddd747b3`；`run_main.sh=9be36636ff13c480c57342b81c78f4b74e95675b`；`u_mount.c=d85fd8155a1805edaf509b047c6441bcdc603e12`；NVIDIA `README.md=44594d4343967a313ff268223c8f638de005062c`、`server.go=9281b48ef52f9eda9cbed6d98491729da85b5a75`；containerd `config.md=3a206263f4f9e76b6ca14110461b8661a03b1619`；Syft `README.md=9ffd2affa3b00031ea1fd01ee3fe228379978492`。均非本机 curl 下载摘要。

## 4. 逐项复核与剩余关闭条件

### B21-C32 — P2 / OPEN

**权威条件：** 第二十六次复核 L91。**位置证据：** 正文 L60、L72、L78、L82–84、L109–114、L118、L131–138；第二十七轮映射 L322。

**认可并保留：** 宿主内核驱动、注入用户态组件、镜像自带库的分层及既有 Allocate/CDI/OCI 连接；节点与许可分开；L112 区分缺方法/缺采样，L118 将缺规则置于无法确定优先。不把诚实 unknown 本身记作错误，不重开 C30/C31。

**仍未满足：**

1. **扫描范围/字段和逐库来源连接仍未交付。** L60 仍是“所选扫描配置”，L72 仍是“来源层字段，以实际输出为准”；没有明确所选扫描范围、必要字段及包/文件路径与层的解析/连接键。digest→层清单→SBOM→宿主来源→挂载→目标的箭头不是可核对的逐库连接规则。抽查 13 只支持工具入口，不由审阅者补读替作者完成设计；不要求实际生成 SBOM。
2. **逐 ordinal 稳定映射仍明确未交付。** L78 原文仍为“稳定物理标识映射方法（未交付，unknown）”；L82–84 是待填表，不是有来源的连接方法。缺可见集快照→分配 ID/CDI 名或传递字段→完整节点（类型、major/minor、路径及来源）→稳定身份的具体关联。抽查 09、14 不完成该证明，数量或编号文本相同不能替代稳定对应。
3. **分类未同步到共同记录和判定。** L109“未记录即缺失”、L110“无法确定写 unknown”、L111“同上”仍未共同携带缺方法/缺采样原因、具体缺项、证据定位；L114 和 L131–138 的比较也未统一引用。L127 本轮补的是阶段/对象证据关联，值得保留，但不因此补出扫描/稳定映射方法或全局缺项分类。映射 L322“分类同步”不能作为独立关闭证据。

**剩余关闭条件：** 按固定来源交付所选扫描范围、必要字段、包/文件/层解析与逐库来源连接，以及完整逐 ordinal 稳定映射；将缺方法/缺采样原因、具体缺项与证据定位的公共规则同步到核对表、最小清单及 C34 比较/判定。**现场值可 unknown；不要求拉镜像、生成 SBOM、审全部 cataloger、采设备或实测，不重开 C30。**

### B21-C33 — P2 / OPEN

**权威条件：** 第二十六次复核 L106。**位置证据：** 正文 L90、L92；[作者来源记录](batch-21-t05-01-sources.md) L12、L17；登记 L5446、L5457、L5462（既有边界）；第二十七轮映射 L320。

**本轮新增认可：** L90 已展开 14 个辅助候选名，补了 manager 回退后的容器目标重命名、UB 目录/跳过子目录条件；“作业 davinci 失败＝直接返回错误；UB/manager 失败＝Errorf 后返回；仅 310B 14 辅助项与 dvpp 等特定分支＝警告后继续”与抽查 01 对应，不再以旧 `(warn)` 短句混淆作业失败和辅助项继续。新增“CLI 成功返回＋目标可达均不单独证明挂载，须来源-目标关联记录”原则正确。此前认可的所选 310B/default/base 条件、两端卡型来源不互证、VIRTUAL 与条件化 poststop 分离、GPU 不套用 NPU 和支持交集 unknown 均保留，不再次要求补同一批辅助名称。

**仍未满足：**

1. **完整可复用记录规则仍未完成。** L90 的 worker 部分仍是“worker 组 7 项……local-rank 有生成函数”，不是 7 个实际输出键及各自生成规则；组数或函数存在不能替代规则。抽查 02 可逐项核对 `api.MsLocalWorkerEnv`、`api.MsWorkerNumEnv`、`api.PtWorldSizeEnv`、`api.PtLocalWorldSizeEnv`、`api.PtLocalRankEnv`、`api.TfWorkerSizeEnv`、`api.TfLocalWorkerEnv` 及 `localRankStr`。现有箭头也未用共同格式把所选条件、宿主来源/容器目标、节点/许可/环境结果、失败/跳过、证据位置逐项连接。runtime 的 UB 节点与 hook 的 UB 文件/目录挂载须在记录中分清（抽查 01、04），不要求真实设备号、输出值或运行结果，也不要求机械重复 14 行。
2. **旧挂载成功判据仍未被替换，逐库记录仍缺来源—目标取证关联。** 同一 L90 后半仍原样保留“挂载成功以 CLI 返回＋目标可达为准，未执行”，直接冲突于本轮新增原则；映射“替换”尚不成立。抽查 07 的源 stat 失败/NODRV 可返回成功而没有该次挂载，容器目标也可能原已存在。新增“宿主源路径→CLI 目标→容器内同路径三方一致”只规定路径文本连接，尚未明确实际来源—挂载证据的定位。逐库字段仍仅“库文件名/版本/CLI 目标路径/挂载结果”，缺父候选＋子库相对路径→宿主子库完整来源、采样证据与实际挂载证据的连接，以及缺项/原因；“缺则记 unknown 并注缺采样”不能覆盖尚缺设计规则的情况。
3. **正文与作者清单的旧宽口径仍在。** L90 末尾仍有“runtime 库注入语义未核对，unknown”；作者记录 L17 仍将“实际库挂载/白名单/hook 可执行/dcmi 完整实现”合列 unknown，L12 和 L90 的“所选记录 filled 值未交付”未消除设计缺项与现场未采的混称。应区分默认 base/hook/CLI 机制已读、未读产品变体、尚缺记录/方法设计、现场未采/未执行。登记 L5462 的源码/部署产物限定保留，不要求再补登记，不让审阅者补读代替作者同步。

**剩余关闭条件：** 保留已展开辅助集合、manager 重命名、准确错误传播及来源—目标原则；补全 worker/控制键生成和所选节点/许可/环境、UB 挂载、条件化 vdevice/poststop 的共同记录规则，逐项连条件、来源、目标、失败/跳过、证据位置；真正删除/改正残留挂载成功旧判据，补逐库来源/实际挂载证据/缺项原因关联；清除正文与作者清单的旧宽口径，分开机制已读、方法/记录设计缺项和现场未采。**支持交集、现场文件/设备号、库版本、结果可 unknown；不要求安装、执行脚本、实测、完整 DCMI、全部产品白名单或 CLI 审计。**

### B21-C34 — P1 / OPEN

**权威条件：** 第二十六次复核 L121。**位置证据：** 正文 L127、L131–138，关联 L109–114、L118–125、L140–142；第二十七轮映射 L321。

**本轮新增认可：** L132 已将 `flags.plugin.passDeviceSpecs=false` 作为所选假设；已开始选定原生 CDI 基线的空 `options.BinaryName`/默认 runc，并明确 NVIDIA runtime 不参与、Toolkit mode 不适用。这是实质进展，不再指称全部设计值都未选择。**L127 的 R1 公共连接规则已补齐前次要求的设计字段：每阶段主体（重建类新旧 ID）、完整目标节点、稳定身份、时间窗、正负访问结果或未执行原因、可定位证据，并覆盖变更前/后/恢复后。该公共规则子条件本轮认可，不要求各行机械重写，不再以恢复栏只有配置摘要为由判其仍缺完整公共对象。** 缺负向授权只记未执行，不要求补做负向。此前认可的 S1、R1 各变体引用、单独负向授权、权限完整比较对象、更新/回退/重建拆分、NPU 独立 unknown 均保留。

**仍未满足：**

1. **两端设计取值仍未形成无矛盾的完整配置对。** L132 前半已选“Toolkit mode 不适用”，同一行后半仍写“Toolkit mode 取 CDI 模式设计值，待填”；`options.BinaryName` 已选默认空，同一链又保留“值待填”，且没有把所选 runtime_type/执行器放到一致的两端设计。legacy 端已有“legacy 模式”的方向，但仍写“设计值待填”，未固定该端实际消费执行器及相应 Toolkit 配置键/取值。不能仅由 `[envvar]`＋NVIDIA_VISIBLE_DEVICES＋无 CDI 引用确定 legacy（抽查 08–11）。需保留已选基线，清理冲突待填文字，补完变体端所选 runtime_type/options.BinaryName 与 Toolkit mode 的来源支持设计值；现场 handler 名、安装路径和实际配置输出仍可待采。
2. **资源更新接口/字段仍明确未选。** L137 仍为“CPU 限制（接口/字段未选定，unknown；内存限制另立变体）”；缺所选接口、完整字段、单位/语义、旧→新记录格式及同一次更新前后采样的具体绑定。写“接口选定后绑定”是后续承诺，不是已经交付。抽查 12 只提供场景依据，不由审阅者选字段补作者设计；镜像/驱动回退或重建变体不能代替该项。
3. **C32 依赖仍未闭合。** L131 的基线及 L132–138 各比较仍缺已交付的稳定映射方法，缺方法/缺采样原因与具体缺项的公共分类也未同步。该部分归 C32 原缺口，不另计发现；不拿它掩盖或重复计算前两项独立设计缺项。R1 的阶段/对象公共规则已认可，不因此将方法未交付改写成仅缺现场采样。

**剩余关闭条件：** 保留本轮 false 取值、原生 CDI/不适用边界和已认可的每阶段 R1 公共连接规则；清除同一行的旧矛盾，给出完整、无歧义的两端所选配置键/设计取值、消费执行器及 Toolkit mode/不适用说明并保留旁路排除；选定资源更新接口、完整字段、单位/语义、旧新记录格式与同次采样关联；引用 C32 已交付方法并同步缺方法/缺采样分类。**保留 NPU 独立未知、S1/R1、负向授权和回退拆分；不要求实测、现场值、扩大生产权限或制造结果，无负向授权不执行。**

## 5. Acceptance 与最终计数

| T05-01 acceptance | 本轮判定 | 对应原发现 |
|---|---|---|
| 镜像身份、层、构建输入、SBOM/签名与拉取策略 / L5403 | 沿用此前完整通过，不重审；不据此宣称已有供应链系统 | C30 已 CLOSED，范围外 |
| 固定运行时/NVIDIA 版本与各层边界 / L5404 | 部分满足、未完整通过：逐库来源连接和稳定映射方法仍缺 | C31 已 CLOSED（范围外）；C32 OPEN |
| Ascend 独立实现与目标组合 / L5405 | 部分满足、未完整通过：辅助项/错误传播进展认可；完整规则、逐库关联和旧判据/口径仍缺 | C33 OPEN |
| 清单、异常/隔离、对照与源案例 / L5406 | 部分满足、未完整通过：R1 公共规则认可；无矛盾的两端配置与资源更新设计未完成，另依赖 C32 | C34 OPEN |

四条 acceptance：**1 沿用既有完整通过 / 3 未完整通过**。本轮 **0 CLOSED / 3 OPEN（1 P1、2 P2）**，**第二十七次定向复核不通过**，无新增发现 ID。阻断来自方法/记录设计、残留事实判据及口径矛盾、配置取值和资源更新方案，**不是 curl DNS 失败、现场值 unknown、未做实测或未证明整栈兼容**。不修改计划或正文审核状态，不以审阅者补读代替作者交付。

## 6. 结构校验与写入审计

- 写入前原仓库执行 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS，96 content entries / 440 sources**；只验证结构和本地链接，不验证技术正确性或远程正文。
- 写入后原仓库 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS，96 content entries / 440 sources**。
- 为遵守仅写一份报告的限制，在 `/private/tmp/b21-t05-01-recheck27-fI1Ouq/validation` 独立副本中，使用原仓库虚拟环境 Python、禁写字节码执行 `make check` / `make build`：均 **PASS，96 content entries / 440 sources**，仅副本生成 `build/catalog.json` / `build/catalog.md`；原仓库未运行会更新生成文件的构建。
- 文件摘要审计覆盖 **411 个**既有文件（排除 `.git`、`.venv` 与 Python/工具缓存）：无修改或删除，唯一新增为本报告；七份输入摘要保持 §2 所列值，剔除本报告后的 Git 状态与开始时一致。原仓库 `build/` 包含在摘要审计内；临时目录保留摘要基线、Git 状态、curl URL/错误记录与副本校验日志。
- 未运行 `make test`，因为未修改 `src/kb/` 或测试代码；结构检查和构建成功不计为内容审核或真实环境验证通过。

**最终结论：B21-C32 OPEN、B21-C33 OPEN、B21-C34 OPEN；0/3 关闭，本次不通过。后续只复核上述剩余关闭条件，不重开 C30/C31；已认可的辅助项、错误传播、false 取值和 R1 公共规则不重复索取，不以实测或现场值替代设计交付。**
