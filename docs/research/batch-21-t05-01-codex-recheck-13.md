# Batch 21 补交 T05-01 第十三次定向复核

## 1. 结论、角色与范围

- 日期：2026-10-14（Asia/Shanghai）。执行者：当前 Codex 会话，承担独立审阅角色；未承担本轮作者修订。
- `gpt-6.1-sol / xhigh` **仅为用户约定**。本会话没有可独立核验的实际模型/推理配置执行元数据，不将约定、作者自述或历史记录写成已确认的执行元数据。
- 唯一复核范围：**B21-C31–C34**；以[第十二次复核](batch-21-t05-01-codex-recheck-12.md) L79、L95、L112、L125 的剩余关闭条件为权威。[初审报告](batch-21-t05-01-codex-review.md)仅用于核对原 ID 与优先级。C30 保持此前 CLOSED，范围外，不重开供应链验收。
- **1 CLOSED / 3 OPEN；第十三次定向复核不通过。** C31（P2）关闭；C32（P2）、C33（P2）、C34（P1）仍 OPEN，开放项为 **1 P1、2 P2**。
- 没有新增发现 ID。正文已改正的条件与安全门槛分别认可；登记中未同步的 Ascend 条件仍追记 C33，模式判定的缺项仍归 C34，不另立发现。
- 未安装组件、拉取或构建镜像、运行容器、生成 SBOM、采集设备、修改配置、执行负向/恢复试验。本报告是来源与设计审阅，不是硬件验证。

## 2. 输入身份与单文件边界

用户给出的两个 SHA-256 前缀全部吻合。以下为起始读取的完整摘要；正文、映射、计划、登记与历史报告的位置使用仓库原文件行号。

| 输入 | 起始 SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md)，145 行 | `a9ebc5abb58375ffdf9d49ec85875b73bc0e5ed418c9596aec93bc88f13af01e` |
| [修订映射](batch-21-review-fixes.md)，240 行 | `0cd4ea18e5c3bd1964ad16ac69171c105e1fbd462a8665869c81c6b91da295fe` |
| [第十二次复核](batch-21-t05-01-codex-recheck-12.md) | `ad06d31033bd585c816c41beb9b07a9070055298a1d5500c75db09febe61f578` |
| [初审报告](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` |
| [任务计划](../../plans/full-coverage-backlog.yaml)，T05-01 acceptance L5403–5406 | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml)，438 项 | `61388eb10023ff425ab83891604529b05764afbe19b478257feb62a19c1262f7` |

修订映射仅采用 **T05-01 第十三轮节 L235–240**，作为落盘改动索引而非关闭证据；第十二轮节现仅一份（L228–233），去重已完成。另读 README、编写指南、内容总目录和 metadata schema。为检查 C33 的同步要求，补读[作者来源记录](batch-21-t05-01-sources.md) L12、L17（摘要 `ae26470307fe2bb04c255c76d408343c16be53c4d178baf4a87fe44a6a49fed5`）；只核对已读/未读范围，不把作者或历史审阅者的取证冒充本轮取证。关联 Ascend 来源案例/待执行实验只核对缺项和授权边界，不重审外部事件史。

起始工作区已有修改及未跟踪文件，本会话不回滚、不代写。原仓库唯一允许新增或修改的文件为本报告；请求诊断、摘要审计与 catalog 构建使用临时目录，不纳入仓库。

## 3. 一次源抽查与方法限制

### 3.1 实际 curl 请求

本机 curl **8.7.1**。对下表 01–12 实际执行只读 GET：GitHub 文件用同仓库/ref/路径的 `raw.githubusercontent.com` 地址；厂商/PyTorch 页面用表内版本 URL。请求清单与逐点结果保留于 `/private/tmp/b21-t05-01-recheck-13.H4AGqM/` 的 `urls.tsv`、`curl-results.tsv`、`*.stderr`。调用形态：

```bash
curl --disable --location --silent --show-error --connect-timeout 8 --max-time 20 \
  --output "$audit_dir/$name.body" --write-out '%{http_code}' "$url"
```

保持默认 TLS 校验；没有使用 `-k`、改 DNS/证书、提权或绕过沙箱。**12/12 退出码 6、HTTP `000`，均为 `Could not resolve host`。** 没有取得 curl 响应正文，TLS 握手未发生；不声称 curl 成功、HTTP 200 或本机验证了远端 TLS 链。

### 3.2 允许的只读替代通道与文字核对

使用 `web.run` 读取版本化文档正文，并使用 GitHub 只读连接器读取同 ref 原文件区间，实际核对文字、字段及控制流，**不是只判可达性**。网页读取可能使用缓存并归一化文本，不等于本机即时 GET；GitHub 行号采用原文件读取区间，不把网页阅读器行号拼成源码锚点。

| 点 | 精确一次源 / 本轮实际阅读位置 | 支持的核对及边界 |
|---|---|---|
| 01 | [containerd config@v2.4.1](https://github.com/containerd/containerd/blob/v2.4.1/docs/cri/config.md)，GitHub L1–365 | Config versions、Cgroup Driver、Runtime classes、Full configuration；核对完整表头/default_runtime_name/runtime_type、systemd 条件及 v2→v3，不证明现场生效或全模式默认值有效。 |
| 02 | [syft README@v1.54.1](https://github.com/anchore/syft/blob/v1.54.1/README.md)，GitHub 全文及网页 Features/The basics | 镜像/文件系统扫描与输出格式入口；README 入口不能替代正文所缺的扫描范围、逐库字段与层匹配方法；不重开 C30。 |
| 03 | [PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html)，网页 Best practices / Device-agnostic code 的 CUDA_VISIBLE_DEVICES 段 | 可见集管理，不把该段扩充为 ordinal→UUID/节点的稳定映射；也不据此断言框架不存在其他接口。 |
| 04 | [Ascend common.go@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go)，GitHub L90–130 | 有效响应中 ID/options 不受 worker 条件限制；allow-link 由 310B 条件控制；只有 worker 环境组受 !PresetVDevice 限制。 |
| 05 | [Ascend plugin.go@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go)，GitHub L1080–1175 | 原生 DeviceSpec 的 rw、UseAscendDocker 两条互斥分支；不审计完整 ID 生成链，不替原生分支指定未经读取的消费端。 |
| 06 | [Ascend process.go@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go)，GitHub L185–245、L243–410、L490–580、L600–812、L850–910 | 库搜索路径修改、设备集 gate、产品/UB 分支、完整节点/cgroup rwm、VIRTUAL 提前返回、CreateVDevice 与 poststop 条件；添加 hook 引用不等于已读 hook 可执行实现，改 LD_LIBRARY_PATH 不等于库挂载。 |
| 07 | [CDI SPEC@cb98bcf6](https://github.com/cncf-tags/container-device-interface/blob/cb98bcf66dc68530012483bd56e33e14d815e167/SPEC.md)，GitHub L90–265 | qualified kind/name、全局/设备级 edits、deviceNodes/mounts/env/hooks；存在 hook 不足以区分 CDI 与独立 legacy 注入。 |
| 08 | [OCI Linux@92249139](https://github.com/opencontainers/runtime-spec/blob/92249139eea7161e13745abd4cb6d0ea02a3227a/config-linux.md)，GitHub L127–151、L402–418 | 完整节点与许可分离；许可条目有 access、顺序及可选字段的通配语义，不能只按 type/major/minor 选择比较对象。 |
| 09 | [Toolkit 1.20.0 CDI support](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html)，网页 Running a Workload / Non-CDI-Enabled Runtimes / Setting the CDI Mode Explicitly | CDI 原生消费、NVIDIA runtime CDI 模式和独立 NVIDIA Runtime Hook 的区别；前者允许 CDI 自身的 edits/hooks，不能把任意 hook 都算作另一注入路径。 |
| 10 | [Toolkit 1.20.0 troubleshooting](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html)，网页 NVML/SELinux、Unknown Error、Affected Environments、Mitigations | hook/legacy 更新访问丢失、CPU/内存显式更新及 systemd 条件、重建/缓解边界；不提供正文欠缺的所选更新接口与完整字段，未执行其处置建议。 |
| 11 | [NVIDIA README@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/README.md)，网页 Configuration Option Details / Shared Access to GPUs / With CUDA Time-Slicing | 传递策略可多选，cdi-cri 的转发/消费前提，replicas 的计数作用域与 time-slicing 边界；不将 NVIDIA 字段用于 NPU。 |
| 12 | [NVIDIA server.go@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go)，GitHub L280–481 | ValidateRequest、ID 策略/去重、qualified 名与 CdiDevices 响应，以及 CDI/non-CDI 策略控制流；不把中间链补成框架稳定映射。 |

GitHub 本轮返回的原文件 blob：containerd config `3a206263f4f9e76b6ca14110461b8661a03b1619`；syft README `9ffd2affa3b00031ea1fd01ee3fe228379978492`；Ascend common/plugin/process `6cd038e9f1d67a8a913aa4bb1301692f177b3dbe` / `b7692611b12884854d973fa2a3da18e381353f10` / `acbd7a1ec0703498abfcfcb6ce1aa493069091b1`；CDI SPEC `2bc480a20ce447f5281b5d6844a486a81bb635b0`；OCI Linux `c71757494ca743fd90692c25e4897bf74cf00388`；NVIDIA server `9281b48ef52f9eda9cbed6d98491729da85b5a75`。blob 不是 commit、现场输出或实验结果。本轮没有重新解引用所有 tag，也没有重读 runc 状态文件；这些此前已认可部分不作为新取证成果。

## 4. 逐项判断与剩余关闭条件

### B21-C31 — P2 / CLOSED

**权威条件：** 第十二次复核 L79。**位置证据：** 正文 L64、L145；第十三轮映射 L237。

**关闭证据：** L64 已将两处省略表头分别展开为 `plugins."io.containerd.cri.v1.runtime".containerd`＋`default_runtime_name`、`plugins."io.containerd.cri.v1.runtime".containerd.runtimes.<handler>`＋`runtime_type`，不再依赖未定义的省略号。抽查 01 的 Runtime classes 与 Full configuration 直接支持这两个定位；其中完整配置的 runc 默认记录与自定义 runtime 示例不能混为所有部署都生效的设置。正文将这些内容限定为所选 v3 模式的记录清单，保留“完整键｜来源限定参考值｜实际值或 unknown｜证据”，并串接配置文件/摘要、daemon/endpoint、Pod handler、容器与有效状态/日志对象。

systemd 条件、kubelet 手动配置或启用自动探测、runc 类设置一致的前提继续保留，抽查 01 已核对；L145 只将现场消费输出列为 unknown，并引用已补齐的完整键清单，两者不再冲突。此前已认可的 v3 分区、v2 转换、RuntimeClass 与 runc 状态/日志关联不重开。**剩余关闭条件：无。** 本项关闭仅证明本轮要求的配置记录方法已交付，不表示取得现场输出、配置已经生效或全栈兼容已验证。

### B21-C32 — P2 / OPEN

**权威条件：** 第十二次复核 L95。**位置证据：** 正文 L70、L73、L76、L80–82、L108–110、L112、L116；第十三轮映射 L238。

**已满足：** L82 示例判定现有“无法确定”，且规则缺失时只允许该判定；L116 的 GPU/NPU 通用映射门槛已同步，不再仅保护 NPU。Allocate→CDI→edits→最终 OCI 的中间链、节点/许可/LSM 分离及不以数量或编号文本证明同一设备继续认可；抽查 07、08、12 支持相应有限机制。

**仍未满足：**

1. L70 仍以“所选扫描配置”“字段以实际输出为准”表示待确定要求；没有选定扫描范围、必要输出字段及成分/路径→来源层的匹配规则。层清单与 diff_ids 记录不能自行完成逐库归属。抽查 02 只支持工具/格式入口，未使这一缺失的方法成为已交付。
2. L76 明确写稳定物理标识映射方法“未交付，unknown”；L80–82 是待填写表，不是逐 ordinal 的可见集→分配 ID/CDI→完整节点→稳定身份规则。抽查 03 的可见集管理以及抽查 12 的分配中间链均不能补足框架端与稳定物理身份的连接。
3. L108–110 仍统一写“无法确定写 unknown”，未分别规定方法/规则缺失与现场采样缺失的原因和记录格式；L112 的“按已取证映射对应”及依赖该映射的对照比较也未统一关联一个已交付方法。新增表头/示例和 L116 门槛是安全进展，不等于扫描和稳定映射两套方法已完成。

**剩余关闭条件：** 在固定来源基础上交付所选扫描范围、必要字段与层匹配规则，将镜像内库关联到宿主注入来源、最终挂载和目标路径；交付逐 ordinal 的完整稳定映射规则。分别标记“规则未交付→无法确定”和“规则已交付但样本缺项→无法确定”，同步核对表、清单及 C34 的映射依赖比较/判断。**实际值可以 unknown；不要求拉取镜像、生成 SBOM、采集设备、审计全部 cataloger、实测或重开 C30。**

### B21-C33 — P2 / OPEN

**权威条件：** 第十二次复核 L112。**位置证据：** 正文 L88、L90、L145；第十三轮映射 L239；登记 L5325–5335；补读作者记录 L12、L17。

**已满足：** L88 的所选 B 路径已按字段拆分：有效响应中的 ID/options 不受 `!PresetVDevice` 限制，allow-link 由 `RealCardType==Ascend310B` 控制，worker 环境组才受 `!PresetVDevice` 限制；抽查 04 的 L107–121 支持这一纠正。A/B 互斥分工、所选 UseAscendDocker=true、原生 rw 不接成 wrapper rwm、LD_LIBRARY_PATH 不是挂载的边界继续认可；抽查 05、06 已核对。**未选原生路径的真正消费端可以继续 unknown，不阻断所选 wrapper 路径。**

**仍未满足：**

1. 正文改正的条件尚未同步登记：L5335 仍将“ID 串/runtime options/310B allow-link/worker 组”一起限定为 `!PresetVDevice`，与同 commit common.go 及正文新字段级表述不符。这是前次已确认问题的登记残留，继续归 C33，不新增 ID。
2. L88 自列 api 实际环境键、所选产品、manager/UB 条件及节点/许可逐字段关联为 unknown，L90 仍以固定 commit 与未知条件代替所选样板条件。没有交付所选产品、输入 ID/options、字段级条件及最终节点/许可/环境对应表；不是要求取得现场值或支持交集。
3. 所选 wrapper 路径需要的 hook 可执行行为、库挂载来源/目标与白名单仍未取得。作者记录 L12/L17 与正文均披露未读；抽查 06 只核实添加 hook 引用、设备/cgroup 和库搜索路径的控制流，不把这些内容算作 hook 内部行为或真正库挂载证据。
4. L88 虽保留 VIRTUAL 提前返回、非提前返回调用 CreateVDevice、有效 VdeviceID 才进入更新/poststop 的条件链，但“未选分支明确排除”未绑定所选 options、PresetVDevice 或其他固定条件。抽查 06 的 addHook 显示非 VIRTUAL 仍调用 CreateVDevice；因此没有根据所选输入完成虚拟/poststop 纳入或排除。

**剩余关闭条件：** 保留路径分工与正文条件纠正，并同步登记；为所选 wrapper 路径确定产品、输入 ID/options、实际环境键及字段级条件，落完整节点/许可/环境对应表。补该路径必要的 hook、库挂载来源/目标与白名单依据；用所选条件完成虚拟/poststop 的纳入或排除，同步正文/作者记录/登记的局部已读范围，不把审阅者读取算作作者交付。**现场值、未选原生路径与支持交集可 unknown；不要求安装、试运行、完整 dcmi 审计或实测。**

### B21-C34 — P1 / OPEN

**权威条件：** 第十二次复核 L125。**位置证据：** 正文 L108–110、L112、L116–123、L125–136、L138–140；第十三轮映射 L240。

**已满足：** L116 已补 GPU/NPU 通用的规则缺失优先门槛；L130 新增混合路径不强行归因的限制。S1/R1、镜像/驱动回退拆分、重建后新主体关联、replicas 只作计数对照、NPU 固定对照未知的收窄及授权/安全/来源案例边界均继续认可。不要求把 NVIDIA 字段套用于 NPU，不要求各行机械重复公共安全集合。

**仍未满足：**

1. **模式配置对：** L130 增加 CRI CDIDevices 与 cdi_spec_dirs 条件，但仍没有固定两端的配置/消费组合与传递字段，另一端仅写“经 prestart hook 注入”。未区分独立 NVIDIA Runtime Hook 与 CDI containerEdits 自身 hooks 的来源/作用；不能只用有某个 hook 的文字完成模式或混合路径判断。抽查 07、09 支持这一区分，抽查 11、12 还显示设备传递策略可多选。拒绝对混合路径归因值得保留，但未替代已要求的配置对与排除规则。
2. **有序许可比较：** L131 仍只按 type/major/minor 选规则并保存顺序上下文，未同时固定目标访问 access、规则索引、通配上下文与旧新完整比较对象。抽查 08 的 Allowed Device list 明确按顺序应用、字段可有通配语义；L75 通用字段清单不能替代本变体的选择/比较方法。
3. **资源更新对象：** L135 仍写候选 CRI 更新对象/OCI linux.resources.cpu，固定字段未取；所选接口、完整字段、旧新比较格式及更新/重建各自采样关联仍没有交付。抽查 10 仅支持 CPU/内存显式更新这一类别，不补出所选接口。L133–134 的回退对象已拆开，不再作为这项缺失的替代。
4. **证据对象和依赖：** L130–136 的证据定位仍主要是三单、注入集、拒绝事件或影响记录，未逐变体指定受控访问及原负向边界恢复的证据对象，并关联前后/恢复后主体、节点和时间窗。L131 及 S1/R1 已提访问证据，但仍未形成这些证据对象的定位格式。引用恢复判据不能用可见性证明访问/负向恢复；依赖 C32 的三单比较也尚无已交付映射方法可统一引用。

**剩余关闭条件：** 固定两端模式配置/消费组合和传递字段，按来源区分 CDI 自身 hook 与独立 legacy hook，并落实混合路径排除规则；为完整目标节点与目标访问选定带 access、索引和顺序/通配上下文的许可比较对象；选定资源更新接口/完整字段及旧新格式。保留回退拆分，逐变体落实更新或重建生命周期、前后/恢复后主体/节点/时间窗及访问/负向恢复证据对象，统一引用 C32 已交付的方法，方法缺失时优先无法确定。保留 NPU 对照未知的收窄及全部安全边界。**不要求执行试验、取得现场值、扩大生产权限或制造结果。**

## 5. Acceptance 与最终计数

| 计划 acceptance / 原文件位置 | 本轮判断 | 对应原 ID |
|---|---|---|
| 镜像身份、构建输入、SBOM/签名、拉取策略 / L5403 | 沿用此前完整通过，不重审供应链 | C30 CLOSED，范围外 |
| 固定 runtime/Toolkit/CDI、各层与映射分离 / L5404 | 部分满足，未完整通过：runtime 完整配置记录已补齐，扫描/层匹配与稳定映射方法仍缺 | C31 CLOSED；C32 OPEN |
| Ascend 独立实现与目标组合 / L5405 | 部分满足，未完整通过：正文条件纠正已核实，登记同步及所选路径必要方法/证据仍缺 | C33 OPEN |
| 清单、异常/隔离、对照及来源案例 / L5406 | 部分满足，未完整通过：通用门槛已补，配置对、许可/更新对象及逐变体证据关联仍缺 | C34 OPEN |

四条 acceptance 汇总：**1 沿用既有完整通过 / 3 未完整通过**。本轮范围 **1 CLOSED / 3 OPEN（开放项 1 P1、2 P2）**；没有新增 ID。不通过是因为上述方法与证据关联尚未交付，**不是因为 curl DNS 失败、现场值 unknown、没有实测或未证明整栈兼容**。本轮不修改正文 draft/source_checked 状态或计划验收状态。

## 6. 结构校验与写入审计

- 写入前原仓库 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS：96 content entries / 438 sources**；仅结构与本地链接校验，不验证技术正确性或远程正文。
- 写入后原仓库同一检查：**PASS：96 content entries / 438 sources**。在临时副本 `/private/tmp/b21-t05-01-recheck-13.H4AGqM/validation/`（包含本报告及既有 build 链接目标）执行 `make check` / `make build`，均 **PASS：96 content entries / 438 sources**；使用原仓库虚拟环境 Python、禁写字节码，仅在副本重新生成 build/catalog.json 与 build/catalog.md，不改原仓库 build。
- 报告四项 ID/原优先级/状态、九个本地 Markdown 链接及行尾空白检查：**PASS**。写入后的摘要审计覆盖 **396 个**起始 Git 所列 tracked/untracked 非忽略文件及 build 文件：既有文件摘要全部不变，唯一新增为本报告；六个指定输入与补读作者来源记录均保持 §2 摘要。
- 本会话只写本报告，不改作者正文/来源记录/修订映射/来源登记/计划；不修改 src/kb/ 或测试，不执行容器或硬件实测。catalog 构建也不是镜像构建或实验验证。

**最终技术结论：C31 CLOSED；C32、C33、C34 OPEN；1 CLOSED / 3 OPEN，第十三次定向复核不通过。C30 保持此前 CLOSED、范围外；用户约定模型配置不作为已独立确认的执行元数据。**
