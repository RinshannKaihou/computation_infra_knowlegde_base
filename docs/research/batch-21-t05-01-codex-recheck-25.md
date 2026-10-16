# Batch 21 补交 T05-01 第二十五次定向复核

## 1. 结论、角色与范围

- 日期：2026-10-14（Asia/Shanghai）。执行者：当前 Codex 会话，以独立审阅角色核对作者第二十五轮修订，与作者修订角色分开；未派发其他模型或子代理。
- `gpt-6.1-sol / xhigh` **仅为用户约定，不是已独立确认的执行元数据**。本会话没有可独立核验的实际模型、推理档位或路由证据，不宣称已确认模型一致性或无 fallback。
- 唯一复核范围：**B21-C32–C34**。剩余关闭条件以[第二十四次复核](batch-21-t05-01-codex-recheck-24.md) L87、L103、L118 为权威；[初审报告](batch-21-t05-01-codex-review.md)用于核对原 ID、职责和优先级。**C30/C31 保持此前 CLOSED，范围外，不重审。** 第二十五轮修订映射仅说明落盘改动，不代替关闭证据。
- **0 CLOSED / 3 OPEN（1 P1、2 P2）；第二十五次定向复核不通过。** 本轮认可 Ascend 所选产品形态/示例条件、父目录候选与逐库采样的区别，以及 GPU 两端消费链字段框架和 R1 阶段关联的新增文字；这些进展不再列为完全未交付。
- 只新增本报告，不修改作者正文、来源记录、修订映射、登记、计划或原仓库生成文件，保留开始时已有工作区改动；不提交、不创建分支。不新增发现 ID：本轮核到的 Ascend 失败语义/挂载判据问题归 C33，插件内部集合名与配置键的区别归 C34，均属于原关闭条件的直接核对。
- 未安装组件、拉取/构建镜像、生成 SBOM、运行容器、采集设备、接入集群、修改运行配置或执行访问、负向、资源更新、恢复实测；上游源码/脚本只读，不执行。结构检查与目录构建不是环境或硬件验证。

| 原 ID | 原优先级 | 本轮状态 | 位置证据与剩余问题 |
|---|---|---|---|
| B21-C32 | P2 | OPEN | 正文 L60、L72、L78、L82–84、L109–114、L118、L131–138：扫描/逐库归层连接及逐 ordinal 稳定映射仍缺方法；缺方法/缺采样分类未贯通相关记录 |
| B21-C33 | P2 | OPEN | 正文 L90、L92；作者来源记录 L12、L17；登记 L5446、L5457、L5462：示例产品与采样依据有进展，所选完整输出/证据关联仍缺，错误传播与挂载成功判据须修正，旧宽口径未清除 |
| B21-C34 | P1 | OPEN | 正文 L66、L127、L132–138：新增字段链/阶段文字不足以确定两端消费配置和分阶段访问证据；资源更新接口/字段及 C32 方法依赖仍缺 |

## 2. 输入身份与写入边界

用户给定的 **3 个 SHA-256 前缀全部与当前整文件吻合**。修订映射仅审第二十五轮节 L306–310，不把旧轮次改动清单视为本轮关闭证据。来源登记经 YAML 解析为 **440 项**。以下完整摘要由本轮独立计算；仓库行号均指这些输入原文件坐标。

| 输入 | SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md)，指定前缀 `989250afa7855121` | `989250afa7855121d09f40f7b02df9d45802df8fd9d5635ff08b1bef5dbbecd3` |
| [作者来源记录](batch-21-t05-01-sources.md)，指定前缀 `3719c44a87798ef0` | `3719c44a87798ef001541fa241877decc3f0817483cea3408c2f609a8d888235` |
| [修订映射](batch-21-review-fixes.md)，指定前缀 `d2410111eca08394` | `d2410111eca0839462b1da720caaa815d43b50adb6ece925191a64b51b0821fc` |
| [第二十四次复核](batch-21-t05-01-codex-recheck-24.md) | `fc362695ea6801632669e0f0f6f777e097baaa5bd2f9d2f436bbba6dcf3199c1` |
| [初审报告](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` |
| [任务验收](../../plans/full-coverage-backlog.yaml)，T05-01 acceptance L5403–5406 | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml) | `af8d7441ba9fb3da5413475200b8a75278586877e06dc004d70a89ef4453d4b8` |

从 `README.md`、`docs/authoring-guide.md`、`content-outline.md` 开始核对规则，并读取元数据 schema、初审与前次复核。临时取证/校验目录为 `/private/tmp/b21-t05-01-recheck25-l3Kxxi`；临时响应、错误日志、摘要基线和副本构建产物不写入知识正文或来源登记。

## 3. 一次源抽查方法、文字与限制

### 3.1 curl 实际尝试与只读替代通道

对下表 01–13 的精确 HTTPS 地址实际执行只读 GET；源码使用相同 ref/path 的 `raw.githubusercontent.com` 地址，文档使用表列原地址。命令形态：

```sh
curl --location --fail --silent --show-error \
  --connect-timeout 8 --max-time 20 --output "$audit_dir/curl-$point.body" \
  --write-out 'http_code=%{http_code}\n' "$url"
```

保留默认 TLS 校验，未用 `-k`/`--insecure`，未申请提权或自定 IP 绕行。**13 次均在 DNS 阶段失败：退出码 6、HTTP 000、Could not resolve host**，涉及 `raw.githubusercontent.com`、`docs.nvidia.com`、`docs.pytorch.org`。没有取得 curl HTTP 正文，不能称 curl 200、TLS 握手/校验成功或已取得上游 HTTP 字节摘要。请求清单与结果保存于临时目录的 `curl-urls.tsv`、`curl-01.meta` 至 `curl-13.meta` 及对应 `.stderr`。

随后使用用户允许的只读通道：GitHub 连接器 `fetch_file` 按固定 ref 实读原文件区间，网页读取通道实际打开版本化 NVIDIA/PyTorch 文档并核对相关段落；不是只判可达性，也不以作者自述、前次摘录或搜索片段代替本轮实读。插件 README 另经网页通道打开，再以连接器原文件区间复核配置键。网页可能经过解析/缓存（本轮 NVIDIA 排障页显示三日前抓取），不等同本机 curl 新鲜原始字节；Git blob SHA 不等于 HTTP SHA-256。源码坐标以连接器请求的原文件区间为准，不把网页阅读器行号拼成 GitHub 原文件锚点。未执行上游示例，不独立背书历史 curl 成功记录。

### 3.2 本轮实读点与有限支持范围

Ascend 文件均固定 commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e`。各点均属于既有登记来源，不新增来源项；编号仅为取证点，不是发现 ID。

| curl 点 | 精确一次源 / 本轮实读位置 | 核到的文字或实现与有限支持范围 |
|---|---|---|
| 01 | [runtime/process/process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go)，L45–405、L455–830；错误分支另定向读 L550–660、L680–775 | 节点信息取得失败返回 error；310B 辅助项/dvpp 失败可警告，主 davinci、manager 最终加入及 UB 条目错误有传播路径。manager 宿主回退后容器路径有重命名；UB 目录/非子目录条目有独立条件。VIRTUAL 提前返回与条件化 vdevice/poststop 分开；不能把所有节点失败统称跳过 |
| 02 | [device-plugin common.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go)，L90–145 | ID 转字符串并逗号拼接；写 options；插件 RealCardType 为 310B 才写 allow-link；!PresetVDevice 才写七个 worker 字段，计数取输入长度，local-rank 有生成函数。不是两端卡型相同或已交付本文完整输出记录的证明 |
| 03 | [hook/process/process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/hook/process/process.go)，L85–225、L237–440 | 默认 base；列表逐行计数后按 stat 分类文件/目录，构造 CLI 参数；父 lib64 目录入选不是逐库分类。CLI 路径/exec 可失败，hook 机制已读不等于现场执行已验证 |
| 04 | [build/scripts/base.list](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/scripts/base.list)，完整五行 | 默认五个宿主路径，包含 lib64/include/dcmi/npu-smi/queue_schedule；没有逐库身份、版本或挂载成功记录 |
| 05 | [run_main.sh](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/scripts/run_main.sh)，L278–315 | 五个产品分支之外复制默认 base.list，目标统一为配置目录 base.list，chmod 440。源码列表与部署产物不同，不证明示例组合配套或安装成功 |
| 06 | [cli/src/u_mount.c](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/cli/src/u_mount.c)，L45–240 | rootfs＋源路径；源 stat 失败可返回 0，NODRV 的 DoMounting 亦可直接返回 0；建目标/校验/bind/只读 remount 可失败。成功返回值不单独证明执行了挂载；不外推整个 runtime 无其他挂载 |
| 07 | [NVIDIA server.go@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go)，L280–507 | CDI/非 CDI 策略分支不同，全 CDI 策略提前返回；envvar/volume-mounts 和 PassDeviceSpecs 另有条件。内部 deviceListStrategies 集合不等于消费端 runtime mode |
| 08 | [Toolkit 1.20.0 CDI support](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html)，Running a Workload / Non-CDI-Enabled Runtimes / Setting the CDI Mode Explicitly | hook/CDI 冲突；显式配置 nvidia-container-runtime.mode=cdi 时仍可用 NVIDIA_VISIBLE_DEVICES 选择设备。因此 envvar/无插件 CDI 引用不证明最终走 legacy |
| 09 | [Toolkit 1.20.0 troubleshooting](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html)，NVML/SELinux、访问丢失、Affected Environments | hook/legacy 更新可撤销访问；显式 CPU/内存限制更新与 systemd reload 有不同条件；禁用 SELinux 有隔离代价。源场景不代替作者所选更新接口/字段或恢复记录 |
| 10 | [containerd CRI config@v2.4.1](https://github.com/containerd/containerd/blob/v2.4.1/docs/cri/config.md)，L1–160、L270–385 | RuntimeClass→handler、default_runtime_name、runtimes 项 runtime_type/options.BinaryName、cdi_spec_dirs 有具体字段。只给通用 options 名称不确定每端消费执行器；不重开 C31 |
| 11 | [Syft README@v1.54.1](https://github.com/anchore/syft/blob/v1.54.1/README.md)，L1–110，Features / The basics | 镜像/目录扫描、输出格式与配置/schema 入口已核到；不替作者固定扫描范围、必要字段或包/文件/层连接规则；不重开 C30 |
| 12 | [PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html)，Device-agnostic code 的 CUDA_VISIBLE_DEVICES 段 | 可管理 PyTorch 可用 GPU 范围；该段不交付本文 ordinal→分配/CDI→完整节点→UUID 的连接方法，不据此否认其他身份接口存在 |
| 13 | [NVIDIA README@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/README.md)，原文件 L194–315，配置文件/flag 段 | 配置示例字段为 flags.plugin.deviceListStrategy、flags.plugin.passDeviceSpecs；flag/env 另列。正文的 deviceListStrategies 需明确是内部/逻辑集合并映射真实配置入口，不能当作已经交付配置键 |

连接器返回的文件身份（Git blob SHA）：runtime `process.go=acbd7a1ec0703498abfcfcb6ce1aa493069091b1`；`common.go=6cd038e9f1d67a8a913aa4bb1301692f177b3dbe`；hook `process.go=816212afa5f69b8edfb1554d3935af2ebcd28f06`；`base.list=4ea1b223fdeed19fed7fdf1a3b4457b8ddd747b3`；`run_main.sh=9be36636ff13c480c57342b81c78f4b74e95675b`；`u_mount.c=d85fd8155a1805edaf509b047c6441bcdc603e12`；NVIDIA `server.go=9281b48ef52f9eda9cbed6d98491729da85b5a75`、`README.md=44594d4343967a313ff268223c8f638de005062c`；containerd `config.md=3a206263f4f9e76b6ca14110461b8661a03b1619`；Syft `README.md=9ffd2affa3b00031ea1fd01ee3fe228379978492`。均不是本机 curl 下载摘要。

## 4. 逐项定向复核

### B21-C32 — P2 / OPEN

**权威条件：** 第二十四次复核 L87。**位置证据：** 正文 L60、L72、L78、L82–84、L109–114、L118、L131–138；第二十五轮映射 L310。

**认可/保留：** 宿主内核驱动、注入用户态组件、镜像库分层及 Allocate/CDI/edits/OCI 连接继续认可；节点与许可不合并。L112 的缺方法/缺采样区分、L118 的缺映射规则优先无法确定继续认可。诚实标 unknown 本身不是事实错误；不重开 C30/C31。

**仍未满足：**

1. **扫描与逐库来源连接仍缺设计。** L60 保留“所选扫描配置”，L72 保留“来源层字段，以实际输出为准”，未固定扫描范围、必要输出字段、包/文件路径与层的解析/连接键。层清单、diff_ids、annotations 与箭头不能替代逐库来源→最终挂载→容器目标的可核对连接。抽查 11 是工具入口证据，不要求本轮生成真实 SBOM。
2. **完整稳定映射仍明确未交付。** L78 仍写“稳定物理标识映射方法（未交付，unknown）”，L82–84 仍为待填表；固定来源支持的逐 ordinal 可见集快照→分配 ID/CDI 名或传递字段→完整节点（类型/major/minor/路径与来源）→稳定身份规则没有落盘。抽查 12 的可见范围管理不是该连接；数量、编号文本相同不能替代身份关联。
3. **分类同步未贯通。** L109“未记录即缺失”、L110“无法确定写 unknown”、L111“同上”仍未共同记录缺方法/缺采样原因、具体缺项和证据定位；L114、L131–138 的比较亦未统一引用。L112 的局部分类不补全方法，也不能把尚缺方法的行统一归成缺现场样本。

**剩余关闭条件：** 按固定来源交付所选扫描范围、必要字段、包/文件/层解析与逐库来源连接，以及完整逐 ordinal 稳定映射；把缺方法/缺采样原因、具体缺项、证据定位的公共规则同步到核对表、最小清单及 C34 比较/判定。**现场值可 unknown；不要求拉镜像、生成 SBOM、审全部 cataloger、采设备或实测，不重开 C30。**

### B21-C33 — P2 / OPEN

**权威条件：** 第二十四次复核 L103。**位置证据：** 正文 L90、L92；作者来源记录 L12、L17；登记 L5446、L5457、L5462；第二十五轮映射 L308。

**本轮新增认可：** L90 已明确“产品形态示例＝310B 推理卡”，搭配默认安装分支、空 options、base 组、PresetVDevice=false 假设和整数 ID 数组形式；不再把产品形态设计选择列为完全缺失，不要求 310B 执行后续 GetProductType。L90 已说明逐库采样来自部署后目录枚举，不是 hook 逐库分类，并注明缺采样；作者记录 L12 纳入示例条件与三分提示。登记 L5462 的源码/部署产物边界继续认可，无需重复补登记；示例条件不证明支持交集或两端卡型一致。

**仍未满足：**

1. **所选条件未展开为完整可填写输出记录。** “14 尝试项”“worker 组”“UB stat 门控”仍主要是组名，未交付所选辅助候选集合、worker/控制环境键及生成规则、UB 目录/条目规则、manager 回退后的宿主→容器路径和节点/许可输出的公共记录形式，亦未逐项连接条件、失败/跳过与来源/证据位置。抽查 01–02 支持这些实现可展开。L92 的支持交集 unknown 可保留，但“所选记录 filled 值未交付”不能把尚缺设计规则降成只缺现场值；不要求填真实设备号、库版本或实际运行结果。
2. **失败语义须按对象分开，不能把挂载跳过外推到节点。** L90 的节点输出概括含“stat 失败可跳过”。抽查 01 的 `addDeviceToSpec`（原文件 L550–660）取得设备信息失败返回 error，`addDevice`（L680–775）对作业 davinci、UB、manager 失败继续返回；310B 的辅助尝试项/dvpp 警告与 manager 回退是不同条件。抽查 03/06 的列表源 stat 跳过/CLI 返回 0 不能代替 runtime 节点错误传播。这是 C33 原“条件—输出—失败/跳过”范围内的事实追记，不新增 ID。
3. **父候选→子库→最终挂载证据仍未闭合。** L90 新格式为“库文件名/版本/CLI 目标路径/挂载结果，缺则记 unknown 并注缺采样”，仍缺子库来源路径与父候选/相对路径连接、采样与挂载证据定位、具体缺项/原因。其“挂载成功以 CLI 返回＋目标可达为准”不足：抽查 06 中源 stat 失败及 NODRV 可成功返回而未执行该挂载，目标可达也没有证明目标来自所选宿主源。需记录实际挂载对象/来源与目标的关联，不以可能原有的目标路径充当注入证明；只要求设计该证据形式，不要求本轮执行。
4. **旧宽口径仍未清除。** L90 仍两次写“runtime 库注入语义未核对，unknown”，与同段“机制/常量/白名单源码与消费规则已读”并存；作者记录 L17 仍把“实际库挂载/白名单/hook 可执行/dcmi 完整实现”合列 unknown。L12 的增补不消除这两个旧口径。需稳定区分已读默认 base/hook/CLI 机制、未选产品变体、尚缺所选记录规则以及现场未采/未执行；登记已补边界不代替正文和作者记录同步。

**剩余关闭条件：** 保留产品示例、输入形式、两端来源、父候选/子库区别与已补登记；交付所选节点/许可/环境、manager/dvpp/UB、条件化 vdevice/poststop 的完整可复用记录规则，含条件、来源、目标、失败/跳过及证据位置；修正节点错误传播与挂载成功判据，完善逐库来源/挂载/缺项证据关联；清除正文与作者清单的旧宽口径，明确机制已读、方法/记录设计缺项、现场未采。**支持交集及现场文件/设备号/库版本/结果可 unknown；不要求安装、执行脚本、实测、完整 DCMI、全部产品白名单或 CLI 审计。**

### B21-C34 — P1 / OPEN

**权威条件：** 第二十四次复核 L118。**位置证据：** 正文 L66、L118–125、L127、L131–138、L140–142；第二十五轮映射 L309。

**本轮新增认可：** L132 已串联 Pod/default→RuntimeClass.handler→containerd handler 项→CDI/legacy 分支，并列 runtime_type/options 与混合输出判定；不再指称完全没有字段链。L127 新写变更前/变更后/恢复后三阶段，重建类新旧主体分别记 ID；不再指称完全没有阶段关联。此前认可的正负 open 形式、单元素逻辑策略、完整许可比较对象、S1/R1、负向授权、回退/更新/重建拆分及 NPU 独立 unknown 均保留。

**仍未满足：**

1. **字段链不等于确定两端消费配置。** L132 仍只写 `runtime_type＋options` 类目，未把每端实际选择的低层 runtime/包装器关键字段（如 `options.BinaryName`）和 Toolkit mode 的设计取值绑入配置对；L66 通用清单不能替代两端设计。抽查 08 的显式 cdi mode 仍消费 NVIDIA_VISIBLE_DEVICES，故 envvar、无 CDI 引用、排除并行输出不充分证明 legacy。另 L132 的 `deviceListStrategies=[…]` 若作内部/逻辑集合可保留，但需映射所选配置入口：抽查 13 给的是 `flags.plugin.deviceListStrategy`（或对应 flag/env），不是复数配置键；`passDeviceSpecs` 的设计值与实际输出排除条件也应对应，不以“出现才判混合”代替所选配置。无需提供现场 handler 名/路径或审全部模式，不重开 C31。
2. **资源更新接口/字段仍未选定。** L137 仍原样保留“候选字段为 CRI 更新对象/OCI linux.resources.cpu，固定字段未取，unknown”。没有接口、完整字段、单位/语义、旧→新格式及同一次更新前后采样关联。抽查 09 支持 CPU/内存更新源场景，不替作者完成选择；镜像/驱动回退和容器重建不能替代该变体。
3. **阶段有了，完整对象/结果绑定仍缺。** L127 的阶段序列与三元组有进展，但未交付把每变体每阶段的主体（重建为新旧 ID）、完整目标节点（类型/major/minor/路径/来源）及稳定身份、时间窗、成功 open/原负向拒绝结果与可定位证据逐一连接的公共规则。恢复证据仍主要为配置摘要＋主体/节点/时间窗；L132 无 R1 引用，L133–138 局部绑定或“同上”不能补齐缺失的共同证据对象。允许复用公共规则，不要求机械重复表格；关键是恢复后的正向成功与原负向边界要有同阶段/同对象的记录，不能由三单可见性、配置摘要或单独未见拒绝代替。缺负向授权只记未执行，不要求执行。
4. **C32 方法依赖未闭合。** 三单归一化仍依赖未交付的稳定映射；公共缺方法/缺采样原因及具体缺项未同步。该依赖属于 C32 原缺口，不新增发现、不重复计数，也不代替 C34 前三项独立设计要求。

**剩余关闭条件：** 保留新增字段链和三阶段文字；落实两端真实配置键/设计取值、消费执行器与 Toolkit mode、旁路排除；选定资源更新接口、完整字段、单位/语义和旧新记录格式；用公共规则把各变体各阶段主体、完整目标节点/稳定身份、时间窗与正负访问/恢复结果、证据定位一一连接，引用 C32 已交付方法并统一缺方法/缺采样判定。**保留 NPU 独立未知、S1/R1、负向授权与回退拆分；不要求实测、现场值、扩大生产权限或制造结果，无负向授权不执行。**

## 5. Acceptance 与最终计数

| T05-01 acceptance | 本轮判定 | 对应范围 |
|---|---|---|
| 镜像身份、层、构建输入、SBOM/签名与拉取策略 / L5403 | 沿用此前通过，不重审，不据此宣称已有供应链系统 | C30 已 CLOSED，范围外 |
| 固定运行时/NVIDIA 版本与各层边界 / L5404 | 部分满足、未完整通过：逐库连接/稳定映射方法仍缺 | C31 已 CLOSED（范围外）；C32 OPEN |
| Ascend 独立实现与目标组合 / L5405 | 部分满足、未完整通过：示例条件/采样区别认可；完整输出、失败语义、逐库证据及口径同步仍缺 | C33 OPEN |
| 清单、异常/隔离、对照与源案例 / L5406 | 部分满足、未完整通过：字段链/阶段文字认可；消费配置、更新字段、完整访问恢复绑定及映射依赖仍缺 | C34 OPEN |

四条 acceptance：**1 沿用既有完整通过 / 3 未完整通过**。本轮 **0 CLOSED / 3 OPEN（1 P1、2 P2）**，**第二十五次定向复核不通过**，无新增发现 ID。阻断来自方法/记录设计、事实语义、配置取值、证据关联及口径一致性，**不是 curl DNS 失败、现场值 unknown、没有实测或未证明整栈兼容**。不修改计划/正文审核状态，不以审阅者补读代替作者应交付内容。

## 6. 结构校验与写入审计

- 写入前原仓库 `PYTHONDONTWRITEBYTECODE=1 make check` **PASS：96 content entries / 440 sources**，仅验证结构和本地链接，不验证技术正确性或远程正文。
- 独立副本 `/private/tmp/b21-t05-01-recheck25-l3Kxxi/validation` 包含只读复制的既有 `build/`；以原仓库虚拟环境 Python、禁写字节码执行 `make check` / `make build`，均 **PASS：96 content entries / 440 sources**。构建仅更新副本的 `build/catalog.json` / `build/catalog.md`，原仓库生成文件不改。
- 写入后原仓库 `PYTHONDONTWRITEBYTECODE=1 make check` **PASS：96 content entries / 440 sources**；报告同步到副本后复跑 `make check` / `make build`，均 **PASS：96 content entries / 440 sources**。
- 文件摘要审计覆盖 **409 个**既有文件（不含 `.git`、`.venv` 与 Python/工具缓存）：无修改或删除，唯一新增为本报告；七份输入身份保持 §2 摘要，剔除本报告后的 Git 状态与开始时一致。临时目录留存摘要基线、Git 状态、curl 错误与副本校验日志；未运行 `make test`，因为未修改 `src/kb/` 或测试代码。

**最终结论：B21-C32 OPEN、B21-C33 OPEN、B21-C34 OPEN；0/3 关闭，本次不通过。下一轮仅核对上述剩余关闭条件，不重开 C30/C31，不以实测或现场值替代设计交付。**
