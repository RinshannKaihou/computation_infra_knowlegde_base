# Batch 21 补交 T05-01 第二十四次定向复核

## 1. 结论、角色与范围

- 日期：2026-10-14（Asia/Shanghai）。执行者：当前 Codex 会话，以独立审阅角色核对作者第二十四轮修订，与作者修订角色分开；未派发其他模型或子代理。
- `gpt-6.1-sol / xhigh` **仅为用户约定，不是已独立确认的执行元数据**。本会话没有可独立核验的底层实际模型、推理档位或路由证据，不宣称已独立确认模型一致性或无 fallback。
- 唯一复核范围：**B21-C32–C34**。剩余关闭条件以[第二十三次复核](batch-21-t05-01-codex-recheck-23.md) L87、L106、L121 为权威；[初审报告](batch-21-t05-01-codex-review.md)用于核对原 ID、职责和优先级。**C30/C31 保持此前 CLOSED，范围外，不重审。** 修订映射仅说明作者落盘改动，不代替关闭证据。
- **0 CLOSED / 3 OPEN（1 P1、2 P2）；第二十四次定向复核不通过。** 本轮认可整数 ID 数组的设计形式、Ascend 逐段条件说明的补充、来源登记的源码/部署产物边界，以及 R1 新选定的正负向 open 记录形式；这些进展不再列为完全未交付。
- 只新增本报告，不修改作者正文、来源记录、修订映射、登记、计划或原仓库生成文件，保留开始时已有工作区改动；不提交、不创建分支。不新增发现 ID，剩余问题归原 ID 追记。
- 未安装组件、拉取/构建镜像、生成 SBOM、运行容器、采集设备、接入集群、修改运行配置或执行访问、负向、资源更新、恢复实测；上游源码及安装脚本只读，不执行。知识库结构检查/目录构建不是环境或硬件验证。

| 原 ID | 原优先级 | 本轮状态 | 位置证据与剩余问题 |
|---|---|---|---|
| B21-C32 | P2 | OPEN | 正文 L60、L72、L78、L82–84、L109–114、L118、L131–138：固定扫描/逐库归层连接、逐 ordinal 稳定映射仍未交付，缺方法/缺采样分类尚未贯通相关记录 |
| B21-C33 | P2 | OPEN | 正文 L90、L92；作者来源记录 L12、L17；登记 L5446、L5457、L5462：输入形式与登记边界有进展，完整所选条件/输出、逐库证据关联及正文/作者 unknown 口径仍未齐 |
| B21-C34 | P1 | OPEN | 正文 L66、L127、L131–138：已选择正负 open 记录形式；两端字段级消费配置、资源更新接口/字段、分阶段访问恢复关联及 C32 方法依赖仍缺 |

## 2. 输入身份与写入边界

用户给定的 **5 个 SHA-256 前缀全部与当前整文件吻合**。修订映射只审 T05-01 第二十四轮修订节 L300–304，不把旧轮次的改动清单或执行记录当成本轮关闭证据。来源登记经 YAML 解析为 **440 项**。以下完整摘要由本轮独立计算；本报告中的仓库行号均为这些输入原文件坐标。

| 输入 | SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md)，指定前缀 `77d5c1086f3b3330` | `77d5c1086f3b333084ab04de8665793eb332dcfc3f968a06e044a61cc02de812` |
| [作者来源记录](batch-21-t05-01-sources.md)，指定前缀 `b1f84b609211aeda` | `b1f84b609211aeda978cc14c5551ff74ac5648c305793681dc44d921c588aed2` |
| [修订映射](batch-21-review-fixes.md)，指定前缀 `30eb3141359ed379` | `30eb3141359ed379a995ff77a3ba38fdaf1a0aa24e33adcb3c50826992eb8fa7` |
| [第二十三次复核](batch-21-t05-01-codex-recheck-23.md) | `118bb1986944e092f56234f240d667372164722f3a6adc72e17dbbd54223eb79` |
| [初审报告](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` |
| [任务验收](../../plans/full-coverage-backlog.yaml)，T05-01 acceptance L5403–5406 | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml)，指定前缀 `af8d7441ba9fb3da` | `af8d7441ba9fb3da5413475200b8a75278586877e06dc004d70a89ef4453d4b8` |

从 `README.md`、`docs/authoring-guide.md`、`content-outline.md` 开始核对仓库规则，并读取元数据 schema、初审与前次复核。取证/校验目录为 `/private/tmp/b21-t05-01-recheck24-uizLMA`；不把临时响应、日志或副本构建产物写入知识正文/来源登记。

## 3. 一次源抽查方法、文字与限制

### 3.1 curl 实际尝试与只读替代通道

对下表 01–12 的精确 HTTPS 地址实际执行只读 GET。源码以所列 blob 链接的相同 ref/path 请求 `raw.githubusercontent.com`，文档用所列原地址。命令形态：

```sh
curl --location --fail --silent --show-error \
  --connect-timeout 8 --max-time 20 --output "$audit_dir/curl-$point.body" \
  --write-out 'http_code=%{http_code}\n' "$url"
```

保留默认 TLS 校验；未用 `-k`/`--insecure`，未申请提权或自定 IP 绕行。**12 次均在 DNS 阶段失败：退出码 6、HTTP 000、Could not resolve host**，涉及 `raw.githubusercontent.com`、`docs.pytorch.org`、`docs.nvidia.com`。没有取得 curl HTTP 正文，不能称 curl 200、TLS 握手/校验成功或已取得上游 HTTP 字节摘要。请求清单、退出码和错误保存在临时目录 `curl-urls.tsv`、`curl-01.meta` 至 `curl-12.meta` 及对应 `.stderr`。

随后使用用户允许的只读通道：GitHub 连接器 `fetch_file` 实读固定 ref 的原文件区间，网页读取通道实开版本化 PyTorch/NVIDIA 文档并核对相关段落文字；**不只判可达性，也不以搜索片段、作者自述或前次摘录代替本轮实读**。网页经过解析且可能来自缓存（本次 NVIDIA 排障页显示缓存抓取时间为三日前），不等同本机 curl 新鲜原始字节；连接器 Git blob SHA 不是 curl HTTP SHA-256。源码坐标采用连接器原文件请求区间，不把网页阅读器行号拼成 GitHub 原文件锚点。未执行上游示例，不独立背书历史 curl 成功记录。

### 3.2 本轮实读点及有限支持范围

Ascend 文件均固定 commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e`。这些抽查属于已有登记来源，不新增来源项；表中编号只是取证点，不是发现 ID。

| curl 点 | 精确一次源 / 本轮实读位置 | 核对文字与有限支持范围 |
|---|---|---|
| 01 | [build/scripts/base.list](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/scripts/base.list)，完整五行 | 默认源码列表含 driver/lib64、driver/include、dcmi、npu-smi、queue_schedule 五个宿主路径；不是逐库身份/版本或挂载成功记录 |
| 02 | [run_main.sh](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/scripts/run_main.sh)，L278–315 | 五个产品分支之外复制默认 base.list；安装后目标统一为配置目录 base.list，chmod 440。支持源码列表与部署产物的区分，不证明产品配套或安装成功 |
| 03 | [cli/src/u_mount.c](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/cli/src/u_mount.c)，L45–240 | 目标拼接 rootfs 与源路径；源 stat 失败可跳过，建目标/校验/bind/只读 remount 可失败。NODRV 的提前返回限定该 CLI 的 DoMounting，不证明整个 runtime 没有其他挂载 |
| 04 | [runtime/process/process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go)，L45–405、L455–830 | 核到芯片分类、节点信息→OCI 节点/allow rwm、310B 的 14 个辅助尝试及警告、manager 回退并映射容器 manager 名、dvpp 条件、UB 目录条目规则；310B 提前返回，不执行后续 GetProductType。非 VIRTUAL 仍可能创建 vdevice 并加 poststop；LD_LIBRARY_PATH/DP mounts 与 hook 库挂载分开 |
| 05 | [device-plugin common.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go)，L90–145 | 整数 ID 逐个转字符串并逗号拼接；写 options；插件 RealCardType 为 310B 才写 allow-link；!PresetVDevice 才写七个 worker 环境字段。不证明两端卡类型一致 |
| 06 | [hook/process/process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/hook/process/process.go)，L85–225、L237–440 | 默认组 base；每份列表计行后按 stat 分类文件/目录，构造 CLI 参数，另处理存在的 UB 挂载项。lib64 入选是目录候选入选，不是 hook 已逐库分类的证据 |
| 07 | [Syft README@v1.54.1](https://github.com/anchore/syft/blob/v1.54.1/README.md)，L1–110，Features/The basics | 核到镜像/目录扫描与输出格式、配置/schema 入口；这些入口不替作者选择扫描范围、必要字段、包/文件/层解析与逐库连接键。不重开 C30，也不推断其他材料不存在 |
| 08 | [PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html)，Device-agnostic code 的 CUDA_VISIBLE_DEVICES 段 | 该段说明管理 PyTorch 可用 GPU 范围，不交付本文 ordinal→分配/CDI→完整节点→稳定身份的连接方法；不据此否认其他身份接口 |
| 09 | [NVIDIA server.go@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go)，L280–507 | Allocate 校验请求 ID，策略转换/去重后输出 CDI 或环境变量/volume mounts；全 CDI 策略提前返回，非 CDI 输出还受 PassDeviceSpecs 条件影响。插件策略不等于消费端模式 |
| 10 | [Toolkit 1.20.0 troubleshooting](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html)，NVML/SELinux、访问丢失、Affected Environments | 核到关闭 SELinux 的隔离代价；hook/legacy 修改未被低层 runtime 感知，容器更新可丢 GPU 访问；CPU/内存显式更新和 systemd reload 的条件不同。源场景不代替本文所选更新接口/字段或恢复结果 |
| 11 | [Toolkit 1.20.0 CDI support](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html)，Running a Workload、Non-CDI-Enabled Runtimes、Setting the CDI Mode Explicitly | 核到 hook/CDI 冲突及显式 CDI mode；NVIDIA_VISIBLE_DEVICES 也可用于 CDI 消费。因此 envvar/无插件 CDI 引用本身不能证明消费端是 legacy 或无并行注入 |
| 12 | [containerd CRI config@v2.4.1](https://github.com/containerd/containerd/blob/v2.4.1/docs/cri/config.md)，L1–160、L240–385 | 核到 version 3、default_runtime_name、runtimes.<handler>.runtime_type/options.BinaryName、RuntimeClass→handler、runtime 分区 cdi_spec_dirs。支持消费设计所需字段，不证明本文已把它们分别绑定至两端；不重开 C31 |

连接器返回的文件身份：`base.list=4ea1b223fdeed19fed7fdf1a3b4457b8ddd747b3`；`run_main.sh=9be36636ff13c480c57342b81c78f4b74e95675b`；`u_mount.c=d85fd8155a1805edaf509b047c6441bcdc603e12`；runtime `process.go=acbd7a1ec0703498abfcfcb6ce1aa493069091b1`；`common.go=6cd038e9f1d67a8a913aa4bb1301692f177b3dbe`；hook `process.go=816212afa5f69b8edfb1554d3935af2ebcd28f06`；Syft `README.md=9ffd2affa3b00031ea1fd01ee3fe228379978492`；NVIDIA `server.go=9281b48ef52f9eda9cbed6d98491729da85b5a75`；containerd `config.md=3a206263f4f9e76b6ca14110461b8661a03b1619`。均为连接器返回的 Git blob SHA，不是本机 curl 下载摘要。

## 4. 逐项定向复核

### B21-C32 — P2 / OPEN

**权威条件：** 前次复核 L87。**位置证据：** 正文 L60、L72、L78、L82–84、L109–114、L118、L131–138；本轮映射 L304。

**认可/保留：** 已有的宿主内核驱动/注入用户态组件/镜像库分层，Allocate/CDI/edits/OCI 连接，节点/许可分离继续认可。L112 明确缺方法/缺采样，L118 规定缺映射规则优先无法确定，均保留；不重开 C30/C31。

**仍未满足：**

1. **扫描与逐库来源连接仍未交付。** L60/L72 仍写“所选扫描配置”“来源层字段，以实际输出为准”，没有固定扫描范围、必要输出字段、包/文件路径与来源层的解析和连接键。层清单、diff_ids、annotations 与链条箭头不能替代逐库来源→最终挂载→容器目标的可核对连接。抽查 07 只支持工具与材料入口，不是在要求本轮生成真实 SBOM。
2. **完整稳定映射仍明确缺方法。** L78 原文仍为“稳定物理标识映射方法（未交付，unknown）”；L82–84 仍是待填表。未交付固定来源支持的逐 ordinal 可见集快照→分配 ID/CDI 名或传递字段→完整节点（类型/major/minor/路径与来源）→稳定身份规则。抽查 08 的可见范围管理不等于该连接；数量或编号文本相同不能代替设备身份关联。
3. **分类同步尚未贯通。** L109“未记录即缺失”、L110“无法确定写 unknown”、L111“同上”，与 L112 的细分未形成共同的缺方法/缺采样原因、具体缺项和证据定位格式；L114、L131–138 的比较也未统一引用。认可已写的局部分类，不把诚实标 unknown 当作交付缺失方法。

**剩余关闭条件：** 按固定来源交付所选扫描范围、必要字段、包/文件/层解析与逐库来源连接，以及完整逐 ordinal 稳定映射；把缺方法/缺采样原因、具体缺项、证据定位的共同记录规则同步至核对表、最小清单及 C34 比较/判定。**现场值可 unknown；不要求拉镜像、生成 SBOM、审计全部 cataloger、采设备或实测，不重开 C30。**

### B21-C33 — P2 / OPEN

**权威条件：** 前次复核 L106。**位置证据：** 正文 L90、L92；作者来源记录 L12、L17；登记 L5446、L5457、L5462；本轮映射 L302。

**本轮新增认可：**

- L90 新增输入 ID“设计形式为整数 ID 数组，值待采”，并重新串联插件卡型、路径 A/B、env/wrapper 与 runtime 分支。**不再列“输入 ID 设计形式完全未选”。** 两端卡型来源不互证、310B 提前返回与条件化 vdevice/poststop 继续认可，不要求 310B 执行后续 GetProductType。
- L90 已把默认 base 的 lib64 标为目录候选并给“目录存在”条件，保留逐库文件名/版本/入选/目标/结果待采字段；不是完全没有父目录条件。实际库名、版本、挂载结果可 unknown。
- 作者来源记录 L12 已加“机制已读、所选记录未交付、现场未采”三分提示；登记 L5462 已明确源码列表在 build/scripts、安装后文件为部署产物并关联 install 逻辑。**这项登记边界补充予以认可，不再列为未补；不把 L5446 的四个子目录限定改判为全树未见。**

**仍未满足：**

1. **逐段说明仍未构成完整所选条件/输出记录。** L92 产品形态仍随整组目标组合写 unknown，未给设计上所选产品形态及插件卡型/运行时芯片条件与输出的连接；真实值与支持交集可以 unknown，但不能用其代替设计选择/条件记录。L90 的“14 尝试项”“worker 组”“UB stat 门控”等仍主要是组名：所选辅助候选集合、worker/控制环境键值生成规则、UB 目录/条目规则、manager 回退后的宿主→容器重命名与节点/许可输出，未共同关联条件、失败/跳过、证据位置。抽查 04–05 支持这些输出可按固定实现展开；不要求机械抄全部源码、填真实主次号或审完整 DCMI。
2. **逐库待采证据关联仍缺。** L90 格式仍为“库文件名/版本/hook 入选与否/CLI 目标路径/挂载结果”，未带采样/证据定位、具体缺项/原因，亦未把父目录候选→库子路径→最终挂载记录连接。虽已明确父目录存在条件，但“逐库 hook 入选与否”还未区分父候选入选与子库的采样观察；抽查 06 是目录项分类，03 是目录挂载，不能暗示 hook 已逐库分类。缺的是可填写证据规则，不是本轮没有检查目录或没有真实库清单。
3. **正文/作者 unknown 口径仍未完整同步。** L90 仍两次写“runtime 库注入语义未核对”，另保留“所选变体内容与实际结果未读/未执行”，没有把已读默认 base 与未选五份产品变体、机制与逐库记录/现场结果稳定分开。作者来源记录 L12 新增的三分提示是进展，但 L17 仍把“实际库挂载/白名单/hook 可执行/dcmi 完整实现”合列 unknown；“入口与条件链已读，见上”不足以限定其中已核对的完整 hook/默认白名单机制。登记 L5462 的已补边界不替代正文及该清单的同步。

**剩余关闭条件：** 保留已认可的输入设计、两端来源、失败摘要、逐库字段与登记边界；补所选产品/两端条件设计与其输出连接；以可复用字段规则交付完整节点/许可/环境、manager/dvpp/UB 与条件化 vdevice/poststop 的所选记录，含来源、目标、失败/跳过与证据位置；完善父候选→子库→最终挂载的待采证据关联及缺项/原因。同步正文/作者记录的旧宽口径，明确**机制已读、所选记录未交付、现场未采**，区分已读默认 base 与未选产品变体。**现场文件/设备号/库版本/结果可待采，支持交集可 unknown；不要求安装、执行脚本、实测、完整 DCMI/全部白名单或 CLI 审计。**

### B21-C34 — P1 / OPEN

**权威条件：** 前次复核 L121。**位置证据：** 正文 L66、L118–125、L127、L131–138、L140–142；本轮映射 L303。

**本轮新增认可：** L127 已选择成功访问操作为目标进程打开所选设备节点，并写出 open 结果/可见集/进程设备时间记录；单独授权负向拒绝选择了 open 拒绝事件（errno/AVC）与主体/节点/时间窗；恢复后另记配置摘要与主体关联。**不再指称完全未选成功访问操作或正负结果记录形式。** L133 权限变体与 L135 镜像回退已有局部 S1/R1 绑定；逻辑消费类型、单元素策略、完整许可比较对象、负向授权、回退/更新/重建拆分及 NPU 独立 unknown 均保留认可。

**仍未满足：**

1. **两端字段级消费配置对仍缺。** L66 是通用键清单，L132 是 CDI 原生/legacy 的逻辑选择；尚未把每端 Pod/RuntimeClass 或默认选择→handler→低层 runtime/包装器及 Toolkit mode 的关键字段、设计取值绑成一对。抽查 11 表明环境变量也可用于 CDI，09 表明非 CDI 输出另受 PassDeviceSpecs 条件影响；“envvar＋legacy runtime hook、无 CDI 引用”不足以排除其他最终消费模式/并行设备输出。需要所选配置与旁路条件，不要求所有模式审计、现场 handler 名/路径或重开 C31。
2. **资源更新接口与完整字段仍缺。** L137 仍明确“候选字段为 CRI 更新对象/OCI linux.resources.cpu，固定字段未取，unknown”。未选定接口、完整字段、单位/语义、旧→新记录形式并绑定同一次更新前后采样。抽查 10 给出 CPU/内存更新源场景，不替作者交付更新设计；镜像/驱动回退与重建不能替代该变体。
3. **正负访问形式有了，分阶段恢复关联还未完整交付。** L127 的通用三元组未连接完整目标节点/稳定身份、各生命周期阶段及正负结果的证据定位；其“恢复后证据”仍主要为配置摘要和主体/节点/时间窗。L133/L135 的局部引用可保留，但 L134、L136–138 仍主要以“同上”或注入集对比承接，未形成共同规则，把每变体变更前、变更后、恢复后的主体（重建须新旧 ID）、完整目标节点/稳定身份、时间窗与成功 open/原负向拒绝证据一一关联。问题不是必须重复抄 R1，而是缺少可复用的阶段/对象/结果连接规则；恢复后的配置摘要、可见集或单独“未见拒绝”不能替代正向成功与原负向边界恢复。缺负向授权只记未执行。
4. **C32 方法依赖未闭合。** 三单比较仍依赖未交付的完整稳定映射；缺方法/缺采样原因及具体缺项未统一同步。这是 C32 原缺口的依赖，不新增发现、不重复计数，也不替代前三项独立设计要求。

**剩余关闭条件：** 保留已选消费类型/策略及新增 open 记录形式；落实每端 runtime 模式/handler 字段级消费配置、设计取值与旁路排除；选定资源更新接口、完整字段、单位/语义与旧新记录格式；用公共连接规则把正负访问和恢复记录对应各变体生命周期前后及恢复后的主体、完整目标节点/稳定身份、时间窗与可定位结果。引用 C32 已交付方法，缺方法优先无法确定并区分缺采样。**保留 NPU 独立未知、S1/R1、负向授权与回退拆分；不要求实测、现场值、扩大生产权限或制造结果，无负向授权不执行。**

## 5. Acceptance 与最终计数

| T05-01 acceptance | 本轮判定 | 对应范围 |
|---|---|---|
| 镜像身份、层、构建输入、SBOM/签名与拉取策略 / L5403 | 沿用此前通过，不重审，不据此宣称已有供应链系统 | C30 已 CLOSED，范围外 |
| 固定运行时/NVIDIA 版本与各层边界 / L5404 | 部分满足、未完整通过：逐库连接/稳定映射方法仍缺 | C31 已 CLOSED（范围外）；C32 OPEN |
| Ascend 独立实现与目标组合 / L5405 | 部分满足、未完整通过：输入形式与登记边界认可，所选输出记录、逐库证据及旧口径同步仍缺 | C33 OPEN |
| 清单、异常/隔离、对照与源案例 / L5406 | 部分满足、未完整通过：open 形式认可，消费配置/更新字段/分阶段恢复关联及映射依赖仍缺 | C34 OPEN |

四条 acceptance：**1 沿用既有完整通过 / 3 未完整通过**。本轮 **0 CLOSED / 3 OPEN（1 P1、2 P2）**，**第二十四次定向复核不通过**，无新增发现 ID。阻断来自未交付的方法、完整所选记录、字段级配置与证据关联及口径一致性，**不是 curl DNS 失败、现场值 unknown、没有实测或未证明整栈兼容**。不修改计划/正文审核状态，不用审阅者补读替代作者应交付内容。

## 6. 结构校验与写入审计

- 写入前原仓库 `PYTHONDONTWRITEBYTECODE=1 make check` **PASS：96 content entries / 440 sources**；仅验证结构与本地链接，不验证技术正确性或远程正文。
- 独立副本 `/private/tmp/b21-t05-01-recheck24-uizLMA/validation` 初次因未复制已有 `build/`，`make check` 报两个 catalog 本地链接缺失；这是副本准备缺项，不是作者内容缺陷。补拷原有 `build/` 后，以原仓库虚拟环境 Python、禁写字节码执行 `make check` / `make build`，均 **PASS：96 content entries / 440 sources**；构建只更新副本的 `build/catalog.json` / `build/catalog.md`。
- 写入后原仓库 `PYTHONDONTWRITEBYTECODE=1 make check` **PASS：96 content entries / 440 sources**；报告同步至副本后复跑 `make check` / `make build`，均 **PASS：96 content entries / 440 sources**。原仓库 `build/` 未改。
- 文件摘要审计覆盖 **408 个**既有文件（不含 `.git`、`.venv` 与 Python/工具缓存）：无修改或删除，唯一新增为本报告；七份输入身份保持本报告表列摘要。剔除本报告后的 Git 状态与开始时一致。临时目录留存摘要基线、Git 状态、curl 错误与副本校验日志；不运行 `make test`，因为未修改 `src/kb/` 或测试代码。

**最终结论：B21-C32 OPEN、B21-C33 OPEN、B21-C34 OPEN；0/3 关闭，本次不通过。下一轮仅核对上述剩余关闭条件，不重开 C30/C31，不以实测或现场值替代设计交付。**
