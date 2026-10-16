# Batch 21 补交 T05-01 第十二次定向复核

## 1. 结论、角色与范围

- 日期：2026-10-14（Asia/Shanghai）。执行者：当前 Codex 会话，承担独立审阅角色；未承担本轮作者修订。
- `gpt-6.1-sol / xhigh` **仅为用户约定**。本会话未取得可独立确认的实际模型/推理配置执行元数据，不把约定、作者记录或历史报告写成执行元数据已核验。
- 唯一复核范围：**B21-C31–C34**。以[第十一次复核](batch-21-t05-01-codex-recheck-11.md) L79、L93、L108、L124 的剩余关闭条件为权威条件；[初审](batch-21-t05-01-codex-review.md)仅用于核对原项分工。C30 保持此前 CLOSED、范围外，不重开供应链验收。
- **0 CLOSED / 4 OPEN（1 P1、3 P2）；第十二次定向复核不通过。** 本轮已补内容逐项认可，但完整配置记录、扫描/稳定映射方法、Ascend 所选消费路径的必要证据和具体对照方法仍未全部交付。
- 本轮新确认的 Ascend 条件作用域问题追记原 **C33**；没有新增发现 ID。未安装组件、构建/拉取镜像、运行容器、生成 SBOM、采集设备、修改配置或执行负向/恢复试验。本报告是来源与设计审阅，不是硬件验证。

## 2. 输入身份与单文件边界

四个用户指定 SHA-256 前缀全部吻合。以下为本轮起始读取的完整摘要；正文位置均采用仓库原文件行号。

| 输入 | 起始 SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md)，145 行 | `68e771ff85e4ec54012d4b9a69e6259b3880de02ceb4b30d800faf1628ae423b` |
| [作者来源记录](batch-21-t05-01-sources.md)，28 行 | `ae26470307fe2bb04c255c76d408343c16be53c4d178baf4a87fe44a6a49fed5` |
| [修订映射](batch-21-review-fixes.md)，仅采用 T05-01 第十二轮节 | `0e215f30ab3ddb5bc9e1681669f377e062d397bfe1f5a01e0536dfe02a52b7c4` |
| [第十一次复核](batch-21-t05-01-codex-recheck-11.md) | `3be733c9dcd4147ce5d21057db1341c48f085eaa72f6ce6229d956186ca0073a` |
| [初审](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` |
| [任务计划](../../plans/full-coverage-backlog.yaml)，T05-01 acceptance L5403–5406 | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml)，438 项 | `61388eb10023ff425ab83891604529b05764afbe19b478257feb62a19c1262f7` |

修订映射中有两段同名、同文的第十二轮节：L228–233 与 L235–240。只作为落盘改动说明读取一次，不把重复段、作者自述或上一轮审阅者取证当成本轮独立证据；不为这个输入形态新增发现 ID。

另读 README、编写指南、内容总目录与 metadata schema；读取关联 Ascend 来源案例/待执行实验的缺项、映射及授权边界，不重核来源案例的外部事件史。写入前再次核验，上述七个摘要均不变。起始工作区已有修改和未跟踪文件，本会话不回滚、不代写这些内容。

## 3. 一次源抽查与方法限制

### 3.1 实际 curl 请求

本机 curl **8.7.1**。对下表 01–14 的精确版本 URL 实际执行只读 GET；GitHub 文件使用同仓库/ref/路径的 `raw.githubusercontent.com` 地址，厂商/PyTorch 页面使用表中 URL。请求清单、结果和逐点诊断保留于临时目录 `/private/tmp/b21-t05-01-recheck-12.guTCiF/` 的 `urls.tsv`、`curl-results.tsv` 与 `*.stderr`，不加入仓库。调用形态：

```bash
curl --disable --location --silent --show-error --connect-timeout 8 --max-time 20 \
  --output "$audit_dir/$name.body" --write-out '%{http_code}' "$url"
```

保持默认 TLS 校验；未使用 `-k`、修改 DNS/证书、提权或绕过沙箱。**14/14 退出码 6、HTTP `000`，均为 `Could not resolve host`。** 未取得 curl 响应正文，TLS 握手未发生；不声称 curl 成功、HTTP 200 或本机核验了远端 TLS 链。

### 3.2 允许的只读替代通道与文字核对

使用 `web.run` 阅读版本化页面正文，使用 GitHub 只读连接器读取同 ref 原文件区间，实际核对字段、文字及控制流，**不是只判可达性**。网页通道可能使用缓存并归一化文本，不等于本机即时 GET；GitHub 源码位置以原文件读取区间为准，不把网页行号拼成源码锚点。Ascend process.go 的网页打开为 Internal Error / Cache miss，但同 commit 文件已由 GitHub 连接器读取；不把网页错误当作来源不存在。

| 点 | 精确一次源 / 实际阅读位置 | 本轮核对用途与限制 |
|---|---|---|
| 01 | [containerd config@v2.4.1](https://github.com/containerd/containerd/blob/v2.4.1/docs/cri/config.md)，网页 Config versions；GitHub L22–148、L150–342 | v3 分区、完整表头、systemd/kubelet 条件、RuntimeClass、local/transfer 配置区别；C31/C34，不核验现场生效。 |
| 02 | [runc state.go@v1.5.2](https://github.com/opencontainers/runc/blob/v1.5.2/state.go)，GitHub 全文 | 状态构造及 stopped PID 置零；C31，未执行查询。 |
| 03 | [runc list.go@v1.5.2](https://github.com/opencontainers/runc/blob/v1.5.2/list.go)，GitHub L1–85 | JSON 字段与 `--root` 查询作用域；C31，不把 init PID 当任意目标进程 PID。 |
| 04 | [NVIDIA server.go@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go)，网页 Allocate/ID 策略；GitHub L280–438 | 分配校验、CDI qualified 名及响应字段；C32，不补成框架稳定映射。 |
| 05 | [CDI SPEC@cb98bcf6](https://github.com/cncf-tags/container-device-interface/blob/cb98bcf66dc68530012483bd56e33e14d815e167/SPEC.md)，GitHub L90–265 | kind/name、全局/设备级 edits、节点/挂载/env/hook；C32/C34，不宣称消费端支持交集。 |
| 06 | [OCI Linux@92249139](https://github.com/opencontainers/runtime-spec/blob/92249139eea7161e13745abd4cb6d0ea02a3227a/config-linux.md)，GitHub L127–151、L402–418 | 完整节点与许可对象分离、访问规则顺序及 access；C32/C34。 |
| 07 | [Ascend plugin.go@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go)，GitHub L1080–1175、L1296–1416 | 原生 `rw`、互斥分支及 Allocate 调用位置；C33，不冒称审计完整 ID 生成链。 |
| 08 | [Ascend common.go@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go)，GitHub L80–155，定点重读 L94–129 | 区分 ID/options、310B allow-link 与 worker 组的不同条件；C33。 |
| 09 | [Ascend process.go@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go)，GitHub L1–220、L243–410、L490–580、L600–812、L850–910 | hook、设备集 gate、产品/UB 条件、VIRTUAL/CreateVDevice、poststop、env/库路径；C33。不证明真正库挂载/白名单或 hook 可执行行为。 |
| 10 | [Toolkit 1.20.0 troubleshooting](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html)，网页 NVML/SELinux、Unknown Error、Affected Environments、Mitigations | hook/legacy 与 CPU/内存更新、systemd 条件、重建建议；C34，未执行任何建议。 |
| 11 | [NVIDIA README@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/README.md)，网页 Configuration Option Details / Shared Access to GPUs / With CUDA Time-Slicing | 传递策略、replicas 及共享边界；C32/C34，不支持 NPU 计数开关。 |
| 12 | [syft README@v1.54.1](https://github.com/anchore/syft/blob/v1.54.1/README.md)，网页及 GitHub 全文 | 扫描对象/格式入口；C32，不从 README 推定逐库路径/层字段齐全，不重开 C30。 |
| 13 | [PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html)，网页 CUDA_VISIBLE_DEVICES 段 | 可见集管理；C32，所引段不能替代正文缺少的 ordinal→稳定身份规则，不断言框架无其他接口。 |
| 14 | [Toolkit 1.20.0 CDI support](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html)，网页 Running a Workload / Non-CDI-Enabled Runtimes / Setting the CDI Mode Explicitly | 原生消费、非原生 CDI 与 legacy hook 不能靠 handler 名或 hook 字样混判；C34。 |

补充通过 GitHub 连接器读取同 commit [Ascend runtime README](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/README.md)全文，核对设计简介中的 prestart 与 Host CANN 库挂载职责。这个补充点没有另行 curl 请求，不计入 14 点；README 职责说明不替代 hook/库实现证据。

本轮 GitHub 返回的原文件 blob：containerd config `3a206263f4f9e76b6ca14110461b8661a03b1619`；runc state/list `b645e5ab62b682efc26b805e977199cbbc3124a3` / `3bfd6b831531212ebe448bd962f3bf7bd9982b7f`；NVIDIA server `9281b48ef52f9eda9cbed6d98491729da85b5a75`；CDI SPEC `2bc480a20ce447f5281b5d6844a486a81bb635b0`；OCI Linux `c71757494ca743fd90692c25e4897bf74cf00388`；Ascend plugin/common/process/README `b7692611b12884854d973fa2a3da18e381353f10` / `6cd038e9f1d67a8a913aa4bb1301692f177b3dbe` / `acbd7a1ec0703498abfcfcb6ce1aa493069091b1` / `f612ad6b5d2edcf65d9ad683d57a4f1a4e1f9088`；syft README `9ffd2affa3b00031ea1fd01ee3fe228379978492`。blob 不是 commit、现场输出或实验结果。

作者记录的已读范围与本轮独立抽查分别处理；审阅者读取更多区间不等于作者已交付相应方法，也不替作者修改来源记录/登记。

## 4. 逐项判断与剩余关闭条件

### B21-C31 — P2 / OPEN

**权威条件：** 第十一次复核 L79。**位置证据：** 正文 L64、L145；作者记录 L10、L26–27；映射 L230/L237；登记 L5248–5258、L5314–5324。

**已满足：** L64 现有完整 `plugins."io.containerd.cri.v1.runtime".containerd.runtimes.<handler>.options.SystemdCgroup`，且明确 systemd 主机参考值为 true、kubelet 手动配置或启用自动探测、runc 类设置一致的条件。抽查 01 支持这些条件。L145 已将 containerd 现场消费输出列为 unknown，未再把 handler/options 整体当作未读取；v3 分区、版本转换、RuntimeClass 与 runc 状态直接引用继续认可。未要求现场实际值或完整配置全文。

**仍未满足：** 所称逐项“完整键”清单中，默认 runtime 与 handler 的表头仍写作 `...runtime.containerd`、`...containerd.runtimes.<handler>`，没有显式定义省略号展开规则或给这两组完整表头。只补 options 的完整键，不能同时把 `default_runtime_name`、`runtime_type` 的定位格式算作补齐；L145 的“完整键清单……已交付”仍强于落盘内容。这里欠缺的是无歧义的记录格式，不是上游没有这些字段，也不是 handler 现场名称待填。

**剩余关闭条件：** 保留已正确的 systemd 条件及其他已认可部分；把上述两处改为完整 TOML 表头＋明确子键，或直接写 `plugins."io.containerd.cri.v1.runtime".containerd.default_runtime_name` 与 `plugins."io.containerd.cri.v1.runtime".containerd.runtimes.<handler>.runtime_type`，关联来源限定参考值、实际值/unknown 与证据定位，并协调 L145 的交付表述。来源默认记录不得当作所有模式都生效的处方。**不要求补全部 options、现场输出、配置修改或整栈兼容证明。**

### B21-C32 — P2 / OPEN

**权威条件：** 第十一次复核 L93。**位置证据：** 正文 L68–82、L108–110、L112、L116；作者记录 L11、L24–25；映射 L231/L238；登记 L5281–5302。

**已满足：** L80 判定表头现已明确规则缺失时记无法确定、不记一致。宿主/注入组件记录、Allocate→qualified CDI 名→edits→OCI 主干、节点/许可/LSM 分离及不以 major/数量/编号文本证明稳定对应，均继续认可。抽查 04–06、12–13 支持所引用入口及上述有限机制，不把这些入口扩充为缺失方法。

**仍未满足：**

- L70 仍未选定扫描范围、输出字段及成分/路径→来源层的匹配依据；“所选扫描配置……以实际输出为准”是待确定要求，不是固定的扫描/层匹配方法。L110 增加留存字段不能补出这一步。
- L76 仍明确稳定物理标识映射方法未交付；L80–82 是空表，不是已经固定的 ordinal→分配/CDI→完整节点→稳定身份规则。中间 CDI 链不能替代框架端与物理身份的连接。
- 表头已纠偏，但 L82 示例判定仍只有“一致/待查”，L108–110 未分开规则缺失与采样缺失；C34 的 L116 只显式设置 NPU 门槛，GPU 依赖映射的完成/失败条件仍未同步。表头的安全限制不能据此倒推方法已交付。

**剩余关闭条件：** 在已固定来源基础上交付所选扫描范围、必要输出字段和层匹配规则，连接镜像内库与宿主注入来源/最终挂载/目标对象；交付逐 ordinal 的完整稳定映射规则。将规则缺失与现场值缺失各自的无法确定格式同步到表格、清单和 C34 所有映射依赖判断。**实际值可以 unknown，不要求拉取镜像、生成 SBOM、采集设备、审计全部 cataloger、实测或重开 C30。**

### B21-C33 — P2 / OPEN

**权威条件：** 第十一次复核 L108。**位置证据：** 正文 L88、L90、L145；作者记录 L12、L17；映射 L232/L239；登记 L5237–5247、L5325–5335、L5419–5429。

**已满足：** L88 已拆开路径 A/B，并选择 `UseAscendDocker=true` 的环境/wrapper 路径。false 原生分支提前 return，不调用 SetAscendRuntimeEnv；原生 `rw` 不再被改写成 wrapper `rwm`，也不再把 DeviceSpec 直接接到 process.go。抽查 07–09 支持这个纠正。**未选原生分支的真正消费端可以继续 unknown，不再以该缺项阻断所选 wrapper 路径。**

**本轮新确认的条件作用域问题，追记原 C33：** L88 所选 B 路径将 ID/options/310B allow-link/worker 组一起写为“限 `!PresetVDevice`”；登记 L5335 也使用同样的合并限定。固定 [common.go L107–121](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go#L107-L121)实际有三种条件：有效响应下 ID/options 写入不受该 worker 条件限制；allow-link 由 RealCardType 为 310B 控制；只有 worker 环境组位于 `!PresetVDevice` 内。不能把整个环境传递链统一套用该门槛，须拆成字段级条件。这里不把缺失 API 字符串值补写为已确认。

**其他剩余缺项：**

- 产品和所选 ID/options/产品相关 manager/UB 条件仍未具体落地；L90 仍以固定 commit 与未知条件代替所选产品/条件。L88 自列 API 实际键、节点/许可逐字段关联为 unknown，未交付对应表。选择 wrapper 分支解决路径分工，不自动完成该表。
- 既然选择环境/wrapper 路径，其必要 hook 可执行行为、库来源/目标/挂载与白名单仍未取得。process.go 中添加 prestart 引用和修改 LD_LIBRARY_PATH 不是真正库挂载证据；README 职责说明也不能代替实现。
- “未选分支明确排除”没有给出所选 options、PresetVDevice 或其他固定条件与 VIRTUAL/CreateVDevice 返回路径的对应关系。抽查 09 的 addHook 在非 VIRTUAL 时仍调用 CreateVDevice，返回有效虚拟 ID 才进一步更新环境/设备与 poststop；仅声称排除虚拟分支，不能关闭该条件链。
- 作者记录 L12/L17 的已读/未读范围保持披露，但未与本轮路径选择形成字段级条件闭环；登记中上述合并条件须随正文纠正。不将本轮审阅者读取区间冒充作者已补取证。

**剩余关闭条件：** 保留 A/B 拆分和许可纠错；按所选 wrapper 路径确定产品、输入 ID/options、实际环境键及各自条件，落完整节点、许可、环境对应表。补该路径必要的 hook、库挂载来源/目标与白名单依据；用所选固定条件明确虚拟/poststop 的纳入或排除，纠正 worker 条件作用域，并同步正文/作者记录/登记的局部已读范围。**现场值、未选原生路径和支持交集可 unknown；不要求安装、试运行、完整 dcmi 审计或实测。**

### B21-C34 — P1 / OPEN

**权威条件：** 第十一次复核 L124。**位置证据：** 正文 L108–110、L116–123、L125–136、L138–140；作者记录 L13；映射 L233/L240。

**已满足：** L130 从 handler 名改为消费机制的描述；L131 新增 type/major/minor 选择及规则顺序上下文；L133–134 将镜像与驱动回退拆开，并记录重建后新主体。L123 已撤去“副本/关共享见表”承诺，明确 NVIDIA replicas 不适用且 NPU 固定对照未知，认可这一收窄，不要求靠 NVIDIA 字段补 NPU。GPU 副本计数解释、NPU 优先门槛、S1/R1、安全/授权与来源案例边界继续认可；不要求各行机械重复公共安全集合。

**仍未满足：**

- **模式配置对：** L130 的 CRI CDI 引用 vs prestart 注入仍是机制分类，没有固定两端的配置/消费条件、传递字段及排除混合路径的规则。目录路径及站点 handler 名可待采集，但两种模式成立的配置条件不能靠名称或 hook 字样代替。抽查 05/14 中 CDI 也可带 hook；不能以存在 prestart/某个 hook 自行完成模式判定。
- **有序许可规则：** L131 虽补节点选择和顺序，但没有把目标访问的 access 与 type/major/minor、规则索引/通配上下文一起固定为所选规则及比较对象。L75 的通用许可字段不能替代这里的选择规则。抽查 06 要求按顺序应用，字段与上下文不足时应无法确定此次唯一 allow 差异的效果。
- **资源更新：** L135 仍将 CRI 更新对象/OCI `linux.resources.cpu` 列为候选，固定字段明确未取。尚未选定更新接口、完整字段、旧新比较格式和更新/重建各自的采样关联。L133–134 分拆回退是进展，但不能替代资源更新对象。抽查 10 只支持 CPU/内存显式更新这一类别，不提供本文欠缺的所选接口。
- **证据对象与依赖门槛：** S1/R1 和旧新主体有进展，但 L130–136 的证据定位仍主要为三单/注入集/影响记录，未把受控访问及原负向边界恢复的证据对象逐变体关联至前后/恢复后的目标主体、节点、时间窗。引用 R1 可以保留，却不能用可见性记录证明访问与负向恢复。L116 的 GPU 分支仍可在 C32 规则未交付时进入“三单一致/映射错”的技术完成/失败，未明确先判无法确定；NPU 门槛不自动覆盖 GPU。

**剩余关闭条件：** 固定模式配置对及排除混合路径的规则；为完整目标节点/目标访问选择带 access 与顺序上下文的许可规则；选定资源更新接口/完整字段及旧新比较格式。保留拆开的回退对象，逐变体落实更新或重建生命周期与前后/恢复后主体、节点/时间窗，关联访问及原负向边界恢复的证据对象。统一引用 C32 已交付的固定方法；方法未交付时所有映射依赖分支优先无法确定。保留 NPU 对照未知的收窄与全部安全边界。**不要求执行试验、取得现场值、扩大生产权限或制造结果。**

## 5. Acceptance 与最终计数

| 计划 acceptance / 位置 | 本轮判断 | 原 ID |
|---|---|---|
| 镜像身份、构建输入、SBOM/签名、拉取策略 / L5403 | 沿用此前完整通过，不重新验收供应链 | C30 CLOSED，范围外 |
| 固定 runtime/Toolkit/CDI、各层与映射分离 / L5404 | 部分满足，未完整通过：配置记录格式、扫描/层匹配与稳定映射仍缺 | C31、C32 OPEN |
| Ascend 独立实现与目标组合 / L5405 | 部分满足，未完整通过：路径拼接已纠正，所选条件/必要消费证据仍缺，并有条件作用域问题 | C33 OPEN |
| 清单、异常/隔离、对照及来源案例 / L5406 | 部分满足，未完整通过：具体配置对、许可/更新选择与证据/门槛关联仍缺 | C34 OPEN |

四条 acceptance 汇总：**1 沿用既有完整通过 / 3 未完整通过**。本轮范围：**0 CLOSED / 4 OPEN（1 P1、3 P2）**，没有新增 ID。不通过由上述剩余条件所致，**不是 curl DNS 失败、没有现场值、未实测或未证明全栈兼容所致**。本轮不改正文的 draft/source_checked 状态，也不修改计划。

## 6. 结构校验与写入审计

- 写入前原仓库 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS：96 content entries / 438 sources**。结构与本地链接检查不验证技术正确性或远程内容。
- 写入后原仓库 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS：96 content entries / 438 sources**。临时副本 `/private/tmp/b21-t05-01-recheck-12.guTCiF/validation/` 初次检查因未复制既有 build/catalog.json、build/catalog.md 而报两项本地缺链，make build 尚未执行；复制原有 build 到副本后重跑 `make check` / `make build`，均 **PASS：96 content entries / 438 sources**。使用原仓库虚拟环境 Python、禁写字节码，只在副本生成 catalog，不在原仓库重建 build，不构建镜像。
- 报告四项 ID、原优先级/状态、九个本地 Markdown 链接及行尾空白独立检查：**PASS**。写入后的摘要审计中，**395 个**既有 Git 所列 tracked/untracked 非忽略文件及 build 文件均保持起始摘要，唯一新增为本报告；七个输入摘要仍为 §2 所列值。
- 本会话只写本报告；不改作者正文/记录/映射/登记/计划，不改 src/kb/ 或测试，不执行实测。结构检查与 catalog 构建不改变上述技术判断。

**最终技术结论：B21-C31–C34 均 OPEN，0 CLOSED / 4 OPEN，第十二次定向复核不通过；C30 保持此前 CLOSED、范围外。用户约定模型配置不作为已独立确认的执行元数据。**
