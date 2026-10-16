# Batch 21 补交 T05-01 第八次定向复核（作者第八轮修订后）

## 1. 结论、角色与范围

- 日期：**2026-10-14（Asia/Shanghai）**；本机日期同日，时区 `CST / +0800`。
- 执行者：本会话 Codex，独立审阅角色，与作者第八轮修订角色分开；没有另行派发模型。本轮只新增本报告，不改作者正文、记录、修订映射、来源登记、计划、关联条目或历史报告，不提交 Git commit。
- 用户约定审阅配置：`gpt-6.1-sol / xhigh`。**此处仅记录用户约定，不写成已独立确认的执行元数据。** 本轮未取得可独立核验的实际模型标识或 reasoning 配置，不以模型自述充当确认。
- 范围：仅 **B21-C31–C34**，优先级沿用初审；剩余关闭条件以[第七次定向复核](batch-21-t05-01-codex-recheck-7.md) L96、L110、L121、L136 为权威，结合[初审](batch-21-t05-01-codex-review.md) §6 与[任务验收](../../plans/full-coverage-backlog.yaml) L5403–5406。[第八轮修订映射](batch-21-review-fixes.md) L152–157 只用于定位落盘改动，不作为关闭证明。
- **本轮结果：0 CLOSED / 4 OPEN；第八次定向复核不通过。** OPEN：C31、C32、C33（各 P2）、C34（P1）。**不新增发现 ID，不调整优先级。** C30 已 CLOSED，不在本轮复核范围，不重开、不以它扩大本轮分母；若仅汇总既有五项状态，仍为 1 CLOSED / 4 OPEN。
- 认可配置转换判据纠偏、Allocate 角色纠正、OCI 节点身份列、同 commit Ascend runtime 入口、设备集合分层、部分 NPU 未知判据、负向组拆分、资源更新变体和重建旧新对象记录的进展；不会把这些已补子条件重新判作全缺失。
- 未执行镜像构建/拉取、SBOM 生成/比对、签名/验签、容器启动、设备访问、配置修改、负向/隔离试验或 GPU/NPU 实测。知识库结构检查和清单生成不是上述实测，也不建立版本支持交集或硬件验证结论。

## 2. 输入身份与位置口径

起始读取时，用户提供的四个 SHA-256 前缀**全部匹配**。下表记录本轮审阅输入版本，其余三个输入另记录完整摘要；正文、作者记录、映射和登记行号均为该版本的本地文件坐标。上游行号采用 GitHub 只读连接器的固定 ref 原文件区间，不把网页阅读器行号拼成源码锚点。

| 输入 | 完整 SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md) | `9d84ed747cd42c1a46bfd46bad1be551432cc3b8668b67e4ba4200aace56bcd5` |
| [作者来源记录](batch-21-t05-01-sources.md) | `da14e78aa242ebbf2a9bf52b66d2ef1dbe204bf5ad9d8e966cabde192f7652fc` |
| [修订映射](batch-21-review-fixes.md)，只取第八轮 L152–157 | `572574794c465028334fc52bea2daf81c4cacc1b8320dd6081c3bab34a04aa76` |
| [第七次定向复核](batch-21-t05-01-codex-recheck-7.md) | `74b98fd8bdcc6b01ee1285c089483cda46fdacc3081ff23c68297b46187771a1` |
| [初审](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` |
| [任务验收计划](../../plans/full-coverage-backlog.yaml)，T05-01 L5386–5418 | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml) | `b33acc3964761d2cb314cd36f4645acae470e5df9deb0d513137928c237838ab` |

另读 README、编写指南、内容总目录、元数据 schema、[Ascend 来源案例](../../knowledge/05-cluster-platform/ascend-device-visibility-source-case.md) L32–40，并定位[关联实验](../../knowledge/05-cluster-platform/ascend-device-visibility-experiment.md)的前提、旁路、停止及判据章节；关联页不重新验收。起始登记实计 **437 项**；新增 runtime 项在 L5419–5429。历史登记中的 `curl 200` 是作者记录，不计作本轮请求结果，也不独立确认作者历史执行。

**并发版本边界：** 报告写入后观察到其他工作区变更，修订映射完整摘要变为 `4bb9653f65a66ac98aa96952c30cb711287993b4e83af2f49cc61f7a3e519589`（追加 T05-02 修订节），登记变为 `7f64bf94474248b5edfed8ea671bb5950abd63e3721e39e7b6f749f2f559a9d4`（现 438 项，追加 T05-02 的 api-gc 来源等变化）。再次读取确认 T05-01 第八轮 L152–157 与 runtime 新项仍保留上述内容，其余五个输入完整摘要未变。本报告结论针对上表审阅版本和本次未变的 T05-01 正文，**不宣告后来完整映射/登记版本已获同等复核**；未覆盖、回滚或吸收并发修订。

## 3. 一次源抽查、方法与限制

### 3.1 实际 curl 请求

本机 curl **8.7.1**；对下表 01–14 的精确 URL 分别执行只读 GET，保持默认 TLS 校验，未使用 `-k`、替换证书、修改 DNS、提权或绕过沙箱。调用形态：

```bash
curl --location --silent --show-error --connect-timeout 8 --max-time 20 \
  --output "$audit_dir/$name.body" --write-out '%{http_code}' "$url"
```

**14/14 均退出码 6、HTTP `000`、`Could not resolve host`。** 没有取得 curl 响应正文，TLS 握手未发生；不声称 curl 成功、HTTP 200 或本机验证了远端 TLS 链。请求清单、诊断及前后摘要仅留临时目录 `/private/tmp/b21-t05-01-recheck-8.z00Od7/`，未加入知识库。

### 3.2 允许的只读替代通道：实际文字核对

使用 `web.run` 阅读精确页面的正文，并用 GitHub 只读连接器读取固定 ref 的源码区间。以下记录的是实际文字/实现核对，**不只是可达性**；网页通道失败处改读 GitHub 原文件。网页通道的缓存或归一化文本不等于本机即时 GET，也不作“最新版本”确认。

| curl 点 / 精确一次源 | 本轮实际核对内容与边界 |
|---|---|
| 01 / [containerd config@v2.4.1](https://raw.githubusercontent.com/containerd/containerd/v2.4.1/docs/cri/config.md) | GitHub L22–140、L215–288：v3 images/runtime 分区、RuntimeClass/handler、完整 runtime 键、CDI 目录、systemd 与 kubelet 条件；网页正文另确认 v2 支持/转换。用于 C31，不确认现场生效。 |
| 02 / [runc-state 手册@v1.5.2](https://raw.githubusercontent.com/opencontainers/runc/v1.5.2/man/runc-state.8.md) | 手册确认 JSON 状态输出；另补读同 tag 的 [state.go](https://github.com/opencontainers/runc/blob/v1.5.2/state.go)完整文件与 [list.go L1–82](https://github.com/opencontainers/runc/blob/v1.5.2/list.go#L1-L82)，核对输出构造、JSON 字段及 `--root` 的查询作用域。用于 C31。 |
| 03 / [runc libcontainer/state.go@v1.5.2](https://raw.githubusercontent.com/opencontainers/runc/v1.5.2/libcontainer/state.go) | curl DNS 失败；随后 GitHub 精确文件请求返回 404。只记该路径在本次通道不可解析，不据此否定 state 功能；判定改用上行已读的 CLI 实际文件，不把此路径算作已读源码。 |
| 04 / [NVIDIA server.go@v0.20.1](https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.20.1/internal/plugin/server.go) | GitHub L280–438、L448–481 与网页全文：读取/校验 `DevicesIds`，UUID 去标注或 index 转换并去重，生成 qualified 名，追加其他 CDI 请求，再填 `CdiDevices[].Name`。用于 C32，不能替代框架 ordinal 映射。 |
| 05 / [NVIDIA README@v0.20.1](https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.20.1/README.md) | 配置段与 Shared Access：`cdi-cri` 的 CRI/engine 条件，UUID/index 策略，以及 time-slicing 不提供工作负载隔离的边界。用于 C32/C34。 |
| 06 / [CDI SPEC@cb98bcf6](https://raw.githubusercontent.com/cncf-tags/container-device-interface/cb98bcf66dc68530012483bd56e33e14d815e167/SPEC.md) | GitHub L90–265：kind/name、全局与设备级 edits 的应用条件、deviceNodes、host/container mount 路径和 env 字段。用于 C32/C34，不推定所有注入项都是获配作业设备。 |
| 07 / [OCI Linux config@92249139](https://raw.githubusercontent.com/opencontainers/runtime-spec/92249139eea7161e13745abd4cb6d0ea02a3227a/config-linux.md) | GitHub L127–151、L402–418：节点 type/path/major/minor/属主与访问 allow/type/major/minor/access 是不同对象；仅 major 不构成身份。用于 C32/C34。 |
| 08 / [Ascend common.go@44385c13](https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go) | GitHub L90–150：ID 逗号串/options、310B allow-link、限 `!PresetVDevice` 的 worker 组。用于 C33；未把符号名当作已核对全部 api 字符串值。 |
| 09 / [Ascend plugin.go@44385c13](https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go) | GitHub L1087–1185：DeviceSpec 的 HostPath/ContainerPath/rw、默认设备/UB 设备和 UseAscendDocker 两条分支。用于 C33/C34，不审计整个 Allocate 实现。 |
| 10 / [Ascend runtime README@44385c13](https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/README.md) | 设计简介：OCI 插件、可见设备变量、设备 cgroup、库挂载与 hook。另读同 ref 组件目录，确认实际 runtime 入口；README 的库挂载设计不能充当完整 hook/白名单实现审计。用于 C33。 |
| 11 / [Ascend process.go@44385c13](https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go) | GitHub 分四段读完 L1–938，并定向重读 L243–282、L350–400、L725–795、L850–910：create 改写 spec、变量解析、节点与 cgroup 写入、环境库路径、hook/虚拟设备条件。未继续审计 hook 可执行文件、dcmi 子实现或白名单。用于 C33。 |
| 12 / [Toolkit 1.20.0 troubleshooting](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html) | NVML 权限与 hook/legacy Unknown Error 分段；资源更新（含 CPU/内存限制）可能撤销设备访问；重建只是所述恢复路径之一，放弃 SELinux label 分离不是常规隔离证明。用于 C34。 |
| 13 / [PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html) | `CUDA_VISIBLE_DEVICES` 的可用 GPU 范围管理；本页所引用段不是逐 ordinal→UUID 的取证规则。用于 C32，不声称 PyTorch 没有其他映射接口。 |
| 14 / [syft README@v1.54.1](https://raw.githubusercontent.com/anchore/syft/v1.54.1/README.md) | Features：镜像/文件系统扫描及输出格式能力；未据 README 推定所有输出必有逐库路径/来源层，也未读全部 cataloger。用于 C32。 |

关键原文件 blob：containerd config `3a206263f4f9e76b6ca14110461b8661a03b1619`；NVIDIA server `9281b48ef52f9eda9cbed6d98491729da85b5a75`；CDI SPEC `2bc480a20ce447f5281b5d6844a486a81bb635b0`；Ascend plugin/common `b7692611b12884854d973fa2a3da18e381353f10` / `6cd038e9f1d67a8a913aa4bb1301692f177b3dbe`；runtime README/process `f612ad6b5d2edcf65d9ad683d57a4f1a4e1f9088` / `acbd7a1ec0703498abfcfcb6ce1aa493069091b1`。blob 不是 commit、现场运行身份或实验结果。补读源码仅作本报告证据，遵守单文件约束未改登记，也不将审阅者补读冒充作者已交付。

## 4. B21-C31–C34 逐项复核

### B21-C31 — P2 / OPEN

**权威条件：** 第七次复核 L96。**本轮位置：** 正文 L29、L40、L64、L142；作者记录 L10、L26–28；映射 L154。

- **已补：** L64 将 v2 自动转 v3、RuntimeClass 显式选择与单纯文本差异分开，不再仅凭版本头/默认 handler 名不等就判配置未生效；也说明 `--root` 不是状态内容。固定版本、CDI 三层身份和 OCI 双页边界保持满足，抽查 01–02 支持这些进展。
- **完整字段/生效关联仍缺：** L64 和 L142 继续把 handler/options 完整键留为待填/unknown。没有落实所选 v3 的完整 images/runtime 插件键、default/所选 handler、`runtime_type`、options 中 `SystemdCgroup` 及其条件化参考值；同一 daemon/endpoint 的一句判据也未交付配置来源→所选 Pod/handler→容器→有效状态/日志对象的记录关联。缺现场值可以 unknown，已固定文档中的方法/键不能整体交给读者补。抽查 01 的 Cgroup Driver、Runtime classes、Full configuration 已给这些字段。
- **runc 状态方法仍缺：** L64 明写“状态字段与 bundle config.json/进程/运行期对应规则待填”。同 tag 的 [state.go](https://github.com/opencontainers/runc/blob/v1.5.2/state.go)和 [list.go L21–41](https://github.com/opencontainers/runc/blob/v1.5.2/list.go#L21-L41)已提供 `ociVersion/id/pid/status/bundle/rootfs/created/annotations` 的输出构造/字段依据；正文没有列所需保留字段或关联规则。state 构造还在 stopped 状态把 PID 置零，不能把所有状态的 PID 当作活进程身份证据。
- **按 C31 追记判据限制：** L64“排除转换/选择后，仍无对应状态/日志对象即记未生效”虽比上一轮窄，仍需区分“已取得实际生效对象且与所选配置冲突”与“未采到对象/日志”。证据缺失本身不证明配置未加载；后者须进入无法确定，而不是从无记录直接推定失效。

**剩余关闭条件：** 在所选 v3 模式列清精确分区/完整字段键、条件化参考值和实际值/unknown 格式，串联配置来源、daemon/CRI endpoint、Pod 所选 handler、容器身份与有效状态/日志。列清 runc 状态字段及 bundle/config/进程/时间窗关联；将确证不符与未采到证据分开。保留已补转换/显式选择/CDI 身份限定；**不要求配置变更、现场输出或整栈兼容证明**。

### B21-C32 — P2 / OPEN

**权威条件：** 第七次复核 L110。**本轮位置：** 正文 L68–76、L80–82；作者记录 L11、L24–25；映射 L155；登记 L5226–5236。

- **Allocate 角色纠正主干满足：** L73 不再把请求数量当作 ID 生成规则，读取/校验 DevicesIds→按策略转换去重→qualified 名→CdiDevices 的改写与本轮独立读取的 [server.go@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go#L280-L438)及 [L455–473](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go#L455-L473)一致。不能由此独立确认作者历史请求；该事实附近、作者记录与原登记仍没有精确 server.go 实现位置。框架映射不属于此转换，所选 cdi-cri 不混其他通道的限定保持满足。
- **edits→最终对象仍不是完整字段对应：** L73 增加三类最终对象，但只写 `devices[]`，没有明确 Linux 节点的 `linux.devices[]` 与许可的 `linux.resources.devices[]`；也未按全局/设备级来源连接 `deviceNodes` 的路径/类型/设备号/权限、mounts 的 hostPath→source/containerPath→destination 与 env→process.env。匹配还须 qualified 名的 kind 与设备 name 一起对应，不仅匹配 devices[].name；全局 edits 在该 spec 任一设备被请求时应用，设备级 edits 只在对应设备被请求时应用。依据见抽查 06–07，不能以箭头替代这些规则。
- **库/层方法仍部分欠缺：** L70 已正确承认 README 不保证逐库来源层字段，并逐项 unknown；不再判为“强称全部有来源层”。但所选扫描配置/输出依据及路径/成分→层的匹配规则仍未固定，L68–70 也没有把注入组件宿主来源→最终挂载配置→容器目标对象串成可追溯记录。未执行结果与未交付方法是两类缺项；不要求审计所有 cataloger。
- **稳定身份方法仍缺：** L80–82 新增完整 OCI 节点身份列，认可；L76 却仍明写固定 ordinal→UUID 方法未取，并保留仅“最终 OCI 节点主设备号”的旧叙述。框架快照、分配 ID、CDI 名和完整节点身份如何依据固定材料关联仍未交付；仅 major 或数量/编号文本不提供稳定物理对应。抽查 13 仅支持可见范围，不能补足该映射。

**剩余关闭条件：** 保留正确 Allocate 主干并补精确实现引用/来源记录；落实 qualified kind/name、全局/设备级应用条件、edits 各字段→完整 OCI 节点/许可/挂载/env 的对应格式。固定所选成分输出/层归属依据、匹配及最终挂载关联方法；用固定框架/设备身份材料完成 ordinal→分配/CDI→完整节点→稳定身份的取证方法。实际值可 unknown，**不要求拉取、生成 SBOM、采集现场值或负向试验**。

### B21-C33 — P2 / OPEN

**权威条件：** 第七次复核 L121。**本轮位置：** 正文 L18、L29、L40、L88–90、L141–142；作者记录 L12、L17；映射 L156；登记 L5335、L5419–5429。

- **入口/检索纠偏满足：** L88 选定同 commit 的 ascend-docker-runtime，纠正同级未定位及独立仓库名 404 的推论。README、process.go 和新增登记是实际存在的固定证据，本轮独立读取确认；不再把 runtime 实现入口判作未交付。
- **消费链主体已有进展：** process.go 支持 create 改写 bundle config.json、空/void 处理、设备列表解析、节点与 cgroup 写入。插件两分支/common 静态输出也经抽查 08–11 确认，不将这些已读部分重新判作全部 unknown。
- **按 C33 追记库注入对象混写：** L88 将“库挂载”并入 process.go→最终 OCI 的链条；但 [process.go L243–282](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go#L243-L282)所读 `addAscendLibraryPath` 只检查宿主路径存在并改写 `process.env` 的 `LD_LIBRARY_PATH`，不是添加库挂载。README 的设计说明与环境搜索路径不能代替实际库的来源/目标、白名单及必要 hook 消费实现；正文同时保留“runtime 库注入语义未核对”，该子链尚未闭环。
- **条件化设备/hook 链仍缺：** [process.go L850–910](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go#L850-L910)只在解析设备非空时进入 addHook/addDevice。[L350–400](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go#L350-L400)在 VIRTUAL 条件下跳过创建，另在返回 VdeviceID 非 -1 时改写设备列表/options 并加入 poststop destroy。L88 的笼统 ID 串→davinci*→hook 连接尚未交代这些条件，也未将 api 实际键、所选产品/manager/UB 条件与最终节点/许可逐字段关联。可以排除未选分支并标 unknown，但必须固定所选分支及其必要消费条件，而不是要求审计全部功能。
- **已读范围同步不完整：** 新登记 L5424 记录 README/process 已读，正文 L40/L142 也区分了部分未读范围；然而作者表 L12 仍只有 plugin.go 位置并称 runtime 消费端 unknown，L17 仍整体列“白名单/runtime 消费端”，common 登记 L5335 亦仍笼统写库注入未取。应把“已读入口/设备/env 改写”和“未读实际库挂载/白名单/hook”分开，不用新登记一项代替主张表同步。L90 的目标组合字段/支持交集 unknown、GPU 不套用 NPU/digest 非兼容证明保持满足。

**剩余关闭条件：** 固定所选实际分支及 api 键/设备列表/options→runtime 条件→最终完整节点、许可、环境的对应；区分 LD_LIBRARY_PATH 与实际库挂载，并补所选路径必要 hook/库挂载/白名单实现取证，说明虚拟设备与 poststop 条件或明确排除范围。同步正文、作者记录、登记的局部已读/未读状态。**支持交集、现场值和未选分支仍可 unknown；不要求安装、试运行或实测**。

### B21-C34 — P1 / OPEN

**权威条件：** 第七次复核 L136。**本轮位置：** 正文 L96–110、L114–121、L125–135；作者记录 L13；映射 L157。

- **设备集合边界已补：** L110 区分公共/默认控制设备节点、作业获配设备、资源请求数量和框架逻辑集合，并把机器位置另列，明确按取证映射对应而非全等。L129 拆开公共控制节点可见性、未请求作业设备不可见和未授权访问拒绝；保留单独授权及旁路清单，认可这些子条件。
- **本清单仍未落实三层库/最终配置/稳定身份关联：** L108 只加镜像内 CUDA/框架库字段；L106 仍只有容器内设备路径/变量实测值。缺宿主/注入库的来源→目标与版本证据、最终配置对象/摘要及分配与稳定身份的关联定位。§2 的概念格式不代替本清单的关联字段，且 C32 的固定映射方法仍未交付。
- **NPU 未知门槛只补了部分分支：** L119/L120 已加固定映射/访问语义缺失→无法确定，L120 补同一目标进程访问通过/原边界恢复；保持满足。L118 却仍在“昇腾语义未取源”下以“三单一致”判完成、三单齐且映射错判失败，没有同样的固定语义缺失门槛。L119/L120 的无法确定应明确优先于未具备解释依据的技术完成/失败，而不是仅写“不判完成”；观测仍可记录，不据未知语义归因。
- **每变体的可执行单变量仍不足：** L128 的 CDI 开关/cdi_spec_dirs/runtime handler 混列不同职责，具体配置键和唯一旧新差异仍待填；CDI 目录字段本身不等于模式选择。L129 的 UID/GID 仍需选明单一字段，L130 的 replicas/开关及 L132 的 CPU/内存限制也需选定一项实际键。不是要求填现场旧新值，而是交付固定路径下的键/作用/比较格式及前提，不能靠“一次只改一项”的声明代替。
- **主体/时间窗与安全恢复仍不足：** L133 已分别记录重建旧新容器/PID/快照，认可；L128 仍称“主体/时间窗同基线”，其余行“同上”。须按变体区分前后对象和各自观察时刻；同一对象可关联，需重建的变体不能照搬同 ID/PID。“偏离即停查/以三单复核”没有具体安全触发及恢复访问边界证据，三单可见性不证明权限边界恢复。须界定例如未授权作业设备暴露/访问、旁路或身份/节点漂移、影响其他负载时停止，并把同一目标进程受控访问及原负向边界恢复纳入恢复判据。
- **hook/legacy 更新类型及既有案例边界保持满足：** L131 已明说镜像/驱动回退不能代替资源更新；L132 增加源文档所述 CPU/内存资源更新变体，L133 保留重建≠充分恢复。所选键/时间窗仍属于上一条待补，不再判整个资源更新类别缺失。共享影响只解释本分支、不证明其他隔离维度，以及 L135 的案例环境/缺项/非本库复现摘要保持满足；抽查 12 支持更新范围限定。

**剩余关闭条件：** 在本清单落实三层库、实际分配、最终配置对象/摘要、稳定身份的关联；保留已补集合边界，在所有依赖 NPU 固定语义的分支落实缺失→无法确定的优先门槛。选定每变体具体配置键和单一差异格式，分别记录前后主体/时间窗；补具体安全停止与访问/原负向边界恢复判据，资源更新变体按所选源条件细化。保留分栏、隔离解释、旁路、授权和案例摘要；**不要求执行试验或制造结果**。

## 5. Acceptance 与最终计数

| 计划位置 / acceptance | 判断 | 原 ID |
|---|---|---|
| L5403 / 镜像身份、构建输入、SBOM/签名、拉取方法与限制 | 沿用第七次复核已关闭结论，本轮不重新验收；不等于已执行供应链验证 | B21-C30 CLOSED，范围外 |
| L5404 / 固定 runtime/Toolkit/CDI、各层与映射分离 | 部分满足，**未完整通过**；配置/状态方法、最终对象字段、库/层与稳定身份链仍欠缺 | B21-C31、B21-C32 OPEN |
| L5405 / Ascend runtime/plugin 独立实现与目标组合 | 部分满足，**未完整通过**；入口及部分消费实现已补，所选条件链/实际库挂载/必要 hook 与范围同步仍欠缺 | B21-C33 OPEN |
| L5406 / 清单、异常/隔离分支、对照与案例，不作安装处方 | 部分满足，**未完整通过**；清单关联、全部未知门槛、具体单变量/前后身份及安全恢复仍欠缺 | B21-C34 OPEN |

四条 acceptance 的状态汇总：**1 沿用既有完整通过 / 3 未完整通过**。本轮范围四项：**0 CLOSED / 4 OPEN（1 P1、3 P2）；第八次定向复核不通过。** 未通过的原因是剩余关闭条件未满足，不是 curl DNS 失败或没有实测；不会以审阅者补读替代作者应交付的方法和证据位置。新增修订中的事实/判据问题均追记所属原 ID，没有新增 ID。

## 6. 结构校验与单文件边界

- 写入前原仓库 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS：96 content entries / 437 sources**。
- 写入后原仓库 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS：96 content entries / 438 sources**。来源数增加来自上节观察到的并发变更，不是本报告新增来源。
- 临时副本首次排除 build 后，`make check` 因既有 `docs/first-fill-status.md` 指向缺失的两份 catalog 失败，`make build` 当次未运行；这是副本准备问题，不是本轮技术发现。随后把既有 build 一并复制到 `/private/tmp/b21-t05-01-recheck-8.z00Od7/validation/`，用原仓库虚拟环境 Python、禁写字节码执行副本 `make check` / `make build`，均 **PASS：96 content entries / 438 sources**。只在副本重建 catalog，没有镜像构建。
- 前后摘要审计：起始 **384 个**既有 Git 所列 tracked/untracked 非忽略文件及 build 文件中，观察到五个文件变化：`build/catalog.json`、`docs/research/batch-21-review-fixes.md`、`docs/research/batch-22-t05-02-sources.md`、`knowledge/05-cluster-platform/kubernetes-job-lifecycle.md`、`sources/registry.yaml`；另出现 `docs/research/batch-22-t05-02-claude-review.md`。这些不是本会话报告编辑，保留并如实披露，不声称“全部既有文件不变”。本会话写入范围仍只有本报告；T05-01 正文/作者来源记录、前次/初审报告及验收计划摘要保持输入值。
- 单文件约束下本会话只在临时副本生成清单，不重建原仓库 `build/`；不改 `src/kb/` 或测试，不为内容复核报告新增测试。报告四项 ID/优先级/状态、普通相对链接及行尾空白另作核对；结构检查不验证远程文字/技术正确性，不改变技术结论。

**最终技术结论：本轮 C31–C34 均 OPEN，0 CLOSED / 4 OPEN，第八次定向复核不通过。C30 保持此前 CLOSED、范围外；未执行实测，取证通道与执行元数据限制如实披露。**
