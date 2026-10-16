
## T04-06 修订（claude-opus-5-5 初审 B21-C01–C09 → 本轮处理全部 9 项）

- 文件/ID 按计划对齐改名（storage-workload-baselines）；tag 对象 bef04e7b 记录。
- C01：fio http/rados 引擎行（终点＋限制）；rados 标 RADOS 层；RGW 基准 unknown 改述。
- C02：MLPerf 终点 host DRAM＋sleep；训练/checkpoint 分列；与 profiler 并列不可比。
- C03：fio 计时起止＋源码行；ramp/status-interval/lat log；跨客户端三工具汇总；knfsd 改服务器侧；口径不可比。
- C04：latency_target/rate 机制；发起/完成区分；指标落字段；三对照记录要求。
- C05：维度→参数映射；direct/invalidate；rados 缓存推论标注；重试 unknown；后端空间定义；计划 ID 改链接。
- C06：I/O Kit＋LNet Self-Test 行；Jobstats/brw_stats 已核；CollectL 性质。
- C07：实现×工具表；训练关联双链接；长尾百分位＋时间序列。
- C08：source_refs 与依据一致；notes 只写实际范围；记录逐条目行号。
- C09：verify 移出终点；rados 约束＋默认值。

## T04-06 第二轮修订（claude-opus-5-5 定向复核 5/4 → 处理 C02/C04/C05/C07）

- C02：MLPerf 终点加节号/行号（§4.1/§4.2）。
- C04：rate 上限纠正＋推论/约定标注；失败重试 continue_on_error。
- C05：计划 ID 改链接（durability/对照行）。
- C07：训练关联精确到节；C01 附带措辞（Ceph 侧未检索到）。

## T04-06 第三轮修订（claude-opus-5-5 第二次定向复核 6/3 → 处理 C04/C05/C07）

- C04：上限值≠实际发出负载，须单独记录发出速率。
- C05：缓存行/T04-02 双链接化；L79 T04-02 §4 链接化。
- C07：L46 计时口径改精确节名链接。

## T04-07 修订（claude-opus-5-5 初审 B21-C10–C18 → 本轮处理全部 9 项）

- 文件/ID 按计划对齐改名；初审报告旧链机械对齐（输入 SHA 不变）。
- 登记新增 OSD 排查页、健康检查页、scrub-repair 测试；博客 kind 沿用 documentation（schema 无博客类，已备注）。
- C10：官方定位链＋JSON 输出保存；read_error 前置；repair 移出可信恢复（权威不可证/标 missing/人工判断）；Filestore/BlueStore 限定＋auto_repair；丢数据标推论。
- C11：博客 FileStore 前提＋Squid 不适用（OSD 页）；两 shard 细节＋先试 repair/noout 差异；主案例换 scrub-repair 测试（函数/行号/判据；tracker 未开 unknown）。
- C12：§5 五类判据表（实现分行；前置/预期/失败/留空/授权；负载恢复引 T04-06 或 unknown）。
- C13：存储侧停止/完成条件自列；训练指南仅下游交接。
- C14：Lustre 改 Ch.35.3/38.1/health_check；RGW 健康未检索 unknown；删 knfsd 句；ext4 errors=；NFS server not responding；责任判据示例。
- C15：故障×实现表；超时行引 nfs(5) 参数；池满/Full OST 分开；凭据逐项；慢盘 health-checks 条目。
- C16：repair/remount/回放分节引源；Lustre 回放/OSD 服务恢复补齐。
- C17：source_refs 与依据一致；plan 不用来源说明；notes 只写实际范围；记录逐主张定位。
- C18：计划 ID 改链接；节名＋锚点；标题/博客措辞修正。

## T04-07 第二轮修订（claude-opus-5-5 定向复核 1/8 → 处理 C10/C12/C13/C14/C15/C16/C17/C18）

- C10：Filestore/BlueStore 限定纠正（无 checksum 材料针对 Filestore）；删"可信副本恢复"指向；记录 unknown 第 6 条澄清（repair 前清单即定位链输出）。
- C12：ext4 重连行（T04-02 §5）；预期全带链接/约定；可读/完整判据对调（get↔diff＋PG 健康）。
- C13：存储侧停止条件三分实现；完成条件逐条链接＋保留上游 unknown。
- C14：Lustre 行 3 格（手册链并入）；Ceph/Lustre 判据示例；ext4 转只读改述。
- C15：凭据/超时格具体化；不适用/unknown 二选一；TOO_MANY_REPAIRS 阈值直写。
- C16：三动作停止条件分列；§38.2.7 要点。
- C17：plan 未用来源理由；记录逐主张拆分＋Ch.36 删除；source_refs 补 exports-5；RGW 登记引用；6258 纠正。
- C18：计划 ID 改链接；L80 移记录；训练指南节名链接。

## T04-07 第三轮修订（claude-opus-5-5 第二次定向复核 1/8 → 处理 C10/C12/C13/C14/C15/C16/C17/C18）

- C10：权威不可证限 Filestore/checksum 不可用；BlueStore 选择 unknown；删可信恢复指向；记录第 6 条澄清。
- C12：ext4 行预期修正；提交行改 §5 设计预期＋§2 unknown；负载恢复标约定；L88 active+clean 归属。
- C13：failed recovery 只停不完成；NFS 停止改可区分＋约定；Ceph 统一约定标注；ext4 条件＋unknown。
- C14：Lustre 3 格修复；两判据示例；ext4 改述。
- C15：凭据 §30.6；超时理由修正。
- C16：§38.2.7 按原文重写；停止信号改可观察。
- C17：记录 L3/L11 订正。
- C18：L90 链接文字；L78 删句；首条措辞。
- 附带：复核报告两处笔误修正（哈希前缀、计划行号）。

## T04-07 第四轮修订（claude-opus-5-5 第三次定向复核 5/4 → 处理 C10/C12/C13/C17）

- C10：权威不可证限 Filestore/checksum 不可用＋BlueStore unknown；删可信恢复指向；记录第 6 条澄清。
- C12：L86 failed recovery 只停不预期；L88 active+clean 改 PG 页＋本库约定；L84 完成判据措辞。
- C13：NFS 停止改可区分；ext4 停止条件新增；完成条件 unknown 沿用。
- C17：source_refs 补 rgw-s3；notes 去内核 NFS；记录第 6 条改写。
- 附带：映射只列落盘改动（本节）。

## T04-07 第五轮修订（claude-opus-5-5 第四次定向复核 7/2 → 处理 C12/C13）

- C12：L73 active+clean 改 PG 页＋本库约定（与 L89 一致）。
- C13：停止条件"任一触发"（四条件）；Lustre 重连预期改 replay/failed-recovery 分支（Ch.38.2/38.1.6 去 38.1.2）。

## T04-07 第六轮修订（claude-opus-5-5 第五次定向复核 8/1 → 处理 C13）

- C13：ext4 停止条件并入停止列表；L87 预期删 failed recovery（只留失败栏）；复核报告两处占位补结果。

## T05-01 初审作废记录（2026-10-14）

- 首轮 opus 别名审阅作废：`modelUsage` 出现 `claude-opus-5`（输出 41k tokens）与 `claude-opus-5-5`（19k）双键，且中途一次回复被安全分类器中断。按审阅约定 fallback 条款，该轮弃用：报告已删除，不留档、不引用、不计数。
- 后续改用全称 `claude-opus-5-5` 固定模型重跑（探针确认单键）。

## T05-01 初审二次作废记录（2026-10-14）

- 全称 `claude-opus-5-5` 重跑仍出现 session 内模型切换（模型自报由 opus-5-5 变为 opus-5，中途再被安全分类器中断）；`modelUsage` 再次双键。按约定本轮亦弃用：未产生报告文件，无需删除。
- 连续两轮同一故障，依 fallback 条款将 T05-01 初审切换回 `gpt-6.1-sol / xhigh`（codex 执行）。

## T05-01 修订（codex 初审 B21-C30–C34 → 本轮处理全部 5 项）

- 登记新增 Ascend device-plugin 实现；containerd/runc/CDI 以 tag 解引用固定（正文未读，见注）。
- C30：构建输入五要素＋注解/config 明文；SBOM/签名分列＋unknown；拉取策略固定要求。
- C31：版本基线四项固定点；CDI 三方区分；config.md/config-linux.md 分指；containerd 表述修正。
- C32：透传三分；分配→注入通道（非框架映射）；权限三分＋框架映射方法。
- C33：Ascend 组件/ref 两路径；目标组合字段＋交集 unknown；ACP 删除；GPU 不套用。
- C34：可填写清单；三类分支表；对照方案；Ascend 源案例链接＋关联说明。

## T05-01 第二轮修订（codex 定向复核 0/5 → 处理 C30–C34）

- 登记新增 containerd CRI/CDI SPEC/vLLM 案例；tag/commit 双核（containerd/runc/CDI）。
- C30：注解 MUST/SHOULD 分级；config 必填/可选；subject 可选；拉取策略 containerd 路径＋digest 限定。
- C31：版本基线四项（containerd CRI/runc/CDI 1.1.0/Toolkit）；三方区分；config.md/config-linux.md 分链。
- C32：透传三分；CDI 样板链；权限三分＋框架映射 unknown；插件前置以 tag 为准。
- C33：Ascend 双路径行号＋Allocate 链；对应端/白名单 unknown；目标组合字段。
- C34：可填写五栏清单；分支表 GPU/NPU 分开＋完成/失败/无法判定；对照展开；案例症状/版本/未复现落页；NVML 情境分开。

## T05-01 第三轮修订（codex 第二次定向复核 0/5 → 处理 C30–C34）

- 登记新增 k8s Images/torch CUDA/syft/cosign/runc-man；正文 source_refs 同步。
- C30：构建三行改记录格式＋缺项判据；SBOM/签名工具固定＋边界；拉取策略改 k8s 路径。
- C31：版本基线补 CRI 字段/runc 手册/CDI 三层身份；config.md 链接修正。
- C32：CDI 样板链实例；权限 UID/GID/allow 分开；框架映射 torch 方法＋NPU unknown。
- C33：分支行号精确（L1087/L1161/Allocate）；消费端 unknown 收窄到包文件。
- C34：五栏模板表实装；NPU 三分支；对照计划表；案例症状落页；NVML 情境分开。

## T05-01 第四轮修订（codex 第三次定向复核 0/5 → 处理 C30–C34）

- 登记/记录同步：SBOM/签名工具行、CDI 三层身份、common.go 输出字段。
- C30：SBOM 范围收敛＋比对边界；拉取策略 k8s 默认化规则；记录同步。
- C31：containerd CRI 字段/runc 手册/CDI 身份；OCI config 链接修正。
- C32：NGC 库记录方法；CDI 单链实例；权限 LSM 方法；框架 torch 方法＋稳定映射三方比对。
- C33：分支行号精确＋Allocate 链；消费端 unknown 收窄。
- C34：五栏模板表实装；NPU 三分支判据；对照计划表；案例症状/版本落页；NVML 情境分开。

## T05-01 第五轮修订（codex 第四次定向复核 0/5 → 处理 C30–C34；只列落盘改动）

- C30：SBOM 比对字段/差异处置；签名信任输入＋结果格式；拉取 k8s 默认化规则；记录同步。
- C31：containerd 值/诊断；runc 对应记录；CDI 三层已定；OCI 错链修正。
- C32：NGC 库记录方法；CDI 单链去 envvar；权限 LSM 关联；框架三方比对＋核对表。
- C33：分支坐标 L1161-1169；common.go 精确引用＋输出字段；消费端 unknown 收窄。
- C34：模板硬件/库行；NPU 判据（缺证据→无法判定）；对照计划表；案例落页；NVML 分开。

## T05-01 第六轮修订（codex 第五次定向复核 0/5 → 处理 C30–C34；只列落盘改动）

- C30：SBOM 比对字段/差异处置；签名 CLI 版本锚＋信任输入；拉取 k8s 默认化规则。
- C31：containerd 值/诊断；runc 对应记录；CDI 身份已定。
- C32：NGC 库留存格式；CDI 单链；框架三方比对＋核对表。
- C33：common.go 精确引用＋输出字段；消费端 unknown 收窄；静态措辞。
- C34：模板硬件/库行；NPU 判据；对照计划表；案例落页。

## T05-01 第七轮修订（codex 第六次定向复核 0/5 → 处理 C30–C34；只列落盘改动）

- C30：签名行补 CLI 同修订三文件位置＋source_refs 登记同步；待确认收窄为未读/未执行/未固定修订。
- C31：containerd 参考值＋来源/handler 核对＋不符判据；runc 同容器 ID＋三处身份/时间窗/日志定位＋不符判据；summary 限定 CDI 为仓库 tag/规范版本。
- C32：Allocate ID→qualified CDI 名→CDIDevices→devices[].name→全局/设备级 edits→OCI 连接规则；宿主/注入组件记录格式；层清单→SBOM 交叉定位（不代替归属）；ordinal＋CDI＋OCI 主设备号，固定依据 unknown。
- C33：消费端检索范围落盘（ascend-docker 404、同级/pkg 未定位）；已读插件静态输出 vs 未读 api 字符串值/runtime 注入区分同步登记。
- C34：请求数量≠Allocate ID；默认/控制 vs 作业节点分别记录；隔离完成改本分支解释完成；对照表主体/时间窗/证据定位/旁路清单/负向组/回到基线；回退更新拆分为版本回退与重建容器两变体；本页摘要 CANN 8.2.RC1 与关键缺项。

## T05-01 第八轮修订（codex 第七次定向复核 1/4 → 处理 C31–C34；只列落盘改动）

- C31：版本头 v2 自动转 v3＋RuntimeClass 显式选择区分基线不符/未生效；runc state JSON＋list `--root` 作用域 vs 状态内容。
- C32：Allocate 角色纠正（DevicesIds 校验→策略转换去重→qualified 名→CdiDevices）；全局/设备级 edits→OCI 三对象；核对表加最终 OCI 列；SBOM 缺项逐项 unknown。
- C33：纠正检索错误，选定同 commit ascend-docker-runtime；README＋process.go 消费链（可见变量解析/挂载/cgroup/库/hook）；连接插件输出→runtime→最终 OCI；vdevice/dcmi/白名单未审计。
- C34：设备集合边界（公共控制 vs 获配 vs 请求数量 vs 逻辑集）；NPU 语义缺失→无法确定＋访问完成条件；单变量逐项；负向组区分＋安全停止；重建旧新对象分别记录；资源更新对照拆分。

## T05-02 首轮修订（claude 初审 B22-C01–C11 → 处理全部 11 项；只列落盘改动）

- C01：终态条件延迟语义纠正（终止 vs 删除分离）；排查表拆两行；引用 TestDelayTerminalPhaseCondition。
- C02：podReplacementPolicy 入节＋L48 转述纠正；重建行加 terminating/策略；新旧并存标推论；引用替换测试。
- C03：Workload 命名格式＋反查＋文档不一致声明；-attemptN 归 PR；身份/代次对照表；记录/登记同步。
- C04：账本分终止/重试/取消三情形＋字段/指标/测试；身份步修正；ResourceQuota 范围声明。
- C05：状态转移链；调度事件移控制面行；Pending 收窄。
- C06：删除传播默认孤立、节点失联 recovery、重排循环、失败原因分流四行。
- C07：驱逐/去活按因区分；resource-in-use finalizer＋保留策略；v1beta2 为准。
- C08：属主/GC/三步记账纠正；新增 api-gc 登记。
- C09：K8s≥1.29 交集声明＋门控表。
- C10：source_refs/evidence 与依据一致；复用理由；Kueue 范围划分；测试文件行号。
- C11：措辞五处（不必/输出列/事件顺序/ready 口径/Started 同名）。

## T05-01 第九轮修订（codex 第八次定向复核 0/4 → 处理 C31–C34；只列落盘改动）

- C31：v3 完整键＋关联链＋确证/无法确定两档判据；runc state 七字段＋stopped-PID-zero＋关联规则。
- C32：kind+name 匹配＋全局/设备级应用条件；linux.devices vs resources.devices；mount/env 落位；server.go 精确引用三处同步；宿主→挂载→目标可追溯；核对表 OCI 列。
- C33：LD_LIBRARY_PATH 改 env 与库挂载区分；条件链（空/void/VIRTUAL/VdeviceID）；api 键/产品/manager/UB 逐字段关联。
- C34：清单加库关联/稳定身份行；NPU 注入缺失门槛优先；单变量逐键（CDI 开关/handler、allow、replicas、CPU）；主体/时间窗逐变体；安全停止＋访问/负向边界恢复。

## T05-03 首轮修订（claude 初审 B22-C12–C21 → 处理全部 10 项；只列落盘改动）

- C12：节点动作表（DOWN 终止作业/RESUME 非状态/UNDRAIN 不改 base）；INVAL 行＋GRES 互引；ReturnToService 0/2＋有效配置。
- C13：健康职责表（探测/校验/脚本/drain）；GPU 运行期健康 unknown；登记扩 slurm.conf 范围。
- C14：sacct -D 改 duplicates；样板按四场景分组＋PERFORMANCE 提醒；test12.7 目的引用。
- C15：scancel 信号四情形重写。
- C16：GRES 绑定行；GPU 编号映射/环境范围/drain 口径/MIG；TRES 记账前提。
- C17：重排上限/清理卡住/预留约束/终止原因分支行。
- C18：gang 分时辨义＋L109/L131；成组资源条件条目（全有或全无 unknown）。
- C19：文档默认与站点实际分开（KillWait/JobRequeue 等）。
- C20：tag/commit；补丁级由路径确定；用例精确文件名；许可 notes。
- C21：措辞（后缀/FAIL/RESUME/无需drain/交互取消/加权/TRES/库杀/检测值/NPU 指 Ascend）。

## T05-01 第十轮修订（codex 第九次定向复核 0/4 → 处理 C31–C34；只列落盘改动）

- C31：v3 键事实纠正（独立 images/runtime 插件、`.containerd.runtimes.<handler>`、default_runtime_name、RuntimeClass→handler）。
- C32：稳定映射方法改 unknown＋无法确定格式（不再写仅 major 旧法）。
- C33：VIRTUAL 提前返回 vs CreateVDevice 解串；空/void 只 gate 设备-hook 分支；env/库路径/DP-mounts 独立。
- C34：NPU 全分支语义缺失优先门槛；replicas 改副本计数对照；单变量逐完整键；主体/时间窗逐变体；漂移触发＋访问/负向恢复。
- 记录/登记已读-未读范围同步。

## T05-03 第二轮修订（claude 定向复核 5/10 → 处理 C12/C14/C16/C17/C21；只列落盘改动）

- C12：节点动作段移出表格（另立段落）＋表格完整性自检；待确认收窄为前态×新态组合/全有或全无/站点实际值。
- C14：测试读取范围诚实表述（头注释＋审阅者行区间）；记录/登记同步。
- C16：编号映射引文补全（硬件/OS 变更＋bootup 检查要求）。
- C17：Cleaning/节点 DOWN 分支行；样板按四场景分组＋`scontrol completing`（scontrol 页有出处，已独立复核原文）；终止/PENDING reason 分开。
- C21：Billing TRES 纠正（不直接参与 priority）。

## T05-03 第三轮修订（claude 第二次定向复核 1/4 → 处理 C14/C16/C17/C21；只列落盘改动）

- C14：L140 改审阅者取证表述；存在性三处同步；页数改二十＋清单补 sacct。
- C16：引文改原文连续片段；对账推论标注；`is omitted from the node with an error`。
- C17：L150 改 `scontrol completing`；失败组加 `-t all`＋MinJobAge 窗口。
- C21：L132 第三列改 PriorityWeightTRES 按类型加权；L71/L72 去重；L99 加 prolog_epilog 出处；记录同步。
- 范围外：L88 拆标题行＋段落。

## T05-01 第十一轮修订（codex 第十次定向复核 0/4 → 处理 C31–C34；只列落盘改动）

- C31：v3 完整键记录清单（独立插件/default_runtime_name/runtimes/options.SystemdCgroup/RuntimeClass→handler）；state.go/list.go 直接链接。
- C32：稳定映射诚实边界（框架 ordinal 侧 unknown＋无法确定格式；分配 UUID/index→CDI→OCI 三方为已有方法）。
- C33：选定 UseAscendDocker=false 原生挂载分支＋字段对应表；库/hook/白名单未取。
- C34：L116 门槛引用；handler 对/allow 首条/replicas 资源名/CPU 候选逐键；隔离对照收窄＋命名 S1/R1 集合。

## T05-03 第四轮修订（claude 第三次定向复核 3/4 → 只剩 C21；只列落盘改动）

- C21：删 L135 第三列错误原句；MinJobAge 改最短保留时间；记录首轮十九页＋sacct 审阅者补取诚实表述。

## T05-01 第十二轮修订（codex 第十一次定向复核 0/4 → 处理 C31–C34；只列落盘改动）

- C31：options.SystemdCgroup 完整键＋条件化参考值；L144 待确认改消费端输出 unknown。
- C32：判定栏加无法确定格式（诚实边界；扫描/稳定方法仍 unknown）。
- C33：拆两条互斥路径，选定 env/wrapper 路径；原生 DeviceSpec 消费端 unknown；删 rw→rwm。
- C34：模式规则（非名称）；allow 目标选择＋顺序上下文；NPU 独立对照；镜像/驱动回退拆分；S1/R1 逐变体关联。

## T05-01 第十三轮修订（codex 第十二次定向复核 0/4 → 处理 C31–C34；只列落盘改动）

- C31：default_runtime_name/runtime_type 完整表头；去重第十二轮节。
- C32：示例判定加无法确定（扫描/稳定方法仍 unknown，诚实边界）。
- C33：worker 字段级条件拆分（ID/options 无条件、allow-link 按卡、worker 组按 !PresetVDevice）。
- C34：GPU 通用门槛同步；混合路径排除规则；示例判定同步。

## T05-01 第十四轮修订（codex 第十三次定向复核 1/3 → 处理 C32–C34；只列落盘改动）

- C32：判定/清单缺失分类表述（诚实边界；扫描/稳定方法仍 unknown）。
- C33：登记 worker 条件同步；产品/条件对应表（芯片→manager/VIRTUAL→vdavinci；实际值 unknown）。
- C34：模式对排除规则（CDI 自身 hook vs 独立 hook）；allow 完整比较对象；清单缺失分类。

## T05-01 第十五轮修订（codex 第十四次定向复核 0/3 → 处理 C32–C34；只列落盘改动）

- C33：VIRTUAL 摘要纠正（options 含 VIRTUAL 即提前返回，不进 CreateVDevice/poststop；vdavinci 选择为另一独立判断）。
- C34：模式对传递策略组合（cdi-cri/envvar/volume-mounts 可多选）；R1 证据对象格式逐变体绑定。
- C32：清单缺失分类（诚实边界；方法仍 unknown）。

## T05-01 第十六轮修订（codex 第十五次定向复核 0/3 → 处理 C32–C34；只列落盘改动）

- C33：hook 可执行行为取证（DoPrestartHook 控制流、白名单 .list 机制、CLI 调用参数）；新登记 docker-hook。
- C32/C34：判定/清单分类（诚实边界；方法仍 unknown）。

## T05-01 第十七轮修订（codex 第十六次定向复核 0/3 → 处理 C32–C34；只列落盘改动）

- C33：hook 取证（main 入口＋DoPrestartHook 全流程）；环境变量别名链追踪到 vendored 包（登记/记录同步）；实际挂载结果仍 unknown。
- C32/C34：分类同步（诚实边界）。

## T05-01 第十八轮修订（codex 第十七次定向复核 0/3 → 处理 C32–C34；只列落盘改动）

- C33：纠正模块归属（go.mod replace→兄弟 api default_name.go 四键＋配置目录）；128 行精确化；--options 条件；所选基线（options 空/base 组）＋三分口径。
- C32/C34：分类同步（诚实边界）。

## T05-01 第十九轮修订（codex 第十八次定向复核 0/3 → 处理 C32–C34；只列落盘改动）

- C33：空 options 排除纠正（仅排除 VIRTUAL 提前返回）；allow-link 插件/hook 作用域区分；旧"api 包未定位"口径全清；.list 内容检索边界（四目录未见，部署产物）。
- 登记/记录口径同步（128 行语义、CLI 参数构造已读）。

## T05-01 第二十轮修订（codex 第十九次定向复核 0/3 → 处理 C32–C34；只列落盘改动）

- C33：白名单完整链（base.list 5 项＋5 产品变体＋run_main 选择＋u_mount 消费规则）；纠正“固定树未见”；新登记 install；口径全篇同步。
- C32/C34：分类同步（诚实边界）。

## T05-01 第二十一轮修订（codex 第二十次定向复核 0/3 → 处理 C32–C34；只列落盘改动）

- C33：所选示例基线（310B＋options 空＋base 组＋默认安装分支）＋5 项全选入记录；登记口径同步。
- C32/C34：分类同步（诚实边界）。

## T05-01 第二十二轮修订（codex 第二十一次定向复核 0/3 → 处理 C32–C34；只列落盘改动）

- C33：所选示例基线完整化（310B＋默认安装分支＋5 项全选入记录）；PresetVDevice 所选假设。
- C34：两端完整策略集合（[cdi-cri] vs [envvar]＋混合排除）；换权限配置 R1 逐变体绑定。
- C32：分类同步（诚实边界）。

## T05-01 第二十二次复核执行记录（2026-10-14；未产出报告）

- codex 两次执行均返回 `Selected model is at capacity`（EXIT:1，无报告文件）。第二十二轮修订已落地（`make check` PASS），复核待容量恢复后重跑，不换模型。

## T05-01 第二十三轮修订（codex 第二十二次定向复核 0/3 → 处理 C32–C34；只列落盘改动）

- C33：卡类型两端来源连接 unknown；分支失败语义；lib64 逐库待采格式。
- C34：两端消费配置对（逻辑固定）。
- C32：分类同步（诚实边界）。

## T05-01 第二十四轮修订（codex 第二十三次定向复核 0/3 → 处理 C32–C34；只列落盘改动）

- C33：完整条件表（两端来源＋失败语义＋逐段对应）；逐库待采（父候选条件＋逐库格式）；口径同步。
- C34：R1 成功访问/负向拒绝记录形式＋逐变体绑定。
- C32：分类同步（诚实边界）。

## T05-01 第二十五轮修订（codex 第二十四次定向复核 0/3 → 处理 C32–C34；只列落盘改动）

- C33：完整条件表（示例基线＋逐段对应）；逐库采样依据澄清；口径同步。
- C34：两端字段级消费配置对；R1 阶段×证据绑定规则表。
- C32：分类同步（诚实边界）。

## T05-01 第二十六轮修订（codex 第二十五次定向复核 0/3 → 处理 C32–C34；只列落盘改动）

- C33：失败/跳过三分语义；完整条件表。
- C34：真实配置入口（deviceListStrategy/passDeviceSpecs/BinaryName/Toolkit mode）；R1 逐变体绑定；资源更新诚实 unknown。
- C32：分类同步（诚实边界）。

## T05-01 第二十七轮修订（codex 第二十六次定向复核 0/3 → 处理 C32–C34；只列落盘改动）

- C33：完整记录规则（辅助集合/worker 键/UB/manager 回退逐项）；错误传播精确三分；挂载成功判据替换为来源-目标关联。
- C34：设计取值（passDeviceSpecs/BinaryName/Toolkit mode 所选假设）；R1 公共连接规则。
- C32：分类同步（诚实边界）。

## T05-01 第二十八轮修订（codex 第二十七次定向复核 0/3 → 处理 C32–C34；只列落盘改动）

- C33：worker 七键与生成规则精确落盘；默认设备表展开。
- C32/C34：分类同步（诚实边界）。

## T05-02 第二轮修订（claude 定向复核 2/11 → 处理 C02–C07、C09–C11；只列落盘改动）

- C02：L52 拆分原文引用与本库推论（Pod 数超 parallelism/同 index 多 Pod 为原文；同 rank 双进程/资源双占为推论）。
- C03：身份清单逐项出处（ObjectMeta/Pod 生命周期/Job v1 API/workload L147–163/admission L28–32/jobs L222–240）；Concurrent Admission 标 Alpha 默认关。
- C04：取消分支按 Hold/HoldAndDrain/active=false/删 Job 四触发分别写预期＋不一致判读；reclaimablePods 归运行期；admission 保留改待确认；L5306 改弹性样本；L2707 按原文 It 名。
- C05：转移链逐跳出处；C06：四行补出处＋失败原因五条＋reason unknown；L56 与 failure recovery 对齐。
- C07：删 v1beta1“全集”，改 v1beta2 子集；细分 reason 加 UnadmittedWorkloadsObservability 门控说明（默认关）。
- C09：门控/默认值补齐（JobBackoffLimitPerIndex/JobSuccessPolicy/PodReadyToStartContainers/PartialAdmission）；ElasticJob 改 Beta 默认开＋注解＋文档滞后声明。
- C10：api-gc 新登记；kueue/测试条目范围同步（含 setup_* 三文档、metrics/cluster_queue、kube_features/workload、README 声明）；admission.md 链接；测试文件行号；来源记录 unknown 修正。
- C11：L96 改无序列举＋顺序注记；Hold 截断词修正。

## T05-02 第三轮修订（claude 第二次定向复核 6/9 → 处理 C04、C09、C10；只列落盘改动）

- C04：L88 It 名按原文；L2416 改运行期部分释放样本＋全名；删 Job 分支按传播策略（Background/Foreground 被 GC/Orphan 保留/L4042）；不一致判读加 GC 区分。
- C09：PodReadyToStartContainersCondition 门控名。
- C10：metrics/clusterqueue/setup 三文档/retention/GC/strategy-storage/admission_check/README-安装页/kube_features-workload 链接补齐；来源记录 api-gc 行＋测试行号＋unknown 同步。

## T05-02 第四轮修订（claude 第三次定向复核 6/9 → 处理 C04、C10；只列落盘改动）

- C04：L68 Workload 保留改 Kueue 不主动删（与 L125 GC 区分）。
- C10：L80 stopPolicy 出处；L125 reconciler owner 出处；记录 strategy/storage 归属。

## T05-02 第五轮修订（claude 第四次定向复核 10/11 → 处理 C10；只列落盘改动）

- C10：登记 reconciler.go 归属；记录 L16 同步（含 strategy/storage 归属行）；L130 门控出处；L68 自引用修正。

## T05-05 首轮修订（claude 初审 B22-C22–C30 → 处理全部 9 项；只列落盘改动）

- C22：失败与回退分层表（入队/会话决策/会话关闭/控制器/rendezvous）；Kueue PodsReady 行；unknown 收窄。
- C23：双样板五维观测表＋反例＋对照验收（设计未执行）。
- C24：minMember/minResources 归属纠正；Ready 口径＋文档差异；NotEnoughPods 区分；AddJobReadyFn 命名。
- C25：新旧抢占按动作分写（bundle/allowWholeBundle 默认 true；站点配置 unknown）。
- C26：适用前提改写；Kueue Never 默认＋Fair Sharing/StrictFIFO 代价；Slurm 评估顺序＋fair-share＋预留代价；Slurm 配置参数名。
- C27：Slurm 反例前提修正＋推论标注；Kueue 反例前提/分支/门控 Pending 区分。
- C28：Kueue 来源术语修正。
- C29：删重复段＋概念前置；F12 链接修正；抢占三字段；root/SlurmUser；去设备层。
- C30：登记 tag/commit＋URL；Kueue 许可统一；frontmatter 补全；就近链接；记录方法/行区间。

## T05-05 第二轮修订（claude 定向复核 1/9 → 处理 C22–C27、C29、C30；只列落盘改动，逐条 grep 已核对）

- C22：allocate 跳过前提；unknown 同步（frontmatter/记录/登记）；commit 链接＋行区间。
- C23：样板 B 同因素正反配对（QOS 限额）；TopologyPlacementFailed 来源修正＋门控注。
- C24：Ready 口径＋文档差异；控制器同步句＋actions 登记；链接 commit＋区间。
- C25：gang.go/gangpreempt/gangreclaim 行区间；registry 增 gangreclaim（独立打开全文）。
- C26：Fair Sharing 代价；GrpTRES/FLEX 参数；适用前提措辞。
- C27：L155 阈值 nominal＋borrowingLimit；L152 门控说明。
- C29：删重复段；去设备层；链接文字修正。
- C30：新登记 commit＋tag 对象；registry 增文件；记录行区间＋新登记；正文链接 commit＋区间。

## T05-05 第三轮修订（claude 第二次定向复核 2/8 → 处理 C22–C25、C29、C30；逐条 grep 已核对）

- C22：L94/L95/L97 行区间补齐（enqueue L95–99、allocate L152–169/L313–336/L832–844、running/restarting/util）。
- C23：样板 B 同因素 QOS 配对＋DenyOnLimit 前提；TopologyPlacementFailed 改 workload_types L956–958＋门控名（L149/L150）。
- C24：job_controller_actions.go 纳入登记。
- C25：gangreclaim.go L32–52/L247（正文＋记录）。
- C29：L139 来源差异指向记录新增行。
- C30：新登记 URL 改 commit＋tag 对象；job_info.go 纳入 scheduler-actions；记录补行区间。
- 另：recheck-2 报告 4 处行号笔误机械修正（L48–52 一处未在文件中找到，未改）。

## T05-05 第四轮修订（claude 第三次定向复核 2/6 → 处理 C22、C23、C25、C30；逐条 grep 已核对）

- C22：L95 补 allocate L152–169。
- C23：样板 B 对照加 Partition QOS/OverPartQOS＋AccountingStorageEnforce 前提；门控名三处齐全。
- C25：gangreclaim L247（正文＋记录）。
- C30：job_info/actions/util 行区间入记录；登记已含文件。
- 注：recheck-3 报告"五个→四个"措辞未改——原文"五个前缀中四个给定前缀一致"已准确（前次报告无前缀），改动反而失实。

## T05-05 第五轮修订（claude 第四次定向复核 3/4 → 处理 C23；逐条 grep 已核对）

- C23：对照前提改通用写法（站点实际执行 QOS 限额，站点配置 unknown）；L11 残留清理。

## T05-01 第二十九轮修订（2026-10-17，本会话作者角色；处理 codex 第 28 次复核 OPEN 的 C32/C33/C34；新取证见 batch-21-t05-01-sources.md 第四轮）

- C32-1：§1 SBOM 行交付所选扫描范围与字段——`--scope all-layers`（选定理由：逐层归属；默认 squashed/deep-squashed 见 scope.go L8–24，flag/默认见 catalog.go L41/L78/L228–233）＋`syft-json`（schema 16.1.11，constants.go L6）；必要字段 name/version/type/foundBy＋locations[].path/layerID（coordinates.go/location.go，镜像源 layerID＝层 digest）。§2 镜像自带库行交付逐库连接键：layerID→层清单（diff_ids↔layers 同序，image-spec config.md）→宿主来源→挂载→目标；缺项按分类注明。
- C32-2：§2 框架映射行交付 M-ID 五步（可见集快照→分配 ID（先固定 deviceIDStrategy，所选 uuid）→CDI qualified 名→完整节点（类型/major/minor/路径/来源）→稳定身份）；宿主节点↔UUID 复核与框架枚举顺序未取源记 K1；核对表列名同步 M-ID 步骤。
- C32-3：§4 新增公共缺项分类 K1/K2/K3 定义；清单 11 行缺失解释、异常分支表 6 行判定、对照方案引言与基线行全部统一引用。
- C33-1：§3 散文改为逐对象对应表（10 行：作业设备/manager/310B 辅助 14 项/dvpp_cmdlist/UB 设备节点/UB 配置文件/控制键/worker 7 键/LD_LIBRARY_PATH/vdevice+poststop），公共记录规则＝条件｜宿主来源｜容器目标｜结果｜失败/跳过｜证据定位；UB 设备节点（runtime addUBDevice/addDevicesInDir，cgroup rwm）与 UB 配置文件（hook addUBMount：/etc/hccl_rootinfo.json＋/usr/local/Ascend/driver/topo，CLI 文件/目录挂载）分两行。
- C33-2：交付逐库记录规则 M-LIB（父候选＋子库相对路径→宿主完整来源→CLI 目标→容器目标；来源—目标三方关联为挂载证据；CLI 返回/目标可达不单独证明，u_mount.c 反例）；删除①旧判据"挂载成功以 CLI 返回＋目标可达为准"与②③⑤"同①规则"。
- C33-3：worker 7 键字符串定位改指 `api/consts.go` Env 段，ASCEND 控制键留 `api/default_name.go`，两处旧合并表述删除；两处"runtime 库注入语义未核对，unknown"宽口径删除，改机制已读/未读变体（K1）/filled 未采（K2）/现场未执行（K3）四分；§3 口径句、文末待确认清单、本记录 unknown 清单同步四分。
- C34-1：换注入模式变体两端设计取值全部选定——基线端 `runtime_type='io.containerd.runc.v2'`＋`options.BinaryName` 默认空（默认 runc）＋Toolkit mode 不适用（NVIDIA runtime 包装器不在链）；变体端 `options.BinaryName`＝NVIDIA Container Runtime 包装器（安装路径 K2）＋mode＝legacy（排障页措辞；CDI 页 mode 键显式设定/auto→JIT-CDI）；补"envvar 单策略不足以证明 legacy"旁路证据要求（CDI 页显式 cdi mode 节）。
- C34-2：资源更新变体选定接口＝k8s Pod `/resize` 子资源（新登记 src.k8s.pod-resize-v1.32）：字段 requests/limits.cpu、单位（700m/800m）、语义限制、InPlacePodVerticalScaling 门控（alpha 默认关，不可用则退化重建路径）、完成判定（resize 收敛空＋status 一致＋restartCount 不变）、旧→新记录格式、同次更新前后采样关联。
- C34-3：基线行与对照方案引言接通 M-ID＋K1/K2/K3。
- 结构：front matter updated_at→2026-10-17、source_refs 加 src.k8s.pod-resize-v1.32、summary/verification.notes 同步；registry 增 src.k8s.pod-resize-v1.32、syft 与 Toolkit 1.20.0 条目 revision/notes 补第四轮实读范围。

## T05-01 第三十轮修订（2026-10-17，本会话作者角色；处理 codex 第 29 次复核剩余子项；C33-1/C34-1/C34-2 已 CLOSED 不动）

- C32-1：§1 SBOM 行补注 locations＝发现/佐证位置（非成员库路径）并加选文件编目 `files[]`（location.path/layerID＋digests；CLI 默认 selection=owned-by-package、digests sha1+sha256，options/file.go L34–47）；§2 逐库归属改两段：包段（locations/证据层）与成员文件段（cataloger metadata.Files，无清单包类型记 K1）→文件→层经 files[] 同 path 条目 layerID；缺项判据按 K1/K2 分列。
- C32-2：M-ID 补单卡完整闭合段（请求 1×`nvidia.com/gpu`＋uuid：envvar 经 `updateResponseForDeviceListEnvVar` 直写分配 UUID→可见集单元素→ordinal 0；cdi-cri 经 qualified 名→deviceNodes→唯一作业节点→ordinal 0）；多卡枚举顺序、index 策略、宿主复核显式 K1 出所选范围。
- C32-3：summary 改"单卡所选范围闭合＋K1 余项"；清单"宿主内核/驱动"行缺失解释改 K1（NPU 语义未取源）＋K2（记录未采）分列；逐库归属缺项判据区分 K1（成员清单语义未覆盖）/K2（未采/缺字段）。
- C33-2：M-LIB 实际挂载证据改为来源—挂载—目标三方关联：宿主源 st_dev/路径身份 → 容器进程 `/proc/<pid>/mountinfo` 条目（field 3/4/5/9/10，proc_pid_mountinfo(5) man-pages 6.19，新登记 src.linux-man-pages.proc-pid-mountinfo-6.19）→容器内目标；st_dev 一致＋root 子路径一致才记关联成立；镜像内同路径文件不产生新条目故不能替代；CLI 返回/可达仅旁证；缺条目/不一致/未采→K2，未执行→K3。
- C33-3：§3 口径句与来源记录 unknown 清单同步：实际挂载证据未采单列 K2、CLI 执行/部署产物核对 K3；M-LIB 挂载判据属已交付方法（不再压成"仅缺 filled 值"的笼统 K2，也不留 K1 缺段）。
- 登记：新增 src.linux-man-pages.proc-pid-mountinfo-6.19；syft 条目 revision/notes 补 debian cataloger/model file.go/filecataloging/options file.go/selection.go 实读；正文 source_refs 加 mountinfo 项；来源记录加第五轮增补表。

## T05-01 第三十一轮修订（2026-10-17，本会话作者角色；处理 codex 第 30 次复核剩余子项；C32-2 已 CLOSED 不动）

- C32-1a：成员清单解析路径改为 syft-json 键 `artifacts[].metadata.files[].path`，并注明 Go 字段 `Files`/`Path` 与 JSON 键 `files`/`path` 的对应（dpkg.go L55–70，成员记录另带 digest/isConfigFile），避免按错误键解析误报缺项。
- C32-1b：交付 all-layers 同路径跨层归属/消歧规则——候选集（`location.path`==P，每层至多一条，同层多条冲突记 K2）→按 manifest 层序取最上层为运行时有效文件（layerID＝内容来源层、digests＝内容身份，历史候选分列）；包 metadata digest（dpkg md5）与文件编目 digests 比对须加配 md5（options/file.go 可选值）；whiteout/上层删除检测方法未选定单列 K1；包证据层不等于成员层。
- C32-3：summary、待确认清单、来源记录 unknown 清单同步新增 whiteout K1；C32-1 缺项判据已按 K1（成员清单/whiteout 方法）/K2（未采/缺字段/消歧证据不全）分列。
- C33-2a：M-LIB 目录项改按父挂载处理——有效父挂载＝目标目录路径最长前缀 mountinfo 条目，堆叠取 top-most（同页 field 2 注），更长前缀遮蔽另注明；逐库目标全路径＝父挂载点＋子库相对父目录路径；父挂载缺失→整体未挂载（K2）；父挂载成立但子库两侧存在性未核→无法确定（K2）。
- C33-2b：源路径→root 坐标换算——P_src→宿主 mountinfo 最长前缀挂载点 M_host（st_dev）→R＝P_src 相对 M_host 子路径；容器条目须 field 3＝M_host.st_dev 且 field 4＝R（field 4 为源文件系统内部路径，不等于宿主绝对路径），两者一致才记来源关联成立。
- C33-3：§3 口径句 M-LIB 描述同步为"目录父挂载/遮蔽处理与 root 坐标换算判据"；缺项分类补"有效父挂载缺失或遮蔽未判明（K2）"。
- 登记：syft 条目 revision 补 dpkg.go L55–70。
