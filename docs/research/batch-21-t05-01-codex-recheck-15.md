# Batch 21 补交 T05-01 第十五次定向复核

## 1. 结论、角色与范围

- 日期：2026-10-14（Asia/Shanghai）。执行者：当前 Codex 会话，以独立审阅角色复核作者第十五轮修订；与作者修订角色分开，未派发其他模型或子代理。
- `gpt-6.1-sol / xhigh` **仅为用户约定**，不是本会话已独立确认的执行元数据。本会话未取得可独立核验的实际模型、推理档位或路由信息，不宣称实际模型一致性或无 fallback 已获独立确认。
- 唯一范围为 **B21-C32–C34**；剩余关闭条件以[第十四次复核](batch-21-t05-01-codex-recheck-14.md) L81、L95、L109 为权威，[初审报告](batch-21-t05-01-codex-review.md)用于核对原 ID、优先级及职责。C30/C31 保持此前 CLOSED，范围外，不重审。
- **0 CLOSED / 3 OPEN（1 P1、2 P2）；第十五次定向复核不通过。** 认可 VIRTUAL 摘要纠正、策略可多选说明和 R1 公共证据格式的局部补充，但不把这些局部修订计为整项关闭。
- 没有新增发现 ID。R1 的剩余证据关联问题继续归入 C34；没有另立新事实错误项。
- 未安装组件、拉取或构建镜像、运行容器、生成 SBOM、采集设备、修改运行配置、接入集群或执行访问/负向/恢复实测。本报告只评审来源与设计，不建立硬件验证结论。

| 原 ID | 原优先级 | 本轮状态 | 正文位置 / 主要剩余问题 |
|---|---|---|---|
| B21-C32 | P2 | OPEN | L70、L76、L80–82、L108–112、L116、L130–136：扫描归层和逐 ordinal 稳定映射方法未交付，缺方法/缺采样分类未全量同步 |
| B21-C33 | P2 | OPEN | L88、L90、L145；作者记录 L12、L17：VIRTUAL 摘要矛盾已解决，但所选 wrapper 条件对应表及必要 hook/库挂载依据仍缺 |
| B21-C34 | P1 | OPEN | L125、L130–136：模式配置对、资源更新对象仍未固定，R1 公共格式未闭合逐变体访问/负向恢复关联，并依赖 C32 缺失方法 |

## 2. 输入身份与单文件边界

用户给出的 **2 个 SHA-256 前缀均吻合**。完整起始摘要如下；正文及仓库记录的行号均指原文件，不是网页阅读器坐标。

| 输入 | 起始 SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md)，145 行 | `a0115d810842b88930d5c66fb28ed21cfbc2fc409f28c6d8ea391e434450ecbd` |
| [修订映射](batch-21-review-fixes.md)，252 行 | `e1e5b5d8b9979a94bf88e9293be8cf1e992fb2d9e7db139c5b80050c90e6ebe4` |
| [第十四次复核](batch-21-t05-01-codex-recheck-14.md) | `13196d1390443427a0a4d5ad6006bbcb8b6fac02533803a2505601379efc69e6` |
| [初审报告](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` |
| [任务计划](../../plans/full-coverage-backlog.yaml)，T05-01 acceptance L5403–5406 | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml)，438 项 | `dc7bfae1a35d53fa31e816aae0b8efcbcaddafaae3cf249d915010d5b28c114c` |

仅采用修订映射的 **T05-01 第十五轮节 L248–252**，将其作为落盘改动索引，不作为关闭证据。补读 README、编写指南、内容总目录、metadata schema，以及[作者来源记录](batch-21-t05-01-sources.md) L12、L17（摘要 `ae26470307fe2bb04c255c76d408343c16be53c4d178baf4a87fe44a6a49fed5`），用于核对所选 Ascend 路径的已读范围。本轮审阅者读取一次源，不等于作者已补交相应证据。

起始工作区已有修改与未跟踪文件，均保留、不回滚。原仓库唯一写入目标为本报告；请求诊断、摘要审计及隔离构建使用 `/private/tmp/b21-t05-01-recheck-15.kDihzb/`，不作为永久证据附件或仓库内容。

## 3. 一次源文字抽查与方法限制

### 3.1 实际 curl 请求

本机 curl **8.7.1**，对下表 01–10 各执行一次只读 GET。GitHub 文件请求同仓库/ref/路径的 `raw.githubusercontent.com` 原文地址；厂商/PyTorch 请求表列版本 URL。请求清单及结果留在临时目录的 `urls.tsv`、`curl-results.tsv`、`*.stderr`。调用形态为：

```bash
curl --disable --location --silent --show-error --connect-timeout 8 --max-time 20 \
  --output "$audit_dir/$name.body" --write-out '%{http_code}' "$url"
```

使用默认 TLS 校验，未使用 `-k`、改 DNS/证书、提权或绕过沙箱。**10/10 退出码 6、HTTP `000`，诊断均为 `Could not resolve host`。** 未取得 curl 响应正文，TLS 握手未发生；不声称 curl 成功、HTTP 200 或本机完成证书验证。登记中的历史 curl 200 不是本轮结果。

### 3.2 允许的只读替代通道

使用 `web.run` 阅读版本化厂商/PyTorch 页面及 README 的实际文字，使用 GitHub 只读连接器读取固定 ref 的原文件区间，逐点核对字段和控制流，**不是仅检查可达性**。网页通道可能使用缓存或归一化文本，版本 URL 本身也不是内容哈希，不能当成本机即时 GET 或不可变页面快照。下表源码行号只来自连接器读取的原文件区间；网页以章节定位，不将网页坐标拼成源码锚点。

| 点 | 本轮实际阅读的一次源 / 位置 | 核对文字及有限支持范围 |
|---|---|---|
| 01 | [syft README@v1.54.1](https://github.com/anchore/syft/blob/v1.54.1/README.md)，Features / The basics | 支持镜像/文件系统成分扫描及 SBOM 输出格式入口；不能替当前正文选定扫描范围、必要字段和逐库归层规则。不重开 C30。 |
| 02 | [PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html)，Best practices / Device-agnostic code 的 `CUDA_VISIBLE_DEVICES` 段 | 支持管理 PyTorch 可见 GPU 集合；该段不是逐 ordinal→分配 ID/CDI→完整节点→UUID 的连接规则，不据此否定其他身份接口。 |
| 03 | [Ascend common.go@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go)，L90–125 | 有效响应内 ID 串/options、310B allow-link、`!PresetVDevice` worker 组分别有条件；登记 L5335 的已同步边界继续认可。 |
| 04 | [Ascend process.go@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go)，L60–130、L243–330、L345–405、L576–720、L722–812、L850–910 | 核对 VIRTUAL 提前返回、未提前返回后的 CreateVDevice/poststop、独立 vdavinci 选择、产品/manager/UB 条件、env 库路径与设备非空分支；未读取 hook 可执行内部的真正库挂载/白名单实现。 |
| 05 | [CDI SPEC@cb98bcf6](https://github.com/cncf-tags/container-device-interface/blob/cb98bcf66dc68530012483bd56e33e14d815e167/SPEC.md)，L90–175 | 全局/设备级 edits 的条件，以及节点、mounts、env、hooks 字段；CDI edits 自身含 hooks，不能只凭存在 hook 判独立 legacy 路径。 |
| 06 | [OCI Linux@92249139](https://github.com/opencontainers/runtime-spec/blob/92249139eea7161e13745abd4cb6d0ea02a3227a/config-linux.md)，L127–151、L402–418 | 完整节点与访问许可分开；许可含 allow/type/major/minor/access，列表有序，省略的设备类型/设备号有通配语义。 |
| 07 | [Toolkit 1.20.0 CDI support](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html)，Running a Workload / Non-CDI-Enabled Runtimes / Setting the CDI Mode Explicitly | 区分原生 CDI、NVIDIA runtime 的 CDI 模式与独立 Runtime Hook；CDI 模式也能使用 `NVIDIA_VISIBLE_DEVICES`，变量存在不证明 legacy。 |
| 08 | [Toolkit 1.20.0 troubleshooting](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html)，NVML/SELinux、Unknown Error / Affected Environments / Mitigations | 权限错误与 hook/legacy 更新访问丢失分开；显式 CPU/内存更新及 systemd 条件可触发该场景，页面不替正文选定更新接口/完整字段。未执行其恢复建议。 |
| 09 | [NVIDIA README@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/README.md)，Configuration Option Details / Shared Access / With CUDA Time-Slicing | 设备列表策略可多选；envvar、volume-mounts、cdi-annotations、cdi-cri 是不同传递方式，cdi-cri 需要 CRI 转发与消费端支持；replicas 不证明隔离。 |
| 10 | [NVIDIA server.go@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go)，L280–438、L448–481 | `AnyCDIEnabled` 与 `AllCDIEnabled` 分开，非纯 CDI 时继续按 Includes 添加 envvar/volume-mounts，`PassDeviceSpecs` 另有条件；cdi-cri 写 `CdiDevices[].Name`。只写策略“含 cdi-cri”不能排除其他传递路径。 |

连接器返回的文件 blob SHA：common.go `6cd038e9f1d67a8a913aa4bb1301692f177b3dbe`；process.go `acbd7a1ec0703498abfcfcb6ce1aa493069091b1`；CDI SPEC `2bc480a20ce447f5281b5d6844a486a81bb635b0`；OCI Linux `c71757494ca743fd90692c25e4897bf74cf00388`；NVIDIA server.go `9281b48ef52f9eda9cbed6d98491729da85b5a75`。这些是文件 blob，不冒充 commit SHA。

## 4. 逐项复核与剩余关闭条件

### B21-C32 — P2 / OPEN

**权威条件：** 第十四次复核 L81。**位置证据：** 正文 L70、L76、L80–82、L108–112、L116、L130–136；第十五轮映射 L252。

**认可的修订：** L110 明示“规则未交付→无法确定（缺方法，当前状态）”与“规则已交付但样本缺项→无法确定（缺采样）”。认可诚实限定，而非要求作者填写不存在的现场结果。此前 Allocate/CDI/edits/最终 OCI 中间链、节点与许可/LSM 分离、不以数量或编号文本证明同一设备的边界不重开。

**仍未满足：**

1. **扫描与逐库归层方法仍缺。** L70 仍用“所选扫描配置”“字段以实际输出为准”，未选定扫描范围、必要字段及成分/路径→来源层规则；层清单、diff_ids、annotations 不能替代这一规则。抽查 01 只确认工具入口，没有完成当前作者交付的配置/字段选择；镜像库端到宿主注入来源/最终挂载/目标路径的完整连接仍缺。
2. **逐 ordinal 稳定映射仍未交付。** L76 明写“未交付，unknown”，L80–82 是待填表。抽查 02 的可见集管理不补成逐 ordinal→分配 ID/CDI 名或传递字段→完整节点（类型、major/minor、路径/来源）→稳定身份的规则。空表和无法确定门槛只能防止误判，不能作为已交付的方法。
3. **缺失分类与依赖未全量同步。** L108 仍为“无法确定写 unknown”，L109 为“同上”；L112 仍依赖“按已取证映射对应”。L116 已有缺规则优先无法确定门槛，但同一映射的清单/对照 L130–136 未统一引用一个已交付方法及缺方法/缺采样格式。映射 L252 自述“方法仍 unknown”，不构成关闭证据。

**剩余关闭条件：** 在固定来源上交付所选扫描范围、必要字段及逐库归层规则，连接镜像库、宿主注入来源、最终挂载和目标路径；交付逐 ordinal 的完整稳定映射规则。将缺方法/缺采样的原因、缺项与记录格式同步到核对表、清单和 C34 的映射依赖比较/判断。**现场值可 unknown；不要求拉取镜像、生成 SBOM、采集设备、审计全部 cataloger 或实测；不重开 C30。**

### B21-C33 — P2 / OPEN

**权威条件：** 第十四次复核 L95。**位置证据：** 正文 L88、L90、L145；第十五轮映射 L250；作者记录 L12、L17；登记 L5335、L5419–5429。

**认可的修订：** L88 已将输入 options 含 VIRTUAL 的提前返回与 `addDevice` 内 vdavinci 选择分开；未提前返回才调用 CreateVDevice，仅返回 `VdeviceID!=-1` 才调用 `updateEnvAndPostHook` 改设备列表/options 并添加 poststop。与抽查 04 的 `addHook` L345–405、`addDevice` / `updateEnvAndPostHook` 所在 L722–812 读取区间的控制流一致。**前轮新增摘要矛盾已解决，不再列入剩余条件。** 此处“不加 poststop”限于该调用不继续进入添加路径，不推定删除输入 spec 中既有 hooks。common worker 条件同步、A/B 互斥分工、原生 rw 不拼 wrapper rwm、env 搜索路径不当作库挂载等既有边界继续认可。

**仍未满足：**

1. **分支摘要不是所选条件对应表。** L88 仍未确定一组产品、输入 ID/options、PresetVDevice 条件及实际环境键，也未据此交付完整节点/许可/环境字段对应。抽查 03/04 确认 worker、310B、产品分支和 UB 目录条件须分别处理；正文末尾继续把这些所选关联写成 unknown。支持交集与现场值可 unknown，但不能替代设计条件与规则的选定。
2. **所选 wrapper 必要 hook/库挂载依据仍未交付。** L88 与作者记录 L12、L17 明示 hook 可执行、实际库来源/目标/白名单未读。抽查 04 的库路径逻辑只改 `process.env`，hook 引用与设备控制流不是实际库挂载证据；登记 L5419–5429 也没有新补这些局部已读范围。本轮审阅者重新读 process.go 不能算作者已补交 hook 内部取证。

**剩余关闭条件：** 保留已纠正的 VIRTUAL 提前返回/独立设备命名和 common 字段条件；为所选 `UseAscendDocker=true` 样板确定产品、输入 ID/options、PresetVDevice 等必要设计条件与实际环境键，交付完整节点/许可/环境对应表，按所选条件覆盖 manager/产品/UB，并明确虚拟/poststop 纳入或排除。补所选路径必要的 hook、库挂载来源/目标与白名单依据，同步正文/作者记录/登记的局部已读范围。**现场值、未选原生路径真正消费端和支持交集可 unknown；不要求安装、试运行、完整 dcmi 审计或实测。**

### B21-C34 — P1 / OPEN

**权威条件：** 第十四次复核 L109。**位置证据：** 正文 L108–112、L116–123、L125、L130–136、L138–140；第十五轮映射 L251。

**认可的修订：** L130 已列 cdi-cri 与 envvar/volume-mounts 传递方式，明确策略可多选，符合抽查 09/10；CDI edits 自身 hooks 与独立 legacy hook 区分继续认可。L125 已补 R1 公共证据格式：audit/AVC 定位、进程/设备/时间、恢复后 config.json 摘要与恢复后主体/节点/时间窗，并保留重建按新主体关联。认可这份格式，**不再说完全没有证据对象**，也不要求各行机械复制公共集合。此前有序许可比较、S1/R1、镜像/驱动回退拆分、replicas 解释收窄、NPU 独立对照未知和全部授权/安全边界不重开。

**仍未满足：**

1. **模式配置对仍未固定，混合路径排除不能代替配置选型。** L130 的基线是策略“含 cdi-cri”，变体仍是“envvar 或 volume-mounts”，没有选定两端完整策略集合、runtime 模式/handler 消费组合及传递字段对应，也未显式排除并行的非 CDI/DeviceSpec 路径。抽查 10 的 AnyCDIEnabled/AllCDIEnabled 控制流允许组合继续输出其他策略字段；抽查 07 显示选择环境变量也可能由 CDI 模式消费。因此 envvar 不是 legacy 充分证据，只补“可多选”不能构成受控配置对。站点 handler 名和现场旧新值可待填，逻辑配置组合须先选定。
2. **资源更新对象仍明确未取。** L135 仍写“候选字段为 CRI 更新对象/OCI linux.resources.cpu，固定字段未取，unknown”。抽查 08 只确认 CPU/内存显式更新的场景，不能代替接口、完整字段、单位/语义及旧新记录格式。需要与所选更新对象关联的前后采样，不能借用镜像/驱动回退或重建记录来补齐更新生命周期。
3. **R1 格式仍未闭合成功访问、负向恢复及逐变体生命周期关联。** L125 给了 audit/AVC 路径与恢复后摘要，但未选定受控成功访问的记录对象/结果、单独授权负向拒绝的记录对象，以及它们与各变体前后/恢复后主体、目标节点和时间窗的定位规则。L130–136 的证据栏仍主要是三单快照、拒绝事件/注入集或共享影响；恢复判据文字与公共路径/摘要不能自动生成这些证据的关联。正文 L75 已限定无拒绝只支持“未见拒绝”，不能代替受控成功访问结果；恢复后的配置摘要也未连接原负向边界的恢复比较。公共格式可统一引用，但须规定每个变体在更新或重建中的绑定方法。
4. **C32 依赖未补。** 三单/框架物理对应仍依赖未交付的稳定映射方法，缺方法/缺采样分类也未统一同步；不能凭三单可见性判访问或恢复完成。此处引用 C32 的同一方法缺口，不新增发现，也不把两项职责混为一项。

**剩余关闭条件：** 固定两端完整设备传递策略集合及 runtime 模式/handler 消费组合、传递字段和旁路排除，保留 CDI 自身 hooks/独立 legacy 区分。保留已补许可比较字段，选定资源更新接口、完整字段及旧新记录格式。完善 R1 的受控成功访问与原负向边界恢复记录，把已有主体/节点/时间窗按各变体更新或重建生命周期绑定到可定位证据；公共格式可以复用，无需逐行复制。统一引用 C32 已交付方法，缺方法时优先无法确定并区分缺采样。保留 NPU 独立对照未知、S1/R1、回退拆分及全部安全/授权边界。**不要求执行试验、取得现场值、扩大生产权限或制造结果。**

## 5. Acceptance 与最终计数

| T05-01 acceptance / 原文件位置 | 本轮判断 | 原 ID |
|---|---|---|
| 镜像身份、构建输入、SBOM/签名、拉取策略 / L5403 | 沿用此前完整通过；范围外，不重审供应链 | C30 CLOSED |
| 固定 runtime/Toolkit/CDI、各层与映射分离 / L5404 | 部分满足，未完整通过：扫描归层、稳定映射方法及同步仍缺 | C31 CLOSED（范围外）；C32 OPEN |
| Ascend 独立实现与目标组合 / L5405 | 部分满足，未完整通过：VIRTUAL 摘要已纠正；所选条件对应表与必要 hook/库挂载证据仍缺 | C33 OPEN |
| 清单、异常/隔离、对照及来源案例 / L5406 | 部分满足，未完整通过：策略说明与 R1 格式局部补充；配置对、更新对象、访问/恢复关联和映射依赖未闭合 | C34 OPEN |

四条 acceptance 汇总：**1 沿用既有完整通过 / 3 未完整通过**。本轮范围 **0 CLOSED / 3 OPEN（1 P1、2 P2）**，**第十五次定向复核不通过**；没有新增 ID。阻断依据是尚未交付的具体方法、条件对应和证据关联，**不是 curl DNS 失败、现场值 unknown、没有实测或未证明整栈兼容**。不改正文 `draft / source_checked` 或任务验收状态。

## 6. 结构校验与写入审计

- 写入前原仓库 `PYTHONDONTWRITEBYTECODE=1 make check` **PASS：96 content entries / 438 sources**；仅验证结构与本地文件链接，不验证技术正确性或远程文字。
- 报告写入后原仓库 `PYTHONDONTWRITEBYTECODE=1 make check` **PASS：96 content entries / 438 sources**。
- 为遵守单文件写入边界，在 `/private/tmp/b21-t05-01-recheck-15.kDihzb/validation/` 复制源文件、本报告及既有 build 链接目标，用原仓库虚拟环境 Python、禁写字节码执行 `make check` / `make build`，均 **PASS：96 content entries / 438 sources**；仅在副本重新生成 `build/catalog.json` 和 `build/catalog.md`，不改原仓库 build。最终补记后再同步副本并复跑同样检查。
- 原 ID/优先级/OPEN 状态、无新增发现 ID、9 个本地 Markdown 链接和行尾空白检查均 **PASS**。摘要审计覆盖 **398 个**起始 Git 所列 tracked/untracked 非忽略文件及 build 文件：既有文件摘要不变，唯一新增为本报告；六个指定输入与补读作者记录均保持 §2 摘要。临时诊断与副本不是原仓库改动。
- 未修改 `src/kb/` 或测试，本轮不需要 `make test`；结构检查和构建通过不改变 §4 技术状态。
- 本会话未修改作者正文、修订映射、作者来源记录、来源登记、任务计划、`src/kb/` 或测试；未执行容器/硬件实测。知识目录构建不是镜像构建或实验验证。

**最终技术结论：B21-C32、B21-C33、B21-C34 均 OPEN；0 CLOSED / 3 OPEN，第十五次定向复核不通过。C30/C31 保持此前 CLOSED、范围外；用户约定配置不作为已独立确认的执行元数据。**
