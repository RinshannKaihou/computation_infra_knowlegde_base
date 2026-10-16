# Batch 21 补交 T05-01 第十九次定向复核

## 1. 结论、角色与范围

- 日期：2026-10-14（Asia/Shanghai）。执行者：当前 Codex 会话，以独立审阅角色核对作者第十九轮修订，与作者修订角色分开；未派发其他模型或子代理。
- `gpt-6.1-sol / xhigh` **仅为用户约定**，不是本会话已独立确认的执行元数据。未取得可独立核验的实际模型、推理档位或路由信息，不宣称实际模型一致性或无 fallback 已获独立确认。
- 唯一范围为 **B21-C32–C34**；以[第十八次复核](batch-21-t05-01-codex-recheck-18.md) §4 三项各自的“剩余关闭条件”（原文件 L83、L103、L118）为权威。[初审报告](batch-21-t05-01-codex-review.md)用于原 ID、优先级与职责核对。C30/C31 保持此前 CLOSED、范围外，不重审。
- **0 CLOSED / 3 OPEN（1 P1、2 P2）；第十九次定向复核不通过。** 空输入 options 的排除范围、插件/hook 的 allow-link 作用域、四键定义链及登记的每列表 128 扫描行口径可以认可；但方法、所选条件及对照/恢复关联仍未交付完整。
- 新事实问题按原 **C33** 追记，不新增发现 ID：正文末尾“固定 commit 树内未见”白名单的说法不成立；同提交 `build/scripts/base.list` 及产品变体均存在，打包和安装脚本也有对应复制分支。四个子目录的有限检索不能推出整个固定树无此来源。
- 只新增本报告，不改作者正文、作者来源记录、修订映射、来源登记、计划或原仓库生成文件。保留开始时已有工作区改动；未提交或新建分支。
- 未安装组件、拉取/构建镜像、运行容器、生成 SBOM、采集设备、接入集群、改变运行配置或执行访问/负向/恢复实测。知识库结构校验与目录构建不构成容器或硬件验证；所读上游脚本没有执行。

| 原 ID | 原优先级 | 本轮状态 | 位置证据与主要剩余问题 |
|---|---|---|---|
| B21-C32 | P2 | OPEN | 正文 L59、L71、L77、L81–83、L108–113、L117、L130–137：扫描归层及逐 ordinal 稳定映射方法仍缺；缺方法/缺采样分类未全量同步 |
| B21-C33 | P2 | OPEN | 正文 L30、L41、L89、L91、L146；作者记录 L12、L17；登记 L5335、L5446、L5451：局部事实修正成立，完整所选条件表、必要库源/目标和三分口径仍缺；“固定树未见白名单”须纠正 |
| B21-C34 | P1 | OPEN | 正文 L126、L130–137：两端完整模式配置、资源更新接口/字段、成功访问及原负向边界恢复的逐变体关联仍缺，且依赖 C32 未交付方法 |

## 2. 输入身份与写入边界

用户提供的 **4 个 SHA-256 前缀全部吻合**。以下为本轮独立计算的完整摘要；正文、作者记录、登记与计划的仓库行号均对应这些输入原文件，不是网页阅读器坐标。

| 输入 | SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md) | `6daf22d9226d9d54094467f2797b9056509fcffb712809a5643671b2adc30719` |
| [作者来源记录](batch-21-t05-01-sources.md) | `e256c4c6ad70f328f1c95000a1ea58227b10875ecc9de6dac8d5390051feb6d8` |
| [修订映射](batch-21-review-fixes.md)，第十九轮节 L269–272 | `af4bc4753d1b9c288518541202ff2c72813ae3f86d4446e0f8cc40be1a9978bf` |
| [前次复核](batch-21-t05-01-codex-recheck-18.md) | `04091edf0c0397d341a0ecac2791294d1a04cad410f534473f0b6ba37dff3ede` |
| [初审报告](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` |
| [任务验收](../../plans/full-coverage-backlog.yaml)，T05-01 acceptance L5403–5406 | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml) | `adb483196d3c4ab8ce33a6cb545f6834e9e608c03cec6d70705182ec9e102c77` |

修订映射仅作为作者落盘改动说明，不作为关闭证明。已读取 `README.md`、`docs/authoring-guide.md` 并核对 `content-outline.md` 的 05.1 主归属/边界；`docs/` 下未发现更深层 `AGENTS.md`。写入前将 Git 所列 tracked/untracked 非忽略文件及既有 build 文件做摘要快照和临时副本，位置为 `/private/tmp/b21-t05-01-recheck19-e_7cv6je`，供单文件写入审计与隔离构建使用。

## 3. 一次源抽查方法、文字与限制

### 3.1 curl 实际尝试

实际对下表 **13 个**精确 URL 执行只读 GET：

```sh
curl --location --fail --silent --show-error --connect-timeout 8 --max-time 20 "$url"
```

未使用 `-k`/`--insecure`，未更改默认 TLS 校验配置。全部在 DNS 阶段失败，退出码均为 **6**，分别报 `Could not resolve host: raw.githubusercontent.com`、`docs.nvidia.com` 或 `docs.pytorch.org`；没有取得 HTTP 正文，不能报告 curl 200、TLS 校验成功或独立字节摘要。后改用允许的**只读 GitHub 连接器**读取固定 ref 文件，以及**网页读取通道**打开精确版本页并定位正文；不是仅判可达性，也未将搜索片段作为结论依据。

### 3.2 本轮重新读取的关键文字

下表 Ascend 文件均固定到 commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e`。GitHub 连接器按原文件区间读取；网页按章节定位，不把网页阅读器行号拼成源码锚点。

| curl 点 | 精确一次源 / 实际核对位置 | 核对文字与有限支持范围 |
|---|---|---|
| 01 | [hook/process/process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/hook/process/process.go)，L18–410 | 默认 mount group、每列表扫描行计数、路径/stat 分类、allow-link 空值转 False、CLI 参数构造及条件 `--options`、exec 已读；没有以此证明实际挂载 |
| 02 | [runtime/process/process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go)，L60–130、L243–405、L455–812、L850–910 | 非 VIRTUAL 时仍调用 CreateVDevice；有效 ID 改设备集合/options 并加 poststop；addDevice 独立读更新后的 options；manager/产品/UB、节点与 rwm、env 与独立挂载处理分开 |
| 03 | [ascend-common/api/default_name.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/api/default_name.go#L145)，L145–182 | 四个环境键与配置目录确为常量定义；不等于现场值或支持交集 |
| 04 | [NVIDIA server.go@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go#L280)，L280–481 | AnyCDIEnabled 与 AllCDIEnabled 分别判断；非全 CDI 策略下仍按条件添加 env、volume 或 DeviceSpecs，支持要求固定完整策略集合 |
| 05 | [Toolkit 1.20.0 CDI support](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html)，Running a Workload / Non-CDI-Enabled Runtimes / Setting the CDI Mode Explicitly | 独立 NVIDIA Runtime Hook 与 CDI 路径应区分；CDI 模式也能消费选择环境变量，变量存在不能单独证明 legacy |
| 06 | [Toolkit 1.20.0 troubleshooting](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html)，NVML / Containers losing access / Affected Environments / Mitigations | 权限拒绝与 hook/legacy 更新后访问丢失分开；CPU/内存限制更新及 CDI/重建的来源条件已读，但不替作者选择更新接口/字段或提供恢复结果 |
| 07 | [syft README@v1.54.1](https://github.com/anchore/syft/blob/v1.54.1/README.md)，Features / The basics | 支持扫描对象与输出格式入口；未替本文交付所选范围、必需字段与逐库归层规则。不重开 C30 |
| 08 | [PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html)，Device-agnostic code 的 CUDA_VISIBLE_DEVICES 段 | 说明管理 PyTorch 可见 GPU；该段不是本文逐 ordinal 全链连接规则，不据此声称其他身份接口不存在 |
| 09 | [build/scripts/base.list](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/scripts/base.list)，完整五行 | 有 driver 的 lib64/include、dcmi、npu-smi、queue_schedule 五项候选；固定提交的列表源可读，不是只能等现场部署才知其源码内容 |
| 10 | [build/scripts/run_main.sh](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/scripts/run_main.sh)，L1–330，重点 L278–315 | 定义安装配置目录；不同安装产品选择不同 base.list 源，统一复制为配置目录下 base.list，部分分支调用 add_so；不证明现场安装采用了哪份文件 |
| 11 | [build/build.sh](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/build.sh)，L105–182 的 copy_file_output | 将源码 scripts/base.list 及产品变体复制进安装包；不能把“部署产物”解读为无可读取的源列表 |
| 12 | [cli/src/main.c](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/cli/src/main.c)，L220–文件末 | 参数/列表转 ParsedConfig，使用目标 PID 的 mount namespace 并调用 DoMounting；只读静态控制流，不是 CLI 执行结果 |
| 13 | [cli/src/u_mount.c](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/cli/src/u_mount.c)，L18–文件末 | MountFile/MountDir 拼接 rootfs 与候选路径，执行 bind 后只读/nosuid remount；DoMounting 有 NODRV 条件。源/目标规则存在，实际文件、成功结果及所有校验分支并未据此确认 |

另以连接器补读同提交 [common.go L90–136](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go#L90)、[constants.go L18–100](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/constants.go#L18)、[device-plugin/go.mod L103–112](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/go.mod#L103)、[plugin.go L1087–1101/L1153–1172](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go#L1087) 与 docker-runtime README，独立确认归属/输出/互斥路径；这些不是新增 curl 成功记录。

目录证据由固定提交 Contents → 返回 tree SHA → 只读 Git Trees 获取：runtime/install/assets/hook 子树所示范围内未见 `.list`，assets 为两张图片；**build 子树另有 `scripts/base.list` 和五个产品变体**，见[固定提交的 scripts 目录](https://github.com/Ascend/mind-cluster/tree/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/scripts)。build tree SHA 为 `413f2877a582b6f5b82611d9b314ec9349f6ca94`。不以有限目录列表作全仓库穷尽证明；上表 09–11 的正面文件正文已经足以反证“固定树未见”。

连接器返回的关键 blob SHA：hook `816212afa5f69b8edfb1554d3935af2ebcd28f06`、runtime `acbd7a1ec0703498abfcfcb6ce1aa493069091b1`、default_name `4bc4f25f076ff992542b3032fe785fd4de4d6ef7`、base.list `4ea1b223fdeed19fed7fdf1a3b4457b8ddd747b3`、build.sh `34322058d3784446ce7475bdf7853588c0bb265b`、run_main.sh `9be36636ff13c480c57342b81c78f4b74e95675b`、CLI main `af622dc4b9bfbefc55acf2feffd1b2ec4f549c44`、u_mount `d85fd8155a1805edaf509b047c6441bcdc603e12`。这是上游文件身份，不是 curl 字节摘要或现场证据。补充文件属于既有 MindCluster 固定实现的取证范围；本轮只在报告引用，未改来源登记，也未复制外部全文。

## 4. 逐项定向判定

### B21-C32 — P2 / OPEN

**权威条件：** 前次复核 L83。**位置证据：** 正文 L59、L71、L77、L81–83、L108–113、L117、L130–137；第十九轮映射 L269–272 没有列出本项方法补交。

**认可/保留：** 宿主内核驱动、注入用户态组件、镜像库的分层，Allocate/CDI/edits/最终 OCI 连接，节点与许可/LSM 分离，以及不以数量/编号证明同一设备，继续认可。L111 已区分缺方法/缺采样，L117 有缺规则优先门槛；不重开 C30/C31。

**仍未满足：**

1. L71 仍使用“所选扫描配置”“字段以实际输出为准”“缺项逐项记 unknown”，没有固定扫描范围/必要字段、成分或路径到镜像来源层的解析规则，以及逐库身份与宿主来源→最终挂载→容器目标各段的连接键。L59 的包名/版本/来源层比对字段与层清单不能代替该方法。抽查 07 不支持把 README 能力入口当作方法已交付；缺的是设计与依据，不是现场 SBOM。
2. L77 仍明确写“稳定物理标识映射方法（未交付，unknown）”，L81–83 是待填表；没有来源支持的可见集快照/ordinal→分配 ID 或 CDI 名/传递字段→完整节点（类型、major/minor、路径/来源）→稳定身份连接规则。抽查 08 只支持可见集管理，不填补本文方法。
3. L108“未记录即缺失”、L109“无法确定写 unknown”、L110“同上”、L113“按已取证映射对应”和 L130–137 尚未统一连接到已交付规则及“原因、缺项、记录格式”；L111 的局部修正不能全量替代。C34 三单比较因此仍缺可用的物理对应前提。

**剩余关闭条件：** 按固定来源交付所选扫描范围、必要字段、逐库归层及宿主来源→最终挂载→容器目标连接规则；交付逐 ordinal 的完整稳定映射方法。将缺方法/缺采样的原因、缺项和记录格式同步到核对表、清单及 C34 依赖比较/判定。**现场值可 unknown；不要求拉取镜像、生成 SBOM、审计全部 cataloger、采集设备或实测；不重开 C30。**

### B21-C33 — P2 / OPEN

**权威条件：** 前次复核 L103。**位置证据：** 正文 L30、L41、L89、L91、L146；作者记录 L12、L17；第十九轮映射 L271–272；登记 L5335、L5446、L5451。

**本轮已确认的修正，不再列为剩余缺口：**

- 正文 L89 已将空输入 options 限定为只排除 VIRTUAL 提前返回，并保留 CreateVDevice 返回有效 ID 后修改设备集合/options 与 poststop 的条件。抽查 02 的 addHook/updateEnvAndPostHook/addDevice 支持此修正，不再沿用前轮“二者均不触发”的指摘。
- L89 已区分插件 310B 专属 allow-link 写入与 hook 的独立解析：hook 空值按 False 处理，getArgs 仍传 `--allow-link`。抽查 01 与补读 common.go 支持，不能再称作者未区分这两个作用域。
- 两处旧“api 包字符串值未定位”的具体错误说法已替换；兄弟模块、四个环境键和配置目录定义链重新核对属实。插件输出三个别名与 hook 另消费 mounts 键继续分开。
- 登记 L5446 已同步为**每份 `.list` 扫描行数上限 128**，不是合并挂载总数；L5451 已说明 CLI 参数构造已读。机制、定义与参数构造不因缺现场输出重新变成未定位。

**仍未满足及原 ID 内事实追记：**

1. **所选完整条件/节点/许可/环境表仍缺。** L89 仅选 `UseAscendDocker=true`、输入 options 为空和默认 mount group `base`，没有固定具体芯片/产品、输入 ID 的设计选择、PresetVDevice、manager/UB 等条件并形成对应表；L91 仍只列目标组合字段/未知条件。抽查 02 还有非空且非 910A5 的 `dvpp_cmdlist` 尝试、产品型选择及 UB 目录项分支，当前泛列芯片摘要不替代所选样板的完整对应。虚拟/poststop 条件文字修正成立，但仍须纳入所选对应表或有依据限定分支；无需取得实际 DCMI 返回值。
2. **“固定树未见白名单”不成立，按 C33 追记。** L89 的 runtime/install/assets/hook 四子目录检索可以保留其有限范围；但 L146 扩成“固定 commit 树内未见”，遗漏同提交 [build/scripts/base.list](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/scripts/base.list)。[build.sh 的 copy_file_output](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/build.sh#L120)复制它及产品变体进安装包；[run_main.sh L278–315](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/scripts/run_main.sh#L278)按产品安装分支选源并复制为配置目录的 base.list。故“安装后的列表是部署产物”可以成立，**“源码列表不可读/必须待部署才能取其来源内容”不能由此推出**。默认 mount group 名也不自动选定安装产品变体。该追记直接涉及前次要求的所选白名单/必要库，不新增 ID，不扩为全部安装流程审计。
3. **必要库源/目标仍未落盘交付。** 作者记录 L12 仍明确“所选列表内容/CLI 源目标”未读。本轮抽查 09 读到 driver lib64 等候选；抽查 12–13 读到候选路径经 rootfs 拼接、目标 PID mount namespace、bind/remount 的静态消费链，说明该部分有可读依据。正文仍未为所选列表选择必要库及其宿主来源→CLI 消费条件→容器目标记录；目录候选不能当作每个库的名称/版本已知，也不能当作挂载成功。**审阅者补读到源码不等于作者已交付样板**，不能据本报告直接关项。
4. **三分口径未全篇同步。** 定义链和 128 行/CLI 参数两处修正认可；但作者记录 L17 仍把“实际库挂载/白名单/hook 可执行/dcmi 完整实现”合列 unknown，未分别定位机制已读、所选列表/CLI 源目标未交付与现场结果未采。正文 L89 尾部还把“设备节点/环境/库挂载的环境变量与白名单未取源”合列；L30/L41 的“白名单未取”亦应限定是所选内容/现场文件，而非机制或源码不存在。L146 与登记 L5446 的目录检索说明须同时区分有限检索和 build/scripts 的正面来源。

**剩余关闭条件：** 保留空 options、allow-link、兄弟模块/四键、每列表扫描行与条件参数的已确认修正。为所选样板固定必要芯片/产品、输入 ID/options、PresetVDevice、安装列表变体/mount group、manager/UB 等设计条件，交付完整节点/许可/环境对应表，条件化保留或限定虚拟/poststop。读取并选择同提交所需白名单及必要库来源/目标，交代源码→打包/安装选择→hook 候选→CLI 消费规则→容器目标，纠正固定树无列表的说法；精确同步正文/作者记录/登记的三分口径。**现场文件/设备号/库版本和挂载结果可待采，支持交集可 unknown；不要求安装、运行上游脚本、完整 DCMI/全部白名单或 CLI 审计、实测，也不要求重开已确认定义链。**

### B21-C34 — P1 / OPEN

**权威条件：** 前次复核 L118。**位置证据：** 正文 L108–113、L117–124、L126、L130–137、L139–141；第十九轮映射没有列出本项对照设计补交。

**认可/保留：** 策略可多选、CDI 自身 hooks 与独立 legacy 区分、有序完整许可规则比较、S1/R1、旧新主体/时间窗、回退与更新/重建拆分、副本数解释收窄、NPU 独立方法未知、源案例/未执行与授权边界继续认可。L126 已有公共证据对象格式，不说完全没有对象，也不要求各行机械重复。

**仍未满足：**

1. **两端完整配置对仍未选定。** L131 基线仍是策略“含 cdi-cri”，变体仍是“envvar 或 volume-mounts”；未定两端完整策略集合、runtime 模式/handler 消费组合与传递字段。抽查 04 表明策略组合可同时产生不同传递字段，抽查 05 表明 CDI 模式也可消费选择环境变量。混合证据→无法确定是判断边界，不是选定受控配置对；现场 handler 名及旧新值可以待填。
2. **资源更新接口/完整字段仍缺。** L136 仍将 CRI 更新对象/OCI `linux.resources.cpu` 写为候选，明示“固定字段未取，unknown”。抽查 06 只支持该类更新场景；设计仍须选择一个接口及完整字段，交代单位/语义和旧新记录格式，绑定同一更新生命周期前后采样。镜像/驱动回退与重建不替代这一对照。
3. **R1 成功访问、原负向边界恢复及逐变体绑定仍不足。** L126 有 audit/AVC 路径、进程/设备/时间三元组和恢复后配置摘要，却未选定受控成功访问操作/结果记录、单独授权负向拒绝的记录形式，以及将它们绑定各变体更新/重建前后和恢复后主体、目标节点/稳定身份、时间窗的统一连接键。L132/L134–137 仍主要依赖拒绝事件/注入集/“同上”。未见拒绝、配置摘要或可见集恢复，不等于受控访问成功及原负向边界恢复；公共格式可复用，但须具体到生命周期证据关联。
4. **C32 方法依赖未闭合。** 三单物理对应仍依赖未交付的稳定映射；缺方法/缺采样分类未全量同步。此处引用同一 C32 缺口，不新增 ID，也不把它替代上述对照/恢复设计要求。

**剩余关闭条件：** 固定两端完整传递策略集合、runtime 模式/handler 消费组合、字段与旁路排除；保留 CDI 自身 hooks/独立 legacy 区分和许可比较字段。选定资源更新接口、完整字段、单位/语义及旧新记录格式。完善受控成功访问及原负向边界恢复的设计记录，按各变体更新/重建生命周期关联主体、目标节点/身份、时间窗与可定位结果；可统一引用公共规则。引用 C32 已交付方法，缺方法时优先无法确定并区分缺采样。保留 NPU 独立对照未知、S1/R1、回退拆分及所有授权/安全边界。**不要求执行试验、取得现场值、扩大生产权限或制造结果；无负向授权不执行。**

## 5. Acceptance 与最终计数

| T05-01 acceptance / 原文件位置 | 本轮判断 | 原 ID |
|---|---|---|
| 镜像身份、构建输入、SBOM/签名、拉取策略 / L5403 | 沿用此前完整通过；范围外，不重审供应链 | C30 CLOSED |
| 固定 runtime/Toolkit/CDI、各层与映射分离 / L5404 | 部分满足，未完整通过：扫描归层、稳定映射与分类同步仍缺 | C31 CLOSED（范围外）；C32 OPEN |
| Ascend 独立实现与目标组合 / L5405 | 部分满足，未完整通过：局部事实修正认可；所选条件/必要库源目标与同步仍缺，列表检索结论须纠正 | C33 OPEN |
| 清单、异常/隔离、对照与源案例 / L5406 | 部分满足，未完整通过：完整配置对、更新字段、访问/恢复关联与映射依赖仍缺 | C34 OPEN |

四条 acceptance 汇总：**1 沿用既有完整通过 / 3 未完整通过**。本轮 **0 CLOSED / 3 OPEN（1 P1、2 P2）**，**第十九次定向复核不通过**，无新增发现 ID。阻断依据是未交付的方法/条件/证据关联及 C33 固定树列表结论问题，**不是 curl DNS 失败、现场值 unknown、没有实测或未证明整栈兼容**。本报告不变更正文、计划或验收状态。

## 6. 结构校验与写入审计

- 写入前原仓库 `PYTHONDONTWRITEBYTECODE=1 make check` **PASS：96 content entries / 439 sources**，仅验证结构与本地链接。
- 写入后原仓库 `PYTHONDONTWRITEBYTECODE=1 make check` **PASS：96 content entries / 439 sources**。
- 将本报告同步到 §2 临时副本，使用原仓库虚拟环境 Python、禁写字节码执行 `make check` / `make build`，均 **PASS：96 content entries / 439 sources**。仅在副本重新生成 `build/catalog.json` / `build/catalog.md`，未重写原仓库生成文件；本节补记后再同步最终报告并复跑同样校验/构建。
- 摘要审计覆盖 **402 个**既有文件（Git 所列 tracked/untracked 非忽略路径及既有 build 文件）：既有文件摘要不变，无删除；唯一新增为本报告。去除本报告后的 Git 状态与写入前快照相同，七个输入保持 §2 摘要。报告仅有 C32/C33/C34 三个原发现标题，优先级/OPEN 状态吻合；报告行尾空白和 `git diff --check` 检查通过。
- 未修改 `src/kb/` 或测试，不需要 `make test`；所有技术状态仅按 §4 判断，结构/构建不替代技术或硬件验证。

**最终技术结论：B21-C32、B21-C33、B21-C34 均 OPEN；0 CLOSED / 3 OPEN，第十九次定向复核不通过。C30/C31 保持此前 CLOSED、范围外；本轮局部修正已认可，C33 的白名单来源问题仍按原 ID 追记；约定审阅配置不是已独立确认的执行元数据。**
