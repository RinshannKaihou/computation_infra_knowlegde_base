# Batch 21 补交 T05-01 第二十九次定向复核

## 1. 结论、角色与范围

- 日期：2026-10-17（Asia/Shanghai）。执行者：当前本地 Codex CLI 会话，以独立审阅角色核对作者第二十九轮修订，与正文作者角色分开；未派发子代理或其他模型。
- **模型核验：** 实读 `~/.codex/sessions/2026/10/17/rollout-2026-10-17T02-40-16-01a14603-cbb0-78a3-9450-19e172e1f1cc.jsonl`，会话 ID 为 `01a14603-cbb0-78a3-9450-19e172e1f1cc`。`turn_context` 时间为 `2026-10-16T18:40:22.145Z`（本地 2026-10-17 02:40:22），其中 `model=gpt-6.1-sol`、`effort=xhigh`；`collaboration_mode.settings` 同样为 `gpt-6.1-sol / xhigh`。本轮所见执行上下文为单一约定模型，审阅者已输出文本未检出 fallback 标记；不把用户提示中的标记示例计作执行回退。`session_meta` 的 originator 为 `codex_exec`、model_provider 为 `custom`；这是本地 CLI 执行元数据核验，不是独立服务端模型路由、推理计算量或供应商证明，不追改历史模型记录。核验摘录保存在仓库外审计目录。
- 唯一复核范围为 **B21-C32、B21-C33、B21-C34**。关闭条件以[第二十六次复核](batch-21-t05-01-codex-recheck-26.md) L91、L106、L121 为权威，并逐项继承[第二十八次复核](batch-21-t05-01-codex-recheck-28.md) §4 的剩余条件。C32-1 等是该节子项定位，不是新增发现 ID。**C30/C31 已 CLOSED，范围外，不重审、不重开。** [初审](batch-21-t05-01-codex-review.md)仅用于继承 ID、优先级和职责边界。
- **本轮 0 CLOSED / 3 OPEN（1 P1、2 P2）；第二十九次定向复核不通过。** 新增扫描选型/JSON 字段、Ascend 逐对象表与 UB 分道、旧挂载判据删除、worker/控制键定位、两端消费配置和 resize 接口设计均有实质进展；其中 C33-1、C34-1、C34-2 子条件可认可。仍缺包证据位置到逐库文件/层的可靠连接、完整来源支持的 ordinal 稳定映射、实际挂载来源的取证判据及相应分类/口径同步；C34-3 仅剩 C32 方法依赖。
- 只新增本报告，不修改或删除任何其他仓库文件，不提交 Git、不建分支。作者修订映射、来源记录中的“已交付”等自述只是索引，不作为关闭证据；不新增发现 ID，不改变正文或计划状态。
- **未执行实测，不构成硬件验证。** 未拉取/构建镜像、生成 SBOM、安装或运行上游组件、执行上游脚本、运行容器、查询设备或接入集群；未做访问、负向、更新、回退、恢复实测。下述阻断是方法/记录设计和口径问题，不是缺少现场值或实测。

| 原发现 | 优先级 | 本轮状态 | 当前剩余范围 |
|---|---|---|---|
| B21-C32 | P2 | OPEN | 正文 L61、L73、L79、L81–85、L116、L122、L128–132：扫描范围/字段已选；逐库文件归层、完整稳定映射和分类同步未全部闭合 |
| B21-C33 | P2 | OPEN | 正文 L91、L93–106；作者来源记录 L12、L17：逐对象/UB 分道认可；M-LIB 的实际挂载证据仍不足，“只缺 filled 值”需随之收窄 |
| B21-C34 | P1 | OPEN | 正文 L145、L149–150、L155：两端消费配置与资源更新设计认可；仅余 C32 方法依赖，不重开 R1 |

优先级沿用原报告：P1 是核心验收主干阻断，P2 是必须补齐的方法、证据或版本边界；不是生产漏洞/事故严重性评级。

## 2. 输入身份（SHA-256）

正文工作区字节与当前 Git HEAD `a6ea5386940d2464d5074d8f127d19b4295caf6c` 中对应文件一致；开始时 Git 工作区干净。以下对完整文件原始字节计算 SHA-256，行号是本轮仓库物理行号，不沿用修订前正文行号。

| 输入 | 本轮 SHA-256 | 审阅定位 |
|---|---|---|
| [第二十八次复核](batch-21-t05-01-codex-recheck-28.md) | `d2f170de9a842022e8c7578ebb671c72dbe3df18d71d5c193f6c3b77bfd1ea11` | §4 三项剩余条件及已认可项 |
| [第二十六次复核](batch-21-t05-01-codex-recheck-26.md) | `ade616897c367afb566c3076ffc8b36f2dbf6c95af8558d74af8d537ed3402b0` | L91、L106、L121 权威关闭条件 |
| [初审报告](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` | 原 ID、优先级、C32/C34 分工 |
| [作者修订映射](batch-21-review-fixes.md) | `ae067173f7863fc3c951d23efab4c6f98ae6dd28e7fa441814bb42171d18980e` | L400–412“第二十九轮修订”，仅作索引 |
| [修订后正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md) | `cee47fac5cf4cab1bfda4387e9e9e4179a0e610ea28a6ce3a4a0cf673cb6a302` | L61、L73–85、L91–108、L114–156；仍为 `reference / draft / source_checked` |
| [作者来源记录](batch-21-t05-01-sources.md) | `7afca8b15941e831af615feb0a295804f2f21b43cf1a33cf4de5a9480ac8803f` | L12、L15–25，含“第四轮增补” |
| [任务计划](../../plans/full-coverage-backlog.yaml) | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` | T05-01 L5386–5430；acceptance L5403–5406 |
| [来源登记](../../sources/registry.yaml) | `c948b238a7121fafcd1102d696679e70e5115dbe9979e9790578e12b729a9af9` | Toolkit/NVIDIA/containerd L5215–5269；resize/Syft L5281–5313；Ascend common/runtime/hook/install 相关项 |

先读 [README](../../README.md)、[写作指南](../authoring-guide.md)，并核对 [归属边界](../../content-outline.md)、[元数据 schema](../../schemas/content.schema.json)。其 SHA-256 分别为 `21759d9b1fc122d94bb3c3990d1b2e621c53dabc7ba022852545cae7b2329b44`、`75ee28d1aca7a4ac1d56ae493856037770a14fcdac27fa9b662451cee169a801`、`ed9033d2f53fa504fc05e55b221697dd7a1d14c5adaf58f8cc0a6613f8fe7046`、`b60b8d9ccb8728f034607901124c4206f5dc705ca824e31ce0ab5615523d0147`。检查适用目录，未发现 `docs/` 等目标目录下有新增嵌套 AGENTS 指令。登记解析计数为 **445 sources**，不套用前轮 444。

## 3. 一次源取证

### 3.1 实际通道、失败与限制

本轮使用本机 `curl` 只读 HTTPS GET 获取下表固定 ref 原文件及版本化文档正文，**29 次成功 GET 均为 exit 0 / HTTP 200**，默认 TLS 校验开启，没有 `-k`；成功文件保存到 `/private/tmp/b21-t05-01-recheck29-zCExFx/upstream/`。不是仅检查 HTTP 状态：随后实读原文件相应函数/字段和文档相关节，并在本机从原文件生成行号。命令形态为 `curl --fail --show-error --silent --location --connect-timeout 10 --max-time 25 URL -o FILE`；批量请求部分最大时限为 45 秒。

另用 Web `open/find` 实读 Toolkit 1.20.0 CDI/排障和 Kubernetes v1.32 resize 页面；Web 工具可能使用缓存或抽取文本，故不将其展示行号冒充 GitHub 源码行号。文档另有本机 curl 正文副本；CDI 页 Web 抓取标记为三日前，排障/resize 页为当日，这些标记不是本机实时性保证。

**实际失败单列：** 为定位 Syft 的包位置语义，曾以试探目录 `syft/pkg/cataloger/deb` 请求 GitHub contents API，curl 返回 **exit 56 / HTTP 403**；同 URL 的 GitHub 只读 `fetch` 连接器返回 **404**。随后连接器读取同 tag 的 cataloger 根目录及正确的 `debian` 目录成功，四份相关原文件再经 curl 返回 200 并实读。前两次定位失败不证明实现缺失，不用于技术不通过；本轮未发生 curl DNS 失败，不借用前轮 DNS 记录。本轮没有只凭搜索摘要形成结论。

`downloads.json` 留存成功请求的 URL、状态、字节数、SHA-256 和按 Git blob 编码在本机计算的 SHA-1；`channel-failures.json` 留存上述失败记录。Git blob 形式摘要不是服务器签名或独立 tag 解引用证明；tag 按用户要求固定，未额外宣称完成其不可变性/发布签名审计。临时副本不是永久证据归档，不搬入第三方全文，不执行取回代码。

### 3.2 本轮实读位置与支持边界

Ascend 以下各文件统一固定 commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e`；未用默认分支或其他提交替代。辅助读取的 Syft Debian 文件仍属既有 `src.anchore.syft-v1.54.1` 固定来源，仅用来检验“包位置等于逐库文件位置”的推论，不要求审全部 cataloger。

| 抽查点 | 精确一次源 / 实读原文件位置或文档节 | 本轮核对结果与限制 |
|---|---|---|
| 01 | [Syft scope.go@v1.54.1](https://github.com/anchore/syft/blob/v1.54.1/syft/source/scope.go#L8)，L8–24；[catalog.go](https://github.com/anchore/syft/blob/v1.54.1/cmd/syft/internal/options/catalog.go#L74)，L34–42、L74–79、L227–233 | 三 scope 定义、CLI 默认 squashed、scope flag 均与正文相符；all-layers 包括运行时不可见的层内容，不自动变成逐库文件归层方法 |
| 02 | [model/package.go](https://github.com/anchore/syft/blob/v1.54.1/syft/format/syftjson/model/package.go#L25)，L19–37；[model/document.go](https://github.com/anchore/syft/blob/v1.54.1/syft/format/syftjson/model/document.go#L16)，L16–25；[internal/constants.go](https://github.com/anchore/syft/blob/v1.54.1/internal/constants.go#L3)，L3–6 | artifacts 与 name/version/type/foundBy/locations 字段、输出 schema 16.1.11 可确认；结构定义不保证 locations 是包内每个库文件 |
| 03 | [coordinates.go](https://github.com/anchore/syft/blob/v1.54.1/syft/file/coordinates.go#L10)，L10–23；[location.go](https://github.com/anchore/syft/blob/v1.54.1/syft/file/location.go#L137)，L23–49、L137–152 | path 是该 location 的规范绝对路径；镜像 location 的 layerID 来自该文件所在层的 Metadata.Digest。支持“该 location→该层”，不支持把任意包证据文件的层当作全部所含库的来源层 |
| 04 | Syft v1.54.1 [debian/cataloger.go](https://github.com/anchore/syft/blob/v1.54.1/syft/pkg/cataloger/debian/cataloger.go#L12) L12–18；[parse_dpkg_db.go](https://github.com/anchore/syft/blob/v1.54.1/syft/pkg/cataloger/debian/parse_dpkg_db.go#L36) L36–49；[debian/package.go](https://github.com/anchore/syft/blob/v1.54.1/syft/pkg/cataloger/debian/package.go#L27) L27–61、L163–193；[parse_dpkg_info_files.go](https://github.com/anchore/syft/blob/v1.54.1/syft/pkg/cataloger/debian/parse_dpkg_info_files.go#L24) L24–53 | dpkg 数据库读入位置进入包 Locations；成员文件清单另入 metadata.Files，新增信息来源位置另加 Locations。反例表明 location 可为数据库/清单证据文件，不能普遍等同成员库路径；不据此宣称所选 NGC 镜像已经扫描或必用该 cataloger |
| 05 | [OCI image config@v1.1.1](https://github.com/opencontainers/image-spec/blob/v1.1.1/config.md#L26)，L26–31、L210–222 | DiffID 与 manifest layer digest 的对象边界、rootfs 层序；支持保留层号/digest/diff_id 对应表，不替代逐库文件解析 |
| 06 | [NVIDIA README@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/README.md#L218)，L218–245、L297–342；[server.go](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go#L305)，L305–365、L375–408、L456–473 | uuid/index 配置、分配请求校验、ID 转换去重、qualified CDI 名及返回通道可确认。它们不提供框架 ordinal 到 UUID 的枚举语义 |
| 07 | [CDI SPEC@cb98bcf6](https://github.com/cncf-tags/container-device-interface/blob/cb98bcf66dc68530012483bd56e33e14d815e167/SPEC.md#L193)，L193–249；[containerd config@v2.4.1](https://github.com/containerd/containerd/blob/v2.4.1/docs/cri/config.md#L128)，L75–109、L128–160、L269–307、BinaryName 说明段 | qualified kind/name、全局/设备 edits、设备 hostPath/path 与设备号字段，以及 RuntimeClass/handler、默认 runc 空 BinaryName、CDI 目录可确认；静态配置关联不等于已采到框架/宿主身份输出 |
| 08 | [PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html)，Device-agnostic code / 可见设备段 | 支持用可见环境控制 PyTorch 可用 GPU；本段不提供正文尚缺的 ordinal→UUID、宿主节点→UUID 完整方法，不据此断言其他 API 不存在 |
| 09 | [Ascend common.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go#L94)，L94–131；[api/consts.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/api/consts.go#L3)，Env 段 L3–25；[api/default_name.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/api/default_name.go#L153)，L153–164 | worker 七字符串在 consts.go，ASCEND 控制键在 default_name.go；已有生成算法及 310B 条件保留认可，不重新索取或外推框架标准语义 |
| 10 | [Ascend plugin.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go#L1161)，L1087–1100、L1161–1169 | 未选原生路径直接返回设备配置，所选 ascend-docker 路径调用环境辅助函数；两路不拼接 |
| 11 | [Ascend runtime/process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go#L536)，L242–277、L344–402、L536–711、L712–805、L855–878 | 节点信息失败、作业/UB/manager 错误向上返回；辅助尝试项/dvpp 警告继续；manager 重命名、UB 跳过子目录、VIRTUAL 提前返回与条件化 poststop 分开；LD_LIBRARY_PATH 仅改 env。只核记录设计依据，不证现场成功 |
| 12 | [Ascend hook/process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/hook/process/process.go#L394)，L43–52、L97–151、L239–293、L322–412 | 默认 base、逐列表行数上限、stat 分类与 CLI 参数；UB 两配置对象由 addUBMount 加入文件/目录通道，不是 runtime 的 UB 设备节点 |
| 13 | [base.list](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/scripts/base.list) 全五项；[run_main.sh](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/scripts/run_main.sh#L278)，L278–315 | 默认候选、五产品选择、两个 add_so、部署 base.list/chmod 链；不把源码列表当现场部署产物，不要求补读全部变体 |
| 14 | [Ascend CLI u_mount.c](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/cli/src/u_mount.c#L57)，L57–81、L84–160、L201–226 | 真实 bind/remount 操作与早退分开；源 stat 失败或 NODRV 可返回 0 而不挂载；目标存在/可读不能替代来源挂载关联 |
| 15 | [Toolkit 1.20.0 CDI](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html)，JIT-CDI / Running a Workload / Non-CDI-Enabled Runtimes / Setting the CDI Mode Explicitly；[排障页](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html#containers-losing-access-to-gpus-with-error-failed-to-initialize-nvml-unknown-error)，访问丢失 / Affected Environments | 原生消费与包装器 mode 分开；auto 的 NVML/WSL2 JIT-CDI 选择、显式 cdi 仍用选择变量、legacy hook 更新丢访问场景支持正文新配置对；不证明本库复现或恢复成功 |
| 16 | [Kubernetes v1.32 resize 页](https://v1-32.docs.kubernetes.io/docs/tasks/configure-pod-container/resize-container-resources/)，页首 / Before you begin / Container Resize Policies / Limitations / Updating the pod's resources | 门控、resize 接口、CPU requests/limits 示例、状态完成和资源一致、无重启证据、QoS 限制与正文相符；只支持设计。未启用门控时，重建不能算 resize 已执行 |

关键原文件的本机 Git blob 形式 SHA-1：Syft `scope.go=02df5cdf0fea658f1062abe6b641c8b375cde765`、`catalog.go=3ff68ecbd57fb7a45be1498a0e6747f74813d279`、JSON `package.go=e2fb5372205734ddd04ee9dad157b895f2a83f9a`、`coordinates.go=afeda5b13b61be709337660e6a8fb3426f59fbc7`、`location.go=76678c40f1ee2cb7e5e08a9fbff77ee929a678f8`、`constants.go=0d2fe0820976ecca4abcdbf46b2814a80fcc2a13`；Debian `package.go=8ad569f0ffb016419cb41d1b287827ba666a6df8`、`parse_dpkg_db.go=daea1b541a1588cd67ffd164858184124c52c75c`；Ascend runtime `process.go=acbd7a1ec0703498abfcfcb6ce1aa493069091b1`、hook `process.go=816212afa5f69b8edfb1554d3935af2ebcd28f06`、`api/consts.go=ea68039808d6e034363936c2c4cc4dff9e941b3e`、`u_mount.c=d85fd8155a1805edaf509b047c6441bcdc603e12`。完整下载身份在仓库外 manifest，不将本机计算值说成连接器返回值。

## 4. 逐项复核与剩余关闭条件

### B21-C32 — P2 / OPEN

**权威条件：** 第 26 次 L91；本轮前剩余条件为第 28 次 §4 C32-1/2/3。**位置：** 正文 L61、L73、L79、L81–85、L116、L122、L128–132、L145、L149。

1. **C32-1 / OPEN，扫描选型和字段子条件已满足，逐库解析/来源连接仍不完整。** L61 已选 all-layers、syft-json，schema 和 JSON 键经抽查 01–03 核实，不再索取这部分。L73 也已给出 layerID 连接层表的明确键，不再描述为完全没有层连接方法。但它把逐 artifact 的 locations.path 当作“包内规范路径”，并从该 location 的 layerID 直接推到逐库来源层，尚未区分包的发现/佐证位置与成员库文件位置。抽查 04 是同 tag 的具体反例：包 Locations 包含 dpkg 数据库和辅助信息文件位置，成员文件列表另在 metadata 中；包证据文件所在层不能自动证明每个库文件所在层。正文尚无所选包/文件表示下“包记录→成员库规范文件路径→该文件的层”的解析规则，后续接宿主来源/挂载/目标也没有补出这一缺段。**不是要求审全部 cataloger 或生成 SBOM；是不能把正确 JSON 键名当作尚未证明的逐库语义。**
2. **C32-2 / OPEN，M-ID 中间链已补，完整 ordinal 稳定映射仍缺方法。** L79 已固定 uuid，分配 ID→qualified 名→spec/最终 OCI 完整节点的设计链有来源支持，表 L83 也同步，不再判为只有空表。未选 index 路径的 unknown 不阻断本轮，也不要求补 NPU 实现。但 L79 明确将宿主节点↔UUID 复核和多元素框架枚举顺序列为 K1；框架侧仍只有“可见 ordinal 列表”及单元素直接对应的断言，没有固定来源支持的框架枚举/身份关联方法。把第五步写回分配 UUID，只确认分配标签相同，不能自动补齐 ordinal 如何对应到该稳定设备。L83、L128、L130 仍明示这些 K1；不能据“方法已交付”或更名 M-ID 关闭。若将所选设计严格限定为单卡，可以交付该范围内有来源支持的完整关联，不强制扩展 index、多卡或 NPU；但单靠数量为一不代替所要求的来源支持映射。
3. **C32-3 / OPEN，公共规则大部分已接通，仍有具体分类冲突。** L116 的 K1/K2/K3、L81/L83、L128/L130、异常表和 L145/L149 的统一引用可认可，不能再称“没有公共分类”。但是 L73 把缺 layerID、SBOM 缺库一律归缺采样；这未区分输出本身未采与尚未选定成员文件解析/覆盖语义，后者仍是 K1。L122 的期望栏明确 NPU 驱动/固件版本语义未取源为 K1，同行缺失解释却仅给 K2。正文 L32“逐 ordinal 稳定映射方法……已交付”也与 L79/L128/L130 的必要 K1 不一致。公共声明不能覆盖这些具体误分类。这里只要求如实分列，不要求补采 NPU 值或扩展实现。

**精确剩余关闭条件：** 保留已核实的扫描选择/JSON 字段/层表连接键，选定并说明适用的包/文件表示，把包证据位置与库成员文件位置分开，交付逐库文件→实际来源层→宿主注入来源（适用时）→挂载/容器目标的连接与缺项判据；交付所选 uuid/GPU 范围内来源支持的完整 ordinal→稳定身份/最终节点方法，不能用 K1 代替设计交付；据实际方法范围同步 L32、L73、L122 及共同记录/比较中的 K1/K2。**现场值可以 unknown；不要求拉镜像、生成 SBOM、审全部 cataloger、扩展未选路径或做设备实测；不重开 C30/C31。**

### B21-C33 — P2 / OPEN

**权威条件：** 第 26 次 L106；本轮前剩余条件为第 28 次 §4 C33-1/2/3。**位置：** 正文 L91、L93–106；作者来源记录 L12、L15–25。

1. **C33-1 / CLOSED（本轮所限记录设计子条件）。** L91 的公共格式和 L93–104 的十对象表已把所选对象的条件、来源、目标、节点/许可/环境结果、失败/跳过和证据定位落到可复用结构。L99 UB 设备目录的非子目录条目由 runtime 形成节点/许可；L100 的两个 UB 配置对象由 hook 到 CLI 挂载，已分行，经抽查 11–14 核实。作业/UB/manager 错误传播、辅助/dvpp 警告继续、manager 回退/容器重命名和条件化 vdevice/poststop 不再混作一条成功链。真实节点号、逐对象结果仍可 K2/K3；不重索取 worker 生成算法、两端卡型一致证明或完整 DCMI。此处认可字段/对象记录结构，不把 L100 引用 M-LIB 当作其挂载判据已另行通过。
2. **C33-2 / OPEN，旧判据删除已满足，实际挂载证据方法仍缺一段。** 定向检索确认正文不再保留旧“挂载成功以 CLI 返回＋目标可达为准”及“同①规则”。L106 的父候选＋相对路径→宿主子库完整路径、CLI 目标与容器路径、版本和分类字段比前轮充分；这些进展认可。剩余问题在它定义的实际挂载证据仍止于“宿主源路径身份→CLI 目标→容器内同路径可见/可读”。CLI 目标只是参数计算值，容器同路径可见/可读不是该挂载的实际来源证据；源侧有元数据摘要，但没有目标侧与之关联的实际挂载记录/判定规则。以“实际挂载证据”命名三方路径串不能使该规则排除镜像中既有同路径文件等替代解释。抽查 14 的早退事实仍成立，源码还把真实 bind/remount 操作明确放在另一段；声明 CLI 返回与可达性不单独证明挂载是正确原则，但需要具体记录把所选源、该容器/挂载命名空间中的实际挂载与逐库目标连接起来。**这仍是原有“逐库来源—实际挂载证据”条件，不是索取现场样本或要求完整 CLI 审计。**
3. **C33-3 / OPEN，仅剩与方法完成度同步的窄口径。** 两处旧“runtime 库注入语义未核对，unknown”已删除；worker 七键指向 consts.go Env 段，ASCEND 控制键留 default_name.go，抽查 09 确认正确；正文/作者清单也不再把已读默认链整体称为未核对。这些清理子条件已满足。但 L106“方法已交付但记录未填＝……M-LIB 的 filled 值（K2）”、来源记录 L12/L17 的 M-LIB 已交付/只缺 filled 值仍把 C33-2 的实际挂载证据设计缺段压成 K2。须将该具体缺段保留为 K1，或真正补齐后再称仅缺采样；不要求重写已确认的 worker/UB 机制或重登记既有来源。

**精确剩余关闭条件：** 在既有 M-LIB 中补充可填写的实际挂载关联记录及判断规则，使宿主子库来源身份、所选容器/命名空间的实际挂载证据、目标子库和采样证据定位按同一对象关联，并说明证据不足时不判已挂载；不要用 CLI 目标路径或容器可读性代替实际来源证明。随后同步正文 L106、作者来源记录 L12/L17 对“方法缺项/仅缺 filled 值”的分类。**已通过的逐对象表、UB 分道、worker/控制键定位和旧判据删除保留；不要求现场值、执行脚本、挂载实测、支持交集、全部产品白名单或完整 DCMI/CLI 审计。**

### B21-C34 — P1 / OPEN

**权威条件：** 第 26 次 L121；本轮前剩余条件为第 28 次 §4 C34-1/2/3。**位置：** 正文 L145、L149–150、L155–156，关联 C32 的方法/分类。

1. **C34-1 / CLOSED（两端设计子条件）。** L150 已一致选择原生基线的 runc v2 runtime_type、空 BinaryName/默认 runc，以及包装器不参与故 Toolkit mode 不适用；变体端选 NVIDIA Container Runtime 包装器、同 runtime_type、mode=legacy。相应配置键由同节及 §2 完整键上下文定位；安装路径/handler 现场名仍可 K2，不再视为未选执行器。原先同行“CDI mode 待填”等矛盾已清。抽查 06/07/15 支持这些层的区分、mode 键和 legacy 场景；正文明确 envvar 单策略不能证明 legacy，要求 handler/执行器/mode 证据并排除旁路。本子项不再索取相同设计取值或现场配置输出。
2. **C34-2 / CLOSED（资源更新设计子条件）。** L155 已选 Pod resize 子资源，给出 requests/limits 的 CPU 字段、CPU/毫核单位、旧新记录格式、门控/限制、完成观察及同次更新前后对象/采样关联；与抽查 16 的 v1.32 页面相符。该页例子的无重启 CPU 更新、resize 状态空且 spec/status 资源一致支持所选判定；正文将 restartCount 不变纳入完成条件，并未把任意重启也算同一次无重启更新。门控未启用退化重建是另一生命周期，L155/L156 已分开。样本未采不阻断，未启用门控不应被报作一次 resize 成功；不要求实测或增加生产权限。
3. **C34-3 / OPEN，仅因 C32 完整方法依赖未闭合。** L145、L149 已引用 M-ID/K1/K2/K3，文内连接动作本身已补齐，不再判“没有引用”。但所引用的 C32-1/2 方法仍有上述缺段，C32-3 的具体误分类也未清，故不能把“三单可按已交付方法比较”的主干判为完整通过。这是原依赖，不新增或重复计数；C34 不另背 C33 的问题。第 28 次已认可的 R1 公共阶段×对象、主体/新旧 ID、完整节点、稳定身份、时间窗、正负访问/恢复结果或未执行原因及可定位证据继续保留，**不重开、不要求各变体重复抄写**。

**精确剩余关闭条件：** 保留已认可的两端配置、resize 设计及 S1/R1；待 C32 所选范围内完整方法和分类闭合后，使本项基线/各变体引用该已闭合方法，不以仅添加方法名称或 K1 标签声称其已交付。**不再要求补两端现场 handler/路径、更新实测或重写 R1；保留 NPU 独立 unknown、负向独立授权、更新/回退/重建拆分，无负向授权不执行。**

## 5. Acceptance 与最终计数

| T05-01 acceptance | 本轮判定 | 原发现对应 |
|---|---|---|
| L5403：镜像 digest、基础系统/依赖层、构建输入、SBOM/签名、拉取策略的作用与限制 | 沿用既有完整通过，不重审；本轮新增逐库语义问题仍归 C32，不重开 C30 | C30 CLOSED，范围外 |
| L5404：固定运行时/NVIDIA 版本，分开驱动、库、设备/环境/挂载、权限与框架映射 | 部分满足，未完整通过：扫描选型/字段进展认可，逐库文件归层、完整稳定映射及分类仍缺 | C31 CLOSED，范围外；C32 OPEN |
| L5405：Ascend 固定实现/目标组合独立取证，GPU/NPU 与 digest 兼容边界 | 部分满足，未完整通过：逐对象表/UB 分道、键定义与旧措辞清理认可；实际挂载证据设计及完成度口径仍缺 | C33 OPEN |
| L5406：最小清单、异常/隔离、对照与源案例，非已验证处方 | 部分满足，未完整通过：两端配置和资源更新设计已补；仅余 C32 方法/分类依赖，R1 不重开 | C34 OPEN |

四条 acceptance：**1 沿用既有完整通过 / 3 未完整通过**。三项原发现合计 **0 CLOSED / 3 OPEN（1 P1、2 P2）**；本轮没有新增发现 ID，也没有重开 C30/C31。子条件关闭不等于所属原发现整体关闭。**第二十九次定向复核不通过；剩余阻断仅为上述方法/记录设计及口径不一致，不是未采现场值、未做实测、未拉镜像/生成 SBOM、未审全部 cataloger 或上游定位请求失败。**

## 6. 结构校验与写入审计

- 审计目录为 `/private/tmp/b21-t05-01-recheck29-zCExFx`。原仓库不运行会更新生成文件的构建；校验使用其中的独立 `validation` 副本，复制既有 `build/`，排除 `.git`、虚拟环境、node_modules 和 Python/工具缓存；原仓库 `build/` 保持不动。
- 写入前，在副本以原仓库虚拟环境 Python、禁写 Python 字节码执行 `make check build`：**均 PASS，96 content entries / 445 sources**，日志为 `validation-before.log`。副本重建 `build/catalog.json` / `build/catalog.md`；这些结果只验证结构与本地链接，不验证技术正确性、远程正文或硬件。
- 报告写入后，将报告同步到该副本，再次执行同一 `make check build`：**均 PASS，96 content entries / 445 sources**，日志为 `validation-after.log`。没有在原仓库运行构建。
- 逐字节摘要审计覆盖写入前的 **425 个既有文件**（排除上述 Git/环境/缓存目录），无修改、无删除；其中原 `build/` 的两个生成文件摘要未变。§2 的 **12 个输入文件**摘要全部未变，HEAD 仍为 `a6ea5386940d2464d5074d8f127d19b4295caf6c`。Git 状态及文件集合均只多出 `docs/research/batch-21-t05-01-codex-recheck-29.md`；`git diff --check` 无报错，另单独检查未跟踪报告，无行尾空白。审计结果保存为仓库外 `audit-result.json`。
- 结束前再次读取同一会话记录：所见两条 `turn_context`（UTC `2026-10-16T18:40:22.145Z`、`2026-10-16T18:54:26.373Z`）的 `model/effort` 均为 `gpt-6.1-sol / xhigh`，相应协作设置一致；审阅者 `output_text` 中未检出 fallback 标记。核验边界仍为 §1 所述本地执行元数据，不扩张为服务端证明。
- 未运行 `make test`：本轮未改 `src/kb/` 或测试代码。不将本报告变为正文修订，不安装/执行任何上游组件，不提交、不建分支。

**最终结论：B21-C32 OPEN、B21-C33 OPEN、B21-C34 OPEN；0/3 关闭。本轮认可的新交付不再重复索取；仅继续上述精确剩余条件。未执行实测，不构成硬件验证。**
