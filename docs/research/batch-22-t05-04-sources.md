# 第二十二批 T05-04 来源记录

任务：T05-04（修订 `knowledge/05-cluster-platform/device-resource-chain.md`，concept）。作者取证方法：本机 curl 字节级取回固定 commit 原文件（SHA-256 见下表，行数与 GitHub blob 页总行数核对一致），K8s 文档经 FetchURL 只读读取版本化页面；未部署运行、未执行任何集群命令。第 1 轮取证＝NVIDIA k8s-device-plugin v0.20.1 `internal/plugin/server.go` 全 557 行＋`internal/rm/health.go` 全 363 行（健康 ListAndWatch/分配/重启策略，backlog 待核查项）；K8s v1.32 Device Plugins 页重开 Handling kubelet restarts/ResourceHealthStatus/PodResources/部署节。初审（`batch-22-t05-04-claude-review.md`，B22-C31–C38）后第 2 轮取证＝同 commit 新增七文件（main.go/plugin-manager.go/factory.go/nvml_manager.go/rm.go/devices.go/device_map.go，重启/重建/发现失败/ID 构造）＋作者侧重开 Slurm 归档六页核对修订引文。复用取证＝T05-01 固定链（Toolkit 1.20.0/CDI、M-ID 方法，见 `container-image-runtime-baseline.md`）与 T05-03 固定 Slurm 24.11.7 GRES/TRES/cgroup/绑定材料（见 `slurm-jobs-and-device-resources.md` 及其来源记录）。

## 取证哈希表（作者侧，curl 字节级取回；与初审取证表逐一一致）

版本锚：`refs/tags/v0.20.1` tag 对象 `03296a61aeb9943906a1789f978ac3c87e13dfdd`，`^{}`→ commit `487d7a93894b0f3ad08097169593972eb3ca8206`（初审 `git ls-remote` 记录，作者侧引用）。

| 文件（commit `487d7a93`） | SHA-256 | 轮次 |
|---|---|---|
| internal/plugin/server.go（557 行） | `215f04ab2ee4cbfe8f57cbd65064930b852f0c9678b0314c4aa65f93c6c020d9` | 1 |
| internal/rm/health.go（363 行） | `4a955f04be78172901308e3bdd508dc2f78931a4ee5190e2bb6db99f64f6b3b4` | 1 |
| cmd/nvidia-device-plugin/main.go | `e48449efbbc74857b66490fa95622c618cdee396b599d9e1d55c440435609d42` | 2 |
| cmd/nvidia-device-plugin/plugin-manager.go | `1142df235c2722708dbd30c6ad207ec2edb4263f802adfdb8f9bf71de58d589d` | 2 |
| internal/plugin/factory.go | `fe77bc093ebd2f1adb3293510e92b7e58232b31cdccabe5e21dec170f010d2d1` | 2 |
| internal/rm/nvml_manager.go | `198291e96eec164c8f48a66cf763a471a4c231bf430252ca8aa3b6c0bb1f6f26` | 2 |
| internal/rm/rm.go | `f6dced1f504f604455315999026352d27bc8dd8607ec844b06c2080dfa321c1b` | 2 |
| internal/rm/devices.go | `e23a3b2e7d3c9fdee9e5e754ed6c334a163bd1c03d52edf126135fc9a340b062` | 2 |
| internal/rm/device_map.go | `26d83432c1f05c66270167fd6e0744e1891851ccefebc45e1d9ebc641edac2b5` | 2 |
| slurm-24.11.7/gres.html | `4c7a58746e36f07ac7bf43cde934a7342b16698068ceb61ee83debc1c6eccff9` | 2（重开） |
| slurm-24.11.7/gres.conf.html | `21aeb902c64844020cca02fe761eb53a8daec7699020d79c7f36d113f47e294e` | 2（重开） |
| slurm-24.11.7/slurm.conf.html | `f4151769ed29968c7de408809a5acb8f0591865cd525d5f2c70925e847a1ff34` | 2（重开） |
| slurm-24.11.7/scontrol.html | `da776891b3e6070f6e576c5b0f7bcbd62465e976919a1dd62b296050aa4e6d97` | 2（重开） |
| slurm-24.11.7/sacct.html | `d96f8299e0b778c8d4cd04a710969f458f118482b122bb99443716ca9ab677f4` | 2（重开） |
| slurm-24.11.7/sbatch.html | `132d28b42e5cb4f9124734b339a9093707d46e30f0b412d2ec12d11f4a10a00f` | 2（新开） |

K8s v1.32 Device Plugins 页经 FetchURL 读取（第 1 轮），作者侧无哈希；初审侧哈希见其报告（可变网页，只代表当次观察）。

## 主张—来源定位表（ID—精确页面/行—字段/支持范围）

| 主张 | 登记 ID | 精确页面/行 | 支持范围 / 未覆盖 |
|---|---|---|---|
| 注册请求字段（Version/Endpoint/ResourceName/GetPreferredAllocationAvailable） | src.nvidia.k8s-device-plugin-v0.20.1 | server.go Register L229–256（RegisterRequest 字面量 **L242–249**，初审勘误后修正） | 插件侧注册行为 |
| ListAndWatch 首发全量＋健康事件置 Unhealthy 重发；进程内无 Unhealthy→Healthy 恢复路径（FIXME 原文 L277） | 同上 | server.go ListAndWatch L267–285 | 单次进程内语义；重启路径见下行 |
| 重启触发与重建（kubelet.sock Create→全部插件重启；SIGHUP；startPlugins 失败 30 s 重试；c.Run 出错 os.Exit(1)；每次重启经 GetPlugins→plugin.New→getResourceManagers→NewNVMLResourceManagers→BuildDevice 以 Healthy 重建，Unhealthy 无持久化） | 同上（第 2 轮新增） | main.go L196–200/L268–347（事件 L314–321、信号 L330–338、重试 L301–304/L311–312）/L385–420（GetPlugins L392、无设备跳过 L402–405、Waiting indefinitely L415–417）；plugin-manager.go L73–80（WithFailOnInitError）/L85–87（CreateSpecFile）；factory.go L93–128；nvml_manager.go L39–85；devices.go L86–93 | 重建后上报 Healthy 的后果为按代码路径的推论（未执行）；kubelet 侧窗口行为仍需 kubelet devicemanager 源码（unknown） |
| 发现失败分支（fail-on-init-error 默认 true；NVML init 失败 true→报错退出/false→nil,nil 无插件；资源名无设备不启动；GPU 名不匹配资源模式报错） | 同上（第 2 轮新增） | main.go L68–73/L415–417；factory.go L104–108；nvml_manager.go L59–62；main.go L402–405；device_map.go L131 | “缺设备”候选断点 |
| 健康检查启动失败降级与静默关闭（CheckHealth 返回错误才记日志；全禁或 init 失败且 false 时返回 nil 无日志） | 同上 | server.go Start L129–160（L151–157）；health.go L45–48/L50–56 | 降级后账本仍显示健康的后果为推论（标注） |
| gRPC 崩溃重启环（崩溃即重启；相邻间隔超 1 h 计数归零否则累加；计数 >5 即连续第 6 次崩溃 Fatalf；Stop 删 socket） | 同上 | server.go Serve L177–226（环 L186–215、Fatalf L193–196）；Stop L163–174 | 措辞经初审 C37 修正（不写“累计”） |
| 分配响应三策略与 ID 转换（账本侧 ID＝构建期 UUID/UUID::n 与策略无关；运行时 ID 才由 deviceIDStrategy 决定，默认 uuid；uuid 去注解/index 查表取枚举序；envvar 直写 NVIDIA_VISIBLE_DEVICES；CDI qualified 名；volume-mounts；passDeviceSpecs 默认 false） | 同上 | devices.go L86–93/L232–240；device_map.go L110–134/L326–342；main.go L87–104；server.go Allocate L306–320/getAllocateResponse L322–366/updateResponseForCDI L377–409/uniqueDeviceIDsFromAnnotatedDeviceIDs L456–474/updateResponseForDeviceListEnvVar L481–483/updateResponseForDeviceMounts L497–514/apiDeviceSpecs L516–557 | index↔UUID 在插件设备表内确定；枚举序↔宿主 nvidia-smi 序号未取（go-nvlib，K1 收窄） |
| 过期分配拒绝（ValidateRequest 对未知 ID 报 unknown device；共享副本请求数限制） | 同上（第 2 轮新增） | rm.go L83–105；server.go L309–311 | 设备集变化后旧 ID 走此分支为推论 |
| 健康检查机制（NVML event set；eventMask 三类事件；循环只处理 XidCriticalError；启动期三类失败即标记 L80–85/L90–95/L97–102；ERROR_NOT_SUPPORTED 只警告 L104–112；等待错误/UUID 解析失败标记全部；命中标记 L169–170） | 同上 | health.go checkHealth L44–172（eventMask L78、L124–131、L133–136、L145–153、L154–158、L160–167） | NVML 事件到具体硬件故障的语义不在本文件 |
| 健康标记粒度限制（parentToDeviceMap 按物理 UUID 只保留一个条目 L74/L88；MIG 取父 UUID；副本 GetUUID 去注解；事件先查唯一条目再比 GI/CI L154–167；WSL 无健康检查） | 同上（第 2 轮补充） | health.go L74/L88/L154–167；devices.go L50–51/L232–235；rm.go L53–56；nvml_manager.go L71–73 | MIG 多实例/共享副本后果为推论（未执行）；tegra unknown |
| 忽略 XID 清单与开关（硬编码 13/31/43/45/68/109，FIXME 未正式化；DP_DISABLE/ENABLE_HEALTHCHECKS） | 同上 | health.go L29–41/L217–254（ignoredXids L232–240） | 清单完整性与 XID 文档对应未核对 |
| kubelet 重启语义＋不健康设备账本语义＋ResourceHealthStatus＋DaemonSet＋PodResources 端点＋扩展资源整数不可超卖/容器间不可共享＋DevicePlugin 服务无释放回调 | src.kubernetes.device-plugins-v1-32（重开） | 版本化页各节（Handling kubelet restarts、unhealthy devices、Monitoring、Deployment、implementation 服务定义） | 分配释放无专节；删除前后对照为本文设计的核对方法（未执行） |
| GPU 容器映射与框架可见集核对（M-ID） | 复用 T05-01 链 | 镜像运行时基线 §2 | 本文不重复取证；基线 M-ID② 的“分配 ID”措辞与本文 C33 修订的对应关系见批次审计待办 |
| Slurm GRES/TRES/绑定/健康（主体复用 T05-03）＋本轮修订引文（File 递增顺序；cgroup 相对编号 /dev/nvidia1→作业内 "0"；NVML 映射完整原文含 fairly stable 句；gres.conf sanity check 为 File/Cores/Links；MPS/Sharding Count 例外；File 必需/全节点逐设备跟踪；drain 前置否则中止作业；scontrol GRES 修改限制与持久性；节点配置变更重启全体；HealthCheckInterval 默认 0；AllocTres 为 job/step 记账字段；SLURM_JOB_GPUS 全局 ID） | 复用：src.slurm.docs-24.11.7、src.slurm.gres-tres-cgroup-24.11.7 | gres.html L366–402；gres.conf.html L211–215/L280–306；slurm.conf.html L1343–1352/L5300–5306；scontrol.html L1438–1456；sacct.html L644–648；sbatch.html L2926–2928 | NPU 接入保持 unknown；GPU 运行期健康探测保持 unknown |

## 来源差异记录

- 插件登记的前轮区域锚 `server.go L280–438/L448–481` 经字节级取回核对为松散超集（初审确认对所列四函数成立）；精确函数行号为 Allocate L306–320、getAllocateResponse L322–366、updateResponseForCDI L377–409、uniqueDeviceIDsFromAnnotatedDeviceIDs L456–474；RegisterRequest 字面量精确行 L242–249（本记录第 1 轮写 L241–248，初审勘误）。
- server.go ListAndWatch 循环注释自述 `FIXME: there is no way to recover from the Unhealthy state.`（L277）＝单次进程内无恢复路径；初审 C31 补充：任何重启路径都从零重建设备集并以 Healthy 上报（main.go/plugin-manager.go/factory.go/nvml_manager.go/devices.go 链），正文按“进程内无恢复、重启即 Healthy 重建（推论）”写。
- **初审引证勘误**：初审 C35 称 `SLURM_JOB_GPUS` 在 gres.html L622–625（“The GPU IDs of GPUs in the job allocation”）；作者侧取回同一哈希（`4c7a5874…`）的 gres.html 全文 grep 无 `SLURM_JOB_GPUS`（0 命中）。实际定义在 [sbatch.html L2926–2928](https://slurm.schedmd.com/archive/slurm-24.11.7/sbatch.html)：“The global GPU IDs of the GPUs allocated to this job. The GPU IDs are not relative to any device cgroup, even if devices are constrained with task/cgroup. Only set in batch and interactive jobs.”（srun.html 亦有 1 处）。正文按 sbatch 页引用，定向复核时请审阅者复核此勘误。

## unknown 清单

1. 插件进程重启窗口内 kubelet 侧 `capacity`/`allocatable` 表现与既有分配关系（需 kubelet devicemanager 源码）；2. NVML 枚举序（go-nvlib `VisitDevices`）与宿主 nvidia-smi 序号的关系；3. tegra 资源管理器、CDI handler 细节；4. 忽略 XID 清单与 NVIDIA XID 文档的完整对应（源码 FIXME 自述未正式化）；5. Slurm GPU 运行期健康探测（沿用 T05-03 unknown）；6. 全部实测（未执行）。
