# Batch 21 补交 T05-01 第十次定向复核（作者第十轮修订后）

## 1. 结论、角色与范围

- 日期：**2026-10-14（Asia/Shanghai）**；本机日期同日，时区 `CST / +0800`。
- 执行者：本会话 Codex，独立审阅角色，与作者第十轮修订角色分开；未另行派发模型。本会话在仓库内只新增本报告，不修改作者正文、来源记录、修订映射、登记、计划或历史报告，不提交 Git commit。
- 用户约定审阅配置：`gpt-6.1-sol / xhigh`。**仅记录用户约定，不写成已独立确认的执行元数据。** 本轮未取得可独立核验的实际模型标识或 reasoning 配置，不以模型自述充当确认。
- 范围仅为 **B21-C31–C34**；优先级沿用[初审](batch-21-t05-01-codex-review.md) §6。剩余关闭条件以[第九次定向复核](batch-21-t05-01-codex-recheck-9.md) L77、L88、L100、L113 为权威；[第十轮修订映射](batch-21-review-fixes.md) L193–199 只定位落盘改动，不作为关闭证明。
- **结论：0 CLOSED / 4 OPEN（1 P1、3 P2）；第十次定向复核不通过。** C31、C32、C33 各 P2，C34 为 P1。不新增发现 ID、不调整优先级；C30 保持此前 CLOSED、范围外，不重开、不计入本轮分母；既有五项汇总为 1 CLOSED / 4 OPEN。
- 认可 v3 分区纠错、RuntimeClass→handler 关联、仅 major 旧说法删除、Ascend 条件解串和部分门槛/主体/安全设计的进展；已满足子条件不重新判为全部缺失。明确写 unknown 是必要的诚实边界，但不等于已经交付前次要求的固定方法。
- 未执行镜像构建/拉取、SBOM 生成/比对、签名/验签、配置变更、容器启动、设备访问、隔离/负向试验或 GPU/NPU 实测。知识库结构检查和 catalog 生成不属于这些实测，也不建立版本支持交集或硬件验证结论。

## 2. 输入身份、位置与并发边界

起始读取时，用户给出的 **5 个 SHA-256 前缀全部匹配**；另为前次报告、初审和验收计划记录完整摘要。下表为起始输入版本。正文和作者记录的行号均按该版本；上游源码区间采用 GitHub 只读连接器的原文件坐标，不把网页归一化行号拼成 GitHub 锚点。

| 输入 | 完整 SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md) | `87600cb56b19a77f08d2a1602d12511b38b7b84d9bb27e951af8856475e4db30` |
| [作者来源记录](batch-21-t05-01-sources.md) | `08fb1004e25804af6d85ae37b37399b89a39d029924d8da5c5896b4cdc8d0cbf` |
| [修订映射](batch-21-review-fixes.md)，本轮只取 L193–199 | `71af5e2aacd17c6dbc13857cfdefecc2ee07592080d52095f33ec1c166914bd0` |
| [第九次定向复核](batch-21-t05-01-codex-recheck-9.md) | `c050eb8de58fc18cd6abe9f51aacb4e756bab3b6d7cd24dcde839c04e8ce0d21` |
| [初审](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` |
| [任务验收计划](../../plans/full-coverage-backlog.yaml)，T05-01 L5386–5418 | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml)，438 项 | `da4af1f7d49eb46273b526791eda5e846e42f6a4dbc8380fe1e2f8d759cdba96` |

另读 README、编写指南、内容总目录、元数据 schema，以及关联 Ascend 案例/实验的环境缺项、授权和未执行边界。本轮不重新审计 C30 的供应链内容，也不重新验收关联案例的远程事件史。

写报告前发现并发变化：完整映射变为 `9618c55c6d70a6019d0c106fdc6d961cde13a29cdea09191302fd527dab4e1f5`，完整登记变为 `54197389a41fa9d4325dc87d175990d864f581c8af3b9da878e8118956e5d846`，登记仍为 438 项。重新读取确认本轮映射 L193–199 原文未变，变动后的映射新增的是 T05-03 第二轮修订节；本轮相关插件/common/runtime 登记 L5237–5258、L5325–5335、L5419–5429 与起始读取内容一致。正文、作者记录、前次/初审和计划摘要保持输入值。不会把后读完整文件摘要冒称用户原输入摘要，也不回滚并发编辑。

## 3. 一次源抽查、方法与限制

### 3.1 实际 curl 请求

本机 curl **8.7.1**。对下表 01–14 的精确 URL 逐个执行只读 GET；`--disable` 禁用用户 curl 配置，保持默认 TLS 校验。未使用 `-k`、替换证书、修改 DNS、提权或绕过沙箱。调用形态：

```bash
curl --disable --location --silent --show-error --connect-timeout 8 --max-time 20 \
  --output "$audit_dir/$name.body" --write-out '%{http_code}' "$url"
```

**14/14 均退出码 6、HTTP `000`、`Could not resolve host`。** curl 没有取得响应正文，TLS 握手未发生；不声称 curl 成功、HTTP 200 或本机验证了远端 TLS 链。精确请求清单/诊断保留在 `/private/tmp/b21-t05-01-recheck-10.v3LNSi/`，不加入知识库。

### 3.2 允许的只读替代通道与文字核对

使用 `web.run` 阅读精确版本页面正文，使用 GitHub 只读连接器读取固定 ref 原文件区间；**核对实际文字/控制流，不只判可达性**。网页通道提供的缓存/归一化文本不等于本机即时 GET，不作“最新版本”确认。未读 API 常量声明、必要 hook 可执行文件、库挂载/白名单和完整 dcmi 实现继续 unknown；审阅者取证不冒充作者已交付的方法。

| curl 点 / 精确一次源 | 替代通道实际核对范围及用途 |
|---|---|
| 01 / [containerd config@v2.4.1](https://raw.githubusercontent.com/containerd/containerd/v2.4.1/docs/cri/config.md) | 网页正文及 GitHub L22–149、L215–341：v3 独立 images/runtime 插件、runc handler/runtime_type/options、CDI 目录、RuntimeClass 和 kubelet 条件；网页另读 v2 自动转换。用于 C31/C34，不确认现场配置生效。 |
| 02 / [runc state.go@v1.5.2](https://raw.githubusercontent.com/opencontainers/runc/v1.5.2/state.go) | GitHub 完整文件：状态对象构造、stopped 时 PID 置零。用于 C31。 |
| 03 / [runc list.go@v1.5.2](https://raw.githubusercontent.com/opencontainers/runc/v1.5.2/list.go) | GitHub L1–82：JSON 字段与 `--root` 查询作用域。用于 C31，不把 init PID 等同任意工作负载进程。 |
| 04 / [NVIDIA server.go@v0.20.1](https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.20.1/internal/plugin/server.go) | GitHub L280–481：Allocate 校验 DevicesIds、UUID/index 转换去重、qualified 名、附加 CDI 设备与 CdiDevices 写入。用于 C32，不构成框架 ordinal 映射。 |
| 05 / [CDI SPEC@cb98bcf6](https://raw.githubusercontent.com/cncf-tags/container-device-interface/cb98bcf66dc68530012483bd56e33e14d815e167/SPEC.md) | GitHub L90–265：kind/name、全局/设备级 edits 应用条件、deviceNodes/mounts/env。用于 C32。 |
| 06 / [OCI Linux config@92249139](https://raw.githubusercontent.com/opencontainers/runtime-spec/92249139eea7161e13745abd4cb6d0ea02a3227a/config-linux.md) | GitHub L127–151、L402–418：节点身份/属主与按顺序应用的访问规则分开。用于 C32/C34。 |
| 07 / [Ascend common.go@44385c13](https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go) | GitHub L90–150：ID 逗号串、options、310B allow-link、限 `!PresetVDevice` 的 worker 环境组。用于 C33；未追查完整常量/API 定义。 |
| 08 / [Ascend plugin.go@44385c13](https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go) | GitHub L1087–1185：DeviceSpec 的 HostPath/ContainerPath/rw、默认与 UB 设备、UseAscendDocker 两分支。用于 C33；非完整 Allocate 审计。 |
| 09 / [Ascend process.go@44385c13](https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go) | GitHub L243–812、L850–910：LD_LIBRARY_PATH 与实际挂载分开、VIRTUAL 提前返回/CreateVDevice 后续条件、节点/cgroup、manager/UB、poststop、空设备集与独立 env/DP-mount 分支、create 入口。用于 C33。 |
| 10 / [Ascend runtime README@44385c13](https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/README.md) | GitHub 文件的设计简介：prestart、设备 cgroup、Host CANN 库挂载职责；简介不替代 hook/白名单实现。用于 C33。 |
| 11 / [Toolkit 1.20.0 troubleshooting](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html) | 网页正文 NVML/SELinux、hook/legacy Unknown Error、Affected Environments、Mitigations：显式 CPU/内存更新、systemd 条件、删除重建建议、runc/设备链接与 CDI 条件。用于 C34，未执行任何处置。 |
| 12 / [NVIDIA README@v0.20.1](https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.20.1/README.md) | 网页 Shared Access/With CUDA Time-Slicing，GitHub L345–455、L490–590：replicas 是所选资源共享访问数，time-slicing 不提供相应工作负载隔离。用于 C34。 |
| 13 / [syft README@v1.54.1](https://raw.githubusercontent.com/anchore/syft/v1.54.1/README.md) | GitHub 文件 Features/基础示例/输出格式：不由 README 推定逐库来源层字段完整存在或已选定层匹配方法。用于 C32，不重开 C30。 |
| 14 / [PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html) | 网页正文的 CUDA_VISIBLE_DEVICES 段只支持可用 GPU 范围管理，所引段未交付逐 ordinal→UUID 规则。用于 C32，不声称框架不存在其他身份接口。 |

原文件 blob 核对：containerd config `3a206263f4f9e76b6ca14110461b8661a03b1619`；runc state/list `b645e5ab62b682efc26b805e977199cbbc3124a3` / `3bfd6b831531212ebe448bd962f3bf7bd9982b7f`；NVIDIA server/README `9281b48ef52f9eda9cbed6d98491729da85b5a75` / `44594d4343967a313ff268223c8f638de005062c`；CDI SPEC `2bc480a20ce447f5281b5d6844a486a81bb635b0`；OCI Linux `c71757494ca743fd90692c25e4897bf74cf00388`；Ascend common/plugin `6cd038e9f1d67a8a913aa4bb1301692f177b3dbe` / `b7692611b12884854d973fa2a3da18e381353f10`；runtime process/README `acbd7a1ec0703498abfcfcb6ce1aa493069091b1` / `f612ad6b5d2edcf65d9ad683d57a4f1a4e1f9088`；syft README `9ffd2affa3b00031ea1fd01ee3fe228379978492`。blob 不是 commit、现场配置或实验结果。

## 4. 逐项判断与剩余关闭条件

### B21-C31 — P2 / OPEN

**权威条件：** 第九次复核 L77。**本轮位置：** 正文 L64、L144；作者记录 L10、L26–28；映射 L195；登记 L5248–5258、L5314–5324。

- **事实纠错与关联已满足：** L64 不再把 v3 images/runtime 塞入 grpc.v1.cri 表，不再写 `containerd_runtimes`；独立插件及 `.containerd.runtimes.<handler>` 主干与抽查 01 一致。新增 RuntimeClass 名→handler 关联，保留默认/显式选择、v2 自动转换、证据缺失不能判失效及 runc stopped-PID 边界；这些不再作为未修正问题。
- **完整键/参考值清单仍未交付：** L64 有完整路径骨架和部分字段，但 `runtime_type`、`SystemdCgroup` 仍是名称/待填写指令，没有组成所选模式逐项“完整键｜来源条件/参考值｜实际值或 unknown｜证据”的记录清单。抽查 01 的 [Cgroup Driver / Runtime classes / Full configuration](https://github.com/containerd/containerd/blob/v2.4.1/docs/cri/config.md) 已给出 runc 的 runtime_type、默认 handler 和条件化 SystemdCgroup 示例；不能因为未取现场值，把方法/参考值也交给读者补。L144 仍整体列“handler/options 完整键”unknown，与 L64 的已补范围未协调。
- **状态实现的作者引用仍欠直接定位：** L64 只是文本提及同 tag `state.go`/`list.go`，实际链接仍为手册；作者记录 L26 也只链接手册。审阅者抽查 02–03 已独立核对代码，但不替作者完成前次要求的状态实现直接引用。

**剩余关闭条件：** 保留已正确的 v3 分区、转换/选择、RuntimeClass 关联和两档证据判据；将所选 images/runtime、CDI 目录、默认 handler、runtime_type、`plugins."io.containerd.cri.v1.runtime".containerd.runtimes.<handler>.options.SystemdCgroup` 等完整键及来源限定的参考值/条件逐项落为记录格式，实际值可 unknown。补状态实现可直接定位的同 ref 引用，并协调 L144/作者记录的已读范围。**不要求配置修改、现场输出或整栈兼容证明。**

### B21-C32 — P2 / OPEN

**权威条件：** 第九次复核 L88。**本轮位置：** 正文 L68–82、L108–110；作者记录 L11、L24–25；映射 L196；登记 L5226–5236、L5281–5302。

- **旧错误删除与 unknown 边界已满足：** L76 已删除仅“主设备号”旧法，明确完整节点身份、仅 major/数量/编号不足、缺规则进入无法确定。server.go 引用、kind+name、两级 edits、节点与许可分离、挂载/env 落位、宿主注入追溯格式继续满足；抽查 04–06 与这些主干一致。
- **稳定身份方法仍明确未交付：** L76 自述“稳定物理标识映射方法（未交付，unknown）”，L80–82 仍为空表；这不是已固定方法但现场 UUID 待采集。所引 [CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html) 可见集段并不补出 ordinal→稳定身份；Allocate/CDI 主干也不能单独替代这一段。L82 判定栏仍为“一致/待查”，须与缺规则时“无法确定”的记录要求协调。
- **镜像内库/来源层方法未新增依据：** L70 仍是“所选扫描配置 SBOM 输出……以实际输出为准”，没有选定扫描范围、输出字段与路径/成分→层的匹配依据。抽查 13 的 [syft README@v1.54.1](https://github.com/anchore/syft/blob/v1.54.1/README.md) 只交付工具/格式入口；层清单、diff_ids、annotations 与注入来源箭头不能自行证明逐库归属。L110 增加字段不等于取得该方法。

**剩余关闭条件：** 不恢复仅 major 旧法，保留已补 CDI/权限和宿主注入字段；选择有固定依据的扫描范围、成分/路径输出字段及层匹配规则，分别关联镜像内成分与宿主注入来源/最终挂载/目标对象。交付固定框架/设备身份材料支持的逐 ordinal→分配/CDI→完整节点→稳定身份规则，并把方法缺失/现场值缺失各自的“无法确定”记录同步到核对表和 C34。**现场值可 unknown；不要求拉取镜像、生成 SBOM、采集设备或负向试验，不重开 C30。**

### B21-C33 — P2 / OPEN

**权威条件：** 第九次复核 L100。**本轮位置：** 正文 L29、L40、L88–90、L144；作者记录 L12、L17；映射 L197、L199；登记 L5237–5247、L5325–5335、L5419–5429。

- **条件链纠错已满足：** L88 现把 VIRTUAL 提前返回与后续 CreateVDevice/VdeviceID 条件分开；空/void 只 gate 作业设备/hook 分支，不再泛称没有任何挂载；env、LD_LIBRARY_PATH、DP-mounts 独立处理。与抽查 09 的 [process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go) L243–410、L600–812、L850–910 一致。LD_LIBRARY_PATH 改 env 不等于实际库挂载的限定保留。
- **已读/未读主张表同步满足：** 作者记录 L12/L17 已明确 README/process 的局部已读与实际库挂载/白名单/hook/dcmi 未读；插件登记 L5247 和 common 登记 L5335 也同步了静态输出范围。**不再将 common 或 runtime 入口整体称为未取源，也不把当前同步判为仍欠缺。** 支持交集 unknown、GPU 不套用 NPU、digest 非兼容证明继续满足。
- **选定分支/逐字段对应及必要实现仍未交付：** L88 的“api 实际键/所选产品/manager/UB 条件与最终节点/许可逐字段关联（缺则 unknown）”仍是待办，不是已选产品/运行路径的字段表。抽查 07–09 能核对静态输出、两路径、节点/cgroup 和产品条件，但正文未落实实际键/ID/options→所选条件→完整节点/许可/env；L90 只选 commit，不等于选定该实现内的分支。
- **必要 hook/实际库挂载仍明确未取：** L88 和作者记录均承认库来源/目标/白名单及 hook 可执行实现未取；抽查 10 的 [runtime README 设计简介](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/README.md) 只能指明职责，不能替代所选路径所需实现。诚实记录缺项可防止误用，但不能关闭前次要求的必要消费实现；未选虚拟分支可以排除，不要求完整 dcmi 审计。

**剩余关闭条件：** 保留已正确的控制流和已读范围同步；明确一个实际选定的产品/插件/runtime 分支，落下插件实际键、ID/options、产品/manager/UB 条件到最终完整节点、许可与环境的对应表。补所选路径必需的 hook、实际库来源/目标/白名单证据；虚拟/poststop 写出条件或明确排除未选分支，并同步局部已读/未读范围。**支持交集、现场值及未选分支可 unknown；不要求安装、试运行、完整 dcmi 审计或实测。**

### B21-C34 — P1 / OPEN

**权威条件：** 第九次复核 L113。**本轮位置：** 正文 L96–123、L125–139；作者记录 L13；映射 L198。

- **已补内容认可：** L121–123 现均有 NPU 语义缺失优先进入无法确定的门槛，L120 继续保留；L130 改用 runtimeClassName→handler，并说明 cdi_spec_dirs 只是目录而非模式开关；L132 已改名“副本计数对照”，明确改变 replicas 不等于禁用共享，与抽查 12 的 [With CUDA Time-Slicing](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/README.md#with-cuda-time-slicing) 一致。L131 新增进程/节点身份漂移，L132/L134 增加目标进程/节点/时间字段；清单、集合差异、授权/旁路排除、访问/负向恢复、案例摘要和未执行边界继续满足。
- **门槛仍未覆盖通用 NPU 注入入口：** L116 继续把 NPU ascend-docker/原生挂载纳入通用“设备注入缺失”，却仍直接允许三单一致判完成/三单齐映射错判失败，只把缺模式作为先定模式条件，未引用 L120 的固定映射语义优先门槛。新增专门行不能防止读者从该通用行绕过门槛；不否定直接观测或明确 DAC/LSM 事件。
- **唯一差异的具体选择仍欠缺：** L130 已有有效的 Pod 字段，但尚未给两个所选 handler 的固定配置为何对应 CDI/非 CDI 模式；L131 仍是“某一节点规则”的 allow，没有规则选择/完整键及顺序保持格式；L132 未固定 resources 项/资源名；L133 仍是 digest 或驱动版本二选一且键待填；L134 仍只称“CPU 限制字段”，未选择实际接口/字段。旧新现场值可以待填，唯一对象/完整键/比较格式不能全部待填；映射 L198 的“逐完整键”不能代替这些正文缺项。
- **关共享分支与对照解释仍未闭环：** L118 仍以“关共享后影响消失”判该分支完成，而唯一共享对照 L132 已正确限定为副本计数。L123 又称“关共享另立变体，见对照表”，但 L129–135 没有该变体。须提供有依据的关共享对照，或将该分支的对照/完成解释一致收窄；NPU 方案也不能借 NVIDIA replicas 字段替代其未取源实现。这属于原 C34 的共享解释/平台分工条件，不新增 ID。
- **主体、停止/恢复和生命周期关联仍不完整：** L130 停止集合仍缺进程/节点身份漂移；L131 已补，但其他变体的多个“同上”未形成明确的命名停止/恢复集合。L133 仍用“同上”继承 L132 的同 Pod/容器前后，未分别选择镜像回退/驱动回退及其生命周期；L134/L135 虽提更新与重建不同，仍未定义恢复后目标主体的关联，不能要求重建后原 PID 不变。各变体还需关联访问与原负向边界恢复的证据对象，而非只有注入集/影响记录。
- **方法依赖仍未完成：** C32 的固定稳定身份规则未交付，清单 L108/L110 与三单名称不能自行证明映射一致。抽查 11 的 [Affected Environments / Mitigations](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html#containers-losing-access-to-gpus-with-error-failed-to-initialize-nvml-unknown-error) 已限定 hook/legacy、CPU/内存显式更新及 systemd 等条件；正文沿用该类别是进展，仍须细化所选更新对象与观察/恢复格式，不推广为所有 CDI/运行时的统一故障原因。

**剩余关闭条件：** 保留已满足的 NPU 专门行门槛、副本计数纠偏、清单与授权安全边界；使 L116 等全部 NPU 依赖入口遵循固定语义缺失优先门槛。各变体选定有来源支持的完整键/规则选择、唯一差异及旧新比较格式，闭环关共享分支与实际对照。逐变体或通过明确命名的公共集合，关联前后 Pod/容器/目标进程、节点/时间窗、漂移停止、访问/原负向边界恢复证据；区分资源更新、回退、重建与恢复后的目标主体关联。引用 C32 已固定方法，未取得时进入无法确定。**不要求执行试验、填现场值或制造结果。**

## 5. Acceptance 与最终计数

| 计划位置 / acceptance | 本轮判断 | 原 ID |
|---|---|---|
| L5403 / 镜像身份、构建输入、SBOM/签名、拉取方法与限制 | 沿用前次已关闭结论，不重新验收；不等于已执行供应链验证 | C30 CLOSED，范围外 |
| L5404 / 固定 runtime/Toolkit/CDI、各层与映射分离 | 部分满足，未完整通过：配置清单/参考值及状态直接引用欠缺；库层匹配和稳定映射方法未交付 | C31、C32 OPEN |
| L5405 / Ascend runtime/plugin 独立实现与目标组合 | 部分满足，未完整通过：条件纠错/范围同步已满足，选定字段和必要 hook/库挂载未闭环 | C33 OPEN |
| L5406 / 清单、异常/隔离分支、对照与案例，不作安装处方 | 部分满足，未完整通过：通用 NPU 入口门槛、具体对象、关共享解释及主体/安全恢复关联欠缺 | C34 OPEN |

四条 acceptance 汇总：**1 沿用既有完整通过 / 3 未完整通过**。本轮范围：**0 CLOSED / 4 OPEN（1 P1、3 P2）；第十次定向复核不通过。** 原因是第九次剩余关闭条件仍有实质缺项，不是 curl DNS 失败、未实测或要求建立整栈兼容。修订映射列“处理”与 unknown 披露均不自动等于发现 CLOSED。

## 6. 结构校验与单文件边界

- 写入前原仓库 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS：96 content entries / 438 sources**；只验证结构和本地链接，不验证技术正确性或远程内容。
- 写入后原仓库 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS：96 content entries / 438 sources**。临时副本 `/private/tmp/b21-t05-01-recheck-10.v3LNSi/validation/` 使用原仓库虚拟环境 Python、禁写字节码执行 `make check` / `make build`，均 **PASS：96 content entries / 438 sources**；只在副本重建 catalog，未在原仓库运行构建、未构建镜像。
- 写报告前的摘要审计已观察到六个既有文件并发变化：`build/catalog.json`、`docs/research/batch-21-review-fixes.md`、`docs/research/batch-22-t05-03-claude-recheck.md`、`docs/research/batch-22-t05-03-sources.md`、`knowledge/05-cluster-platform/slurm-jobs-and-device-resources.md`、`sources/registry.yaml`。这些不是本会话编辑，不回滚，不声称所有既有文件或原 build 相对起始快照不变。
- 起始摘要清单纳入 **390 个**既有 Git 所列 tracked/untracked 非忽略文件及 build 文件。验证后既有文件变动仍为上述六项；新增文件除本报告外，另观察到并发新增 `docs/research/batch-22-t05-03-claude-recheck-2.md`，不是本会话写入。正文、作者记录、前次/初审和计划的摘要保持输入值；完整映射/登记为 §2 披露的后读版本。本会话的仓库写操作仅针对本报告。
- 报告四项 ID/优先级/状态、全部本地 Markdown 链接和行尾空白独立核对：**PASS**。未修改 src/kb/，不需要 make test、不新增测试；无新增发现 ID、无实测。结构检查不改变技术结论。

**最终技术结论：C31–C34 均 OPEN，0 CLOSED / 4 OPEN，第十次定向复核不通过。C30 保持此前 CLOSED、范围外；不将用户约定模型配置写成已核验执行元数据。**
