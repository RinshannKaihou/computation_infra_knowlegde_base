# Batch 21 / T05-01 — Codex 独立初审

## 1. 结论与执行边界

**结论：需修订，本次不通过。** 新增五项开放发现：B21-C30–B21-C34，共 **1 P1、4 P2、0 P3**。四条 acceptance 均有实质缺项；已写出的安全边界可以保留，但来源入口和 `unknown` 清单不能替代要求交付的基线内容。修订后须逐项定向复核，不由作者自行宣布关闭。

- 工作日期：2026-10-14，按任务提供的本地日期记录；输入身份以本报告 SHA-256 表为准，不由日期、tag 名称或既往批次结论推导。
- 执行者：当前 Codex 会话，按用户指定的独立审阅角色工作，与正文作者角色分开；未派发其他模型或子代理。
- 用户约定配置：`gpt-6.1-sol / xhigh`。本会话未取得可独立核验的底层执行模型、推理档位或路由元数据，**不将约定写成已确认的实际执行元数据**，也不宣称完成了模型一致性或无 fallback 的独立核验。
- 只新增本报告。未修改正文、作者来源记录、来源登记、任务计划或其他既有文件；开始时已有工作区改动予以保留。
- 未安装、构建或运行容器/设备组件，未拉取镜像、验签、查询设备、接入集群或执行 GPU/NPU 实测。仓库结构检查和知识目录构建不属于硬件验证。

优先级口径：P1 表示本条目核心验收主干缺失、阻断审阅通过；P2 表示必须补齐的证据、机制或版本边界；P3 表示不改变主干判断的轻微表述/定位问题。本报告的 P1 不是对生产环境漏洞或事故严重性的评级。

## 2. 输入身份

SHA-256 对完整文件原始字节计算，审阅开始及形成结论前两次结果相同。以下行号均属于这些输入快照。

| 输入 | SHA-256 | 审阅定位 |
|---|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md) | `ac08e505028efe797523a9ec729deec83ed2334f671d144686303b6dd8b081a1` | L1–69；`reference / draft / source_checked` |
| [作者来源记录](batch-21-t05-01-sources.md) | `ce413632d1474670701f0f545351aa45b0ea99060de7b0da95a9b057cfadd68e` | L1–16；主张—来源表和 unknown 清单 |
| [任务计划](../../plans/full-coverage-backlog.yaml) | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` | T05-01 L5386–5430；四条 acceptance L5403–5406 |
| [来源登记](../../sources/registry.yaml) | `e8942efcc7ed3c11c0319c27d3b265a171a95883439214bbbbd20ebacae960e8` | 三项新增登记 L5204–5236；复用 OCI runtime L2203 起、MindCluster L235 起、NGC L653 起、框架指南 L675 起 |

另读取 `README.md`、`docs/authoring-guide.md`、`content-outline.md`、`schemas/content.schema.json` 及相关既有设备链条内容作为仓库规则和定位辅助；没有把这些辅助材料变成未经一次源核对的执行证据。未沿用 T04-06/T04-07 的发现或审阅通过结论，也未复用 B21-C01–C18。

## 3. 方法与限制

### 3.1 curl 实际尝试

对下表十二个精确 HTTPS URL 实际发起只读 GET，使用系统 curl 默认 TLS 校验；没有使用 `-k`、`--insecure`、自定解析/IP 绕行或其他降级手段。命令形态如下，输出只落在仓库外的临时目录：

```bash
curl --proto '=https' --proto-redir '=https' \
  --fail --location --silent --show-error \
  --connect-timeout 10 --max-time 30 \
  --output /private/tmp/b21-t05-01-review.UPMYTu/source.body \
  --write-out 'http_code=%{http_code}; ssl_verify_result=%{ssl_verify_result}; size_download=%{size_download}\n' \
  '表内的精确 URL'
```

首个 manifest 请求的 `--max-time` 为 45 秒；部分请求另保存响应头。**十二次均返回 curl exit 6（Could not resolve host），HTTP 000、下载 0 字节**；涉及 `raw.githubusercontent.com`、`docs.nvidia.com` 和 `catalog.ngc.nvidia.com`。未建立连接，`ssl_verify_result=0` 在此不能被解释为完成了 TLS 验证。

因此，**本轮未完成用户要求的“通过 curl 实际打开一次源并核对文字”**，也不能独立确认作者记录中的历史 curl 200。不能将 DNS 失败解释为上游文档不存在或不可访问。此项方法限制单列保留；闭环前需要在允许正常网络访问的环境补做带 TLS 校验的 curl 正文抽查。

### 3.2 补充文字核对

为避免只判断链接可达性，补充使用网页读取工具读取指定版本页面的正文，并用 GitHub 只读连接器读取精确 commit 的原文件。实际核对了下表列出的字段、策略和限制，不使用搜索片段代替正文。

- 网页工具可能返回缓存或转换后的文本：Toolkit 排障页显示缓存于三天前，CDI 页于前一天，NGC 页于两个月前；其他相关网页/原文件显示当天抓取。该标记不等于本地实时 curl 取回，也不能回溯证明作者当日读到的内容。
- OCI runtime 和 Ascend README 的 raw URL 在网页工具中也返回 Cache miss，随后由 GitHub 连接器按相同仓库/ref/path 成功取得文件；这不是 curl 成功。
- GitHub 原文件位置只使用连接器原文件行段；网页转换行号不写成 GitHub `#L` 锚点。未独立解析 OCI/image-spec、设备插件 tag 的对象链，也未核验上游文件签名或 tag 不可变性。
- 抽查不覆盖全部依赖、完整兼容矩阵、CDI 规范文本、containerd/runc 实现、SBOM/签名工具或许可证。未将来源核对升级为目标环境兼容或实验验证。

## 4. 一次源抽查表

表中 curl 结果均为 **exit 6 / HTTP 000 / 0 字节**。S01–S12 是本报告的证据定位号，不是新增登记 ID；现有登记没有被修改。GitHub 连接器读取的是相同 ref/path 的原文件，网页工具和连接器的补充结果分别记载。

| 证据号 / 登记关联 | curl 精确 URL | 补充读取及已核对文字 | 支持边界 |
|---|---|---|---|
| S01 / `src.oci.image-spec-v1.1.1` | [manifest.md@v1.1.1](https://raw.githubusercontent.com/opencontainers/image-spec/v1.1.1/manifest.md) | 网页原文；Image Manifest Property Descriptions 的 config/layers、层顺序，以及 optional subject/annotations | 支持镜像对象结构，不支持运行时/主机兼容 |
| S02 / 同上 | [descriptor.md@v1.1.1](https://raw.githubusercontent.com/opencontainers/image-spec/v1.1.1/descriptor.md) | 网页原文；Properties、Digests、Verification：mediaType/digest/size、对内容字节计算及校验摘要 | 支持内容身份与完整性语义，不补足构建、SBOM、签名或拉取策略 |
| S03 / `src.oci.runtime-spec-v1.3.0` | [config-linux.md@92249139](https://raw.githubusercontent.com/opencontainers/runtime-spec/92249139eea7161e13745abd4cb6d0ea02a3227a/config-linux.md) | GitHub 原文件，blob SHA `c71757494ca743fd90692c25e4897bf74cf00388`；Devices L127–151、Allowed Device list L402–417；另读取 Namespaces/User namespace mappings | 设备节点与访问许可分开，不能替代厂商注入实现；本轮未独立核验登记中的 tag→commit 关系 |
| S04 / `src.nvidia.container-toolkit-1.20.0` | [install-guide.html](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/install-guide.html) | 网页正文；Prerequisites、Configuration、Configuring containerd (for Kubernetes)；安装示例固定包版本 1.20.0-1 | 支持 Toolkit 文档/包版本及宿主驱动前置，不给出选定 containerd/runc 配套组合 |
| S05 / 同上 | [cdi-support.html](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html) | 网页正文；自动生成与已知限制、CDI 解析、Running a Workload with CDI、非原生 CDI runtime 路径 | 区分 native CDI 与 runtime 路径；有 MIG 重配/驱动移除刷新限制及 hook 冲突提示；不是 CDI 规范版本登记 |
| S06 / 同上 | [troubleshooting.html](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html) | 网页正文；SELinux/NVML 权限段、容器更新后丢失 GPU 访问段及 Affected Environments/Mitigations | 给出异常和条件；权限放宽有隔离影响，不构成本库已复现案例或通用修复处方 |
| S07 / `src.nvidia.k8s-device-plugin-v0.20.1` | [README.md@v0.20.1](https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.20.1/README.md) | 网页原文；Configuration Option Details：设备列表传递策略、设备 ID 策略、初始化失败行为；Shared Access to GPUs | 能解释分配 ID 和注入通道；time-slicing 的隔离限制不能由资源计数或 namespace 替代 |
| S08 / `src.ascend.mind-cluster-v26.1.1` | [Ascend Device Plugin README@44385c13](https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/README.md) | GitHub 原文件，blob SHA `a8e257ab89f6c2825b0c11fa28acad6b80a4d943`；组件介绍的发现、健康检查、分配职责 | 支持固定实现入口，不证明目标硬件/驱动/CANN/框架整栈配套 |
| S09 / 同上 | [plugin.go@44385c13](https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go) | GitHub 原文件 L1080–1175，blob SHA `b7692611b12884854d973fa2a3da18e381353f10`；mountDevice、mountDefaultDevice、setNPUDeviceMount 两路径 | 直接设备配置和调用 Ascend runtime 环境辅助函数可分别取证；没有继续核验辅助函数、runtime 库注入或完整 Allocate 链 |
| S10 / `src.nvidia.framework-containers-user-guide-2026-09-30` | [Framework Containers User Guide](https://docs.nvidia.com/deeplearning/frameworks/user-guide/index.html) | 网页正文；§1.1 容器使用宿主内核、§5.9 限制 GPU 暴露、框架库说明 | 当前可变指南；不能据旧观察日期视为不可变版本，不能代替框架 ordinal→物理设备映射证据 |
| S11 / `src.nvidia.ngc-pytorch-25.01-py3-catalog-2026-09-30` | [PyTorch 25.01-py3 layers](https://catalog.ngc.nvidia.com/orgs/nvidia/-/containers/pytorch/25.01-py3/layers) | 网页正文；25.01-py3/Signed、build id 134983853、build ref 3857cfd7a27acea1d4e19243329fcd1dae3b222e、PYVER=3.12 | 只读到可见十条层记录；未获取 manifest digest、拉镜像、验签或核验完整成分 |
| S12 / `src.nvidia.container-toolkit-1.20.0` 下补充页面 | [docker-specialized.html](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/docker-specialized.html) | 网页正文；GPU Enumeration、Driver Capabilities：设备选择变量与挂入容器的 driver libraries/binaries | 支持 NVIDIA 特定注入模式下的职责分离；不外推其他 runtime 或 NPU |

## 5. 四条 acceptance 判定

| Acceptance / 计划位置 | 判定 | 已满足部分 | 未满足部分 / 发现 |
|---|---|---|---|
| 1 / L5403 | 部分满足，不通过 | digest 不作兼容证明；未宣称已经建成供应链系统 | 构建输入、SBOM/签名、拉取策略只列名词和 unknown，缺方法及各自作用限制；B21-C30 |
| 2 / L5404 | 部分满足，不通过 | OCI 双规范、Toolkit 1.20.0、设备插件 v0.20.1 入口有版本；host/container 行在形式上分开 | containerd/runc 与 CDI 规范未固定；设备/库/权限/框架映射缺具体语义和证据；B21-C31、B21-C32 |
| 3 / L5405 | 部分满足，不通过 | 明确 GPU 不套用 NPU；digest 不证明主机/驱动兼容 | Ascend 只有仓库名与 unknown，没有 runtime/plugin 的独立实现证据和目标组合记录；B21-C33 |
| 4 / L5406 | 不通过 | 有六类清单名词、三类异常标签；明确未执行、不作安装处方 | 无可填写的环境基线、异常分支、判定条件、对照设计或实际案例链接；B21-C34 |

`reference / draft` 与 `generic` 的使用未发现结构性错误。`source_checked` 在作者明确列出的已核对范围内解释，不能读成整条 acceptance 已满足或硬件通过；本次没有据此要求修改为 `reviewed` 或 `reproduced`。

## 6. 逐项发现

### B21-C30 — P2 / OPEN：镜像方法清单用 unknown 代替了作用、限制和记录方法

**位置：** 正文 §1 L39–43、待确认 L69；作者记录 L9、L16；acceptance 1。

**证据与影响：**

- L41 仅列 Dockerfile/构建参数，没有说明如何记录构建输入或判断证据是否足够；L42 将 SBOM/签名合为一个条目，未分别交代核对对象、方法及判断限制；L43 没有给出选定平台的拉取策略字段、默认/显式策略条件或精确来源。
- S01、S02 的 manifest/descriptor 内容只支持镜像结构和摘要校验，不包含上述方法的完整依据。S11 可见的 Signed 标记和 build 元数据也不是本库已完成验签、SBOM 审计或可复现构建的证明。这里没有认定作者伪造验证，而是验收交付不足。

**关闭条件：**

1. 给出可填写的构建输入记录方法，至少区分基础镜像身份、构建文件/上下文修订、参数、依赖锁定和构建工具信息；未能固定的输入继续逐项 unknown，不能以列名代替方法。
2. 分列 SBOM 与签名，补官方规范/工具的具体版本和页面；分别说明记录对象、核对方法、可支持的结论及不能支持的结论。没有执行的核对不得写为完成。
3. 在实际选择的 runtime/编排路径中固定拉取策略依据，说明 tag/digest、显式策略与缓存复用之间需要保存哪些事实；将精确引用放在相应条目旁，不只写“各运行时文档”。
4. 保留 digest 不作兼容证明和没有已建供应链系统的限定；新增依据同步到作者记录/来源登记后提交定向复核。

### B21-C31 — P2 / OPEN：运行时/CDI 版本基线没有建立

**位置：** 正文 summary L17、verification.notes L28、§2 L51、L55–56、L69；作者记录 L10–11、L16；acceptance 2。

**证据与影响：**

- L56 明确 containerd/runc 资料未取；没有版本、配置模式或实现位置。summary 却写“containerd 分支”，正文没有指明任何分支。Toolkit 页固定为 1.20.0，不等于已经固定 containerd/runc 文档和实现。
- L51 和 L69 承认 CDI 规范未登记。S05 是 Toolkit 的 CDI 支持页，不是 CDI 规范版本；S07 的 CDI 两种传递策略还有 container engine/CRI 条件。现有入口不能得出完整受支持组合。
- OCI 规范固定不能替代具体 runtime 版本。S03 可以解释 Linux 字段，但不为 containerd/runc 或厂商注入路径提供实现支持交集。

**关闭条件：**

1. 选择明确的 containerd/runc 文档版本或固定 commit，定位实际配置模式/字段和诊断依据，登记并引用；必要时把不同版本分别列出，禁止拼成未经支持的组合。
2. 固定 CDI 规范版本/页面，区分规范、Toolkit 生成/注入实现、container engine 消费端，以及 Kubernetes/CRI 传递路径；未成立的支持交集继续 unknown。
3. 将 OCI 通用字段与 Linux 字段分别指向 `config.md` 和固定 `config-linux.md` 的精确章节，而不是只给 tag 根目录。修正 summary 中没有对应证据的“containerd 分支”表述，或补上其实际定位。

### B21-C32 — P2 / OPEN：GPU 各层只分了表格行，关键机制与权限/框架映射仍混空

**位置：** 正文 §2 L49–55；作者记录 L11；acceptance 2 的职责分离部分。

**证据与影响：**

- L49“宿主机驱动版本独立于容器，由运行时透传”没有说明透传对象；不能据此理解为把宿主内核驱动搬入镜像或容器。S04 要求先安装宿主驱动，S10 §1.1 说明容器使用宿主内核；S12 的 Driver Capabilities 具体描述的是将 driver libraries/binaries 挂入容器。正文没有分开这一部分与镜像内 CUDA/框架库。
- L51 只是“设备节点注入、环境变量、卷挂载”，没有将分配 ID、注入通道和最终应用结果对应起来。S07 的 `deviceListStrategy` 是传递已分配设备列表的策略，`deviceIDStrategy` 是传递 ID 的策略，均不能直接充当框架设备编号映射。
- L52“权限模型，以 Toolkit 文档为准”没有实际模型；S03 的 Devices 与 Allowed Device list 分别涉及节点和访问许可。L53 也没有可核对的框架可见编号→所选物理设备映射；S10 的限制 GPU 暴露段不是这一映射的完整依据。

**关闭条件：**

1. 改写“透传”，分别说明宿主内核驱动、注入/挂载的用户态驱动组件、镜像自带 CUDA/框架库的来源、版本字段和边界，并给具体引用。
2. 用一个已固定但未宣称兼容的 GPU 样板串起“分配 ID→环境变量/CDI/设备配置→最终节点/挂载”；不同路径分别列条件，不能把同一变量缺失当作所有模式的注入失败。
3. 分开设备节点/文件属主和权限、容器进程身份、设备访问控制及 LSM 等策略证据；说明哪些证据只支持可见性、哪些才支持访问判断。补固定框架来源和映射记录方法；无法确定物理对应时明确 unknown。
4. 与 B21-C34 分工：本项关闭层间机制和记录字段，C34 关闭具体异常分支与验证设计。不得靠重复概念表同时关闭两项。

### B21-C33 — P2 / OPEN：Ascend 独立样板仅保留仓库入口，未完成实现/目标组合取证

**位置：** 正文 §3 L58–60、L28、L69；作者记录 L12、L16；acceptance 3。

**证据与影响：**

- §3 只有“按该实现文档为准”，没有精确组件文件、配置条件、设备 ID/节点、环境/挂载路径或目标组合。承认支持交集 unknown 是正确边界，却不能代替 runtime/plugin 固定实现本身的独立取证。
- S08 支持的是插件职责入口；S09 中 [plugin.go L1087–L1169](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go#L1087-L1169) 已有可区分路径：`UseAscendDocker` 为假时返回设备配置及权限，另一分支调用设置 Ascend runtime 环境的辅助函数。该代码支持补充固定插件行为，但本轮没有继续读辅助函数/runtime，不能补写其完整语义或配套结论。
- L60 还提及 MindIO ACP 复用；[登记](../../sources/registry.yaml) L333 起将其用于 Checkpoint/存储接口。该记录不能替代设备暴露依据，且正文 `source_refs` 没有此来源项。本项不要求为了设备基线强行引入 ACP。

**关闭条件：**

1. 明确 Ascend 组件/ref，分别定位 Device Plugin 的分配/返回配置和对应 runtime 的消费、设备/环境/库挂载实现；只复用已经核对的文件与结论，缺失部分明示。
2. 列目标组合所需字段：产品形态、OS/内核、驱动/固件、runtime/plugin、CANN/框架和镜像身份；提供已有固定支持材料或明确未建立支持交集。不得从 GPU/CDI 路径推导 NPU 配置，不要求虚构硬件验证。
3. 删除与设备暴露无关的 ACP 入口，或说明它的有限用途并补正确来源关联；可链接[既有设备链条](../../knowledge/05-cluster-platform/device-resource-chain.md)，但仍须在本基线交代选择的 Ascend 分支和未知条件。
4. 保留 GPU 不套用 NPU、digest 不证明兼容的明确限定；修订后独立定向核对对应一次源。

### B21-C34 — P1 / OPEN：最小清单、异常分支和对照验证主干尚未交付，源案例没有实际链接

**位置：** 正文 §4 L62–64、来源 L68；作者记录 L11–12；acceptance 4。

**证据与影响：**

- L64 六类清单没有记录格式、期望/实际值或证据位置；设备注入缺失、权限拒绝、隔离越界只是症状名称，没有下一分支、替代解释、停止条件或结果判据。“见各样板排障页”没有给出任何具体链接，不能构成对照验证设计或源案例链。
- S05 的 CDI 页面已有刷新/解析错误与 hook 冲突的不同分支；原生 CDI 路径不能要求一定存在 GPU 选择环境变量。正文“设备文件/环境变量缺”没有模式限定，无法据此判断注入异常。
- S06 的 [NVML/SELinux 权限段](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html#nvml-insufficient-permissions-and-selinux) 警告 `--security-opt=label=disable` 会放弃 SELinux 隔离；[GPU 访问丢失段](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html#containers-losing-access-to-gpus-with-error-failed-to-initialize-nvml-unknown-error) 限定 hook/legacy 注入和容器更新等条件，不能当作所有 runtime 的统一原因或修复处方。
- S07 的 Shared Access to GPUs 明示 time-slicing 不提供相应工作负载隔离。因此只列 cgroups/namespaces 不能充当 GPU 显存、计算份额或故障域隔离的验证方法。本文尚未宣称该隔离已经成立，但缺少防止这种误读的观测/判定设计。

**关闭条件：**

1. 给出可填写的最小环境清单，含镜像身份/构建与库信息、宿主软硬件、runtime/plugin/CDI 模式、请求/分配设备、最终节点/挂载/环境、进程身份/访问策略和框架映射。区分期望配置与实际证据，缺失字段可写 unknown。
2. 至少形成设备注入、访问拒绝、隔离范围三类具体分支表：“观测→候选解释→所需证据→受控对照→解释边界→停止/完成条件”；GPU/NPU 条件分别写，避免把环境变量缺失、单个错误消息或设备数量直接判作根因。
3. 提供只设计、未执行的对照方案：控制同一镜像/驱动等条件，核对请求集/最终注入集/框架可见集；限定未授权设备负向验证的授权与隔离前提。不得给出虚构输出，不自动放宽权限、禁用安全策略或重启生产组件。
4. 实际链接至少一个与分支相符的官方问题说明/源案例，提炼症状、发生条件、已知限制和非本库复现属性；可链接[既有 Ascend 来源案例](../../knowledge/05-cluster-platform/ascend-device-visibility-source-case.md)和[待执行实验](../../knowledge/05-cluster-platform/ascend-device-visibility-experiment.md)，但须说明关联及源案例缺失条件，不能用链接代替正文判定设计。
5. 保留“只设计、未执行、不得作为已验证安装处方”；源文档中的修改/恢复建议不赋予执行授权。完成上述内容后再按输入 SHA 定向复核。

## 7. 校验、复核与事实追记

- 审阅写入前的 `PYTHONDONTWRITEBYTECODE=1 make check`：PASS，94 content entries / 420 sources；仅结构和本地文件链接检查。
- 报告写入后的 `PYTHONDONTWRITEBYTECODE=1 make check`：PASS，94 content entries / 420 sources。
- 为遵守“只写这一份报告”，在 `/private/tmp/b21-t05-01-validation.6eSF0g` 的临时源文件副本执行 `make check` 和 `make build`。首次副本排除了既有 `build/`，因 `docs/first-fill-status.md` 的两个生成目录链接无目标，check 报两项结构错误，build 未运行。将当前仓库既有 `build/` 只读复制进副本后重跑，两项均 PASS，94 content entries / 420 sources，成功重新生成副本的 `build/catalog.json` 和 `build/catalog.md`；未修改原仓库生成文件。该首次失败是临时副本缺失链接目标，不作为正文技术发现。
- 写入报告后的四个输入 SHA-256 再次与 §2 相同；最终工作区状态仅比初始状态新增本报告。
- 不需要 `make test`：本轮没有修改 `src/kb/` 或测试代码。未进行任何容器或硬件实测。
- B21-C30–C34 当前全部 OPEN。后续复核须记录修订输入 SHA、一次源具体位置、每项关闭证据及未解决条件；curl 方法缺口和执行模型元数据限制不得被结构检查结果掩盖。
- 后续若发现新的事实错误，继续从 **B21-C35** 起编号并记录位置、证据、优先级和关闭条件，不无编号散记、不复用其他任务发现 ID。本轮截至本报告未另发现需要单列的已确认事实错误；C31 的版本缺项、C32 的机制歧义以及 C34 的判定设计缺失分别在所属 ID 下处理。

最终审阅状态保持：**需修订；不通过；curl 指定方法未完成；未建立任何真实环境验证结论。**
