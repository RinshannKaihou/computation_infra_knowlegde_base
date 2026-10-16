# Batch 21 补交 T05-01 第二十三次定向复核

## 1. 结论、角色与范围

- 日期：2026-10-14（Asia/Shanghai）。执行者：当前 Codex 会话，以独立审阅角色核对作者第二十三轮落盘修订，与作者修订角色分开；未派发其他模型或子代理。
- `gpt-6.1-sol / xhigh` **仅为用户约定，不是已独立确认的执行元数据**。本会话没有可独立核验的实际模型、推理档位或路由证据，不宣称模型一致性或无 fallback 已获独立确认。
- 唯一复核范围：**B21-C32–C34**。剩余关闭条件以[第二十二次复核](batch-21-t05-01-codex-recheck-22.md) L92、L110、L130 为权威；[初审报告](batch-21-t05-01-codex-review.md)用于原 ID、职责与优先级核对。**C30/C31 保持此前 CLOSED、范围外，不重审。** 修订映射只证明落盘改动，不证明问题关闭。
- **0 CLOSED / 3 OPEN（1 P1、2 P2）；第二十三次定向复核不通过。** 本轮认可卡类型两端取值来源的区分、部分分支失败语义、`lib64` 逐库待采字段，以及 CDI 原生/legacy 两端消费类型的逻辑选择；不再把这些进展记成完全未交付。
- 只新增本报告，不修改作者正文、来源记录、修订映射、登记、计划或原仓库生成文件，保留开始时已有工作区改动；不提交、不创建分支。不新增发现 ID，剩余缺口仍归原 ID。
- 未安装组件、拉取/构建镜像、生成 SBOM、运行容器、接入集群、修改运行配置或执行访问、负向、资源更新、恢复实测；上游脚本只读未执行。结构校验与知识库目录构建不属于环境或硬件验证。

| 原 ID | 原优先级 | 本轮状态 | 位置证据与剩余问题 |
|---|---|---|---|
| B21-C32 | P2 | OPEN | 正文 L60、L72、L78、L82–84、L109–114、L118、L131–138：固定扫描/归层连接与逐 ordinal 稳定身份方法仍缺，缺方法/缺采样尚未同步至全部相关记录 |
| B21-C33 | P2 | OPEN | 正文 L90、L92；作者来源记录 L17；登记 L5446：两端来源、失败摘要、逐库字段认可；完整所选条件/输出记录、逐库证据定位及旧宽口径同步仍缺 |
| B21-C34 | P1 | OPEN | 正文 L66、L127、L132–138：消费类型与策略已选；handler/实际消费字段绑定、资源更新接口/字段、成功访问与原负向边界恢复的生命周期关联及 C32 方法依赖仍缺 |

## 2. 输入身份与写入边界

两份指定 SHA-256 前缀均与**当前整文件**吻合；没有沿用前次映射前缀不符的结论。第二十三轮修订节为映射 L294–298，只列 C33/C34/C32 落盘改动。映射 L290–292 的容量失败记录是历史作者记录，不是本轮执行结果或停止指令。

以下完整摘要由本轮独立计算；仓库位置均为输入原文件行号。登记经 YAML 解析计数为 **440 项**。

| 输入 | SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md)，指定前缀 `521b7d540cf11981` | `521b7d540cf11981215937ace24dadf1f5d183671e3e0bd14673696c1bc0888d` |
| [修订映射](batch-21-review-fixes.md)，指定前缀 `eeb8d17cc485c8b7` | `eeb8d17cc485c8b78620494a44330bc788475319658c1a1d0af29110606538bb` |
| [第二十二次复核](batch-21-t05-01-codex-recheck-22.md) | `407792803d0cb897fd1d8eb8b2d3dff0ea1a8db3944ca190a91bb4fe22586a99` |
| [初审报告](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` |
| [任务验收](../../plans/full-coverage-backlog.yaml)，T05-01 acceptance L5403–5406 | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml) | `e774b5c1440bce91a648d10b1ec8bcad6b70eda8e18883a46a60c5a5585c8bb1` |
| 补读：[作者来源记录](batch-21-t05-01-sources.md)，用于前次 C33 口径条件 | `a88ff7db50c3c246567bdbefa3b7825f7bbf6a5c1e3aec35f89e1f302437f6c2` |

从 `README.md`、`docs/authoring-guide.md`、`content-outline.md` 开始，核对适用指令、元数据约定、来源与结构校验边界；未将模型审阅或来源可读当成硬件验证。取证与校验临时目录为 `/private/tmp/b21-t05-01-recheck23-br5UFR`，不把临时输出加入知识正文或来源登记。

## 3. 一次源抽查方法、文字与限制

### 3.1 curl 实际尝试与只读替代通道

对下表 01–12 的精确 HTTPS 地址实际执行只读 GET。源码使用与表中 blob 链接同 ref/path 的 `raw.githubusercontent.com` 地址；文档使用表中原地址。命令形态：

```sh
curl --location --fail --silent --show-error \
  --connect-timeout 8 --max-time 20 --output "$audit_dir/curl-$point.body" \
  --write-out 'http_code=%{http_code}\n' "$url"
```

未用 `-k`/`--insecure`，未关闭默认 TLS 校验，未申请沙箱提权或自定 IP 绕行。**12 次全部在 DNS 阶段失败：退出码 6、HTTP 000、Could not resolve host**，涉及 `raw.githubusercontent.com`、`docs.pytorch.org`、`docs.nvidia.com`。没有 curl HTTP 正文，不能称 curl 200、TLS 握手/校验成功或取得上游 HTTP 字节摘要。请求、状态及错误保存在临时目录的 `curl-urls.tsv`、`curl-01.meta` 至 `curl-12.meta` 和相应 `.stderr`。

随后采用用户允许的只读替代通道：GitHub 连接器 `fetch_file` 实读固定 ref 的原文件区间，网页读取通道实开版本化 PyTorch/NVIDIA 文档并核对相关章节文字；不是只判可达性。源码坐标以连接器请求的原文件区间为准，不把网页阅读器行号转作 GitHub 锚点。网页可能经缓存/解析，不能等同本机 curl 的新鲜原始字节；连接器 Git blob SHA 也不是 curl HTTP SHA-256。未执行上游安装/运行示例，不以搜索片段、作者自述或前次摘录替代本轮实读，不独立背书历史 curl 成功记录。

### 3.2 本轮实读点与有限支持范围

Ascend 文件均固定 commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e`；这些抽查定位于既有登记的来源，不新增来源项。下表的编号仅是取证点，不是发现 ID。

| curl 点 | 精确一次源 / 本轮实读位置 | 核对文字与有限支持范围 |
|---|---|---|
| 01 | [build/scripts/base.list](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/scripts/base.list)，完整五行 | 五个宿主候选为 driver/lib64、driver/include、dcmi、npu-smi、queue_schedule 对应的绝对路径；不是逐库身份/版本或挂载成功记录 |
| 02 | [run_main.sh](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/scripts/run_main.sh)，L278–315 | 未选五个产品安装分支时复制默认列表；各分支最终配置文件名为 base.list 并设 440 权限，不证明所选产品受支持或现场安装成功 |
| 03 | [cli/src/u_mount.c](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/cli/src/u_mount.c)，L45–240 | 目标按 rootfs 与源路径拼接；源 stat 失败可跳过，建目标/校验/bind/只读 remount 可失败。NODRV 提前返回限定该 CLI 的 DoMounting，不证明整个 runtime 没有其他挂载 |
| 04 | [runtime/process/process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go)，L45–405、L455–830 | 核到芯片识别、宿主节点信息→OCI 节点/allow 许可、14 个 310B 辅助尝试、manager 回退与目标重命名、dvpp 前置及 UB 目录处理。14 项失败仅警告；manager 取值/注入可失败。310B 提前返回，不执行后续 GetProductType。非 VIRTUAL 仍可能创建 vdevice 并追加 poststop；LD_LIBRARY_PATH 与独立 DP mounts 不等于 hook 库挂载 |
| 05 | [device-plugin common.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go)，L100–139 | 整数 ID 逐个转字符串并逗号拼接；写 options；插件 RealCardType 为 310B 才写 allow-link；!PresetVDevice 才写七个 worker 环境项。不证明插件取值与 runtime 芯片返回相同 |
| 06 | [hook/process/process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/hook/process/process.go)，L85–225、L237–440 | 默认组 base；每份列表先计扫描行，再按 stat 分类文件/目录，构造 CLI 参数，另处理 UB 挂载候选。默认 lib64 入选是目录候选入选，不是逐库分类证明 |
| 07 | [Syft README@v1.54.1](https://github.com/anchore/syft/blob/v1.54.1/README.md)，L1–110，Features/The basics | 核到镜像/文件系统等扫描对象与输出格式入口；不替作者固定扫描范围、必要字段、包/文件/层解析及逐库连接键。不重开 C30，不断言其他工具材料不存在 |
| 08 | [PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html)，Device-agnostic code 的 CUDA_VISIBLE_DEVICES 段 | 该段说明控制 PyTorch 可用 GPU 范围，不交付 ordinal→分配/CDI→完整节点→稳定身份连接方法；不据此断言其他身份接口不存在 |
| 09 | [NVIDIA server.go@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go)，L280–507 | Allocate 校验请求 ID；按策略转换/去重并输出 CDI 或选择环境变量/volume mounts。全 CDI 策略提前返回，非 CDI 路径另受 PassDeviceSpecs 控制；插件策略不替代消费端配置 |
| 10 | [Toolkit 1.20.0 troubleshooting](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html)，NVML/SELinux、访问丢失、Affected Environments | 核到禁用 SELinux 的隔离代价；hook/legacy 下更新可能丢失 GPU 访问、删除重建后恢复的源场景；CPU/内存调整与 systemd reload 有不同条件，不交付本文所选更新接口/字段或访问结果 |
| 11 | [Toolkit 1.20.0 CDI support](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html)，Running a Workload、Non-CDI-Enabled Runtimes、Setting the CDI Mode Explicitly | 独立 runtime hook 与 CDI 可冲突；NVIDIA_VISIBLE_DEVICES 在显式 CDI 模式也可消费，模式由 runtime 配置决定。故 envvar/无插件 CDI 引用不能替代消费配置对 |
| 12 | [containerd CRI config@v2.4.1](https://github.com/containerd/containerd/blob/v2.4.1/docs/cri/config.md)，L1–385，Config versions/Runtime classes/Full configuration | 核到 version 3、default_runtime_name、runtimes.<handler>.runtime_type/options.BinaryName、RuntimeClass→handler、runtime 分区 cdi_spec_dirs。支持消费设计所需字段，不证明本文两端已经将这些字段绑定到各自选择；不重开 C31 |

连接器返回的关键 Git blob SHA：`base.list=4ea1b223fdeed19fed7fdf1a3b4457b8ddd747b3`；`run_main.sh=9be36636ff13c480c57342b81c78f4b74e95675b`；`u_mount.c=d85fd8155a1805edaf509b047c6441bcdc603e12`；runtime `process.go=acbd7a1ec0703498abfcfcb6ce1aa493069091b1`；`common.go=6cd038e9f1d67a8a913aa4bb1301692f177b3dbe`；hook `process.go=816212afa5f69b8edfb1554d3935af2ebcd28f06`；Syft `README.md=9ffd2affa3b00031ea1fd01ee3fe228379978492`；NVIDIA `server.go=9281b48ef52f9eda9cbed6d98491729da85b5a75`；containerd `config.md=3a206263f4f9e76b6ca14110461b8661a03b1619`。这些是连接器返回的文件身份，非独立 curl 下载摘要。

## 4. 逐项定向复核

### B21-C32 — P2 / OPEN

**权威条件：** 前次复核 L92。**位置证据：** 正文 L60、L72、L78、L82–84、L109–114、L118、L131–138；本轮映射 L298。

**认可/保留：** 宿主内核驱动、注入用户态组件和镜像库分层，Allocate/CDI/edits/OCI 连接以及节点/许可分离继续认可。L112 已区分缺方法/缺采样，L118 已规定缺映射方法优先无法确定；本轮不把这些说成完全没有分类，也不重开 C30/C31。

**仍未满足：**

1. L60/L72 仍用“所选扫描配置”“来源层字段，以实际输出为准”代替固定范围、必要字段、包/文件路径与来源层解析和连接键。层清单、diff_ids、annotations 及链条箭头没有交付逐库来源→最终挂载→容器目标的连接方法。抽查 07 支持工具入口，不是要求取得本轮真实 SBOM。
2. L78 明示稳定物理标识映射方法“未交付，unknown”；L82–84 仍是待填表。尚无固定来源支持的逐 ordinal 可见集快照→分配 ID/CDI 名或传递字段→完整节点（类型/major/minor/路径与来源）→稳定身份规则。抽查 08 仅支持可见范围管理，数量/编号一致不能替代关联。
3. 分类尚未完整同步：L109 的“未记录即缺失”、L110 的“无法确定写 unknown”、L111 的“同上”，以及 L114/L131–138 的比较没有共同的缺方法/缺采样原因、具体缺项与证据记录规则。承认方法未交付与如实保留 unknown 是正确边界，不等于完成该方法。

**剩余关闭条件：** 按固定来源交付所选扫描范围、必要字段及逐库归层/来源连接；交付完整逐 ordinal 稳定映射规则，把缺方法/缺采样原因、具体缺项和证据定位格式同步至核对表、清单与 C34 比较/判定。**现场值可 unknown；不要求拉镜像、生成 SBOM、审计全部 cataloger、采设备或实测，不重开 C30。**

### B21-C33 — P2 / OPEN

**权威条件：** 前次复核 L110。**位置证据：** 正文 L90、L92；映射 L296；作者来源记录 L12、L17；登记 L5446、L5457、L5462。

**本轮新增认可：**

- L90 已分开插件 `ParamOption.RealCardType` 与 runtime `GetChipName()`→`GetDeviceTypeByChipName` 的取值端点，明确两者一致性 unknown；不再指称完全没有两端来源区分。该区分不构成两端值一致或目标组合支持证据。
- L90 新增 14 项失败仅警告、manager 回退、dvpp 前置、UB stat/跳过子目录的分支摘要；抽查 04 支持这些有限机制，不再指称完全没有失败语义。
- `driver/lib64` 目录候选下已新增库文件名、版本、hook 入选、CLI 目标路径、挂载结果的逐库待采格式，保留缺值 unknown；不再沿用“只有笼统身份/版本待采、没有逐库字段”的前次表述。
- 此前的 `UseAscendDocker=true`、空输入 options、base 组、默认安装分支、310B 示例及 `PresetVDevice=false`、五项路径/目标对应、条件化 vdevice/poststop 均保留认可。未选五份产品变体不是必须全部审计的任务。

**仍未满足：**

1. **所选条件和输出还未完整连接。** L90/L92 仍未选择产品形态与输入 ID 的设计形式，亦未将插件侧卡类型条件、runtime 侧所选芯片条件与其输出分支连成一份可填写记录。14 个辅助候选、manager 回退后的宿主→容器重命名、UB 目录/条目、worker/控制环境及节点/许可仍主要用函数名/组名与通用公式概述；缺所选候选集合及输出字段、条件/失败、证据位置的共同连接。可复用公共字段规则，不要求机械重复全部代码或填真实设备号。抽查 04 明确 manager docker 路径可映射为容器 manager 路径；310B 已提前返回，不要求它执行后续 GetProductType。
2. **逐库待采字段有进展，证据关联未齐。** 新格式没有给出采样/证据定位、具体缺项/原因，以及父目录候选→库子路径→最终挂载记录的可核对连接。抽查 06 的 hook 是对列表中的 lib64 目录项入选，03 的 CLI 是目录挂载；“逐库 hook 入选与否”须说明它记录的是父候选条件还是另有采样依据，不能暗示 hook 已逐库分类。实际库名、版本、挂载结果可待采，不要求检查全目录或虚构任何库。
3. **旧宽口径仍未完整同步。** L90 仍两次写“runtime 库注入语义未核对”，另写“实际库挂载来源/目标/白名单未取”，未限定为所选逐库记录或现场结果；“所选变体内容……未读”仍未区分已读默认 base 与未选五份产品变体。作者来源记录 L17 仍将实际库挂载/白名单/hook 可执行/dcmi 完整实现合列 unknown。登记 L5446 的四子目录未见不改判为全树检索错误，但仍缺源码列表在 build/scripts、安装后文件为部署产物的明确区分及与 install 登记的关联；L5457/L5462 已正确登记源码链，不替代这些位置的同步。

**剩余关闭条件：** 保留本轮认可的两端来源、失败摘要及逐库字段，补所选产品/输入 ID 设计与两端条件连接；以可复用规则交付完整节点/许可/环境、manager/dvpp/UB 与条件化 vdevice/poststop 的所选记录，含来源、目标、失败/跳过条件与证据位置；完善逐库待采证据关联。同步正文/作者记录/登记旧宽口径，明确**机制已读、所选记录未交付、现场未采**三分。**现场文件/设备号/库版本/结果可待采，支持交集可 unknown；不要求安装、执行脚本、实测、完整 DCMI/全部白名单或 CLI 审计。**

### B21-C34 — P1 / OPEN

**权威条件：** 前次复核 L130。**位置证据：** 正文 L66、L118–125、L127、L131–138、L140–142；映射 L297。

**本轮新增认可：** L132 不再只列插件策略集合，已逻辑选择 CDI 原生端与 legacy hook 端，分别组合 `[cdi-cri]`/qualified 名/cdi_spec_dirs/CDI 支持/edits 和 `[envvar]`/NVIDIA_VISIBLE_DEVICES/legacy hook/无 CDI 引用，并将计划外字段判混合→无法确定。**不再指称两端消费类型或模式意图完全未选**。此前的两端单元素策略集合、换权限变体的 S1/R1 绑定、完整许可比较对象、负向授权及回退/更新/重建拆分继续认可。

**仍未满足：**

1. **逻辑消费类型不等于字段级消费配置对。** L66 已有配置键清单，L132 已有类型选择，认可两者；但未把各端 Pod/RuntimeClass/default→handler→低层 runtime/包装器及 Toolkit mode 的关键字段/设计取值绑定。`cdi_spec_dirs` 可达和“legacy runtime hook”是条件描述，不是这份绑定。抽查 11 明示环境变量也可走 CDI，09 的非 CDI 输出还受 PassDeviceSpecs 控制；因此无插件 CDI 引用不直接证明最终消费端无 CDI/并行注入，仍须对所选配置限定并排除旁路。站点名/实际路径/旧新实测值可待填，不要求全模式审计或重开 C31。
2. **资源更新接口与完整字段仍缺。** L137 仍把 CPU 限制的 CRI 更新对象/OCI linux.resources.cpu 写成“候选”“固定字段未取，unknown”，未选接口、完整字段、单位/语义和旧新记录格式，亦未绑定同一次更新前后采样。抽查 10 支持源场景，不替作者交付更新设计；镜像/驱动回退和重建不是该更新变体的替代。
3. **成功访问与原负向边界恢复的可定位设计关联仍缺。** L127 R1 与 L133 给出了访问/allow 比较名词、audit/AVC、配置摘要及主体/节点/时间窗，但尚未选择受控成功访问操作及结果记录形式，也未交付单独授权的负向拒绝记录与公共连接规则。L135–138 的注入集和“同上”不能关联各变体生命周期前后、恢复后的主体、完整目标节点/稳定身份、时间窗及正负访问结果。无拒绝事件、配置摘要或可见集恢复不能替代成功访问和原负向边界恢复；缺负向授权时仅记未执行，不制造结果。
4. **C32 方法依赖未闭合。** 三单比较仍依赖未交付的完整稳定映射，缺方法/缺采样原因与具体缺项未统一同步。这是 C32 原缺口的依赖，不新增发现、不重复计数，也不替代前三项独立设计要求。

**剩余关闭条件：** 保留已选消费类型与策略，落实两端 runtime 模式/handler 的字段级消费配置对、设计取值与旁路排除；选定资源更新接口、完整字段、单位/语义及旧新记录格式；完善成功访问和原负向边界恢复的设计记录，以公共连接规则对应各变体生命周期前后及恢复后的主体、目标节点/稳定身份、时间窗和可定位结果。引用 C32 已交付方法，缺方法优先无法确定并区分缺采样。**保留 NPU 独立未知、S1/R1、安全授权与回退拆分；不要求实测、现场值、扩大生产权限或制造结果，无负向授权不执行。**

## 5. Acceptance 与最终计数

| T05-01 acceptance | 本轮判定 | 对应范围 |
|---|---|---|
| 镜像身份、层、构建输入、SBOM/签名与拉取策略 / L5403 | 沿用此前通过，不重审，不据此宣称已有供应链系统 | C30 已 CLOSED，范围外 |
| 固定运行时/NVIDIA 版本与各层边界 / L5404 | 部分满足，未完整通过：层间记录/稳定映射方法仍缺 | C31 已 CLOSED（范围外）；C32 OPEN |
| Ascend 独立实现与目标组合 / L5405 | 部分满足，未完整通过：新增来源区分/失败摘要/逐库字段认可，完整所选记录与口径同步仍缺 | C33 OPEN |
| 清单、异常/隔离、对照与源案例 / L5406 | 部分满足，未完整通过：逻辑消费对认可，字段级配置、更新接口/字段、访问恢复关联与映射依赖仍缺 | C34 OPEN |

四条 acceptance：**1 沿用既有完整通过 / 3 未完整通过**。本轮 **0 CLOSED / 3 OPEN（1 P1、2 P2）**，**第二十三次定向复核不通过**，无新增发现 ID。阻断来自未交付的方法、完整所选记录、消费字段与证据关联及口径一致性，**不是 curl DNS 失败、现场值 unknown、没有实测或未证明整栈兼容**；不改计划或正文审核状态，不以审阅者补读替代作者交付。

## 6. 结构校验与写入审计

- 写入前原仓库 `PYTHONDONTWRITEBYTECODE=1 make check` **PASS：96 content entries / 440 sources**；只验证结构与本地链接，不验证远程文字或技术正确性。
- 写入后原仓库 `PYTHONDONTWRITEBYTECODE=1 make check` **PASS：96 content entries / 440 sources**。
- 独立副本 `/private/tmp/b21-t05-01-recheck23-br5UFR/validation` 使用原仓库虚拟环境 Python、禁写字节码执行 `make check` / `make build`，均 **PASS：96 content entries / 440 sources**；只在副本生成 `build/catalog.json` / `build/catalog.md`，不改原仓库生成文件。最终校验记录随本报告同步至副本后复跑。
- 摘要审计覆盖 **407 个**既有文件（不含 `.git`、`.venv` 与 Python/pytest 缓存）：无修改或删除，唯一新增为本报告；去除本报告后的 Git 状态与开始时一致，六个指定输入及补读来源记录保持 §2 摘要。`git diff --check`、本报告行尾空白及三个原发现标题/优先级/状态检查通过。
- 未修改 `src/kb/` 或测试；内容审阅报告不需要新增测试或执行 `make test`。

**最终技术结论：B21-C32、B21-C33、B21-C34 均 OPEN；0 CLOSED / 3 OPEN，第二十三次定向复核不通过。C30/C31 保持此前 CLOSED、范围外；新增落盘进展已认可；约定审阅配置不是已独立确认的执行元数据。**
