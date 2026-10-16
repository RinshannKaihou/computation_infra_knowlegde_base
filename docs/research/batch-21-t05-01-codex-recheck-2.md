# Batch 21 补交 T05-01 第二次定向复核（作者第二轮修订后）

## 1. 结论、角色与边界

- 日期：**2026-10-14（Asia/Shanghai）**，本机日期与本轮环境日期一致。
- 执行者：本会话 Codex，独立审阅角色；本轮未参与作者修订。只写本报告，不修改作者正文、来源记录、修订映射、来源登记、计划或既有报告。
- 用户约定配置：`gpt-6.1-sol / xhigh`。**仅记为用户约定，不写成已独立确认的执行元数据。** 本轮未取得可独立核验的实际模型标识或 reasoning 配置，未据模型自述确认，也未另行派发模型。
- 范围：仅 **B21-C30–C34**，优先级沿用前次报告。剩余关闭条件以[前次定向复核](batch-21-t05-01-codex-recheck.md) L102、L118、L135、L152、L170 为权威，并对照[初审](batch-21-t05-01-codex-review.md) §6。作者自述和修订映射不代替正文交付或独立证据。
- **结果：0 CLOSED / 5 OPEN（1 P1、4 P2）；定向复核不通过。四条 acceptance 均未完整满足。** 本轮认可已经完成的局部修正，但不把新增术语、链接或 unknown 当作原关闭条件已全部满足。
- 未执行镜像构建、拉取、SBOM 生成、验签、容器启动、设备访问、配置修改或 GPU/NPU 实测。知识库结构检查和目录构建不是上述实测；正文保持 `reference / draft / source_checked`，不建立整栈兼容或硬件验证结论。

## 2. 输入身份与位置口径

四个用户提供的 SHA-256 前缀均匹配。以下七个输入均以完整字节摘要固定；后文“正文”“作者记录”“映射”“登记”分别指表内对应文件，行号为本轮原文件坐标，不沿用旧正文行号。

| 输入 | 完整 SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md) | `eb5606d6a871674de338b886e906ea6f1d1b7a6f2b480c88c0b96b44ce44fd19` |
| [作者来源记录](batch-21-t05-01-sources.md) | `8a10aabc969984479221f36f1c1f051702c6cfc0a5f30b13fcfd15340bd6408b` |
| [修订映射](batch-21-review-fixes.md)，第二轮节 L101–108 | `20b24058ca9d2c66f7286192c20d1dc3af68913fa17361384612afa8fefd31f4` |
| [前次定向复核](batch-21-t05-01-codex-recheck.md) | `0b3c3bd7c6438220bd6c35f46518d9ad499203791c1169ec7be87ebe658b98ee` |
| [初审](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` |
| [任务验收计划](../../plans/full-coverage-backlog.yaml)，T05-01 acceptance L5403–5406 | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml) | `77ec8d1311fe210f615798c8e2295fe7c5d6249cd8f390a0e216bcc459a7431a` |

另读 README、编写指南、内容总目录、元数据 schema，以及本页实际链接的[Ascend 来源案例](../../knowledge/05-cluster-platform/ascend-device-visibility-source-case.md)、[待执行实验](../../knowledge/05-cluster-platform/ascend-device-visibility-experiment.md)。关联条目只用于解释链接能支持什么，不扩大为重新验收这些条目。

登记实计 **423 项**；`src.vllm-ascend.issue-2557` 只有既有一项（登记 L710 起），本页 L19 已复用。新增 containerd CRI、CDI SPEC 条目见登记 L5248–5269，不再把作者删去的重复案例登记当作待修事项。映射 L103 的“新增…vLLM 案例”与当前登记不完全同步，实际以当前登记为准。

## 3. 一次源抽查方法、内容与限制

### 3.1 curl 的实际结果

对下列精确 URL 执行五次只读 GET，使用默认 TLS 校验，命令形态为：

```bash
curl --fail --silent --show-error --location \
  --connect-timeout 10 --max-time 25 \
  --output <本轮临时目录中的响应文件> \
  --write-out 'http=%{http_code}; effective_url=%{url_effective}; bytes=%{size_download}\n' \
  <精确URL>
```

没有使用 `-k`/`--insecure`，没有改 DNS、代理或系统 TLS 设置。五次均 **exit 6 / HTTP 000 / 0 bytes**；失败在 DNS 阶段，未进入 TLS 握手，未取得任何远端正文。

| 精确 GET | 错误 |
|---|---|
| [annotations.md@v1.1.1](https://raw.githubusercontent.com/opencontainers/image-spec/v1.1.1/annotations.md) | `Could not resolve host: raw.githubusercontent.com` |
| [containerd CRI config.md@v2.4.1](https://raw.githubusercontent.com/containerd/containerd/v2.4.1/docs/cri/config.md) | 同上 |
| [CDI SPEC.md@cb98bcf6](https://raw.githubusercontent.com/cncf-tags/container-device-interface/cb98bcf66dc68530012483bd56e33e14d815e167/SPEC.md) | 同上 |
| [Toolkit 1.20.0 troubleshooting.html](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html) | `Could not resolve host: docs.nvidia.com` |
| [Ascend plugin.go@44385c13](https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go) | `Could not resolve host: raw.githubusercontent.com` |

**没有完成“curl 成功取得一次源文字”这一指定方法。** 按用户允许的只读替代通道，使用 `web.run` 和 GitHub 连接器实际读取正文、源码片段及 Git 对象，核对文字而非仅检查可达性。替代读取不记作 curl 成功，不制造 HTTP 200、远端字节 SHA-256 或本机 TLS 验证结果。

网页通道会缓存、转换文字：本轮 NGC 页标示约两个月前抓取，runtime-spec 通用页约一个月前抓取，Toolkit 排障页约三天前抓取；这些不是本机实时字节快照。CDI 的 raw/blob 网页读取均返回 Internal Error，改用 GitHub `fetch_file` 成功读 SPEC；runc README 的网页读取失败，本轮只确认其 tag 对象身份，不声称审计了 runc 实现。Issue 连接器大响应出现截断，另用网页通道核对具体环境、资源请求与错误段；不以截断区推断缺项。源码坐标采用连接器按原文件行号取回的片段；网页显示行号不用于构造 GitHub 行锚点。

### 3.2 本轮独立读取的关键文字

| 一次源与定位 | 实际核对的内容 | 支持范围与限制 |
|---|---|---|
| [image-spec annotations.md@v1.1.1](https://raw.githubusercontent.com/opencontainers/image-spec/v1.1.1/annotations.md)，Rules / Pre-Defined Annotation Keys | 注解属性选填；类型、唯一性等有 MUST；基础镜像关系有相应 SHOULD | 支持正文 L47 修正；不建立构建输入完备性 |
| [image-spec config.md@v1.1.1](https://raw.githubusercontent.com/opencontainers/image-spec/v1.1.1/config.md)，Layer DiffID / Properties；[manifest.md](https://raw.githubusercontent.com/opencontainers/image-spec/v1.1.1/manifest.md)，subject | 未压缩层 tar 的 DiffID、层打包/解包建议；`rootfs.diff_ids` 必填、`history` 可选、`subject` 可选 | 支持正文 L48–49 的边界，不替代 SBOM/签名方法 |
| [containerd CRI config.md@v2.4.1](https://raw.githubusercontent.com/containerd/containerd/v2.4.1/docs/cri/config.md)，Config versions / Runtime classes / Full configuration | `version = 3`、2.x 的 runtime/images 插件配置分区、`runtime_type`、`cdi_spec_dirs` 的两个目录 | 是真实配置入口；不能只提一个字段便视为已交付运行时配置/诊断方法，也不能外推所有 containerd 客户端 |
| [CDI SPEC.md@cb98bcf6](https://github.com/cncf-tags/container-device-interface/blob/cb98bcf66dc68530012483bd56e33e14d815e167/SPEC.md)，Version / Released versions / Overview | spec 自述 1.1.0；v1.1.1 无 Spec 变更；供应商描述设备编辑，消费端据之变换 OCI 配置。原文件 blob `2bc480a20ce447f5281b5d6844a486a81bb635b0` | 证实正文 L56 与登记版本修正，也直接反驳 L64 残留的“CDI 规范 v1.1.1” |
| [runtime-spec config.md@92249139](https://raw.githubusercontent.com/opencontainers/runtime-spec/92249139eea7161e13745abd4cb6d0ea02a3227a/config.md)，User / POSIX-platform User；[config-linux.md](https://github.com/opencontainers/runtime-spec/blob/92249139eea7161e13745abd4cb6d0ea02a3227a/config-linux.md)，原文件 L127–153、L402–420 | 进程 `uid/gid/additionalGids`；节点身份和 Allowed Device list 的许可字段分别核对。Linux 文件 blob `c71757494ca743fd90692c25e4897bf74cf00388` | 支持 L65 的字段分离；不是 image-spec 的 config，也不证明设备可访问 |
| [Toolkit 1.20.0 install-guide.html](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/install-guide.html)，Prerequisites / Configuring containerd；[docker-specialized.html](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/docker-specialized.html)，GPU Enumeration / Driver Capabilities | 宿主驱动前提与包版本 `1.20.0-1`；GPU 选择变量与库/二进制挂入变量职责不同 | 认可 L60–61；不提供镜像自带库版本或框架物理映射证据 |
| [Toolkit 1.20.0 cdi-support.html](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html)，Automatic Generation / Known Limitations / Running a Workload / Non-CDI-Enabled Runtimes | 自动生成、刷新缺口、原生消费和 NVIDIA runtime CDI 路径、hook 冲突 | 认可已列边界；具体 engine/CRI 配置条件不能省略为“按 CDI 消费” |
| [NVIDIA plugin README@v0.20.1](https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.20.1/README.md)，Configuration Option Details / Shared Access to GPUs | `envvar` 与两种 CDI 传递策略不同；`cdi-cri` 用 `CDIDevices` 且依赖 Kubernetes 转发及消费端支持；ID 策略不是框架映射；time-slicing 不隔离显存及故障域 | 认可 L63、L68 部分解释；L63 尚未选出实际传递字段链 |
| [Toolkit 1.20.0 troubleshooting.html](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html#nvml-insufficient-permissions-and-selinux)，NVML 权限段及 [GPU 访问丢失段](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html#containers-losing-access-to-gpus-with-error-failed-to-initialize-nvml-unknown-error) | 两种 NVML 消息对应不同情境；SELinux 关闭标签有隔离代价；hook/legacy 访问更新与删除后重新创建的恢复说明 | L87 错误仍在；L89 的“撤销更新不等于恢复”限定已有进展。没有执行任何官方处置建议 |
| [Ascend plugin.go@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go)，原文件 L1080–1180、L1290–1365 | 直接返回 DeviceSpec 的 `HostPath/ContainerPath/rw`；`UseAscendDocker` 判断在 L1161–1169，另一分支调用辅助函数；Allocate 可到达该函数。blob `b7692611b12884854d973fa2a3da18e381353f10` | 认可插件取证；没有核验辅助函数和对应 runtime 消费/库挂载，不能补成作者已交付 |
| [框架容器指南](https://docs.nvidia.com/deeplearning/frameworks/user-guide/index.html)，§5.9；[NGC 25.01-py3 layers](https://catalog.ngc.nvidia.com/orgs/nvidia/-/containers/pytorch/25.01-py3/layers) | §5.9 是限制 GPU 暴露；NGC 是目录/层元数据入口 | 都不能代替本页欠缺的库身份记录方法和框架 ordinal→物理标识映射方法；未拉取或验签 |
| [vLLM Ascend Issue #2557](https://github.com/vllm-project/vllm-ascend/issues/2557)，环境 / Pod 请求 / 错误与报告者解释 | 4 个 NPU 资源请求；物理编号 0、3、4、7 可列举；把这些编号填入可见变量后出现 `[0,4)` 范围错误。环境含 torch 2.5.1、torch_npu 2.5.1.post1、vLLM 0.9.1、Ascend dev `f6a0e1629`、CANN 8.2.RC1 | 认可 L91 症状摘要；不是完全缺设备案例，也不是本库复现或通用修复证明 |
| [Kubernetes v1.32 Images](https://v1-32.docs.kubernetes.io/docs/concepts/containers/images/#image-pull-policy)，Image pull policy / Default image pull policy | `imagePullPolicy` 与 kubelet 拉取判断、默认化及缓存语义 | 审阅者补充 C30 的职责定位；不能当作作者已经选定该版本路径、登记或完成方法 |

### 3.3 tag 解引用核对

独立读取官方 ref；annotated tag 继续读取其 tag 对象，不把 tag 对象 SHA 当 commit。下表仅确认身份，不确认部署兼容，不把返回的 verification 字段当本库独立验签。

| 固定点 | 实际读取与结果 |
|---|---|
| containerd v2.4.1 | [ref](https://api.github.com/repos/containerd/containerd/git/ref/tags/v2.4.1) → tag 对象 [`e24870ce498feb6721878a1af2fdd1641b926854`](https://api.github.com/repos/containerd/containerd/git/tags/e24870ce498feb6721878a1af2fdd1641b926854) → commit `f2551031d7276a770f65f98c9b52e57e7dad07e8` |
| runc v1.5.2 | [ref](https://api.github.com/repos/opencontainers/runc/git/ref/tags/v1.5.2) → tag 对象 [`b622a5992f0ba88fda05f2fd037d151b4fc5cc88`](https://api.github.com/repos/opencontainers/runc/git/tags/b622a5992f0ba88fda05f2fd037d151b4fc5cc88) → commit `29dd3dc2b13b4123162e5fe132504bb4b15569f1` |
| CDI 仓库 v1.1.1 | [ref](https://api.github.com/repos/cncf-tags/container-device-interface/git/ref/tags/v1.1.1) 直接指向 commit `cb98bcf66dc68530012483bd56e33e14d815e167`；该 commit 的 spec 是 1.1.0 |
| runtime-spec v1.3.0 | [ref](https://api.github.com/repos/opencontainers/runtime-spec/git/ref/tags/v1.3.0) → tag 对象 [`0eaca84ca040a452ebf87480b3f7bedf79d46f46`](https://api.github.com/repos/opencontainers/runtime-spec/git/tags/0eaca84ca040a452ebf87480b3f7bedf79d46f46) → commit `92249139eea7161e13745abd4cb6d0ea02a3227a` |

三个作者新选 tag 均存在；问题不在版本不存在，而在作者交付的配置、传递、诊断方法和记录是否完整。审阅者补充读取不等于作者已修订。

## 4. B21-C30–C34 逐项复核

### B21-C30 — P2 / OPEN

**权威条件：** 前次复核 L102；初审 L97–102。**位置：** 正文 L41–52、L32、L98；作者记录 L9、L17；映射 L104；登记 L5204–5214、L5248–5258。

| 剩余关闭条件 | 本轮判断与证据 |
|---|---|
| 可填写的输入身份/证据格式与缺项判据 | **仍未满足。** L44–46 仍只是“修订/来源、参数/锁文件身份、工具名/版本”，证据格写 unknown；未说明怎样保存上下文/锁文件身份、记录证据定位、判别未固定或缺失。列字段与允许实际值 unknown 是两件事，无须选定工具也能给出记录方法。 |
| 固定并分别交付 SBOM、签名对象、方法、边界 | **未满足。** L50–51 明确材料、方法与限制未取；分列两行已认可，但不能替代验收要求。不能要求作者伪造实际验签结果，也不能把待取证写成方法已交付。 |
| 选实际拉取路径，交付有版本依据的字段/默认/缓存方法 | **部分满足。** L52 选择 containerd/CRI 并保存 digest/时间，限定 digest 的内容身份作用；仍没有策略字段、取值、默认化、实际缓存/拉取行为证据。L56 的 CRI 配置入口不等于这些内容已写入 L52。若选择 Kubernetes→CRI，`imagePullPolicy` 的语义须取自所选 Kubernetes/kubelet 路径，不能笼统声称“字段与默认值见 containerd 配置”。见 §3.2 两个官方入口。 |
| 纠正规范级别/可复现范围，保留边界并同步记录 | **正文纠偏已满足，记录同步仍未满足。** L47–49 对 MUST/SHOULD、层 tar、可选 subject 的修改与原文一致；L37、L43、L52 保留 digest/兼容和非供应链限定。但作者记录 L9 仍写“SHOULD 注解”，登记 L5209、L5214 未同步本轮 annotations/config 核对范围。 |

**剩余关闭条件：** 交付输入身份与证据留存/缺项判断格式；固定官方 SBOM 和签名材料，分别写记录对象、核对方法及完整性/信任边界；选清楚编排或 CLI 到 CRI 的拉取路径，写实际策略字段、默认值和缓存事实记录；同步作者记录与登记。已纠正的正文规范精度不再重复要求，实际环境/结果仍可 unknown。

### B21-C31 — P2 / OPEN

**权威条件：** 前次复核 L118；初审 L114–118。**位置：** 正文 L21、L32、L56、L63–65、L98；作者记录 L10、L17；映射 L103、L105；登记 L5248–5269。

| 剩余关闭条件 | 本轮判断与证据 |
|---|---|
| containerd/runc 固定原文件、配置模式/字段与诊断依据，登记引用 | **部分满足。** containerd 新登记、CRI 精确链接及 `cdi_spec_dirs` 已交付；§3.2 读到对应原文。但 L56 未写版本头实际值/字段归属或诊断方法，runc 仍只有版本名与“正文未读实现”，作者记录/登记中无 runc 原文件、commit 或诊断依据。审阅者本轮解引用成功不关闭该缺口。 |
| CDI 规范身份与生成者、消费端、Kubernetes/CRI 前提 | **部分满足且仍有错误。** L56 与登记 L5259–5269 已正确区分 repo tag 1.1.1、spec 1.1.0、文件 `cdiVersion`；但 L64 仍写“CDI 规范 v1.1.1”。L63 未选择 `cdi-annotations` 或 `cdi-cri`，未交代实际传递字段及 engine/Kubernetes 转发条件；Toolkit 页的链接本身不补齐该链。 |
| OCI 通用/Linux 各自精确链接与版本表述 | **部分满足并追记错误。** L65 正确链接 runtime-spec User 和 Linux 字段；然而 L56 的“OCI 通用字段”链到 **image-spec** `config.md`，不是 runtime-spec 通用运行时配置。同名文件不等义，不能因 L65 有正确链接便忽略 L56 的错指。containerd tag 定位本身已核对。 |
| 新旧取证状态一致 | **未同步。** L32、L98 和作者记录 L10、L17 仍把 containerd/CDI 正文标成未读；登记 L5253、L5264 又声明实开并核对。本轮无法据此独立确认作者实际取证流程，应同步范围和准确入口，不把这个矛盾包装成已独立确认的执行记录。 |

**原 ID 下事实追记：** L64 的 CDI 规范误标是前次纠偏尚未清除；L56 新增的 image-spec/runtime-spec 同名错链仍归 C31 的精确来源与职责边界，**不新增 ID、不变优先级**。

**剩余关闭条件：** 补所选 containerd 配置模式/字段和诊断依据；固定、登记并引用 runc 的相关原文件或版本化文档；清除 CDI 版本残留，补生成/传递/消费的实际前提；纠正 L56 的通用运行时规范入口并同步取证状态。支持交集可以继续 unknown，不要求虚构兼容组合。

### B21-C32 — P2 / OPEN

**权威条件：** 前次复核 L135；初审 L130–135。**位置：** 正文 L60–68；作者记录 L11；映射 L106。

| 剩余关闭条件 | 本轮判断与证据 |
|---|---|
| 宿主、挂入组件、镜像自带库的身份/版本字段 | **部分满足。** L60–61 解释了内核不是搬入镜像，且两类 NVIDIA 变量职责已纠正。L62 仍是目录层元数据、Signed/build 信息；未给 CUDA/框架库具体身份、版本、来源层及证据记录方法。Signed 不等于读者已验签，本页保留未执行限定是正确的。 |
| 固定 GPU 样板，以具体字段串起分配和最终配置 | **部分满足。** L63 明确选 CDI 原生，承认插件策略不是框架映射；但资源请求→Toolkit→engine→节点/挂载仍是概念箭头，缺实际 Allocate ID、CDI 名称/传递字段、文件匹配项、OCI 节点/挂载之间的核对关系。`envvar` 举例也没有被限定为另一个模式，不能替代所选 CDI 传递策略。依据见 §3.2 插件与 CDI 原文。 |
| 节点、进程、设备规则、LSM 的证据位置与判断边界 | **字段分离进展已认可，仍不完整。** L65 新增 UID/GID/附加组并分节点与许可；但 LSM 全部 unknown，未说明现场应记录什么策略/拒绝证据及怎样同进程和设备关联。可见性不等于访问成功这一限定已满足。 |
| 固定框架来源及 ordinal/物理标识对应记录方法 | **未满足。** L66 一面称方法“以分配 ID＋注入通道＋限制暴露段为准”，一面承认该节不定义物理映射；缺框架证据及逐编号→稳定物理标识的记录格式。指南 §5.9 仅控制暴露；无法确定时写 unknown 合理，但不能免交核对方法。 |

**剩余关闭条件：** 用具体字段完成一个选定 GPU 模式的分配→传递→最终配置链；补三个来源层的库身份/版本记录；补 DAC、设备规则及 LSM 的证据关联；固定框架来源，交付逐 ordinal/设备标识映射方法。§2 负责机制/字段、§4 负责异常/对照，两者分别验收，不以重复概念表一次抵充两项。

### B21-C33 — P2 / OPEN

**权威条件：** 前次复核 L152；初审 L147–152。**位置：** 正文 L72–76、L98；作者记录 L12、L17；映射 L107；登记 L5237–5247。

| 剩余关闭条件 | 本轮判断与证据 |
|---|---|
| 选择 Ascend runtime/ref，核对插件辅助函数输出到消费/挂载实现 | **未满足。** L72 明写 runtime 消费端未选定、辅助函数和环境/库注入未知，L98 再列待确认。链接到 Allocate 不会自动补出辅助函数输出或 runtime 消费端。 |
| 分支条件与各阶段具体字段 | **插件部分满足。** §3.2 独立读到 `UseAscendDocker` 两分支、DeviceSpec `HostPath/ContainerPath/rw` 以及 Allocate 调用。L72 的分支判断位置仍应使用 L1161–1169；L1087 起是被调挂载函数，不是 `UseAscendDocker` 判断本身。正文没有展开后续字段语义。 |
| 目标配套未知、平台和 digest 边界 | **满足这些边界。** L37、L74 列出目标组合所需字段，未从 GPU/CDI 推导 NPU，未宣称支持交集。未做硬件验证不是本项新增阻塞。 |
| ACP 无关入口清理 | **已满足并保持。** L76 明确设备暴露不引用 ACP，不再重复要求。 |

**剩余关闭条件：** 固定明确 Ascend runtime 组件/ref，核对插件辅助函数实际输出及消费端的节点、环境、库挂载实现，用具体字段连接两端；精确标明分支条件。允许声明两个固定实现的支持交集未建立，不可把版本不同的既有 runtime 文档直接拼成兼容组合。这里要求实现取证，不要求真实环境运行。

### B21-C34 — P1 / OPEN

**权威条件：** 前次复核 L170；初审 L165–171。**位置：** 正文 L80–93；作者记录 L13；映射 L108；关联案例 L19–25、L32–40、L82，关联实验的设计/前提/判据章节。

| 剩余关闭条件 | 本轮判断与证据 |
|---|---|
| 带字段/期望/实际/证据定位/缺失解释的环境模板 | **未实际交付。** L80 声称“五栏，示例如下，空表由读者填写”，但下面只有异常分支表，没有五栏表或等价可填写记录块；仍是一段字段类别。镜像库身份、分配/最终配置及物理映射的记录位置没有落地。 |
| GPU/NPU 注入、拒绝、隔离各分支与可区分判据 | **部分满足但仍阻塞。** L86 增加模式分类；L86–89 加完成/失败/无法判定文字，进展已认可。L87 的 NPU 拒绝仍无依据，L88 没有 NPU 隔离分支。证据列“三单核对/排障页/影响证据”未形成定位方法；“三单一致”缺 ID 映射与范围定义，“任一单缺失”未区分缺少证据和已证明漏注入。关共享后影响消失，只支持所选对照现象，不能单凭它证明显存、计算或故障域隔离。 |
| 基线/变体、证据、集合身份、旁路排除及授权/停止/恢复 | **部分满足。** L91 增加一次一项、快照、旁路排除及停止提醒；未展开可执行于授权隔离环境的计划表、各变体唯一差异、主体/时间窗/字段和结果判断，旁路排除只是要求一句“说明”。digest/版本固定不能替代设备身份映射。末句仅要求“授权与隔离前提”，未给本页具体前提。关联实验已有更具体设计，但 L91 明确本页判定见上表，不能用链接代替本页交付。 |
| 案例真实症状、缺失条件、版本范围和未复现属性落页并接入分支 | **部分满足。** L91 已正确摘要物理 0、3、4、7 与逻辑范围 `[0,4)` 的分叉，不再把它说成完全无节点。却仍把环境/版本都推给关联页，未在本页明确案例适用版本和非本库复现；“未执行”紧跟的是实验链接。上表缺与该症状相符的“节点在、逻辑编号/选择失败”路径，现有“设备注入缺失”不能直接容纳这个反例。关联案例自身的限定正确，但不是本页已完成的修订。 |
| 分开两个 NVML 情境及更新/恢复边界，保持授权限定 | **仍有事实错误。** L87 仍写 `NVML Unknown Error（限 Insufficient Permissions 段…）`；加“不混用”括号没有改掉消息与来源的错配。§3.2 权限段的消息是 `Failed to initialize NVML: Insufficient Permissions`，Unknown Error 属于后面的 hook/legacy 访问丢失说明。L89 已明确撤销更新不等于恢复，L93 保留只设计、不授予执行权，认可这些修正。 |

**原 ID 下追记：** NVML 消息错配为前次 C34 纠偏仍未清除；模板缺失、集合判据和案例分支连接均属于既有 C34，不另设发现 ID。

**剩余关闭条件：** 真正交付五栏环境模板；分别展开 GPU/NPU 模式下的注入、拒绝、隔离分支和证据/停止/完成/无法判断规则，缺证据不能判技术失败；用设备身份映射比较请求、注入和框架集合，不要求编号文本直接相等；具体列基线/变体、唯一差异、证据定位、旁路与负向验证前提及恢复边界；在本页落下案例版本/缺项/未复现摘要，并接入逻辑编号分叉分支；把 L87 消息改为来源真正支持的情境。仍只要求设计，不要求制造实测或自动放宽权限、禁用 LSM、重启生产组件。

## 5. Acceptance 与最终计数

| 计划位置 / acceptance | 本轮结论 | 未关闭的原 ID |
|---|---|---|
| L5403 / 镜像 digest、基础/依赖、构建输入、SBOM/签名与拉取策略方法/限制 | 部分满足，**未通过**；边界已修正，必交方法仍缺 | B21-C30 |
| L5404 / 固定 OCI/containerd/runc/Toolkit/CDI，分离 host、库、设备/环境/挂载、权限和框架映射 | 部分满足，**未通过**；CRI/SPEC 登记有进展，runc 方法、精确入口、传递和映射仍缺 | B21-C31、B21-C32 |
| L5405 / Ascend runtime/plugin 独立固定实现、目标组合及 GPU/NPU 边界 | 部分满足，**未通过**；插件和未知边界保持，runtime 消费端未交付 | B21-C33 |
| L5406 / 环境清单、观测/异常分支、对照验证和源案例，不作安装处方 | 部分满足，**未通过**；真实模板、平台分支、可判定对照和案例连接仍不足，NVML 消息仍错配 | B21-C34 |

**5 个原发现：0 CLOSED / 5 OPEN；4 条 acceptance：0 完整通过 / 4 未完整通过；无新增发现 ID，无优先级调整。** 本轮不否定真实的局部修正，也不把作者未交付的方法用审阅者追加取证抵充。后续仍须修订并按新的输入 SHA 进行定向复核，不能因本报告交付或结构检查通过而宣告技术审阅通过。

## 6. 结构校验与单文件写入边界

- 写入前原仓库 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS：94 content entries / 423 sources**。仅校验结构、登记和本地链接，不校验技术主张或远程正文。
- 写入后原仓库 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS：94 content entries / 423 sources**；另以校验器检查本报告的本地文件链接，并检查行尾空白，均 PASS。
- 为遵守只写本报告，把仓库及既有 `build/` 复制到 `/private/tmp/b21-t05-01-recheck-2.N58ZqY/validation`，排除 `.git`、`.venv`、`.agents`、`.codex` 和字节码缓存；在副本内使用原仓库虚拟环境 Python 执行 `PYTHONDONTWRITEBYTECODE=1 make check`、`make build`，两项均 **PASS：94 content entries / 423 sources**。只在副本重新生成 `build/catalog.json`、`build/catalog.md`，没有镜像构建或技术实测。
- 收尾摘要对比：七个主输入完整 SHA-256 全部不变；原仓库 `build/` 的前后文件摘要清单相同；除本报告外全部 Git 所列 tracked/untracked 非忽略文件的摘要清单相同。工作区状态相对本轮开始只新增本报告，既有作者改动与未跟踪文件保留。
- 不需要 `make test`：本轮没有修改 `src/kb/` 或测试代码，也不为报告新增测试。

**最终结论：第二次定向复核不通过，C30–C34 全部保持 OPEN；已披露 curl DNS 失败和只读替代取文限制，未确认实际执行模型元数据，未执行实测。**
