# Batch 21 补交 T05-01 第二十二次定向复核

## 1. 结论、角色与范围

- 日期：2026-10-14（Asia/Shanghai）。执行者：当前 Codex 会话，以独立审阅角色核对作者第二十二轮落盘修订，与作者修订角色分开；未派发其他模型或子代理。
- `gpt-6.1-sol / xhigh` **仅为用户约定，不是已独立确认的执行元数据**。本会话没有可独立核验的实际模型、推理档位或路由证据，不宣称模型一致性或无 fallback 已获独立确认。
- 唯一复核范围：**B21-C32–C34**。剩余关闭条件以[第二十一次复核](batch-21-t05-01-codex-recheck-21.md) L86、L104、L119 为权威；[初审报告](batch-21-t05-01-codex-review.md)用于原 ID、职责与优先级核对。**C30/C31 保持此前 CLOSED、范围外，不重审。**
- **0 CLOSED / 3 OPEN（1 P1、2 P2）；第二十二次定向复核不通过。** 认可新增 `PresetVDevice=false` 设计假设、默认五项候选的路径/目标对应、两端传递策略集合及换权限变体的 R1 绑定；这些进展没有关闭其余方法、完整所选记录与对照设计缺口。
- 本轮仅使用三个原 ID；口径问题继续按 C33 追记，**不新增发现 ID**。修订映射只证明落盘改动，不是关闭证明。
- 只新增本报告，不修改作者正文、来源记录、修订映射、登记、计划或原仓库生成文件，保留开始时已有工作区改动；不提交、不创建分支。
- 未安装组件、拉取/构建镜像、生成 SBOM、运行容器、接入集群、修改运行配置或执行访问、负向、资源更新、恢复实测；上游脚本只读未执行。结构校验与知识库目录构建不是环境或硬件验证。

| 原 ID | 原优先级 | 本轮状态 | 位置证据与剩余问题 |
|---|---|---|---|
| B21-C32 | P2 | OPEN | 正文 L60、L72、L78、L82–84、L109–114、L118、L131–138：扫描归层、逐库连接及逐 ordinal 稳定映射方法仍未交付，缺方法/缺采样分类未完整同步 |
| B21-C33 | P2 | OPEN | 正文 L90、L92；来源记录 L17；登记 L5446：新假设与五项路径对应认可；完整所选条件/节点/许可/环境、逐库待采记录及旧宽口径同步仍未完成 |
| B21-C34 | P1 | OPEN | 正文 L127、L132–138：两端策略集合与换权限 R1 绑定认可；runtime 模式/handler 消费配置、更新接口/字段、成功访问/原负向边界恢复的生命周期关联及 C32 方法依赖仍缺 |

## 2. 输入身份与写入边界

正文前缀吻合。修订映射**整文件前缀不吻合，但差异已定位为追加执行记录**，不能写成“两个整文件前缀全部吻合”：

- 用户指定映射前缀：`b1a7c8c551d72325`；当前整文件 SHA-256 为下表 `b2997250…`。
- 独立执行 `head -n 288 docs/research/batch-21-review-fixes.md | shasum -a 256`，所得完整摘要为 `b1a7c8c551d72325577554f4875716a214efcee0872a7ce91639a32323212ef0`，**与用户指定前缀吻合**。当前文件的 L1–288 正好对应所指修订输入；第二十二轮修订节为 L284–288。
- 当前文件另有 L289 空行及 L290–292“第二十二次复核执行记录（未产出报告）”，其中容量失败与历史 `make check` 为作者记录，本轮不独立背书。这一追加不改 L284–288 所列修订；未删去或改写它，也不把其中“待重跑”文字当作停止本轮审阅的指令。本次按正文及已核验的修订节继续，不以该摘要差异另立技术发现。

以下完整摘要由本轮独立计算；所有仓库行号指输入原文件，不是网页阅读器行号。

| 输入 | SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md) | `4864986768bc2eebf237fdd12a86db8f74230ca8385c6bab15c1d9b7a752cba3` |
| [修订映射](batch-21-review-fixes.md)，当前整文件，第二十二轮节 L284–288 | `b299725019e22aed49f8900fec493d83a2270cbcd72be06fe7bd8ed2cfba5864` |
| [第二十一次复核](batch-21-t05-01-codex-recheck-21.md) | `453d2a69d2282d6fa051279c93a2ec74dbe9119d240b464270a09f5624615f74` |
| [初审报告](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` |
| [任务验收](../../plans/full-coverage-backlog.yaml)，T05-01 acceptance L5403–5406 | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml)，440 项 | `e774b5c1440bce91a648d10b1ec8bcad6b70eda8e18883a46a60c5a5585c8bb1` |
| 补读：[作者来源记录](batch-21-t05-01-sources.md)，用于前次 C33 口径条件 | `a88ff7db50c3c246567bdbefa3b7825f7bbf6a5c1e3aec35f89e1f302437f6c2` |

已从 `README.md`、`docs/authoring-guide.md` 开始核对仓库要求，并按 `content-outline.md` 核对 05 主归属及设备暴露/驱动底层边界；相关目录未发现更深层 `AGENTS.md`。写入前保存 Git 状态并对 Git 所列 tracked/untracked 非忽略文件及既有 build 文件做 SHA-256 快照，共 **405 个**既有文件。临时审计目录为 `/private/tmp/b21-t05-01-recheck22-1ip6Wa/`；构建使用其中的独立副本，避免重写原仓库 `build/`。

## 3. 一次源抽查方法、文字与限制

### 3.1 curl 实际尝试与只读替代通道

对下表 01–11 的精确 HTTPS 地址实际执行只读 GET；源码使用与 blob 链接同 ref/path 的 `raw.githubusercontent.com` 地址，文档使用表中原地址。命令形态：

```sh
curl --location --fail --silent --show-error \
  --connect-timeout 8 --max-time 20 --output "$audit_dir/curl-$point.body" \
  --write-out 'http_code=%{http_code}\n' "$url"
```

未用 `-k`/`--insecure`，未关闭默认 TLS 校验，未申请沙箱提权或自定 IP 绕行。**11 次全部在 DNS 阶段失败：退出码 6、HTTP 000、Could not resolve host**，涉及 `raw.githubusercontent.com`、`docs.pytorch.org`、`docs.nvidia.com`。没有 curl HTTP 正文，不能称 curl 200、TLS 握手/校验成功或已有上游 HTTP 字节摘要。请求清单、退出状态及错误保存在审计目录的 `curl-urls.tsv`、`curl-01.meta` 至 `curl-11.meta` 和相应 `.stderr`。

随后采用用户允许的只读替代通道：GitHub 连接器 `fetch_file` 重新实读固定 ref 的原文件区间；网页读取通道实开版本化 PyTorch/NVIDIA 文档并定位章节文字。Syft README 同时由网页与 GitHub 连接器读取，源码位置以连接器原文件区间为准；没有执行其中的安装示例。网页可能经缓存/解析，不能等同本机 curl 的新鲜原始字节；连接器 blob SHA 也不是 curl HTTP 摘要。**不是只判可达性，不以搜索片段、作者自述或前次摘录替代本轮文字核对，不独立背书历史 curl 成功记录。**

### 3.2 本轮实读点与有限支持范围

Ascend 源码均固定 commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e`。源码坐标来自 `fetch_file` 原文件区间；文档按章节定位，不把网页阅读器行号转作 GitHub 源码锚点。

| curl 点 | 精确一次源 / 本轮实读位置 | 核对文字与有限支持范围 |
|---|---|---|
| 01 | [build/scripts/base.list](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/scripts/base.list)，完整五行 | 五个绝对宿主候选为 `/usr/local/Ascend/driver/lib64`、`/usr/local/Ascend/driver/include`、`/usr/local/dcmi`、`/usr/local/bin/npu-smi`、`/var/queue_schedule`。支持新增候选对应，不证明具体库身份/版本、存在或成功挂载 |
| 02 | [run_main.sh](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/scripts/run_main.sh)，L278–315 | 未选五种产品安装类型时复制默认列表；各分支落配置目录的 `base.list` 并设 440 权限。不证明 310B 产品支持或现场安装结果 |
| 03 | [cli/src/u_mount.c](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/cli/src/u_mount.c)，L45–240 | 目标按 rootfs 与源路径拼接；源 stat 失败可跳过，建目标/校验/挂载可失败；bind 后只读/nosuid remount。NODRV 提前返回的支持范围是该 CLI 的 `DoMounting`，不是整个 runtime 一切挂载 |
| 04 | [runtime/process/process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go)，L232–405、L455–830 | 读到 LD_LIBRARY_PATH 处理、独立 DP mounts、非 VIRTUAL 下 CreateVDevice/条件化 poststop、节点/许可写入、310B manager 和 UB 条件。14 个辅助项失败仅警告，manager 回退可失败；310B 前另尝试 dvpp_cmdlist；UB 目录下跳过子目录。设备信息取自宿主，许可写 allow/type/major/minor/access=rwm；不是全部节点注入成功证明 |
| 05 | [device-plugin common.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go)，L100–139 | 输入整数 ID 逐个转换并逗号拼接，options 写入；310B 条件写 allow-link；七个 worker 环境项由 `!PresetVDevice` 控制。支持新增 false 设计假设，不证明实际配置与 runtime 芯片返回一致 |
| 06 | [hook/process/process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/hook/process/process.go)，L85–225、L237–440 | mount group 默认 base；每份列表先计扫描行，再做绝对路径/stat/常规文件或目录分类；取 PID/rootfs，构造文件/目录及条件 options 参数调用 CLI；另有 UB 挂载候选。支持候选入选/跳过与目标规则，不保证五项实际均挂入 |
| 07 | [Syft README@v1.54.1](https://github.com/anchore/syft/blob/v1.54.1/README.md)，L1–110，Features/The basics | 核到扫描对象与输出格式入口；这些段落不交付本文所选固定扫描范围、逐库来源层字段解析和连接方法。不重开 C30，不断言其他工具材料不存在 |
| 08 | [PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html)，Device-agnostic code 的 CUDA_VISIBLE_DEVICES 段 | 说明管理 PyTorch 可用 GPU 范围；该段不是 ordinal→分配/CDI→完整节点→稳定身份的连接方法。不据此断言其他身份接口不存在 |
| 09 | [NVIDIA server.go@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go)，L280–507 | Allocate 校验请求 ID；转换/去重后按策略输出 CDI 或 envvar/volume mounts；全 CDI 策略提前返回，非 CDI 路径还受 PassDeviceSpecs 控制。支持新增单元素策略集合，不决定消费端 runtime 模式 |
| 10 | [Toolkit 1.20.0 troubleshooting](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html)，NVML/SELinux、访问丢失、Affected Environments | 权限段警告禁用 SELinux 会放弃隔离；访问丢失段限定 hook/legacy，CPU/内存限制更新与 systemd 场景有区别。这是源场景，不替作者选定更新接口/字段或生成访问恢复结果 |
| 11 | [Toolkit 1.20.0 CDI support](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html)，Running a Workload、Non-CDI-Enabled Runtimes、Setting the CDI Mode Explicitly | 独立 runtime hook 与 CDI 可冲突；NVIDIA_VISIBLE_DEVICES 也可在 CDI 模式消费。因此 envvar 策略不独立确定 legacy 消费端，仍须固定模式/handler 组合 |
| 补读，未列作 curl 点 | [build/build.sh](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/build.sh)，L120–145 | `copy_file_output` 将默认/产品列表送入安装包；补核源码→打包→安装选择链，未执行脚本 |

连接器返回的关键 blob SHA：`base.list=4ea1b223fdeed19fed7fdf1a3b4457b8ddd747b3`；`run_main.sh=9be36636ff13c480c57342b81c78f4b74e95675b`；`u_mount.c=d85fd8155a1805edaf509b047c6441bcdc603e12`；runtime `process.go=acbd7a1ec0703498abfcfcb6ce1aa493069091b1`；`common.go=6cd038e9f1d67a8a913aa4bb1301692f177b3dbe`；hook `process.go=816212afa5f69b8edfb1554d3935af2ebcd28f06`；NVIDIA `server.go=9281b48ef52f9eda9cbed6d98491729da85b5a75`。这些是连接器返回的 Git blob 身份，不是独立下载的 SHA-256。

## 4. 逐项定向复核

### B21-C32 — P2 / OPEN

**权威条件：** 前次复核 L86。**位置证据：** 正文 L60、L72、L78、L82–84、L109–114、L118、L131–138；本轮映射 L288。

**认可/保留：** 宿主内核驱动、注入用户态组件与镜像库分层，Allocate/CDI/edits/OCI 连接及节点/许可分离继续认可。L112 的缺方法/缺采样区分及 L118 缺规则优先无法确定保留，不重开 C30/C31；本轮分类说明没有提供新增完整映射方法。

**仍未满足：**

1. L60/L72 仍以“所选扫描配置”“来源层字段，以实际输出为准”“缺项逐项记 unknown”代替固定扫描范围、必要字段、包/文件路径与来源层解析和连接键。层清单、diff_ids、annotations 与通用箭头不替代逐库来源→最终挂载→容器目标的方法。抽查 07 核到工具入口，不是缺本轮真实 SBOM 输出。
2. L78 仍明确“稳定物理标识映射方法（未交付，unknown）”；L82–84 是待填表，没有来源支持的逐 ordinal 可见集快照→分配 ID/CDI 名或传递字段→完整节点（类型/major/minor/路径与来源）→稳定身份规则。抽查 08 仅支持可见范围管理；数量/编号一致不能替代关联。
3. L109“未记录即缺失”、L110“无法确定写 unknown”、L111“同上”仍未统一记录缺方法/缺采样的原因、具体缺项与证据格式；L114、L131–138 的比较也未引用已交付规则。诚实承认未知不能算完成方法设计。

**剩余关闭条件：** 按固定来源交付所选扫描范围、必要字段、逐库归层/来源连接及完整稳定映射方法；把缺方法/缺采样的原因、具体缺项和记录格式同步至核对表、清单与 C34 比较/判定。**现场值可 unknown；不要求拉镜像、生成 SBOM、审计全部 cataloger、采设备或实测，不重开 C30。**

### B21-C33 — P2 / OPEN

**权威条件：** 前次复核 L104。**位置证据：** 正文 L90、L92；映射 L286；作者来源记录 L12、L17；登记 L5335、L5446、L5457、L5462。

**本轮新增认可：**

- L90 已明确选 `PresetVDevice=false`，结合此前 `UseAscendDocker=true`、空输入 options、base mount group、默认安装分支和 310B 芯片示例。抽查 05 支持该假设下 worker 组的静态条件；**不再指称未选择 PresetVDevice**，也不要求取得实际 DCMI 返回值。
- L90 已逐项交付五个候选的宿主来源、文件/目录候选、hook 入选→CLI MountDir/MountFile→rootfs 与容器目标对应；`driver/include` 的简写可结合①与固定五行列表理解，不要求机械重复公共规则。抽查 01/02/03/06 支持这一新增设计，**不再指称完全没有逐项来源/目标记录**；身份/版本/结果待采不判错。
- 既有虚拟/poststop 条件、默认安装选择、源码链已读及来源记录 L12/登记 L5335 的收窄继续认可；未选五份产品变体不是必须全部审计的任务。

**仍未满足及原 ID 内追记：**

1. **完整所选条件/输出记录仍缺。** L90 有分支摘要，但未选产品形态和输入 ID 的设计形式，未将插件 RealCardType 与 runtime GetChipName 所选条件连接，未将 310B 前置 dvpp_cmdlist、14 个 manager 尝试项、manager 宿主路径回退/容器目标及失败分支、UB 目录/条目条件串成完整记录。抽查 04 说明这些不是“14 项全成功”的保证；310B 分支提前返回，不要求它执行后续 GetProductType。节点 path/type/major/minor 与许可 allow/type/major/minor/access、worker/控制环境、条件化虚拟/poststop 尚未逐段对应，L92 的目标组合字段清单也不是这份所选输出记录。
2. **逐项候选对应的基本路径已经补齐，逐库待采记录仍不完整。** L90 只笼统写“身份/版本/挂载结果待采”，未单列驱动库候选内具体库身份/版本的待采位置与记录字段，不能把 driver/lib64 目录候选当成逐库记录。应关联已知候选与条件化的库记录、采样/证据位置和结果缺项，保留 hook 分类/CLI 校验可跳过或失败的边界；不要求虚构库名/版本、检查全目录或取得实际挂载。
3. **旧宽口径没有完整同步。** L90 开头和结尾仍两次写“runtime 库注入语义未核对”，其中另有“实际库挂载来源/目标/白名单未取”，与同段已经交付的静态来源/目标及消费规则并列，未限定为所选逐库记录或现场结果；“所选变体内容……未读”也未区分已读默认 base 与未选五份产品变体。作者来源记录 L17 继续将实际库挂载、白名单、hook 可执行和 dcmi 完整实现合列 unknown。登记 L5446 的四子目录未见属于有限目录描述，不改判为全树检索错误，但仍需明确源码列表在 build/scripts、安装后文件是部署产物，并关联现有 install 登记。L12/登记 L5335、L5457、L5462 的正确收窄不能代替这些位置的同步。

**剩余关闭条件：** 保留已选 false 假设、芯片/默认安装与五项对应，补产品/输入 ID 及插件与 runtime 条件连接，交付完整节点/许可/环境、manager/UB 与条件化虚拟/poststop 记录；补必要库候选的逐库待采格式及来源、入选与目标关联。同步正文/作者记录的旧宽口径及登记的源码/部署边界，明确**机制已读、所选记录未交付、现场未采**三分。**现场文件/设备号/库版本/挂载结果可待采，支持交集可 unknown；不要求安装、执行脚本、实测、完整 DCMI/全部白名单或 CLI 审计。**

### B21-C34 — P1 / OPEN

**权威条件：** 前次复核 L119。**位置证据：** 正文 L118–125、L127、L131–138、L140–142；本轮映射 L287。

**本轮新增认可：**

- L132 已选两端单元素传递策略集合 `[cdi-cri]` 与 `[envvar]`，并明确计划外字段出现即判混合→无法确定；抽查 09 支持策略分开。**不再指称两端完整传递策略集合尚未选择**；集合表达不等同已经提供可部署配置。
- L133 已把换权限变体的停止/恢复显式绑定至 S1/R1，补目标进程受控访问记录与原 allow 边界比较记录的文字。**不再指称该变体完全没有恢复绑定**；公共规则可复用，不要求逐行机械重复。
- 既有 CDI 自身 hooks/独立 legacy 边界、有序完整许可比较对象、负向授权、回退与更新/重建拆分、旧新主体/时间窗、NPU 独立未知及源案例缺项继续认可。

**仍未满足：**

1. **策略集合不替代完整消费配置对。** L132 仍仅将 handler 名/旧新值交站点待填，未固定两端 runtime 模式与 handler 消费组合及相应关键字段。抽查 11 明示 NVIDIA_VISIBLE_DEVICES 在 CDI 模式仍可消费，故 `[envvar]` 不能独立确定 hook/legacy；“无 CDI 引用”只能描述所选插件传递输出，不能直接证明最终消费端没有 CDI。需选定消费设计并落实两端旁路/并行输出约束；站点 handler 名与现场值可待填，不要求全模式审计或重开 C31。
2. **资源更新接口/完整字段仍缺。** L137 仍写 CPU 限制的 CRI 更新对象/OCI linux.resources.cpu 为“候选”“固定字段未取，unknown”，没有选接口、完整字段、单位/语义及旧新记录格式，亦未将这些字段绑定同一次更新前后采样。抽查 10 支持更新场景，但不交付作者所选接口；镜像/驱动回退或重建不能替代资源更新对照。
3. **成功访问与原负向边界恢复的可定位设计关联仍缺。** L127 的 R1 有 audit/AVC、三元组和配置摘要，L133 又有访问/allow 比较的名词，但没有选定受控成功访问操作及结果记录形式，也未给单独授权的负向拒绝记录与统一连接规则，使各变体更新/重建前后、恢复后的主体、完整目标节点/稳定身份、时间窗及正负访问结果能关联。L135–138 仍主要以注入集和“同上”表达。没有拒绝事件、可见集恢复或配置摘要不能替代成功访问与原负向边界恢复；缺负向授权时只记录未执行，不得补造结果。
4. **C32 方法依赖仍未闭合。** 三单比较依赖未交付的完整稳定映射；缺方法/缺采样原因和具体缺项未统一同步。这是 C32 同一缺口的依赖，不新增发现或重复计数，也不替代前三项独立设计要求。

**剩余关闭条件：** 保留已选两端策略集合及换权限 R1 绑定，补完整 runtime 模式/handler 消费配置对、关键字段与旁路排除；选定资源更新接口、完整字段、单位/语义及旧新记录格式；完善成功访问和原负向边界恢复的设计记录，以公共连接规则对应各变体生命周期前后及恢复后的主体、目标节点/稳定身份、时间窗和可定位结果。引用 C32 已交付方法，缺方法优先无法确定并区分缺采样。**保留 NPU 独立未知、S1/R1、安全授权及回退拆分；不要求实测、现场值、扩大生产权限或制造结果，无负向授权不执行。**

## 5. Acceptance 与最终计数

| T05-01 acceptance / 原文件位置 | 本轮判断 | 原 ID |
|---|---|---|
| 镜像身份、构建输入、SBOM/签名、拉取策略 / L5403 | 沿用此前完整通过；范围外，不重审供应链 | C30 CLOSED |
| 固定 runtime/Toolkit/CDI、各层与映射分离 / L5404 | 部分满足，未完整通过：逐库归层、稳定映射及分类方法仍缺 | C31 CLOSED（范围外）；C32 OPEN |
| Ascend 独立实现与目标组合 / L5405 | 部分满足，未完整通过：false 假设与五项路径对应认可，完整所选输出/逐库记录及口径同步仍缺 | C33 OPEN |
| 清单、异常/隔离、对照与源案例 / L5406 | 部分满足，未完整通过：两端策略/R1 绑定认可，消费配置对、更新接口/字段、访问恢复关联与映射依赖仍缺 | C34 OPEN |

四条 acceptance：**1 沿用既有完整通过 / 3 未完整通过**。本轮 **0 CLOSED / 3 OPEN（1 P1、2 P2）**，**第二十二次定向复核不通过**，无新增发现 ID。阻断来自未交付的方法、完整所选记录、消费配置与证据关联及口径一致性，**不是 curl DNS 失败、修订映射追加记录、现场值 unknown、没有实测或未证明整栈兼容**；不改计划或正文审核状态。

## 6. 结构校验与写入审计

- 写入前原仓库 `PYTHONDONTWRITEBYTECODE=1 make check` **PASS：96 content entries / 440 sources**；只验证结构与本地链接，不验证远程文字或技术正确性。
- 写入后原仓库 `PYTHONDONTWRITEBYTECODE=1 make check` **PASS：96 content entries / 440 sources**。
- 独立副本 `/private/tmp/b21-t05-01-recheck22-1ip6Wa/validation` 使用原仓库虚拟环境 Python、禁写字节码执行 `make check` / `make build`，均 **PASS：96 content entries / 440 sources**；只在副本生成 `build/catalog.json` / `build/catalog.md`，不改原仓库生成文件。首次副本准备漏复制既有 catalog，检查因 `docs/first-fill-status.md` 的两个既有本地链接缺目标而失败，build 未执行；复制原仓库已有两个 catalog 后重跑通过，不是正文技术错误或作者内容修改。本节补记后的最终报告同步至副本复跑相同校验/构建。
- 摘要审计覆盖 **405 个**既有文件：无修改或删除，唯一新增为本报告；去除本报告后的 Git 状态与开始时一致，六个指定输入及补读来源记录均保持 §2 摘要。`git diff --check`、本报告行尾空白检查通过；仅有 C32/C33/C34 三个原发现标题，优先级与 OPEN 状态一致。
- 未修改 `src/kb/` 或测试；内容审阅报告不需要新增测试或执行 `make test`。

**最终技术结论：B21-C32、B21-C33、B21-C34 均 OPEN；0 CLOSED / 3 OPEN，第二十二次定向复核不通过。C30/C31 保持此前 CLOSED、范围外；新增落盘进展已认可，不以审阅者补读替代作者完整交付；约定审阅配置不是已独立确认的执行元数据。**
