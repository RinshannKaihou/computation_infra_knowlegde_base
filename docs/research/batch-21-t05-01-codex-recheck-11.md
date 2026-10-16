# Batch 21 补交 T05-01 第十一次定向复核

## 1. 结论、角色与范围

- 日期：2026-10-14（Asia/Shanghai）。执行者：当前 Codex 会话，承担独立审阅角色，未承担本轮作者修订。
- `gpt-6.1-sol / xhigh` **仅记录为用户约定**。本会话未取得可独立确认的实际模型/推理配置执行元数据，不把约定、历史报告或作者自述写成执行元数据已核验。
- 唯一复核范围：**B21-C31–C34**。以[第十次复核](batch-21-t05-01-codex-recheck-10.md) L77、L87、L98、L111 的剩余关闭条件为本轮权威条件；[初审](batch-21-t05-01-codex-review.md)用于核对分工。C30 保持此前 CLOSED、范围外，不重新验收供应链内容。
- **0 CLOSED / 4 OPEN（1 P1、3 P2）；第十一次定向复核不通过。** 已补内容逐项认可，但部分方法仍未交付，且本轮选定 Ascend 原生挂载分支后又拼入另一分支的消费链，不能以 unknown 披露替代闭环。
- 新确认的分支拼接错误追记在原 **C33**，不新增发现 ID、不要求额外全栈审计。未安装组件、拉取/构建镜像、运行容器、生成 SBOM、采集设备、修改配置或执行负向/恢复试验。以下判断是来源与设计审阅，不是硬件验证。

## 2. 输入身份与并发边界

起始读取的四个指定 SHA-256 前缀全部吻合。完整输入摘要如下；行号均指本轮实际读取的仓库文件，不是网页归一化坐标。

| 输入 | 起始 SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md)，144 行 | `db79e24f0fe45e8514e36a2106778122a337044f09e9be3f4b213b41765f66f0` |
| [作者来源记录](batch-21-t05-01-sources.md)，28 行 | `ae26470307fe2bb04c255c76d408343c16be53c4d178baf4a87fe44a6a49fed5` |
| [修订映射](batch-21-review-fixes.md)，仅采用 T05-01 第十一轮节 L217–222 | `44ca7856d265fa8ac2d2fd45a5ce34cc4e699829d2b724318618c52004716190` |
| [第十次复核](batch-21-t05-01-codex-recheck-10.md) | `c163b953e6e3537836d8d6f0bcd3a7ba26cfad1862406d4a5157a41f2443310b` |
| [初审](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` |
| [任务计划](../../plans/full-coverage-backlog.yaml)，T05-01 acceptance L5403–5406 | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml)，438 项 | `61388eb10023ff425ab83891604529b05764afbe19b478257feb62a19c1262f7` |

另读 README、编写指南、内容总目录、metadata schema，以及关联 Ascend 来源案例/待执行实验的缺项与授权边界；不重新核验关联案例的外部事件史。

写报告前观察到并发编辑：完整映射摘要变为 `61a394f468b5c043d1d7aec5b378475d44689a2106cf977961976fb77cc3b3e9`。重新读取确认 **L217–222 原文不变**，新增的是 T05-03 第四轮节 L224 起，不纳入本轮。其余六个输入摘要保持上表值。另观察到 `docs/research/batch-22-t05-03-sources.md`、`knowledge/05-cluster-platform/slurm-jobs-and-device-resources.md` 变化；这些不是本会话编辑，不回滚，不把后读完整映射摘要冒称用户原输入摘要。

## 3. 一次源抽查与方法限制

### 3.1 实际 curl 请求

本机 curl **8.7.1**。对下表 01–13 对应的精确版本 URL 实际执行只读 GET；GitHub 文件使用同仓库/ref/路径的 `raw.githubusercontent.com` URL，厂商/PyTorch 页面直接使用表中 URL。完整请求清单、退出码和诊断保留在 `/private/tmp/b21-t05-01-recheck-11.qyeuoP/urls.tsv`、`curl-results.tsv` 与逐点 stderr，不加入仓库。调用形态：

```bash
curl --disable --location --silent --show-error --connect-timeout 8 --max-time 20 \
  --output "$audit_dir/$name.body" --write-out '%{http_code}' "$url"
```

保持默认 TLS 校验；未使用 `-k`、修改 DNS/证书、提权或绕过沙箱。**13/13 退出码 6、HTTP `000`，均为 `Could not resolve host`。** curl 未取得响应正文，TLS 握手未发生，不声称 curl 成功、HTTP 200 或本机核验了远端 TLS 链。

### 3.2 允许的只读替代通道与实际文字核对

使用 `web.run` 阅读版本化页面正文，使用 GitHub 只读连接器读取同 ref 原文件区间。核对文字、字段与控制流，**不只判可达性**。网页通道的缓存/归一化文本不是本机即时 GET；源文件坐标以 GitHub 原文件读取区间为准。CDI SPEC 与 OCI Linux 文件的网页打开返回 Internal Error，随后通过 GitHub 连接器成功读取，不把网页错误当成来源不存在。

| 点 | 精确一次源 / 实际阅读位置 | 本次核对用途 |
|---|---|---|
| 01 | [containerd config@v2.4.1](https://github.com/containerd/containerd/blob/v2.4.1/docs/cri/config.md)，网页版本头，GitHub L22–341 | v3 独立插件、完整配置参考项、systemd 条件与 RuntimeClass；另读 Image Pull Configuration 的 local/transfer 区别。用于 C31/C34，未核验现场生效。 |
| 02 | [runc state.go@v1.5.2](https://github.com/opencontainers/runc/blob/v1.5.2/state.go)，GitHub 全文 | 状态构造、init PID 与 stopped 置零。用于 C31。 |
| 03 | [runc list.go@v1.5.2](https://github.com/opencontainers/runc/blob/v1.5.2/list.go)，GitHub L1–82，网页亦读后续 getContainers | JSON 字段、`--root` 查询/存储作用域。用于 C31，不把 init PID 当任意工作负载 PID。 |
| 04 | [NVIDIA server.go@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go)，GitHub L280–481 | Allocate ID 校验、UUID/index 策略与去重、qualified 名及 CdiDevices。用于 C32，不替代框架 ordinal 映射。 |
| 05 | [CDI SPEC@cb98bcf6](https://github.com/cncf-tags/container-device-interface/blob/cb98bcf66dc68530012483bd56e33e14d815e167/SPEC.md)，GitHub L90–265 | kind/name、全局/设备级 edits、节点/挂载/env。用于 C32。 |
| 06 | [OCI Linux@92249139](https://github.com/opencontainers/runtime-spec/blob/92249139eea7161e13745abd4cb6d0ea02a3227a/config-linux.md)，GitHub L127–151、L402–418 | 节点身份/属主与访问许可分开，访问规则须按列表顺序应用。用于 C32/C34。 |
| 07 | [Ascend plugin.go@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go)，GitHub L1087–1185、L1296–1416 | DeviceSpec 的 `rw`、UB/默认节点、false 分支提前返回、true 分支才调用 SetAscendRuntimeEnv，Allocate 的调用位置。用于 C33。 |
| 08 | [Ascend common.go@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go)，GitHub L90–150 | ID 逗号串/options、310B allow-link 与 `!PresetVDevice` worker 组；静态函数输出不证明 false 分支调用它。用于 C33。 |
| 09 | [Ascend process.go@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go)，GitHub L243–410、L490–580、L600–812、L850–910 | env 解析、设备非空才进入 hook/设备注入、rwm 追加、产品条件、VIRTUAL/CreateVDevice、LD_LIBRARY_PATH 与 DP-mounts 的独立处理。用于 C33，不证明原生 DeviceSpec 经此文件消费。 |
| 10 | [Toolkit 1.20.0 troubleshooting](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html)，网页 NVML/SELinux、Unknown Error、Affected Environments、Mitigations | hook/legacy 条件、显式 CPU/内存更新、systemd 条件与删除重建建议。用于 C34；没有执行页面处置。 |
| 11 | [NVIDIA README@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/README.md)，GitHub L345–455 | time-slicing 共享访问副本、resources/name/replicas 及隔离限制。用于 C34，不支持 NPU 计数开关。 |
| 12 | [syft README@v1.54.1](https://github.com/anchore/syft/blob/v1.54.1/README.md)，GitHub 全文 | 工具/扫描对象/输出格式入口；不从 README 推定逐库路径与来源层字段齐全。用于 C32，不重开 C30。 |
| 13 | [PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html)，网页 CUDA_VISIBLE_DEVICES 段 | 所引段说明可用 GPU 范围管理，不交付本文缺少的 ordinal→UUID 连接规则。用于 C32；不声称框架不存在其他身份接口。 |

本次 GitHub 返回的原文件 blob：containerd config `3a206263f4f9e76b6ca14110461b8661a03b1619`；runc state/list `b645e5ab62b682efc26b805e977199cbbc3124a3` / `3bfd6b831531212ebe448bd962f3bf7bd9982b7f`；NVIDIA server/README `9281b48ef52f9eda9cbed6d98491729da85b5a75` / `44594d4343967a313ff268223c8f638de005062c`；CDI SPEC `2bc480a20ce447f5281b5d6844a486a81bb635b0`；OCI Linux `c71757494ca743fd90692c25e4897bf74cf00388`；Ascend plugin/common/process `b7692611b12884854d973fa2a3da18e381353f10` / `6cd038e9f1d67a8a913aa4bb1301692f177b3dbe` / `acbd7a1ec0703498abfcfcb6ce1aa493069091b1`；syft README `9ffd2affa3b00031ea1fd01ee3fe228379978492`。blob 不是 commit、现场配置或试验结果。

作者记录 L10 自述已读 containerd 配置全文及 runc 状态实现；本次以上述独立读取为准，确认相关字段/控制流，不凭自述认定已交付所要求的记录方法，也不将审阅者的抽查范围冒充作者取证范围。所选 hook 可执行实现、库挂载/白名单、框架稳定身份规则与扫描层匹配方法的缺项不会被本次抽查补成作者已交付。

## 4. 逐项判断与剩余关闭条件

### B21-C31 — P2 / OPEN

**权威条件：** 第十次复核 L77。**位置证据：** 正文 L64、L144；作者记录 L10、L26–27；映射 L219；登记 L5248–5258、L5314–5324。

**本轮已满足：** L64 新增 images/runtime 分区下的参考项、默认 handler、runtime_type、RuntimeClass→handler 关联，以及同 tag state.go/list.go 的直接链接。所列 overlayfs、相关布尔值、CDI 目录、默认 runc 与 `io.containerd.runc.v2` 可在抽查 01 的 v3 配置中核对；状态构造、stopped-PID-zero 与查询作用域可在抽查 02–03 核对。此前“没有直接状态实现链接”的问题已经解决，不再重复列为缺项。

**仍未满足：**

- L64 自称逐项“完整键｜来源限定参考值｜实际值或 unknown｜证据”，但 handler/options 部分仍写作 `...runtime.containerd`、`...runtimes.<handler>.options`，`SystemdCgroup` 只有字段名及“与 kubelet 一致”的说明，未落出完整 options 键及所选条件下的布尔参考值。抽查 01 的 Cgroup Driver 节给的是 systemd 主机模式的 `SystemdCgroup = true`，并有 kubelet 手动配置/自动探测条件；不是任意环境的统一默认处方。这里缺的是方法中的键与参考值，不是现场值。
- L144 继续把“handler/options 完整键”整体列为 unknown，与 L64/作者记录 L10 的已补主张未协调。可将已有确定的键、来源条件与实际值分别记录，而不能一面自称完整清单交付，一面整体列为未取。

**剩余关闭条件：** 保留已正确的 v3 分区、参考项、选择/转换边界及状态直接链接；把所选 handler/options 等项补成无歧义的完整键或明确表头＋子键，给出条件化参考值（包括 systemd 样板的 `SystemdCgroup=true`），逐项关联实际值/unknown 与来源。区分来源默认项和所选模式下的生效条件，协调 L144 与作者已读范围。**不要求覆盖整个配置全文、填现场输出、修改配置或证明整栈兼容。**

### B21-C32 — P2 / OPEN

**权威条件：** 第十次复核 L87。**位置证据：** 正文 L68–82、L108–110；作者记录 L11、L24–25；映射 L220；登记 L5281–5302。

**继续认可：** L68 的宿主/注入组件来源记录、L73 的 Allocate→qualified CDI 名→edits→OCI 主干，以及 L75 的节点/许可/LSM 分离与 L76 排除仅 major/数量/编号文本，均保留。抽查 04–06 支持这些主干；未要求以设备数量证明稳定身份。

**仍未满足：**

- L76 仍明确写“稳定物理标识映射方法（未交付，unknown）”，L80–82 仍为空表，判定栏仍为“一致/待查”。这不是已有固定映射规则但实际 UUID 待采集。抽查 13 的可见集段与抽查 04 的分配/CDI 字段不能自行补出逐 ordinal 的物理对应。映射 L220 的“分配 UUID/index→CDI→OCI 三方为已有方法”只涉及中间段，不能关闭缺失的框架侧/稳定身份连接。
- L70 没有新增固定扫描范围、选定输出字段与成分/路径→层的匹配依据，仍写“所选扫描配置……以实际输出为准”；抽查 12 的 README 只给工具/格式入口。层清单、diff_ids 与 annotations 不自行证明逐库归属；L110 增加待填字段也不补齐该方法。
- 方法未取得时的“无法确定”未同步至 L82 的判定栏与所有依赖映射一致性的 C34 判断；L108 的字段名不能替代规则本身。

**剩余关闭条件：** 在已固定来源基础上选定扫描范围、所需输出字段及层匹配规则，分别连接镜像内库与宿主注入来源/最终挂载/目标对象；交付框架 ordinal→分配/CDI→完整节点→稳定身份的固定规则。同步方法缺失与现场值缺失各自的“无法确定”格式到 L80–82、L108–110 和 C34。**实际值可 unknown；不要求拉取镜像、生成 SBOM、采集设备、实测或重开 C30，也不要求审计全部 cataloger。**

### B21-C33 — P2 / OPEN

**权威条件：** 第十次复核 L98。**位置证据：** 正文 L88、L90、L144；作者记录 L12、L17；映射 L221；登记 L5237–5247、L5325–5335、L5419–5429。

**本轮进展：** L88 明确写选定 `UseAscendDocker=false`，列出 DeviceSpec 的 HostPath/ContainerPath/`rw`，并声明排除虚拟分支。此前的 VIRTUAL 提前返回、CreateVDevice 返回条件、设备非空 gate 及 env/库路径独立处理的纠错保留；已读/未读范围仍有诚实披露。

**本轮确认的分支拼接错误，追记原 C33：**

- 抽查 07 的 `setNPUDeviceMount`（L1161–1169）明确是：false→`mountDefaultDevice`＋`mountDevice`→**return**；另一分支才调用 `common.SetAscendRuntimeEnv`。但正文 L88 在“所选分支”字段对应中同时写“环境经 SetAscendRuntimeEnv”及该输出→ascend-docker-runtime 的设备/hook 链。两条互斥分支不能这样连为一条既定消费链。抽查 Allocate L1296–1416 也没有补出这条所称的调用关联；不据此断言 false 分支没有任何其他环境输出。
- 抽查 09 的 `addDeviceToSpec` 接收宿主/容器路径，写节点与 `rwm`；其 `processDevicesAndHooks` 是解析可见环境后、设备集非空才进入 hook/设备注入。它不是已取证的 CRI DeviceSpec 消费实现。L88 把原生 DeviceSpec 的 `rw` 直接接为这里的 `rwm`，既没有对应消费端依据，也会错误改变许可语义。没有独立证明运行 wrapper/设置可见环境的条件，不能把该函数当原生路径的既定下一跳；不推断现场一定未运行 wrapper。

**其余未满足：** 产品、ID/options/defaultDevs/manager/UB 的所选条件仍没有逐字段落地，L90 又以“固定 commit 与未知条件”代替产品/分支选择。库来源/目标/白名单与必要 hook 可执行实现仍明确未取；排除 VIRTUAL 也不能自动排除 CreateVDevice 的后续条件路径。对应 runtime/库消费证据必须随实际选定路径确定，而不是把未取实现统一藏入 unknown。

**剩余关闭条件：** 先纠正原生挂载与 ascend-docker 环境/hook 注入两路径的拼接，再明确产品和实际所选插件/消费端路径，交付输入字段、条件、完整节点、许可及环境对应表。若选 false 原生路径，需补真正消费 DeviceSpec 的依据及该路径的库来源/目标策略，不要求把另一分支的 hook 强行算作必需；若选环境/wrapper 路径，则补实际环境键与该路径必需的 hook、库挂载/白名单证据。虚拟/poststop 按选定条件明确纳入或排除，同步正文/作者记录/登记的局部已读范围。**现场值、未选分支和支持交集可 unknown；不要求安装、试运行、完整 dcmi 审计或实测。**

### B21-C34 — P1 / OPEN

**权威条件：** 第十次复核 L111。**位置证据：** 正文 L108–110、L116–123、L125–135；作者记录 L13；映射 L222。

**本轮已满足的进展：** L116 已引用 NPU 固定语义缺失优先门槛，不能再以“通用行未设 NPU 门槛”判它欠缺。L132 选定 `sharing.timeSlicing.resources` 中 `name=nvidia.com/gpu` 的 replicas，抽查 11 支持其字段/副本含义；GPU L118 已不把它称为关共享或隔离证明。L125 的 S1/R1 补入进程/节点漂移停止、访问/原 allow/负向边界恢复，以及重建后新 PID/容器 ID 的关联原则；不要求各行机械重复公共集合。清单、旁路排除、授权、案例摘要与只设计未执行边界继续认可。

**仍未满足：**

- **模式/权限变体的具体方法不足：** L130 只称“CDI 消费 handler vs legacy hook handler”，没有固定两类 handler 对应的实际配置/消费条件；站点名称可以待填，模式成立的规则不能仅靠名称。L131 从“某一规则”改为“首条节点规则”，但未按目标节点的 type/major/minor/access 选择目标规则并保存其顺序上下文；首条可能是通配或其他节点规则。抽查 06 要求按顺序应用，单写首条 allow 与“其余不变”不能保证控制的是所选设备许可。
- **共享分工仍有遗漏：** GPU 副本计数纠偏认可；NPU L123 却仍写“副本计数对照（关共享另立变体，见对照表）”，L129–135 无该关共享变体，也无固定 NPU 副本计数语义。L132 的 NVIDIA 字段不能充当 NPU 对照；NPU 优先 unknown 门槛防止误用，但不等于设计方法已交付。
- **回退/资源更新对象仍未选定：** L133 仍为镜像 digest 或驱动版本二选一、键待填，并以“同上”继承 L132 的同 Pod/容器前后，未选择对应回退对象与生命周期。L134 仍称“候选字段为 CRI 更新对象/OCI linux.resources.cpu，固定字段未取，unknown”，不是选定接口/完整字段及旧新比较格式。抽查 10 支持 CPU/内存显式更新这一类别，不提供正文缺失的所选更新接口/字段，也不支持把镜像/驱动回退等同该资源更新。
- **公共集合与具体证据尚未闭环：** S1/R1 的安全内容已补，但各变体仍主要只定位注入集/影响记录，未将受控访问及原负向边界恢复的证据对象与变体前后、恢复后目标主体/节点/时间窗关联。L133 的“同上”也未解决需重建的回退与原进程身份保持之间的区别；公共定义不能代替所选生命周期和证据关联。
- **C32 方法依赖仍缺：** 逐 ordinal 稳定对应尚未交付，三单齐全不能自行证明映射一致或错误。NPU 门槛已补，但所有依赖该映射的完成/失败判断仍须明确先满足固定规则；规则缺失应进入无法确定，而不是凭三单名称完成判定。

**剩余关闭条件：** 保留 NPU 门槛、GPU 副本计数、S1/R1 和安全/案例边界；选定模式配置对、针对完整节点的有序许可规则、回退对象及资源更新接口/字段，分别给唯一差异和旧新比较格式。为 NPU 提供独立固定对照或一致移除未交付的“副本/关共享见表”承诺，不继承 NVIDIA 字段。逐变体落实生命周期与前后/恢复后主体、节点/时间窗，并关联访问及原负向边界恢复的证据对象。同步引用 C32 的固定方法或在缺失时优先无法确定。**不要求执行试验、取得现场值或制造结果。**

## 5. Acceptance 与最终计数

| 计划 acceptance / 位置 | 本轮判断 | 原 ID |
|---|---|---|
| 镜像身份、构建输入、SBOM/签名、拉取策略 / L5403 | 沿用既有关闭结论，不重验供应链验证 | C30 CLOSED，范围外 |
| 固定 runtime/Toolkit/CDI、各层与映射分离 / L5404 | 部分满足，未完整通过：状态引用已补；配置完整记录、层匹配和稳定映射仍有缺项 | C31、C32 OPEN |
| Ascend 独立实现与目标组合 / L5405 | 部分满足，未完整通过：选定路径存在分支拼接错误，条件/必要消费证据未闭环 | C33 OPEN |
| 清单、异常/隔离、对照及来源案例 / L5406 | 部分满足，未完整通过：门槛和公共安全集合有进展，具体对照与证据关联仍欠缺 | C34 OPEN |

四条 acceptance 汇总：**1 沿用既有完整通过 / 3 未完整通过**。本轮范围：**0 CLOSED / 4 OPEN（1 P1、3 P2）**，无新增发现 ID。结论不通过是上述剩余条件及 C33 分支错误所致，**不是 curl DNS 失败、没有现场值、未实测或未证明全栈兼容所致**。

## 6. 结构校验与单文件边界

- 写入前原仓库 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS：96 content entries / 438 sources**；只验证结构与本地链接，不验证技术正确性或远程内容。
- 写入后原仓库 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS：96 content entries / 438 sources**。临时副本 `/private/tmp/b21-t05-01-recheck-11.qyeuoP/validation/` 使用原仓库虚拟环境 Python、禁写字节码执行 `make check` / `make build`，均 **PASS：96 content entries / 438 sources**；仅在副本生成 catalog，没有构建镜像或修改原 build。
- 报告四项 ID、优先级、状态、本地 Markdown 链接及行尾空白独立检查：**PASS**。校验后的六个非映射输入摘要仍与 §2 相同，完整映射为 §2 已披露的后读摘要，其 T05-01 第十一轮节未变。
- 截至校验后的摘要审计，既有文件变动为 §2 所列三项加 `docs/research/batch-22-source-audit.md`；另观察到并发新增 `docs/research/batch-22-t05-03-claude-recheck-3.md`、`docs/research/batch-22-t05-03-claude-recheck-4.md`。这些不是本会话写入；原 build 摘要保持起始值。不声称全工作区相对起始快照无变化。
- 起始摘要审计纳入 **392 个**既有 Git 所列 tracked/untracked 非忽略文件及 build 文件。本会话只写本报告，不回滚并发改动，不在原仓库重建 build。
- 未修改 `src/kb/` 或测试代码，不新增测试、不运行硬件/容器实测；结构检查不改变本报告技术状态。

**最终技术结论：B21-C31–C34 均 OPEN，0 CLOSED / 4 OPEN，第十一次定向复核不通过。C30 保持此前 CLOSED、范围外；用户约定模型配置不作为已独立确认的执行元数据。**
