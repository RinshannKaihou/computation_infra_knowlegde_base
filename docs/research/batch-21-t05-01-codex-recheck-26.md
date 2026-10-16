# Batch 21 补交 T05-01 第二十六次定向复核

## 1. 结论、角色与范围

- 日期：2026-10-14（Asia/Shanghai）。执行者：当前 Codex 会话，以独立审阅角色核对作者第二十六轮修订，与作者修订角色分开；未派发其他模型或子代理。
- `gpt-6.1-sol / xhigh` **仅为用户约定，不是已独立确认的执行元数据**。没有可独立核验的底层实际模型、推理档位或路由证据，不宣称已确认模型一致性或无 fallback。
- 唯一复核范围为 **B21-C32–C34**；剩余关闭条件以[第二十五次复核](batch-21-t05-01-codex-recheck-25.md) L86、L101、L116 为权威。[初审报告](batch-21-t05-01-codex-review.md)仅用于核对原 ID、优先级及职责边界。**C30/C31 沿用此前 CLOSED，范围外，不重审。** 第二十六轮修订映射只列落盘改动，不代替关闭证据。
- **0 CLOSED / 3 OPEN（1 P1、2 P2）；第二十六次定向复核不通过。** 本轮认可节点信息错误传播的明确化、挂载成功须有来源—目标关联的新增限定、真实插件配置键和 `options.BinaryName` 的补列，以及更多变体引用 R1；但同段旧判据/旧口径未清除，所选输出记录、方法、设计取值与完整阶段证据关联仍不足。
- 只新增本报告，不改作者正文、修订映射、作者来源记录、来源登记、计划或原仓库生成文件；保留开始时已有工作区改动，不提交、不创建分支。新增表述的语义问题仍归原 C33/C34，**不新增发现 ID**。
- 未安装组件、拉取/构建镜像、生成 SBOM、运行容器、查询设备、接入集群、修改运行配置或进行访问、负向、更新、回退、恢复实测。上游脚本/源码只读，不执行；结构检查与知识目录构建不代表技术或硬件验证。

| 原 ID | 原优先级 | 本轮状态 | 位置证据与剩余问题 |
|---|---|---|---|
| B21-C32 | P2 | OPEN | 正文 L60、L72、L78、L82–84、L109–114、L118、L131–138：所选扫描/逐库归层连接和逐 ordinal 稳定映射方法仍缺；缺方法/缺采样分类未贯通 |
| B21-C33 | P2 | OPEN | 正文 L90、L92；作者来源记录 L12、L17：新增失败/成功限定有进展，但完整所选输出规则未交付，同段旧挂载成功判据与旧宽口径仍在 |
| B21-C34 | P1 | OPEN | 正文 L127、L132–138：真实配置入口已补，设计取值仍待填；资源更新接口/字段明确未选；完整阶段访问/恢复证据及 C32 方法依赖仍缺 |

## 2. 输入身份与审阅边界

用户指定的 **2 个 SHA-256 前缀均与当前整文件吻合**。修订映射本轮只审 L312–316，不把旧轮次清单当作新增关闭证据。来源登记经 YAML 解析为 **440 项**。另只读作者来源记录，因为前次 C33 剩余条件明确包含该清单的口径同步；不扩展为新的审阅项目。

| 输入 | 本轮独立计算的完整 SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md)，指定前缀 `761c09bdca885767` | `761c09bdca8857675ba4801ac2e03ca1633b4996eac3cf2371ef2b119bf6e09e` |
| [修订映射](batch-21-review-fixes.md)，指定前缀 `2427c9c6ee65597c` | `2427c9c6ee65597c7fcd1129398425cddb38dde52fb88ad9710f064f6fe62280` |
| [第二十五次复核](batch-21-t05-01-codex-recheck-25.md) | `95ac0c86df4bc32637c75190f27c69038bf76a62647e6dc81a313751a0395616` |
| [初审报告](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` |
| [任务验收](../../plans/full-coverage-backlog.yaml)，T05-01 acceptance L5403–5406 | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml) | `af8d7441ba9fb3da5413475200b8a75278586877e06dc004d70a89ef4453d4b8` |
| 补充只读：[作者来源记录](batch-21-t05-01-sources.md)，L12、L17 | `3719c44a87798ef001541fa241877decc3f0817483cea3408c2f609a8d888235` |

仓库位置证据均为上述文件的原行号。正文 L90 是一条较长的物理行，以下同时给出精确短语区分同一行中的新增与残留文字。从 `README.md`、`docs/authoring-guide.md`、`content-outline.md` 开始核对规则，并读取元数据 schema；不以指南、作者说明或前次摘录替代本轮一次源实读。

## 3. 一次源抽查方法与结果

### 3.1 curl 实际尝试、替代通道及限制

对下表 01–13 逐一实际发起只读 HTTPS GET；GitHub 文件使用同 ref/path 的 `raw.githubusercontent.com` 地址，其余使用表列文档地址。命令形态：

```sh
curl --proto '=https' --proto-redir '=https' \
  --location --fail --silent --show-error \
  --connect-timeout 8 --max-time 20 \
  --output "$audit_dir/curl-$point.body" \
  --write-out 'http_code=%{http_code}; ssl_verify_result=%{ssl_verify_result}; size_download=%{size_download}\n' \
  "$url"
```

保留默认 TLS 校验，未用 `-k`/`--insecure`、提权、自定解析或 IP 绕行。**13 次全部在 DNS 阶段失败：curl 退出码 6、HTTP 000、下载 0 字节、`Could not resolve host`**，涉及 `raw.githubusercontent.com`、`docs.nvidia.com`、`docs.pytorch.org`。未发生可据以确认成功的 TLS/HTTP 获取；输出中的 `ssl_verify_result=0` 不表示完成了 TLS 校验，不能记作 curl 200 或已核到 HTTP 原始正文。

随后使用用户允许的只读通道：GitHub 连接器 `fetch_file` 按固定 ref 和原文件区间读取，网页读取通道实际打开版本化 NVIDIA/PyTorch 页面，并读取相关正文段落；不是仅判可达性，也不以搜索摘要代替正文。runtime `process.go` L240–405 的首次连接器请求发生传输错误，重试同一只读请求后取得正文；未将失败请求算作取证成功。

网页通道可能解析/缓存页面：本轮 CDI/PyTorch 页面显示当日抓取，NVIDIA 排障页显示三日前抓取；这不等于本机 curl 获得的新鲜原始字节。连接器 Git blob SHA 不是 HTTP SHA-256。源码行号以连接器原文件读取区间为准，不把网页阅读器行号拼成 GitHub 源码锚点；不独立背书作者或历史报告中的 curl 成功记录。请求清单、curl 状态/错误与校验日志位于仓库外临时目录 `/private/tmp/b21-t05-01-recheck26-TRARWH`，不是永久来源或实测证据。

### 3.2 实读位置与有限支持范围

Ascend 文件均固定 commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e`。以下编号只标抽查点，不是发现 ID；均为既有登记来源，不新增来源项。

| curl 点 | 精确一次源 / 本轮实读位置 | 本轮核到的实现或文字及限制 |
|---|---|---|
| 01 | [runtime/process/process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go)，L45–120、L240–405、L550–830 | `DeviceFromPath` 失败返回 error；310B 的 14 辅助项与 dvpp 失败仅警告，manager 最终加入、作业 davinci、UB 条目失败向上返回。UB stat 门控与跳过子目录另有条件；manager 回退后另求容器路径；VIRTUAL 提前返回和条件化 poststop 分开。只核机制，不证现场成功 |
| 02 | [device-plugin common.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go)，L90–145 | ID 转字符串并逗号拼接、写 options；插件 RealCardType 为 310B 才写 allow-link；`!PresetVDevice` 时写七个 worker 字段，计数和 local-rank 有生成规则。不能从组名推定本文已交付完整环境输出记录 |
| 03 | [hook/process/process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/hook/process/process.go)，L85–225、L237–440 | 默认 base；每份列表逐行计数，再按 stat/文件类型分类；构造 CLI 参数并 exec，读取/校验/执行失败可返回错误。父目录候选不是子库身份/归属记录 |
| 04 | [build/scripts/base.list](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/scripts/base.list)，完整五行 | 五个宿主候选为 driver lib64/include、dcmi、npu-smi、queue_schedule；未提供逐库版本或已挂载证明 |
| 05 | [run_main.sh](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/scripts/run_main.sh)，L278–315 | 五产品分支及默认复制分支，目标为配置目录 base.list，chmod 440；源码列表与部署产物有别，不证明安装/组合配套 |
| 06 | [cli/src/u_mount.c](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/cli/src/u_mount.c)，L45–240 | rootfs＋源路径，bind 后只读 remount；源 stat 失败可返回 0，NODRV 也直接返回 0；目标创建、校验或挂载失败可返回非零。CLI 成功返回和目标可达不能单独证明目标来自所选源 |
| 07 | [NVIDIA README@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/README.md)，L194–315 | 文件配置键为 `flags.plugin.deviceListStrategy`、`flags.plugin.passDeviceSpecs`，flag/env 另列。本文已补真实入口；默认值不是作者已经选定的对照设计值 |
| 08 | [NVIDIA server.go@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go)，L280–507 | CDI/非 CDI 分支不同；全 CDI 策略提前返回；envvar、volume-mounts、PassDeviceSpecs 另受条件控制。插件内部策略集合不是消费端 mode 的证明 |
| 09 | [containerd CRI config@v2.4.1](https://github.com/containerd/containerd/blob/v2.4.1/docs/cri/config.md)，L1–160、L270–385 | Pod→RuntimeClass handler、default_runtime_name、同名 runtimes 项、runtime_type/options.BinaryName 和 cdi_spec_dirs 有具体字段；仅补列键名仍不能确定两端执行器 |
| 10 | [Toolkit 1.20.0 CDI support](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html)，Running a Workload / Non-CDI-Enabled Runtimes / Setting the CDI Mode Explicitly | 原生 engine 消费与 NVIDIA runtime 的 cdi mode 有别；显式 cdi mode 仍可用 NVIDIA_VISIBLE_DEVICES 选择设备；hook/CDI 存在冲突边界。envvar 且无插件 CDI 引用不足以确定 legacy |
| 11 | [Toolkit 1.20.0 troubleshooting](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html)，访问丢失 / Affected Environments | hook/legacy 更新可丢失访问，CPU/内存限制更新与特定 systemd reload 场景有条件区别；该段不替本文选择更新接口/字段，也不证明本库恢复成功 |
| 12 | [Syft README@v1.54.1](https://github.com/anchore/syft/blob/v1.54.1/README.md)，L1–110，Features / The basics | 镜像/文件系统扫描、包清单、输出格式与配置/schema 入口已核到；本文仍需选择扫描范围与字段/连接方法，不要求审全部 cataloger 或生成 SBOM |
| 13 | [PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html)，Device-agnostic code 的 CUDA_VISIBLE_DEVICES 段 | 支持管理 PyTorch 可用 GPU 范围；该段不交付本文逐 ordinal→分配/CDI→完整节点→UUID 的关联规则；不据此断言其他身份接口不存在 |

本轮连接器返回的文件身份（Git blob SHA）：runtime `process.go=acbd7a1ec0703498abfcfcb6ce1aa493069091b1`；`common.go=6cd038e9f1d67a8a913aa4bb1301692f177b3dbe`；hook `process.go=816212afa5f69b8edfb1554d3935af2ebcd28f06`；`base.list=4ea1b223fdeed19fed7fdf1a3b4457b8ddd747b3`；`run_main.sh=9be36636ff13c480c57342b81c78f4b74e95675b`；`u_mount.c=d85fd8155a1805edaf509b047c6441bcdc603e12`；NVIDIA `README.md=44594d4343967a313ff268223c8f638de005062c`、`server.go=9281b48ef52f9eda9cbed6d98491729da85b5a75`；containerd `config.md=3a206263f4f9e76b6ca14110461b8661a03b1619`；Syft `README.md=9ffd2affa3b00031ea1fd01ee3fe228379978492`。均非本机 curl 下载摘要。

## 4. 逐项复核与剩余关闭条件

### B21-C32 — P2 / OPEN

**权威条件：** 第二十五次复核 L86。**位置证据：** 正文 L60、L72、L78、L82–84、L109–114、L118、L131–138；第二十六轮映射 L316。

**认可并保留：** 宿主内核驱动、注入用户态组件、镜像自带库的分层和既有 Allocate/CDI/OCI 连接；节点与许可分开；L112 已区分缺方法与缺采样，L118 已将缺映射规则置于无法确定优先。不把诚实 unknown 本身记作事实错误，不重开 C30/C31。

**仍未满足：**

1. **扫描范围及逐库来源连接仍缺设计。** L60 仍为“所选扫描配置”，L72 仍为“来源层字段，以实际输出为准”，没有选定范围、必要输出字段，以及包/文件路径与层的解析/连接键。digest→层清单→SBOM→宿主来源→挂载→目标的箭头不能替代可核对的逐库连接规则。抽查 12 只支持工具入口，不由审阅者补读替作者完成选型；不要求实际生成 SBOM。
2. **逐 ordinal 稳定映射仍明确未交付。** L78 原文仍为“稳定物理标识映射方法（未交付，unknown）”；L82–84 是待填表，不是来源支持的连接规则。须交付可见集快照→分配 ID/CDI 名或传递字段→完整节点（类型、major/minor、路径及来源）→稳定身份的关联方法。抽查 13 的可用范围管理不能承担该证明，数量或编号文本相同也不能替代关联。
3. **分类未同步到共同记录。** L109 的“未记录即缺失”、L110 的“无法确定写 unknown”、L111 的“同上”仍未共同记录缺方法/缺采样原因、具体缺项和证据定位；L114 及 L131–138 的比较亦未统一引用。L112 的局部分类保留，但不能把明确缺方法的行改称仅缺现场样本。映射 L316 的“分类同步”不构成已落实证据。

**剩余关闭条件：** 按固定来源交付所选扫描范围、必要字段、包/文件/层解析与逐库来源连接，以及完整逐 ordinal 稳定映射；把缺方法/缺采样原因、具体缺项、证据定位的公共规则同步到核对表、最小清单及 C34 比较/判定。**现场值可 unknown；不要求拉镜像、生成 SBOM、审全部 cataloger、采设备或实测，不重开 C30。**

### B21-C33 — P2 / OPEN

**权威条件：** 第二十五次复核 L101。**位置证据：** 正文 L90、L92；作者来源记录 L12、L17；登记 L5446、L5457、L5462（既有边界）；第二十六轮映射 L314。

**本轮新增认可：** L90 新增 `oci.DeviceFromPath` 失败返回 error、`addDevice` 作业 davinci/UB/manager 失败继续返回的说明，不再沿用“节点 stat 失败均可跳过”的旧归纳。新增“成功返回不单独证明挂载，目标可达不证明来自所选源，须来源-目标关联”方向正确。此前认可的 310B 产品示例、两端卡型来源不互证、输入数组形式、默认安装/base 组、父目录候选与逐库采样有别、310B 不进后续 GetProductType、VIRTUAL 与条件化 poststop 分开及登记的源码/部署产物边界均保留。

**仍未满足：**

1. **“完整……逐段对应表”仍以组名代替完整记录规则。** L90 仍写“14 尝试项”“worker 组”“UB stat 门控”，未展开所选辅助候选集合、worker/控制环境键与生成规则、UB 目录/非子目录条目规则及 manager 回退后的宿主→容器路径，也未以共同格式逐项连接条件、来源、目标、节点/许可、失败/跳过与证据位置。抽查 01–02 有这些条件可供落实；不要求填真实设备号或执行结果。L92 的支持交集 unknown 正确，但“filled 值未交付”不能把设计规则未交付改称仅缺现场值。
2. **新增错误传播规则有进展，三分短句仍需精确。** L90“作业设备/manager/UB 失败＝继续返回（warn）”中的 `(warn)` 与抽查 01 不符：作业 davinci 失败直接返回错误，UB/manager 在上层 `Errorf` 后返回；仅 310B 辅助尝试项和 dvpp 等特定分支警告后继续。应按对象分别表述，不能让“返回错误”与“仅警告继续”再次混淆。本点仍归 C33 原条件—输出—失败/跳过范围，不新增 ID。
3. **旧挂载成功判据仍与新增限定并存，逐库证据设计未补齐。** 同一 L90 后半仍写“挂载成功以 CLI 返回＋目标可达为准”，与本轮新增来源—目标限定冲突。抽查 06 中源 stat 失败与 NODRV 可成功返回而不执行该挂载，不能据目标可达证明其来自所选源。逐库格式仍只列“库文件名/版本/CLI 目标路径/挂载结果”，缺子库宿主来源与父候选/相对路径的连接、采样和实际挂载证据定位、具体缺项/原因。新增原则不能代替可填写的来源—目标证据关联规则。
4. **旧宽口径未同步清除。** L90 前后仍两次出现“runtime 库注入语义未核对，unknown”；作者记录 L17 仍把“实际库挂载/白名单/hook 可执行/dcmi 完整实现”合列 unknown，L12 的补充没有消除该宽口径。应分别明确已读默认 base/hook/CLI 机制、未读产品变体、尚缺所选记录规则和现场未采/未执行。登记 L5462 已有源码/部署产物限定，不要求重复补登记，也不以审阅者重新读取上游代替作者口径同步。

**剩余关闭条件：** 保留本轮新增错误传播和来源—目标原则；交付所选节点/许可/环境、manager/dvpp/UB、条件化 vdevice/poststop 的完整可复用记录规则，含条件、来源、目标、失败/跳过及证据位置；精确区分错误返回与仅警告分支，删除/改正残留挂载成功旧判据，落实逐库来源/挂载/缺项关联；清除正文与作者清单旧宽口径，区分机制已读、方法/记录设计缺项、现场未采。**支持交集及现场文件、设备号、库版本、结果可 unknown；不要求安装、执行脚本、实测、完整 DCMI、全部产品白名单或 CLI 审计。**

### B21-C34 — P1 / OPEN

**权威条件：** 第二十五次复核 L116。**位置证据：** 正文 L66、L118–125、L127、L131–138、L140–142；第二十六轮映射 L315。

**本轮新增认可：** L132 已映射真实入口 `flags.plugin.deviceListStrategy`、`flags.plugin.passDeviceSpecs`，说明复数是内部集合，并补列 `options.BinaryName`；不再指称完全没有真实配置键或执行器字段。L135、L137 等变体更明确引用 R1。此前认可的字段链、三阶段、新旧主体 ID、正负 open 形式、逻辑单策略、完整许可比较对象、S1/R1、单独负向授权、回退/更新/重建拆分及 NPU 独立 unknown 均保留。

**仍未满足：**

1. **设计取值与两端消费执行器仍未选定。** L132 的 passDeviceSpecs“设计值待填”、BinaryName“值待填”、基线 Toolkit mode“取 CDI 模式设计值，待填”都未完成选择；legacy 端亦未固定其执行器及 Toolkit mode。已有逻辑策略 `[cdi-cri]` / `[envvar]` 继续认可，缺口不是再补一遍策略名。抽查 07–10 表明插件配置入口、执行器和 mode 是不同层；显式 cdi mode 也可消费 NVIDIA_VISIBLE_DEVICES，不能由 envvar、无 CDI 引用和排除并行输出推定 legacy。应给每端来源支持的设计取值；原生 CRI CDI 若直达低层 runtime，应明确 NVIDIA runtime 是否参与，不参与则标 mode 不适用，而非把原生消费与包装器 cdi mode 混为一项。**不要求现场 handler 名、安装路径或实际配置输出。**
2. **资源更新接口/字段仍明确未选。** L137 已诚实改为“CPU 限制（接口/字段未选定，unknown；内存限制另立变体）”，这避免把候选字段当成已定，但未满足前次关闭条件：仍没有所选接口、完整字段、单位/语义、旧→新记录格式及同一次更新前后采样关联。抽查 11 是场景依据，不替作者完成设计选择；回退/重建不能代替资源更新变体。
3. **R1 引用和阶段序列未补齐共同证据对象。** L127 有变更前/后/恢复后，但恢复证据仍主要为配置摘要＋主体/节点/时间窗，未交付将各阶段主体（重建类新旧 ID）、完整目标节点（类型、major/minor、路径/来源）、稳定身份、时间窗、成功 open/原负向拒绝结果或未执行原因、可定位证据一一连接的公共规则。L132 已有恢复判句，不以未写“R1”字样作为独立问题；L133–138 的局部绑定/引用不能补齐共同对象的缺项。允许复用公共规则，不要求机械重复表格；关键是恢复后的正向成功及原负向边界有同阶段、同对象的证据，不能由可见性或配置摘要替代。缺负向授权只记录未执行，不要求执行。
4. **C32 方法依赖仍未闭合。** L131 的三单基线及各变体比较仍依赖未交付的稳定映射；缺方法/缺采样原因和具体缺项未统一。该项归 C32 原缺口，不另计发现，也不能代替 C34 前三项独立要求。

**剩余关闭条件：** 保留真实配置入口与三阶段/R1 引用；落实两端所选配置键的设计取值、消费执行器与 Toolkit mode/不适用边界及旁路排除；选定资源更新接口、完整字段、单位/语义与旧新记录格式；用公共规则连接每变体每阶段的主体、完整目标节点/稳定身份、时间窗、正负访问/恢复结果或未执行原因与证据定位，引用 C32 已交付方法并同步缺方法/缺采样分类。**保留 NPU 独立未知、S1/R1、负向授权与回退拆分；不要求实测、现场值、扩大生产权限或制造结果，无负向授权不执行。**

## 5. Acceptance 与最终计数

| T05-01 acceptance | 本轮判定 | 对应原发现 |
|---|---|---|
| 镜像身份、层、构建输入、SBOM/签名与拉取策略 / L5403 | 沿用此前通过，不重审，不据此宣称已有供应链系统 | C30 已 CLOSED，范围外 |
| 固定运行时/NVIDIA 版本与各层边界 / L5404 | 部分满足、未完整通过：逐库来源连接与稳定映射方法仍缺 | C31 已 CLOSED（范围外）；C32 OPEN |
| Ascend 独立实现与目标组合 / L5405 | 部分满足、未完整通过：新增语义限定认可；完整记录规则、残留判据与口径同步仍缺 | C33 OPEN |
| 清单、异常/隔离、对照与源案例 / L5406 | 部分满足、未完整通过：真实入口/R1 引用认可；设计取值、更新字段和完整阶段访问恢复关联仍缺 | C34 OPEN |

四条 acceptance：**1 沿用既有完整通过 / 3 未完整通过**。本轮 **0 CLOSED / 3 OPEN（1 P1、2 P2）**，**第二十六次定向复核不通过**，无新增发现 ID。阻断来自设计方法、记录完整性、事实语义、配置取值、证据关联及口径一致性，**不是 curl DNS 失败、现场值 unknown、未做实测或未证明整栈兼容**。不修改计划或正文审核状态，不以审阅者补读代替作者交付。

## 6. 结构校验与写入审计

- 写入前原仓库执行 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS，96 content entries / 440 sources**；只验证结构和本地链接，不验证技术正确性或远程正文。
- 原仓库构建产物不改：在 `/private/tmp/b21-t05-01-recheck26-TRARWH/validation` 独立副本中，以原仓库虚拟环境 Python、禁写字节码执行 `make check` / `make build`：写入前均 **PASS，96 content entries / 440 sources**，仅副本生成 `build/catalog.json` / `build/catalog.md`。
- 写入后原仓库 `make check` **PASS，96 content entries / 440 sources**；报告同步副本后 `make check` / `make build` 均 **PASS，同样为 96 / 440**。所有调用均禁写字节码，原仓库未执行会更新生成文件的构建。
- 文件摘要审计覆盖 **410 个**既有文件（排除 `.git`、`.venv` 与 Python/工具缓存）：无修改或删除，唯一新增为本报告；七份输入摘要与 §2 相同，剔除本报告后的 Git 状态与开始时一致。原仓库 `build/` 包含在摘要审计内；临时目录保留摘要基线、Git 状态、curl 错误与副本校验日志。
- 未运行 `make test`，因为未修改 `src/kb/` 或测试代码；未把结构检查、构建成功当作内容审核或环境验证通过。

**最终结论：B21-C32 OPEN、B21-C33 OPEN、B21-C34 OPEN；0/3 关闭，本次不通过。后续只复核上述剩余关闭条件，不重开 C30/C31，不以实测或现场值替代设计交付。**
