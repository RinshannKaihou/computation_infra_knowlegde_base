# Batch 21 补交 T05-01 第十四次定向复核

## 1. 结论、角色与范围

- 日期：2026-10-14（Asia/Shanghai）。执行者：当前 Codex 会话，承担独立审阅角色，与作者第十四轮修订角色分开；未派发其他模型或子代理。
- `gpt-6.1-sol / xhigh` **仅为用户约定**。本会话未取得可独立核验的底层执行模型、推理档位或路由元数据，不将约定写成已确认的实际执行元数据，也不宣称完成实际模型一致性或无 fallback 的独立核验。
- 唯一复核范围：**B21-C32–C34**。剩余关闭条件以[第十三次复核](batch-21-t05-01-codex-recheck-13.md) L85、L100、L115 为权威；[初审报告](batch-21-t05-01-codex-review.md)仅核对原 ID、职责与优先级。C30/C31 保持此前 CLOSED，范围外，不重审。
- **0 CLOSED / 3 OPEN；第十四次定向复核不通过。** 开放项为 **1 P1、2 P2**。已补齐的局部条件单独认可，不因整体仍 OPEN 而重复要求修改。
- 没有新增发现 ID。新增 Ascend 条件摘要的事实错误继续追记 **C33**，属于同一所选路径/虚拟生命周期条件问题；无需另立发现。
- 未安装组件、拉取或构建镜像、运行容器、生成 SBOM、采集设备、修改配置、接入集群或执行负向/恢复试验。本报告是来源与设计审阅，不是硬件验证。

| 原 ID | 原优先级 | 本轮状态 | 正文位置 / 主要依据 |
|---|---|---|---|
| B21-C32 | P2 | OPEN | L70、L76、L80–82、L108–112、L116：扫描/逐库归层与稳定映射方法仍未交付，缺失分类只局部同步 |
| B21-C33 | P2 | OPEN | L88、L90、L145；登记 L5335：worker 条件已同步，但所选路径必要证据仍缺，新增 VIRTUAL 摘要与已读控制流矛盾 |
| B21-C34 | P1 | OPEN | L125–136：hook 区分及许可比较字段已补，模式配置对、资源更新对象、逐变体访问/恢复证据及映射依赖仍未闭合 |

## 2. 输入身份与单文件边界

用户给出的 **3 个 SHA-256 前缀全部吻合**。下表为本轮起始完整摘要；本报告所称正文、映射、计划、登记及历史报告行号均指仓库原文件，不是网页阅读器坐标。

| 输入 | 起始 SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md)，145 行 | `c73ac7d656397c67d3b1380ad760d64fa4e34151e82362c76b32c4cd8920005b` |
| [修订映射](batch-21-review-fixes.md)，246 行 | `4672b6466bfb093323ddfda7d0e103ffa23dbf528e8cb50884e80336e975fbd5` |
| [第十三次复核](batch-21-t05-01-codex-recheck-13.md) | `b965d533e621284c9f5b6ea84b7e6aa003692c68c2de5bf9cbcc9cb8c93135c0` |
| [初审报告](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` |
| [任务计划](../../plans/full-coverage-backlog.yaml)，T05-01 acceptance L5403–5406 | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml)，438 项 | `dc7bfae1a35d53fa31e816aae0b8efcbcaddafaae3cf249d915010d5b28c114c` |

修订映射仅采用 **T05-01 第十四轮节 L242–246**，作为落盘改动索引，不作为技术关闭证据。补读 README、编写指南、内容总目录和 metadata schema；为核对 C33 已读范围，补读[作者来源记录](batch-21-t05-01-sources.md) L12、L17，摘要 `ae26470307fe2bb04c255c76d408343c16be53c4d178baf4a87fe44a6a49fed5`。本轮审阅者读取一次源，不等于作者已经补交该证据。

起始工作区已有修改与未跟踪文件，本会话保留、不回滚、不代写。原仓库唯一允许新增或修改的文件为本报告；请求诊断、写入审计及隔离构建使用 `/private/tmp/b21-t05-01-recheck-14.TYInv5/`，不作为永久证据附件或仓库内容。

## 3. 一次源抽查与方法限制

### 3.1 实际 curl 请求

本机 curl **8.7.1**，对下表 01–10 实际执行只读 GET。GitHub 文件请求同仓库/ref/路径的 `raw.githubusercontent.com` 地址；厂商/PyTorch 请求表列版本 URL。请求与结果位于上述临时目录的 `urls.tsv`、`curl-results.tsv`、`*.stderr`。调用形态：

```bash
curl --disable --location --silent --show-error --connect-timeout 8 --max-time 20 \
  --output "$audit_dir/$name.body" --write-out '%{http_code}' "$url"
```

保持默认 TLS 校验，没有使用 `-k`、改 DNS/证书、提权或绕过沙箱。**10/10 退出码 6、HTTP `000`，均为 `Could not resolve host`。** 未取得 curl 响应正文，TLS 握手未发生；不声称 curl 成功、HTTP 200 或本机完成证书验证。

### 3.2 允许的只读替代通道与文字核对

使用 `web.run` 读取版本化厂商/PyTorch 页面及两个 README 的实际正文，并使用 GitHub 只读连接器读取同 ref 原文件。逐点核对字段、条件和控制流，**不是仅判可达性**。网页通道可能使用缓存并归一化文本，不等于本机即时 GET；GitHub 源码行号取原文件读取区间，不把网页坐标拼成源码锚点。以下“未补足”指作者当前交付缺项，不是宣称上游不存在相应接口或能力。

| 点 | 精确一次源 / 本轮实际阅读位置 | 核对结果与有限支持范围 |
|---|---|---|
| 01 | [syft README@v1.54.1](https://github.com/anchore/syft/blob/v1.54.1/README.md)，GitHub 全文；网页 Features / The basics | 支持镜像/文件系统扫描及输出格式入口；当前正文未据此选定扫描范围、必要字段与成分/路径归层方法。不重开 C30。 |
| 02 | [PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html)，Best practices / Device-agnostic code 的 `CUDA_VISIBLE_DEVICES` 段 | 支持可见集管理；该段未给出当前正文所需的逐 ordinal→分配 ID/完整节点→稳定身份连接规则，不据此否定其他框架接口。 |
| 03 | [Ascend common.go@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go)，GitHub L90–130 | 有效响应内 ID/options、310B allow-link、`!PresetVDevice` worker 组的字段级条件，支持登记 L5335 本轮同步。 |
| 04 | [Ascend plugin.go@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go)，GitHub L1080–1175 | `UseAscendDocker` 两条互斥路径及原生 DeviceSpec `rw`；不把原生输出接到 wrapper `rwm`，不补完整 ID 生成链。 |
| 05 | [Ascend process.go@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go)，GitHub L60–130、L243–410、L490–720、L722–812、L850–910 | 核对库搜索路径、节点与 cgroup、manager/产品/UB 条件、VIRTUAL 提前返回及非提前返回后的 CreateVDevice/poststop；不是 hook 可执行内部行为或真正库挂载取证。 |
| 06 | [CDI SPEC@cb98bcf6](https://github.com/cncf-tags/container-device-interface/blob/cb98bcf66dc68530012483bd56e33e14d815e167/SPEC.md)，GitHub L90–175、L190–265 | kind/name、全局/设备级 edits、节点/挂载/env/hooks；CDI 自身 hooks 不能仅凭“存在 hook”归为独立 legacy 路径。 |
| 07 | [OCI Linux@92249139](https://github.com/opencontainers/runtime-spec/blob/92249139eea7161e13745abd4cb6d0ea02a3227a/config-linux.md)，GitHub L127–151、L402–418 | 完整节点与许可分开；许可含 allow/type/major/minor/access，按列表顺序应用，省略字段有通配语义。 |
| 08 | [Toolkit 1.20.0 CDI support](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html)，Running a Workload / Non-CDI-Enabled Runtimes / Setting the CDI Mode Explicitly | 区分原生消费、NVIDIA runtime 的 CDI 模式与独立 Runtime Hook；仅有选择环境变量也不能直接判 legacy。 |
| 09 | [Toolkit 1.20.0 troubleshooting](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html)，Unknown Error / Affected Environments / Mitigations | 支持 hook/legacy 更新访问丢失、CPU/内存显式更新和 systemd 条件；不替正文选定更新接口与完整字段，未执行其处置建议。 |
| 10 | [NVIDIA README@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/README.md)，网页 Configuration Option Details / Shared Access / With CUDA Time-Slicing | 设备传递策略可多选；cdi-cri 需要 CRI 转发和消费端支持，envvar 是另一传递策略；replicas 不证明隔离。不把 NVIDIA 字段套用到 NPU。 |

GitHub 原文件返回的 blob：syft README `9ffd2affa3b00031ea1fd01ee3fe228379978492`；Ascend common/plugin/process 分别为 `6cd038e9f1d67a8a913aa4bb1301692f177b3dbe` / `b7692611b12884854d973fa2a3da18e381353f10` / `acbd7a1ec0703498abfcfcb6ce1aa493069091b1`；CDI SPEC `2bc480a20ce447f5281b5d6844a486a81bb635b0`；OCI Linux `c71757494ca743fd90692c25e4897bf74cf00388`。不把 blob SHA 当作 commit SHA，也不把历史作者记录的 curl 200 冒充本轮结果。

## 4. 逐项复核

### B21-C32 — P2 / OPEN

**权威条件：** 第十三次复核 L85。**位置证据：** 正文 L70、L76、L80–82、L108–112、L116、L130–136；第十四轮映射 L244。

**本轮认可：** L110 已明确区分“规则未交付→无法确定（缺方法）”与“规则已交付但样本缺项→无法确定（缺采样）”，并要求注明缺项。L82 和 L116 的缺规则优先无法确定门槛继续认可。Allocate/CDI/edits/最终 OCI 中间链、节点与许可/LSM 分开及不以数量/编号文本证明同一设备的边界不重开。

**仍未满足：**

1. **扫描与层匹配方法仍缺。** L70 仍使用“所选扫描配置”“字段以实际输出为准”，没有选定扫描范围、必要输出字段及成分/路径→来源层的匹配规则；层清单/diff_ids/annotations 不能替代逐库归属方法。抽查 01 确认 README 入口，不替作者完成配置或字段选型。宿主来源→最终挂载→目标路径的格式已有，但镜像库端尚未连接完整。
2. **稳定映射仍明确未交付。** L76 自列方法“未交付，unknown”；L80–82 仍是待填表。可见集管理与分配/CDI 中间链并未成为逐 ordinal→分配 ID/CDI→完整节点（类型/major/minor/路径/来源）→稳定身份的已交付规则。抽查 02 不能填补该连接。
3. **缺失分类及依赖未全量同步。** L108 仍只有“无法确定写 unknown”，L109 沿用“同上”；L112 仍引用“按已取证映射对应”，没有统一定位到已交付方法。L116 已有安全门槛，但依赖同一映射的对照表 L130–136 尚未统一关联方法及缺方法/缺采样分类。不能以单行分类改进同时关闭两套方法缺失。

**剩余关闭条件：** 在固定来源上交付所选扫描范围、必要字段与逐库归层规则，并连接镜像库、宿主注入来源、最终挂载和目标路径；交付逐 ordinal 的完整稳定映射规则。将两种无法确定的原因/记录格式同步到核对表、清单及 C34 的映射依赖比较/判断。**现场实际值可以 unknown；不要求拉取镜像、生成 SBOM、采集设备、审计全部 cataloger、实测或重开 C30。**

### B21-C33 — P2 / OPEN

**权威条件：** 第十三次复核 L100。**位置证据：** 正文 L88、L90、L145；第十四轮映射 L245；登记 L5325–5335、L5419–5429；作者记录 L12、L17。

**本轮认可：** 登记 L5335 已按有效响应内的 ID/options、310B allow-link、`!PresetVDevice` worker 组分别写条件，与抽查 03 一致；该登记残留已解决，不再列为剩余项。A/B 互斥分工、所选 `UseAscendDocker=true`、原生 `rw` 不接 wrapper `rwm`、`LD_LIBRARY_PATH` 不是库挂载等边界继续认可。新增芯片/manager/虚拟设备摘要是局部补充，不等于已经固定一个所选产品/输入组合。

**仍未满足：**

1. **新增 VIRTUAL 摘要出现事实矛盾，按原 C33 追记。** L88 新摘要将 `VIRTUAL` 关联到 `vdavinci`、`updateEnvAndPostHook` 和 poststop destroy hook（仅 `VdeviceID!=-1`）。但抽查 05 的 `addHook` 原文件 L370–400 显示：先按需要加入 prestart hook；输入 options 已含 `VIRTUAL` 时提前返回，**不会在该路径继续调用 CreateVDevice 或由该调用加入 poststop**。只有未提前返回，且 CreateVDevice 返回 `VdeviceID!=-1`，才调用 `updateEnvAndPostHook`（L750–812），该函数改 options/设备列表并加入 poststop。`addDevice` 的 VIRTUAL→`vdavinci` 选择是另一判断（L722–758）。正文同一 L88 后半保留了正确提前返回链，不能抵销前半新摘要的相反关联；须一致改正，并用所选输入完成纳入/排除。
2. **产品/manager/UB 仍未成为完整条件对应表。** L88 新摘要只列芯片类别和设备组，未选定产品、输入 ID/options、PresetVDevice 条件和实际环境键；L88 末尾及 L90 仍承认所选条件 unknown。抽查 05 的 `addManagerDevice`（L600–720）除芯片类型外还查 `GetProductType`，Atlas200ISoc/Atlas200 与其他产品分支不同；310B 有单独 manager 路径及 fallback，UB 还受目录存在条件限制。摘要不能把芯片类型当作全部必要条件，也未落到完整节点/许可/环境逐字段对应。本项要求选定设计条件与规则，不要求取得现场硬件值或建立支持交集。
3. **所选 wrapper 的必要 hook/库挂载证据仍未交付。** L88 及作者记录 L12/L17 继续明示 hook 可执行实现、实际库来源/目标/白名单未读。抽查 05 只支持 hook 引用、env 搜索路径与设备/cgroup 控制流，不支持把它们算作实际库挂载依据。登记已有读取范围不等于新补齐了这些局部证据；本轮审阅者阅读不能记成作者已交付。

**剩余关闭条件：** 保留已同步的 common 字段条件与路径分工；纠正新增 VIRTUAL/poststop 摘要，与既有正确控制流一致。为所选 wrapper 样板确定产品、输入 ID/options、PresetVDevice 等必要条件与实际环境键，交付完整节点/许可/环境对应表；按所选条件覆盖 manager/产品/UB，明确虚拟/poststop 纳入或排除。补该路径必要的 hook、库挂载来源/目标与白名单依据，同步正文/作者记录/登记的局部已读范围。**现场值、未选原生路径真正消费端及支持交集可 unknown；不要求安装、试运行、完整 dcmi 审计或实测。**

### B21-C34 — P1 / OPEN

**权威条件：** 第十三次复核 L115。**位置证据：** 正文 L108–112、L116–123、L125–136、L138–140；第十四轮映射 L246。

**本轮认可：** L130 已明确 CDI containerEdits 自身可含 hooks，与独立 legacy hook 分开；两路证据并存时先判混合、无法确定的排除规则已交付，抽查 06/08 支持该区分。L131 已补目标访问 `access`、规则索引、通配上下文、顺序位置、其余规则逐条保持及旧新记录要求；结合 L75 的完整许可字段清单，认可有序许可比较的字段级补充，**不再重复上一轮 access/索引缺项，也不以未填写现场旧新值阻断**。L110 缺失分类、L116 通用门槛、S1/R1、镜像/驱动回退拆分、重建新主体关联、replicas 解释收窄、NPU 独立对照未知及安全/授权边界继续认可。

**仍未满足：**

1. **两端模式配置/消费组合仍未固定。** L130 虽给 CDI 侧 CRI 字段及 hook 来源规则，但没有给出两端所选插件设备列表策略、runtime 模式/handler 消费组合及传递字段对应；legacy 端仍只有独立 prestart hook 的描述。抽查 10 明确传递策略可多选；抽查 08 还显示 NVIDIA runtime 的 CDI 模式也可使用选择环境变量。因此新排除规则有价值，但不能代替一对已经选定且可逐字段核对的基线/变体配置；站点 handler 实际名称可以待填，所选逻辑配置组合不能仅用待填代替。
2. **资源更新接口/完整字段及旧新格式仍未选定。** L135 仍写“候选字段为 CRI 更新对象/OCI linux.resources.cpu，固定字段未取，unknown”。抽查 09 支持显式 CPU/内存更新这一场景类别，不替作者选择接口、字段、单位/语义和完整旧新比较对象。现有主体/时间窗文字有所覆盖，但尚无与该所选更新对象绑定的更新前后采样及与重建生命周期分开的关联方法；L133–134 的回退拆分不能代替它。
3. **逐变体访问/负向恢复证据对象及映射依赖未闭合。** L130–136 的证据栏仍主要是三单快照、拒绝事件/注入集或共享影响记录；虽然 S1/R1 和各恢复栏要求访问证据，仍未逐变体指定可定位的受控访问、原负向边界恢复记录及其前后/恢复后目标主体、节点、时间窗关联格式。已有容器 ID/PID/节点/快照字段予以认可，缺的是这些身份与访问/恢复证据对象的绑定，不是要求各行机械复制公共集合。三单比较依赖的 C32 方法尚未交付，且缺方法/缺采样分类未统一同步；只能保持无法确定，不能凭可见性推定访问或边界恢复。

**剩余关闭条件：** 在保留新 hook 区分与混合排除规则的基础上，固定两端模式配置/消费组合及设备传递字段，排除并行传递路径。保留已补许可比较字段，选定资源更新接口/完整字段及旧新记录格式。逐变体明确更新或重建生命周期，并将已有主体/节点/时间窗绑定到受控访问和原负向边界恢复的证据定位格式；统一引用 C32 已交付的方法，缺方法时优先无法确定，并区分缺采样。保留 NPU 对照未知、S1/R1、回退拆分和全部安全/授权边界。**不要求执行试验、取得现场值、扩大生产权限或制造结果。**

## 5. Acceptance 与最终计数

| T05-01 acceptance / 原文件位置 | 本轮判断 | 原 ID |
|---|---|---|
| 镜像身份、构建输入、SBOM/签名、拉取策略 / L5403 | 沿用此前完整通过；不重审供应链 | C30 CLOSED，范围外 |
| 固定 runtime/Toolkit/CDI、各层与映射分离 / L5404 | 部分满足，未完整通过：版本/配置已有；扫描归层、稳定映射方法及同步仍缺 | C31 CLOSED，范围外；C32 OPEN |
| Ascend 独立实现与目标组合 / L5405 | 部分满足，未完整通过：登记 worker 条件已同步；所选路径必要证据仍缺，新增条件摘要须纠正 | C33 OPEN |
| 清单、异常/隔离、对照及来源案例 / L5406 | 部分满足，未完整通过：hook 区分、许可比较字段已有；配置对、更新对象、证据关联与映射依赖仍缺 | C34 OPEN |

四条 acceptance 汇总：**1 沿用既有完整通过 / 3 未完整通过**。本轮唯一范围 **0 CLOSED / 3 OPEN（1 P1、2 P2）**，**第十四次定向复核不通过**；没有新增 ID。判定依据是尚未交付的方法/证据关联与 C33 摘要事实矛盾，**不是 curl DNS 失败、现场值 unknown、没有实测或未证明整栈兼容**。不修改正文 `draft / source_checked` 或计划验收状态。

## 6. 结构校验与写入审计

- 写入前及报告写入后，原仓库 `PYTHONDONTWRITEBYTECODE=1 make check` 均 **PASS：96 content entries / 438 sources**。这些检查仅验证结构与本地文件链接，不验证技术正确性或远程正文。
- 为遵守只写本报告的边界，`make build` 在临时副本 `/private/tmp/b21-t05-01-recheck-14.TYInv5/validation/` 执行：复制原仓库源文件、本报告及既有 build 链接目标，使用原仓库虚拟环境 Python、禁写字节码；副本 `make check` / `make build` 均 **PASS：96 content entries / 438 sources**。仅在副本生成 `build/catalog.json` 和 `build/catalog.md`，不改原仓库 build。
- 三项原 ID/优先级/OPEN 状态、无新增发现 ID、9 个本地 Markdown 链接及行尾空白检查均 **PASS**。摘要审计覆盖 **397 个**起始 Git 所列 tracked/untracked 非忽略文件及 build 文件：既有文件摘要全部不变，唯一新增为本报告；六个指定输入与补读作者记录保持 §2 摘要。
- 本会话未修改作者正文、修订映射、作者来源记录、来源登记、任务计划、`src/kb/` 或测试；未执行容器/硬件实测。知识目录构建不是镜像构建或实验验证。

**最终技术结论：B21-C32、B21-C33、B21-C34 均 OPEN；0 CLOSED / 3 OPEN，第十四次定向复核不通过。C30/C31 保持此前 CLOSED、范围外；用户约定配置不作为已独立确认的执行元数据。**
