# Batch 21 补交 T05-01 第九次定向复核（作者第九轮修订后）

## 1. 结论、角色与范围

- 日期：**2026-10-14（Asia/Shanghai）**；本机日期同日，时区 `CST / +0800`。
- 执行者：本会话 Codex，独立审阅角色，与作者第九轮修订角色分开；未另行派发模型。本会话在仓库内只新增本报告，不修改作者正文、来源记录、修订映射、来源登记、计划或历史报告，不提交 Git commit。
- 用户约定审阅配置：`gpt-6.1-sol / xhigh`。**仅记录用户约定，不写成已独立确认的执行元数据。** 本轮未取得可独立核验的实际模型标识或 reasoning 配置，不以模型自述充当确认。
- 范围仅为 **B21-C31–C34**；优先级沿用初审。剩余关闭条件以[第八次定向复核](batch-21-t05-01-codex-recheck-8.md) L78、L89、L101、L114 为权威；结合[初审](batch-21-t05-01-codex-review.md) §6、[任务验收](../../plans/full-coverage-backlog.yaml) L5403–5406。[第九轮修订映射](batch-21-review-fixes.md) L173–178 只定位落盘改动，不作为关闭证明。
- **结论：0 CLOSED / 4 OPEN；第九次定向复核不通过。** C31、C32、C33 各 P2，C34 为 P1；不新增发现 ID、不调整优先级。C30 保持此前 CLOSED、范围外，不重开、不计入本轮分母；既有五项汇总为 1 CLOSED / 4 OPEN。
- 认可配置证据缺失判据、runc 状态字段、CDI 匹配与最终对象区分、server.go 引用同步、LD_LIBRARY_PATH 对象纠偏、清单关联行、NPU 注入缺失门槛和部分安全停止/恢复设计的进展，不把已补子条件重新判为全部缺失。新增错误或不足均追记原 ID。
- 未执行镜像构建/拉取、SBOM 生成/比对、签名/验签、配置修改、容器启动、设备访问、隔离/负向试验或 GPU/NPU 实测。知识库结构检查与清单生成不是上述实测，也不建立版本支持交集或硬件验证结论。

## 2. 输入身份、位置与并发边界

起始读取时，用户给出的 **5 个 SHA-256 前缀全部匹配**；另为前次报告、初审和验收计划记录完整摘要。下表是本轮输入版本，本地位置采用该版本文件行号；上游源码区间采用 GitHub 只读连接器的原文件坐标，不把网页归一化行号拼成 GitHub 锚点。

| 输入 | 完整 SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md) | `7aea1df9104e14de6fa3bb16e53deefa5675a9a6474e4382c1013ba24a579d29` |
| [作者来源记录](batch-21-t05-01-sources.md) | `5424feab569a4b28a8e9da506624e00e85496eb324e0fb12c72e649bfea483d4` |
| [修订映射](batch-21-review-fixes.md)，只取第九轮 L173–178 | `254a982001d54c0169b519c0e1d051ba30875c3ae49224d7aae679bb4b46dc07` |
| [第八次定向复核](batch-21-t05-01-codex-recheck-8.md) | `2d3ff1932e29f568f127a0fb192426bb6853611076ff11c7d4f83086063b977e` |
| [初审](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` |
| [任务验收计划](../../plans/full-coverage-backlog.yaml)，T05-01 L5386–5418 | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml) | `65ad00a31f02f4fbf4c678b792c981f2b855166a4882641304f2294bc5cf4a6e` |

另读 README、编写指南、内容总目录和元数据 schema；读取[Ascend 来源案例](../../knowledge/05-cluster-platform/ascend-device-visibility-source-case.md)的症状/环境/缺项，并定位[关联实验](../../knowledge/05-cluster-platform/ascend-device-visibility-experiment.md)的前提、旁路、停止及判据章节；关联页不重新验收。起始登记实计 **438 项**；作者历史 `curl 200` 只作作者记录，不冒充本轮请求结果或历史执行的独立确认。

**并发边界：** 写报告前再次计算摘要，完整映射变为 `4827cc5c02b2ddb6b72c136b60198221f1c12fe95b4dd02cdfb83e2c2e17a63e`（追加 T05-03 首轮修订节），登记变为 `3a3d536d1773c8f706db4442984577b1ef54d5411ad4965bb09ab449594d0420`。再次定向读取确认 T05-01 第九轮 L173–178、NVIDIA Plugin 精确实现位置、containerd/CDI、Ascend plugin/common/runtime 对应登记内容保留；其余五个输入完整摘要不变。本报告结论针对上表输入及本次未变的 T05-01 正文，不宣告后来的完整映射/登记版本已获同等复核，不覆盖或回滚并发修订。

## 3. 一次源抽查、方法与限制

### 3.1 实际 curl 请求

本机 curl **8.7.1**。对下表 01–14 的精确 URL 逐个执行只读 GET；`--disable` 禁用用户 curl 配置，保持默认 TLS 校验，未用 `-k`、替换证书、修改 DNS、提权或绕过沙箱。调用形态为：

```bash
curl --disable --location --silent --show-error --connect-timeout 8 --max-time 20 \
  --output "$audit_dir/$name.body" --write-out '%{http_code}' "$url"
```

**14/14 均退出码 6、HTTP `000`、`Could not resolve host`。** 没有取得 curl 响应正文，TLS 握手未发生；不声称 curl 成功、HTTP 200 或本机验证了远端 TLS 链。请求清单和诊断留在临时目录 `/private/tmp/b21-t05-01-recheck-9.qQZDHE/`，不加入知识库。

### 3.2 允许的只读替代通道与文字核对

使用 `web.run` 阅读精确版本页面正文，并用 GitHub 只读连接器读取固定 ref 原文件区间。**实际核对文字/代码，不只判断可达性。** CDI raw URL 在网页通道返回 Internal Error，改用 GitHub 同 commit 的 SPEC.md；不把该错误当作规范不存在。网页通道的缓存/归一化文本不等于本机即时 GET，不作“最新版本”确认；其他未读实现继续 unknown。

| curl 点 / 精确一次源 | 实际读取与核对范围 |
|---|---|
| 01 / [containerd config@v2.4.1](https://raw.githubusercontent.com/containerd/containerd/v2.4.1/docs/cri/config.md) | 网页正文及 GitHub L22–147、L215–320：v3 images/runtime 插件 ID、default_runtime_name、runtimes/options/SystemdCgroup、CDI 目录与 kubelet 条件；网页另核对 v2 自动转换。用于 C31/C34；不确认现场配置生效。 |
| 02 / [runc state.go@v1.5.2](https://raw.githubusercontent.com/opencontainers/runc/v1.5.2/state.go) | GitHub 完整文件：状态查询/输出构造、stopped 时 PID 置零。用于 C31。 |
| 03 / [runc list.go@v1.5.2](https://raw.githubusercontent.com/opencontainers/runc/v1.5.2/list.go) | GitHub L1–82：containerState 的 JSON 字段、list 的 root 作用域。用于 C31；不把 init PID 等同任意目标工作负载进程。 |
| 04 / [NVIDIA server.go@v0.20.1](https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.20.1/internal/plugin/server.go) | GitHub L280–438、L448–481：Allocate 读取/校验 DevicesIds，UUID/index 转换去重，qualified 名与附加 CDI 设备，CdiDevices 写入。用于 C32；不是框架 ordinal 映射。 |
| 05 / [CDI SPEC@cb98bcf6](https://raw.githubusercontent.com/cncf-tags/container-device-interface/cb98bcf66dc68530012483bd56e33e14d815e167/SPEC.md) | GitHub L90–265：kind/name、两级 edits 的应用条件、deviceNodes 的 hostPath/path/权限、mounts 与 env 字段。用于 C32。 |
| 06 / [OCI Linux config@92249139](https://raw.githubusercontent.com/opencontainers/runtime-spec/92249139eea7161e13745abd4cb6d0ea02a3227a/config-linux.md) | GitHub L127–151、L402–418：节点身份/属主和按顺序应用的访问规则分开；major 不是完整身份。用于 C32/C34。 |
| 07 / [Ascend common.go@44385c13](https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go) | GitHub L90–150：ID 逗号串、options、310B allow-link、限 !PresetVDevice 的 worker 环境组。未追查全部常量声明/api 包。用于 C33。 |
| 08 / [Ascend plugin.go@44385c13](https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go) | GitHub L1087–1185：HostPath/ContainerPath/rw、默认与 UB 节点、UseAscendDocker 两分支。用于 C33；不审计完整 Allocate。 |
| 09 / [Ascend process.go@44385c13](https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go) | GitHub L243–410、L411–600、L600–780、L850–910：LD_LIBRARY_PATH 与 Mounts 分开、VIRTUAL 提前返回、非 VIRTUAL 的 CreateVDevice 返回条件、完整节点/cgroup、manager/UB、空设备集与独立 env/mount 分支、create 入口。未读 hook 可执行文件、白名单与完整 dcmi 实现。用于 C33。 |
| 10 / [Ascend runtime README@44385c13](https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/README.md) | GitHub 文件：设计简介的 prestart、设备 cgroup、Host CANN 库挂载职责；简介不能替代必要 hook/白名单实现。用于 C33。 |
| 11 / [Toolkit 1.20.0 troubleshooting](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html) | 网页正文的 NVML/SELinux、hook/legacy Unknown Error、Affected Environments 与缓解段：资源更新包含 CPU/内存限制；SELinux label 禁用削弱隔离；恢复仍须本设计证据。用于 C34；未执行页面任何修改建议。 |
| 12 / [NVIDIA README@v0.20.1](https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.20.1/README.md) | GitHub L310–480、L490–590：CDI 传递/engine 条件、UUID/index、time-slicing 不提供工作负载隔离、replicas 是资源共享访问计数。用于 C32/C34。 |
| 13 / [syft README@v1.54.1](https://raw.githubusercontent.com/anchore/syft/v1.54.1/README.md) | GitHub 文件：Features/基础使用/输出格式；未由 README 推定全部成分都带来源层或具体层匹配规则。用于 C32，不重开 C30。 |
| 14 / [PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html) | 网页正文的 CUDA_VISIBLE_DEVICES 可用设备范围说明；该引用段不交付逐 ordinal→UUID 方法，不声称框架不存在其他接口。用于 C32。 |

关键原文件 blob：containerd config `3a206263f4f9e76b6ca14110461b8661a03b1619`；runc state/list `b645e5ab62b682efc26b805e977199cbbc3124a3` / `3bfd6b831531212ebe448bd962f3bf7bd9982b7f`；NVIDIA server/README `9281b48ef52f9eda9cbed6d98491729da85b5a75` / `44594d4343967a313ff268223c8f638de005062c`；CDI SPEC `2bc480a20ce447f5281b5d6844a486a81bb635b0`；OCI Linux `c71757494ca743fd90692c25e4897bf74cf00388`；Ascend plugin/common `b7692611b12884854d973fa2a3da18e381353f10` / `6cd038e9f1d67a8a913aa4bb1301692f177b3dbe`；runtime README/process `f612ad6b5d2edcf65d9ad683d57a4f1a4e1f9088` / `acbd7a1ec0703498abfcfcb6ce1aa493069091b1`；syft README `9ffd2affa3b00031ea1fd01ee3fe228379978492`。blob 不是 commit、现场对象或实验结果。审阅者补读仅为本报告证据，不改来源登记，不冒充作者已交付方法。

## 4. 逐项判断与剩余关闭条件

### B21-C31 — P2 / OPEN

**权威条件：** 第八次复核 L78。**本轮位置：** 正文 L64、L144；作者记录 L10、L27–28；映射 L175；登记 L5248–5258、L5314–5324。

- **已补部分满足：** 正文 L64 给出配置来源/摘要→daemon/CRI endpoint→Pod/handler→容器→有效对象的关联骨架，区分“实际生效对象冲突”与“未采到对象/日志”；不再从证据缺失直接判未加载。runc 的八个列举字段、stopped PID 为零及容器/bundle/日志/时间窗关联与抽查 02–03 主干一致，不因映射称“七字段”而另开问题。
- **按 C31 追记新事实错误：v3 分区写错。** L64 把所选 `version = 3` 的完整键写成 `[plugins."io.containerd.grpc.v1.cri"]` 下 `images`/`containerd_runtimes` 分区。抽查 01 的 [Cgroup Driver/Runtime classes](https://github.com/containerd/containerd/blob/v2.4.1/docs/cri/config.md#basic-configuration) 和 [Full configuration](https://github.com/containerd/containerd/blob/v2.4.1/docs/cri/config.md#full-configuration) 明确采用独立的 `io.containerd.cri.v1.images` 与 `io.containerd.cri.v1.runtime` 插件；运行时表是后者的 `.containerd.runtimes.<handler>`，不是所写 `containerd_runtimes`。v3 的 grpc.v1.cri 表仍有 streaming/server 配置，不能据它仍存在，把 images/runtime 放回该表。此错误属于本项配置模式/字段关闭条件，不新增 ID。
- **完整字段与条件化参考值仍未落地：** L64 仍只有“default/所选 handler 名、runtime_type、options 含 SystemdCgroup”及“逐项填写”的指令，缺所选模式的完整键与参考值清单；L144 又将 handler/options 完整键整体 unknown。来源已有 `default_runtime_name`、runc runtime_type、CDI 默认目录和 systemd/kubelet 条件，缺现场值不应把这些方法也交给读者补。Pod 的 runtimeClassName 还须关联 RuntimeClass 的 handler，不能只把名称当 handler。

**剩余关闭条件：** 修正上述 v3 事实错误；列清 images/runtime 插件及 `cdi_spec_dirs`、`containerd.default_runtime_name`、`containerd.runtimes.<handler>.runtime_type`、对应 options 的 `SystemdCgroup` 等完整键、条件化参考值与实际值/unknown 格式，并落实 RuntimeClass handler/默认路径关联。保留已补转换/显式选择、两档证据判据和 runc 状态方法；给状态实现可直接定位的引用，同步 L144/作者记录的已读范围。**不要求配置变更、现场输出或整栈兼容证明。**

### B21-C32 — P2 / OPEN

**权威条件：** 第八次复核 L89。**本轮位置：** 正文 L68–76、L80–82；作者记录 L11、L24–25；映射 L176；登记 L5226–5236、L5281–5302。

- **Allocate 引用同步满足：** 正文 L73、作者记录 L11、登记 L5231 均补 server.go 文件/区间；抽查 04 独立确认请求 ID 校验→按 UUID/index 策略转换去重→qualified 名→CdiDevices 的主干，不再判该引用缺失。插件附加 CDI 请求不必与作业 GPU 集一一相等，已有集合区分继续保留。
- **CDI/最终对象纠偏已有实质进展：** L73 补 kind+name 匹配、全局/设备级应用条件，明确 `linux.devices[]` 与 `linux.resources.devices[]` 不同，mount 的 host/container 路径落到 source/destination，env 落到 process.env；与抽查 05–06 的字段/应用规则主干一致。L75 和 L80–82 保留完整节点身份及可见性不证明访问的边界，不判这些子条件全缺。
- **库/层方法仍未固定：** L70 新增宿主来源→最终挂载→容器目标的追溯箭头，但仍只以“所选扫描配置 SBOM 输出、以实际输出为准”代替已固定的扫描范围、输出字段及路径/成分→层匹配依据。所引 NGC 层目录、diff_ids 和抽查 13 的 README 均不单独给出逐库归属规则；不是要求全部 cataloger 或真实 SBOM 结果，而是要求选择一条有依据的方法。已注入组件的追溯格式有进展，不能由此关闭镜像内成分归属缺口。
- **稳定身份方法仍未交付：** L76 仍明写“固定依据未取（框架 ordinal→UUID 方法 unknown）”，且保留“最终 OCI 节点主设备号”的旧方法叙述；L80–82 的完整节点列不能补出框架可见快照→分配 ID/CDI 名→节点→稳定身份的固定规则。抽查 14 的所引段只支持可用 GPU 范围管理。实际 UUID 可 unknown，与映射方法未取证是不同缺项。

**剩余关闭条件：** 保留已补 server.go 引用和 CDI 规则，补所选扫描范围/成分输出字段/层匹配的固定依据与记录规则；将宿主注入来源、最终挂载、目标对象与镜像内成分分别关联。用固定框架/设备身份材料交付逐 ordinal→分配/CDI→完整节点→稳定身份的方法，纠正 L76 的仅 major 旧说法，并给“无法确定”记录格式。**现场值可 unknown；不要求拉取、生成 SBOM、采集现场值或负向试验，不重开 C30。**

### B21-C33 — P2 / OPEN

**权威条件：** 第八次复核 L101。**本轮位置：** 正文 L29、L40、L88–90、L144；作者记录 L12、L17；映射 L177；登记 L5237–5247、L5325–5335、L5419–5429。

- **入口与 LD_LIBRARY_PATH 对象纠偏满足：** 同 commit runtime 入口继续固定；L88 现明确 addAscendLibraryPath 只改 process.env、不是实际库挂载，和抽查 09 的 L243–282 一致。插件两分支、common 静态输出、非空设备集才进入 addHook/addDevice 已有证据，不重判为全部未取源。
- **按 C33 追记条件链错误：** L88 写成“VIRTUAL→跳过创建走 vdevice 路径（VdeviceID!=-1 时改写设备列表/options＋poststop）”。[process.go L350–400](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go#L350-L400) 的 VIRTUAL 检查先提前返回；只有未提前返回才调用 CreateVDevice 并检查返回的 VdeviceID，二者不能串成 VIRTUAL 分支内的同一条件链。后续 [addDevice/环境更新 L600–780](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go#L600-L780) 支持 VIRTUAL 设备路径选择，但不改变前述控制流。
- **空/void 的边界须收窄：** L88“为空/void→不挂载”不能泛指所有 env/library/mount 处理。[processDevicesAndHooks L850–910](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go#L850-L910) 仅把 addHook/addDevice 放在设备集非空的条件内，随后仍有独立 env/library-path 处理与受条件控制的 addDPMountsToSpec。应说不进入该作业设备/hook 注入分支，并分别记录其他条件，不能把没有设备推成没有任何挂载。
- **字段/必要消费实现仍欠缺：** L88“api 实际键/所选产品/manager/UB 条件与最终节点/许可逐字段关联（缺则 unknown）”仍是待办，没有列出选定产品、键值和条件→最终 path/type/major/minor/allow/access/env 的对应。实际库来源/目标/白名单与必要 hook 消费仍明示未取；纠正 LD_LIBRARY_PATH 不等于补齐这些实现。可排除未选虚拟分支，不能省略所选路径必经实现。
- **已读范围同步仍不足：** 作者记录 L12/L17 仍整体称 runtime 消费端 unknown；登记 L5247 仍称 runtime 辅助函数语义未核对。正文/新 runtime 登记已承认 README/process 设备/env 改写已读，但主张表没有区分局部已读与库挂载/白名单/hook 未读。L90 的支持交集 unknown 及 GPU/NPU 分开、digest 非兼容证明继续满足。

**剩余关闭条件：** 修正 VIRTUAL 与 CreateVDevice 返回条件的串接、收窄空/void 边界；明确所选实际分支，列插件实际键/ID/options/产品/manager/UB 条件→runtime→完整节点、许可、环境的对应。补所选路径必要 hook/实际库挂载/白名单取证，说明虚拟/poststop 条件或明确排除未选分支；同步正文、作者主张表与相关登记的局部已读/未读范围。**支持交集、现场值和未选分支可 unknown；不要求安装、试运行、完整 dcmi 审计或实测。**

### B21-C34 — P1 / OPEN

**权威条件：** 第八次复核 L114。**本轮位置：** 正文 L96–123、L125–137；作者记录 L13；映射 L178。

- **清单与部分安全设计已补：** L105–110 增加实际 Allocate ID、config.json 对象/摘要、宿主注入库追溯、稳定身份行和镜像库字段；本清单不再只有概念表。L112 的公共/控制节点、作业获配设备、资源请求和框架逻辑集合边界保留。L130/L131 补未授权作业设备暴露/访问、旁路漂移、影响其他负载等停止触发及访问/原负向边界恢复，不再把三单可见性当权限恢复证明；L137 的案例摘要/缺项/非本库复现限定继续满足。
- **未知门槛尚未覆盖全部依赖分支：** L120 已让固定映射语义缺失优先进入无法确定，认可。L121/L122 却仍只说缺语义“不判完成”，并同时列技术失败；L123 在隔离语义未取源下仍可判完成/失败，缺同等优先门槛。L116 又把 NPU 模式纳入通用注入缺失行，未说明采用 L120 的门槛。所有依赖 NPU 固定语义的解释应先过门槛，不阻止记录直接观测，也不把明确 DAC/LSM 事件当成不存在。
- **单变量尚未固定为可核对的具体键：** L130 的“所选 runtime handler 的 CDI 使能项”不是具体键/已固定依据；抽查 01 只能证明 CDI 目录和 handler 配置职责，不能替正文证明这个占位项存在。L131 未选定 `linux.resources.devices[]` 中哪一节点规则的 allow，L132 未写完整 sharing.timeSlicing.resources 项/资源名，L134“CPU 限制”未选择限额接口/字段。L133 仍是 digest 或驱动版本二选一、键待填。缺现场旧新值可待填，但唯一变更对象/完整键及比较格式须交付，不能以同上或“一次一项”声明代替。
- **按 C34 追记对照解释限制：** L132 将“仅 replicas 变化”称为关共享。抽查 12 的 [CUDA Time-Slicing](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/README.md#with-cuda-time-slicing) 将该字段定义为所选资源的共享访问副本数；改变计数不自动构成禁用共享策略的证据。须选定确实代表关共享的配置差异，或改名为副本计数对照并限定可支持的解释；不得据一次影响消失证明其他隔离维度成立。
- **主体/时间窗及恢复边界还不完整：** L130/L131/L135 已有新建/重建的旧新 ID/PID/快照安排；L132“同负载开关前后”和 L133“同上”未落实 Pod/容器/目标进程与前后观察窗，L134 缺目标进程身份；资源更新与重建不能用同上混为一个生命周期。L130/L131 的通用停止集合还缺身份/节点漂移触发，各变体须关联回明确的停止/恢复集合及各自证据对象，重建后“同一目标进程”需解释为目标主体关联而非原 PID 必须不变。
- **清单列已补，不等于映射方法完成：** C32 的固定稳定身份规则仍欠缺；L108/L110 的表名不能自行支持三单“映射一致”。本项不再要求重复添加这些列，而是要求引用可用规则，并在规则未取得时进入无法确定。hook/legacy 资源更新类别和恢复非充分性保留，与抽查 11 范围一致。

**剩余关闭条件：** 保留已补清单/集合/授权/旁路/安全恢复及案例摘要，落实所有 NPU 依赖分支的语义缺失优先门槛；在每变体选定有固定依据的完整键、唯一差异及旧新比较格式，纠正 replicas 对照的名称/解释。按变体分别关联前后 Pod/容器/目标进程、节点和观察窗，增加身份/节点漂移等停止触发及访问/原负向边界恢复的证据要求；与 C32 的固定映射方法衔接，资源更新沿所选源条件细化。**不要求执行试验、填现场值或制造结果。**

## 5. Acceptance 与最终计数

| 计划位置 / acceptance | 本轮判断 | 原 ID |
|---|---|---|
| L5403 / 镜像身份、构建输入、SBOM/签名、拉取方法与限制 | 沿用前次已关闭结论，不重新验收；不等于已执行供应链验证 | C30 CLOSED，范围外 |
| L5404 / 固定 runtime/Toolkit/CDI、各层与映射分离 | 部分满足，未完整通过：v3 键错误/方法清单不足、成分层匹配与稳定映射未交付 | C31、C32 OPEN |
| L5405 / Ascend runtime/plugin 独立实现与目标组合 | 部分满足，未完整通过：条件链错误、选定字段/必要库挂载与 hook/范围同步未闭环 | C33 OPEN |
| L5406 / 清单、异常/隔离分支、对照与案例，不作安装处方 | 部分满足，未完整通过：全分支未知门槛、具体键/共享解释、前后身份与停止恢复关联欠缺 | C34 OPEN |

四条 acceptance 汇总：**1 沿用既有完整通过 / 3 未完整通过**。本轮范围：**0 CLOSED / 4 OPEN（1 P1、3 P2）；第九次定向复核不通过。** 判定依据是剩余关闭条件未满足及本轮确认的所属 ID 内错误，不是 curl DNS 失败、没有实测或要求建立整栈兼容。不会用审阅者补读代替作者应交付的方法/依据。

## 6. 结构校验与单文件边界

- 写入前原仓库 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS：96 content entries / 438 sources**。
- 写入后原仓库 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS：96 content entries / 438 sources**。临时副本 `/private/tmp/b21-t05-01-recheck-9.qQZDHE/validation/` 使用原仓库虚拟环境 Python、禁写字节码执行 `make check` / `make build`，均 **PASS：96 content entries / 438 sources**；只在副本重建 catalog，没有镜像构建，原仓库 build 文件摘要不变。
- 前后摘要审计：起始纳入 **388 个**既有 Git 所列 tracked/untracked 非忽略文件及 build 文件。最终观察到 `docs/research/batch-21-review-fixes.md`、`docs/research/batch-22-t05-03-claude-review.md`、`docs/research/batch-22-t05-03-sources.md`、`knowledge/05-cluster-platform/slurm-jobs-and-device-resources.md`、`sources/registry.yaml` 五个既有文件并发变更，写报告前已观察到同一集合；不是本会话编辑，不回滚，也不声称全部既有文件不变。唯一新文件为本报告，T05-01 正文/作者来源记录、前次/初审及验收计划摘要保持输入值，完整映射/登记为 §2 所披露的后读版本。
- 报告四项 ID/优先级/状态、全部本地 Markdown 链接及行尾空白另行核对：**PASS**；无新增发现 ID。结构检查不改变本报告技术结论。
- 单文件约束下不在原仓库执行会重写 build 的构建；临时副本含既有 build，以保留原有本地 catalog 链接。未改 src/kb/，不需要 make test、不新增测试；检查只验证结构与引用，不验证远程文字或技术正确性。

**最终技术结论：C31–C34 均 OPEN，0 CLOSED / 4 OPEN，第九次定向复核不通过。C30 保持此前 CLOSED、范围外；无新发现 ID、无实测；取证通道、并发版本及执行元数据限制如实披露。**
