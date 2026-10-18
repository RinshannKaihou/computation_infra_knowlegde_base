# 第二十四批 T05-10 来源记录

任务：T05-10（控制面故障、平台恢复与账本核对，procedure 类新文章 `knowledge/05-cluster-platform/control-plane-recovery.md` 的知识材料）。取证轮次：主会话作者角色首轮（2026-10-18）。**本轮四路取证子代理全部因账户 403（Consumer is forbidden）失败**（与 Batch 23 记录的子代理周配额问题同源），按 Batch 23 先例改由主会话直接取证；取证方式为 curl 字节级取回（Batch 22 T05-04 轮先例，SHA-256 见下）＋本地锚点提取，未镜像全文入正文。未执行任何 kubectl/etcdctl/scontrol 命令，未做任何恢复演练；命令仅为文档语义转述。

版本声明：固定 **Kubernetes v1.32**（全部 K8s URL 使用 `https://v1-32.docs.kubernetes.io/` 静态快照，页头自带 "You are viewing documentation for Kubernetes version: v1.32 … static snapshot" 声明）与 **Slurm 24.11.7**（`https://slurm.schedmd.com/archive/slurm-24.11.7/` 静态归档）。`https://slurm.schedmd.com/archive/slurm-24.11.7/high_availability.html` 返回 HTTP 404，且实开归档索引页确认 **24.11.7 归档无独立 HA 页面**（index 无 high_availability/resilience 条目）；HA 口径由 quickstart_admin 的 High Availability 节＋slurm.conf＋slurmctld.8＋troubleshoot 拼装。K8s 侧 `configure-upgrade-etcd` URL 实际落地页标题为 "Operating etcd clusters for Kubernetes"（含备份/恢复节）。

## 本轮取回清单（curl 字节级，2026-10-18）

| 文件 | SHA-256（前 16 位） |
|---|---|
| slurm/archive/slurm.conf.html | f4151769ed29968c |
| slurm/archive/quickstart_admin.html | d7e9c31bac0fe920 |
| slurm/archive/troubleshoot.html | 78f519e4e98c869e |
| slurm/archive/slurmctld.html | 67e677b6d0dd57a0 |
| slurm/archive/slurmdbd.html | 5a81ba6e817a1a83 |
| slurm/archive/slurmdbd.conf.html | 6d2529a81316317d |
| k8s/…/configure-upgrade-etcd（落地 Operating etcd） | 19e528c0790d486b |
| k8s/concepts/architecture/controller | a6aecfb049400117 |
| k8s/concepts/architecture/leases | ec68b97369247821 |
| k8s/reference/using-api/api-concepts | ca03957baf69b180 |
| k8s/reference/command-line-tools-reference/kube-controller-manager | 344a05192c36149e |

MindCluster 侧经 codeload `v26.1.1` tag 源码包列出文件树并实读 `component/clusterd/README.md` 与 `component/ascend-operator/README.md`（37–40 行的组件说明）；GitHub API 同刻限流，树由源码包代替。

## 主张—来源定位表（ID—精确页面/节—支持范围）

| 主张 | 登记 ID | 精确页面/节 | 支持范围 / 未覆盖 |
|---|---|---|---|
| etcd 快照备份与恢复官方前提 | NEW src.kubernetes.etcd-backup-restore-v1-32 | Operating etcd clusters（备份/恢复节，提取文本 L909–968） | 备份：所有 K8s 对象存于 etcd，快照含全部状态、建议加密；`etcdctl snapshot save`（或复制不在线的 member/snap/db）；`etcdutl snapshot status` 出 HASH/REVISION/TOTAL KEYS/TOTAL SIZE。恢复：**先停全部 API server 实例→恢复所有 etcd 实例→再重启**，并建议重启 kube-controller-manager 与 kubelet 以免依赖陈旧数据；`etcdutl --data-dir … snapshot restore`（etcdctl 恢复自 3.5.x 弃用）；同目录恢复须先删旧目录并停 etcd。未覆盖：站点 etcd 版本与快照策略 |
| etcd 扩缩容边界 | NEW src.kubernetes.etcd-backup-restore-v1-32 | 同页 Scaling out 节（L944–951） | 一般规则是不对 etcd 集群扩缩容、不配自动扩缩；3→5 成员是可靠性升级例子；恢复期间 API server 路由（负载均衡器）调整提示 |
| 控制器=控制循环、经 API server 作用 | NEW src.kubernetes.controller-pattern-v1-32 | Controllers（L812–878） | 控制器是 watch 集群状态的控制循环；resource 的 spec 是期望状态；控制器自身多经 API server 副作用生效（Job 控制器不直接运行 Pod，只请求创建/删除 Pod）；大量小控制器而非单体；**控制器可以失败，K8s 设计允许**（另一部分控制面接管工作）。未覆盖：workqueue/informer 内部实现（v1.32 文档未展开，按 unknown 处理） |
| 内建控制器宿主 | NEW src.kubernetes.controller-pattern-v1-32 | 同页 Ways of running controllers（L873–878） | 内建控制器运行于 kube-controller-manager；支持弹性控制面（任一内建控制器故障由控制面另一部分接管）；自定义控制器可独立运行 |
| Lease：节点心跳与组件选主 | NEW src.kubernetes.leases-v1-32 | Leases（L800–812） | Lease 对象（coordination.k8s.io）用于系统关键能力：节点心跳与组件级 leader election；每个 Node 在 kube-node-lease 有同名 Lease，**kubelet 心跳＝对该 Lease 的更新请求（spec.renewTime）**，控制面用该时间戳判定节点可用性；kube-controller-manager/kube-scheduler 在 HA 配置下经 Lease 保证单实例活跃。 |
| API server 身份 Lease | NEW src.kubernetes.leases-v1-32 | 同页 API server identity（L813–827） | v1.26 beta：每个 kube-apiserver 用 Lease 发布身份；`kubectl -n kube-system get lease -l apiserver.kubernetes.io/identity=kube-apiserver` 可枚举在役 apiserver 实例（只读证据入口） |
| resourceVersion/watch/410 语义 | NEW src.kubernetes.api-concepts-v1-32 | API Concepts（Efficient detection of changes L973–985、L1015–1019、Bookmarks L1022–1043、分页 L1118–1120、Semantics L1476–1532） | 对象版本＝持久层版本；list-then-watch 不丢事件；断线可从上次 resourceVersion 续看或重新 get/list；**etcd3 默认只保留最近 5 分钟历史，超窗 watch 返回 410 Gone→客户端清缓存重新 list**；BOOKMARK 事件不可假设间隔；continue token 默认 5 分钟过期→410；resourceVersion 不透明、只能比较相等；get/list/watch 的 resourceVersion 语义表；Exact 不可用→410。支撑"身份/时间戳/对象版本"证据口径 |
| 一致读与 watch cache | NEW src.kubernetes.api-concepts-v1-32 | 同页（L1495–1508） | 未设 resourceVersion 的 list 需 quorum read；etcd 3.4.31+/3.5.13+ 且 K8s 1.32 时 "Most Recent" 由 API server 内部 watch cache 提供（靠 progress notification 保持一致）——支撑"资源视图正常不证明 etcd/应用正常"的分层判断 |
| kube-controller-manager 旗标默认值 | NEW src.kubernetes.kcm-reference-v1-32 | kube-controller-manager 参考页（Options 表，单行大表以字节偏移定位） | `--leader-elect` 默认 true；`--leader-elect-lease-duration` 15s、`--leader-elect-renew-deadline` 10s、`--leader-elect-retry-period` 2s、`--leader-elect-resource-lock` 默认 "leases"、resource-name/namespace 默认 kube-controller-manager/kube-system；`--controllers` 默认 "*"；`--node-monitor-grace-period` 50s（须为 kubelet nodeStatusUpdateFrequency 的 N 倍）、`--node-monitor-period` 5s、`--node-startup-grace-period` 1m0s |
| Slurm 控制器 HA 配置与接管流程 | NEW src.slurm.controller-ha-24.11.7 | quickstart_admin High Availability 节（L586–615）＋Controller Node 节（L527–541） | 多个 SlurmctldHost：第一个之后都是 backup；backup 应在不同节点、**所有主备须挂载同一共享文件系统（StateSaveLocation）**；主故障→第二个接管；主恢复→通知 backup，backup 保存状态回 standby，主读取保存的状态恢复运行；前两个都故障→第三个接管；切换间只有短暂无响应；**控制器或硬件在状态落盘前故障会丢状态**（恢复点边界）；状态在每次变化时写盘 |
| SlurmctldHost/StateSaveLocation/超时 | NEW src.slurm.controller-ha-24.11.7 | slurm.conf（L4128–4156、L4422–4425、L4719–4729、L6814–6817） | SlurmctldHost 至少一条、多条时第一条为主其余为备；SlurmctldTimeout＝backup 等待主响应的秒数，**默认 120s**；StateSaveLocation＝状态目录（默认 /var/spool），有备机时须主备均可读写，**建议可靠文件系统（如 RAID）**；**同主机名同时配置为主控制器且各自运行 slurmctld 会造成破坏性行为**（脑裂警告）。注：slurm.conf 页已登记于 src.slurm.docs-24.11.7，本轮为同一归档页的重开补证（新 SHA f4151769…） |
| slurmctld 启动恢复选项 | NEW src.slurm.controller-ha-24.11.7 | slurmctld.8（L121–172） | slurmctld 是中央管理 daemon（监控其余 daemon/接作业/分配资源），可有 backup server；`-c` 清除上次 checkpoint 状态（全部作业与节点状态删除，生产慎用）；`-i` 忽略状态文件错误（会丢未恢复数据）；`-r`（默认）恢复部分状态（作业＋节点 DOWN/DRAIN 与 Reason，无分区状态）；`-R` 恢复完整状态（作业/节点/分区/省电设置） |
| slurmctld 无响应的官方排查路径 | NEW src.slurm.controller-ha-24.11.7 | troubleshoot（L118–162） | `scontrol ping` 判定主/备控制器是否响应；不响应→排查网络/配置→`ps -el \| grep slurmctld` 查进程→不在则重启并读 SlurmctldLog；反复无指示失败→stop＋`startclean`（**丢全部运行中作业与状态**，destructive 门槛证据） |
| 记账状态与调度状态分离 | NEW src.slurm.controller-ha-24.11.7 | slurm.conf（L167–170、L325–332）＋slurmdbd.8（L123–124）＋slurmdbd.conf（L375–377、L837–842） | AccountingStorageType 默认未设＝不维护记账记录；accounting_storage/slurmdbd 插件把记账写入 slurmdbd 管理的数据库；slurmdbd 提供"安全的企业级数据库接口"（归档记账）；DbdHost 必须指定、StorageType 现仅 accounting_storage/mysql（MySQL/MariaDB）；AccountingStorageBackupHost 定义 backup slurmdbd 位置；DbdBackupHost 须能访问同一底层 Storage 数据库（L369–372）——**控制器状态（StateSaveLocation）与记账库（MySQL）是两套状态，恢复路径互不替代** |
| 记账库老化与归档 | NEW src.slurm.controller-ha-24.11.7 | slurmdbd.conf（PurgeJobAfter L698–707、ArchiveJobs L164–169） | PurgeJobAfter 按月（可 hours/days）清除已结束作业记录，聚合信息保留到 PurgeUsageAfter；ArchiveJobs 默认 no——**记账库内容会按策略消失，恢复验证不能只依赖 DB** |
| slurmdbd 自检/修复选项 | NEW src.slurm.controller-ha-24.11.7 | slurmdbd.8（L139–150） | `-R` 重建关联树的 lft/rgt（极少用）；`-u` 只显示数据库版本与是否需要转换即退出（0/1 返回码） |
| 节点心跳/驱逐默认值（K8s） | 复用 src.kubernetes.node-lifecycle-v1-32 | nodes/taint-and-toleration（Batch 23 已核对） | 心跳 Lease、node controller 5s 检查/默认 5 分钟驱逐/限速；失联期删除决定无法下达 kubelet、Pod 可能续跑。本轮未重开 |
| 作业控制器重试/完成与 GC | 复用 src.kubernetes.job-lifecycle-v1-32＋src.kubernetes.api-gc-v1-32 | Job 概念页/GC 页（Batch 22 已核对） | backoffLimit/TTL/finalizer、级联删除；恢复后核对 attempt/完成态的官方语义基础。本轮未重开 |
| 版本偏斜与控制面升级边界 | 复用 src.kubernetes.version-skew-v1-32＋src.kubernetes.kubeadm-upgrade-v1-32＋src.slurm.upgrades-24.11.7 | （Batch 23 T05-09 已核对） | 恢复/重建时的版本与集群身份前提、etcd/组件版本兼容由升级文档约束；K8s 无官方降级路径。本轮未重开 |
| Kueue 控制器身份 | 复用 src.kueue.admission-v0.19.0 | Kueue admission 文档（Batch 22 已核对） | Kueue 以 K8s 控制器/CRD 形态运行，其可用性判断归入 K8s 控制器与 API 链；Kueue 专属备份/恢复文档未专项取证（见 unknown 5） |
| Ascend 集群组件故障聚合与 CRD 控制器 | NEW src.ascend.mind-cluster-clusterd-v26.1.1 | v26.1.1 源码包 component/clusterd/README.md＋component/ascend-operator/README.md | clusterd：提供集群级可用资源信息，收集任务/资源/故障信息及影响范围，从任务、芯片和故障维度统计分析（附带 faultDuration.json/publicFaultConfiguration.json/relationFaultCustomization.json 配置产物）；ascend-operator：CRD 定义 AscendJob，支撑 mindspore/pytorch 在 K8s 上分布式训练。**两者均无 HA/备份/恢复文档**；组件故障恢复行为 unknown |
| 训练负载恢复契约入口 | 复用 src.pytorch.elastic-2.6 | elastic/train_script（checkpoint 是恢复前提）与 run.py（max-restarts 默认值）（前轮已核对） | 恢复验证中"attempt/Checkpoint/持续进展"的训练侧契约基础。本轮未重开 |

## unknown 清单

1. Slurm 24.11.7 归档无 `high_availability.html`（404＋索引实开确认）；HA 完整口径（如状态文件格式、内部协议）分散在 quickstart_admin/slurm.conf/slurmctld.8/troubleshoot，无单页 HA 手册。
2. StateSaveLocation 内 checkpoint 文件的内容级语义（文件级结构）未读源码；`-r`/`-R` 恢复差异以 man 描述为限；备份该目录＝"可恢复"的完整充分性无官方逐字承诺。
3. Kubernetes 控制器框架的 workqueue/informer 内部实现（重试队列、缓存一致性细节）v1.32 概念文档未展开；正文只按"控制器=控制循环＋经 API server"官方口径写。
4. MindCluster clusterd/ascend-operator/NPU 管理组件（含 volcano 相关组件）的故障恢复、备份与状态重建：无一手文档；tarball（tag v26.1.1，codeload）与既有条目 commit 44385c13 的字节等同未核；不以 K8s/Slurm 机制类推。
5. Kueue/Volcano 自身的备份恢复与状态重建专项文档未取证；Kueue 按 K8s 控制器模型归入通用链路，细节 unknown。
6. 站点实际参数（SlurmctldTimeout/Purge 系列/kubeadm etcd 配置/leader 旗标实际值/快照周期）：unknown，须读现场配置；文档默认值见上表。
7. 官方故障测试逐项核对未做：registry 既有 src.kubernetes.job-controller-tests-v1.32.0 与 src.slurm.testsuite-24-11-7-1 为邻近测试材料，本轮未逐用例读取控制面故障场景。
8. 全部演练未执行：未停/起任何 API server、未做 etcd 快照/恢复、未切换 Slurm 控制器、未重启任何 daemon；"恢复后账本核对"为方法设计，不是实测结果。

## 建议登记条目（7 条新增，均本轮实开）

```yaml
- id: src.kubernetes.etcd-backup-restore-v1-32
  title: Kubernetes v1.32 Operating etcd clusters（备份/恢复/扩缩容，静态快照）
  url: https://v1-32.docs.kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/
  kind: documentation
  registered_at: '2026-10-18'
  revision: v1.32 documentation snapshot（configure-upgrade-etcd URL 落地页标题为 Operating etcd clusters for Kubernetes）；curl 字节级取回 2026-10-18，SHA-256 19e528c0790d486b50e361e395a2509b3af7dd62b87912e2eea123b502a39ed7
  license:
    status: partial
    scopes:
    - scope: Kubernetes website 仓库文档许可声明；main 链接为可变定位
      identifier: CC-BY-4.0
      url: https://github.com/kubernetes/website/blob/main/LICENSE
    notes: 沿用既有 K8s 文档条目许可口径，本轮未重新打开 LICENSE 页；仅链接并原创归纳。
  notes: Batch 24（T05-10）取证：快照含全部 K8s 状态、建议加密；etcdctl snapshot save/etcdutl snapshot status（HASH/REVISION/TOTAL KEYS/TOTAL SIZE）；恢复前提＝停全部 API server→恢复所有 etcd 实例→重启，并建议重启 kube-controller-manager 与 kubelet 防陈旧数据；etcdutl --data-dir snapshot restore（etcdctl 恢复 3.5.x 起弃用）、同目录先删旧目录；etcd 不建议扩缩容/自动扩缩。未执行任何 etcdctl/etcdutl 命令。
- id: src.kubernetes.controller-pattern-v1-32
  title: Kubernetes v1.32 Controllers 概念（静态快照）
  url: https://v1-32.docs.kubernetes.io/docs/concepts/architecture/controller/
  kind: documentation
  registered_at: '2026-10-18'
  revision: v1.32 documentation snapshot；curl 字节级取回 2026-10-18，SHA-256 a6aecfb049400117d178dfb3a85bc39c14676a841fc4093920245cc34368720b
  license:
    status: partial
    scopes:
    - scope: Kubernetes website 仓库文档许可声明；main 链接为可变定位
      identifier: CC-BY-4.0
      url: https://github.com/kubernetes/website/blob/main/LICENSE
    notes: 沿用既有 K8s 文档条目许可口径；仅链接并原创归纳。
  notes: Batch 24（T05-10）取证：控制器＝watch 集群状态的控制循环；spec 为期望状态；控制器多经 API server 副作用生效（Job 控制器不直接运行 Pod）；大量简单控制器、控制器可失败且控制面另一部分接管；内建控制器运行于 kube-controller-manager。workqueue/informer 内部实现未展开（unknown）。未操作任何控制器。
- id: src.kubernetes.leases-v1-32
  title: Kubernetes v1.32 Leases（节点心跳/组件选主/apiserver 身份，静态快照）
  url: https://v1-32.docs.kubernetes.io/docs/concepts/architecture/leases/
  kind: documentation
  registered_at: '2026-10-18'
  revision: v1.32 documentation snapshot；curl 字节级取回 2026-10-18，SHA-256 ec68b97369247821e243bbe585808add24f4b763f9df00c60020edd9c5ad43b4
  license:
    status: partial
    scopes:
    - scope: Kubernetes website 仓库文档许可声明；main 链接为可变定位
      identifier: CC-BY-4.0
      url: https://github.com/kubernetes/website/blob/main/LICENSE
    notes: 沿用既有 K8s 文档条目许可口径；仅链接并原创归纳。
  notes: Batch 24（T05-10）取证：coordination.k8s.io Lease 支撑节点心跳（kube-node-lease 同名 Lease、心跳＝spec.renewTime 更新、控制面以时间戳判可用）与组件级 leader election（kcm/scheduler HA 单实例活跃）；apiserver 身份 Lease（v1.26 beta）与 label selector 枚举命令。未执行任何 kubectl 命令。
- id: src.kubernetes.api-concepts-v1-32
  title: Kubernetes v1.32 API Concepts（resourceVersion/watch/410/一致读，静态快照）
  url: https://v1-32.docs.kubernetes.io/docs/reference/using-api/api-concepts/
  kind: documentation
  registered_at: '2026-10-18'
  revision: v1.32 documentation snapshot；curl 字节级取回 2026-10-18，SHA-256 ca03957baf69b180cd8e9e2ee72aafbc8459b4bf78d92219e45d8b4976bbe00e
  license:
    status: partial
    scopes:
    - scope: Kubernetes website 仓库文档许可声明；main 链接为可变定位
      identifier: CC-BY-4.0
      url: https://github.com/kubernetes/website/blob/main/LICENSE
    notes: 沿用既有 K8s 文档条目许可口径；仅链接并原创归纳。
  notes: Batch 24（T05-10）取证：list-then-watch 与 resourceVersion；etcd3 默认保留最近 5 分钟变更、超窗 410 Gone→清缓存重新 list；BOOKMARK 不可假设间隔；continue token 默认 5 分钟过期；resourceVersion 不透明只可比较相等；Exact 不可用→410；未设 RV 的 list 需 quorum read，etcd 3.4.31+/3.5.13+ 且 K8s1.32 的 Most Recent 经 watch cache。未发起任何 API 请求。
- id: src.kubernetes.kcm-reference-v1-32
  title: Kubernetes v1.32 kube-controller-manager 命令行参考（静态快照）
  url: https://v1-32.docs.kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/
  kind: documentation
  registered_at: '2026-10-18'
  revision: v1.32 documentation snapshot；curl 字节级取回 2026-10-18，SHA-256 344a05192c36149e43527b7f649223d8b9217c165c9520498f967e8c7a1badbf；选项表为单行大表，锚点以字节偏移记录
  license:
    status: partial
    scopes:
    - scope: Kubernetes website 仓库文档许可声明；main 链接为可变定位
      identifier: CC-BY-4.0
      url: https://github.com/kubernetes/website/blob/main/LICENSE
    notes: 沿用既有 K8s 文档条目许可口径；仅链接并原创归纳。
  notes: Batch 24（T05-10）取证：--leader-elect 默认 true；lease-duration 15s/renew-deadline 10s/retry-period 2s/resource-lock 默认 leases/resource-name kube-controller-manager/namespace kube-system；--controllers 默认 "*"；node-monitor-grace-period 50s（须为 kubelet nodeStatusUpdateFrequency 的 N 倍）、node-monitor-period 5s、node-startup-grace-period 1m0s。未运行该组件。
- id: src.slurm.controller-ha-24.11.7
  title: Slurm 24.11.7 控制器/DBD HA、状态保存与恢复（归档多页）
  url: https://slurm.schedmd.com/archive/slurm-24.11.7/quickstart_admin.html
  kind: documentation
  registered_at: '2026-10-18'
  revision: 24.11.7 archive；curl 字节级取回 2026-10-18（quickstart_admin d7e9c31bac0fe920b88a8791cc2d0fad0c93133c9299b90e914ee2bf35b480e7、slurm.conf f4151769ed29968c7de408809a5acb8f0591865cd525d5f2c70925e847a1ff34、troubleshoot 78f519e4e98c869e79011bc31056ff8c29182478220a8bc85f5ff9f6c7da4c4c、slurmctld 67e677b6d0dd57a0e223e2c85689d1974b5e6818351dee4bbbb0cb9fec987c49、slurmdbd 5a81ba6e817a1a83fb38bafcbfc8e06d9ca39b715af06cda474dcf108755976e、slurmdbd.conf 6d2529a81316317d122ac944ca512df5a4f9866590361525b5241027bdb9e45b）；24.11.7 归档无 high_availability.html（404＋索引实开确认）
  license:
    status: unknown
    scopes: []
    notes: SchedMD 站点许可未核对；只链接并原创归纳，未复制手册长段。
  notes: Batch 24（T05-10）取证：quickstart_admin HA 节（多 SlurmctldHost 主备/共享 StateSaveLocation/接管与回切流程/状态落盘前故障即丢状态）；slurm.conf（SlurmctldHost 至少一条首主余备、SlurmctldTimeout 默认 120s、StateSaveLocation 默认 /var/spool 且建议可靠 FS、双主警告、AccountingStorageType/BackupHost、ReturnToService 见既有条目）；slurmctld.8（-c 清状态/-i 忽略错误/-r 默认部分恢复/-R 完整恢复）；troubleshoot（scontrol ping/ps 检查/重启/startclean 丢全部运行作业与状态）；slurmdbd.8（角色、-R lft/rgt、-u 转换检查）；slurmdbd.conf（DbdHost 必填、DbdBackupHost 须同库、StorageType 仅 mysql、PurgeJobAfter/ArchiveJobs 默认 no）。未执行任何 Slurm 命令。slurm.conf 页与 src.slurm.docs-24.11.7 为同一归档页的重开补证。
- id: src.ascend.mind-cluster-clusterd-v26.1.1
  title: MindCluster v26.1.1 clusterd 与 ascend-operator 组件 README
  url: https://github.com/Ascend/mind-cluster/blob/v26.1.1/component/clusterd/README.md
  kind: repository
  registered_at: '2026-10-18'
  revision: tag v26.1.1（codeload 源码包取回 2026-10-18；GitHub API 同刻限流，文件树由源码包代替；与既有条目 commit 44385c13 的字节等同未核）
  license:
    status: identified
    scopes:
    - scope: 固定 tag 的 clusterd/ascend-operator README 文本；仓库根 LICENSE 声明范围
      identifier: Apache-2.0
      url: https://github.com/Ascend/mind-cluster/blob/v26.1.1/LICENSE
    notes: 未逐文件核对许可头；仅链接并原创归纳，不复制 README 长段。
  notes: Batch 24（T05-10）取证：clusterd 提供集群级可用资源信息、收集任务/资源/故障信息及影响范围（任务/芯片/故障维度统计），构建产物含 faultDuration.json/publicFaultConfiguration.json/relationFaultCustomization.json；ascend-operator 以 CRD 定义 AscendJob 支撑 mindspore/pytorch 分布式训练。两组件均无 HA/备份/恢复文档，故障恢复行为 unknown；不以 K8s/Slurm 机制类推。
```

## 修订轮补充取证（2026-10-18，初审发现 B24-T10-C01–C10 处理）

按初审报告补取并核对：

- **etcd v3.5 Disaster recovery 指南**（NEW src.etcd.disaster-recovery-v3.5-docs；curl SHA-256 477f5513…，与审阅者独立取回一致）：Revision Difference（恢复后客户端可见 revision 回退；K8s informer 本地缓存与 watch 的失配风险）、`--bump-revision`（64 位增量、K8s 上下文须同时标记全部旧 revision）、恢复自快照改写 member ID/cluster ID→必须作为新逻辑集群、快照完整性哈希与 `--skip-hash-check`。支撑 C02 修订。
- **sacct 24.11.7 归档页**（复用 src.slurm.docs-24.11.7 覆盖页，本轮新开；SHA-256 d96f8299…，与审阅者一致）：L536–556 `--state` 可查当前 RUNNING 作业、PENDING 受 EligibleTime 条件。支撑 C08 修订（记账记录含活动作业）。
- **Slurm testsuite 负结果检索**（slurm-24-11-7-1 codeload 源码包）：expect 目录 593 个用例，按 failover/backup controller/slurmctld 重启主题检索用例名与正文，**无控制器故障专项用例**；Slurm 官方故障测试材料保持缺证（unknown）。支撑 C06 修订。
- **K8s Job 控制器单测文件级定位**：v1.32.0 `pkg/controller/job/job_controller_test.go`（复用 src.kubernetes.job-controller-tests-v1.32.0；未逐用例核对）。支撑 C06/C04 修订。
- 字段语义修正依据：ContainerStatus.restartCount 为容器级计数（v1.32.0 staging types.go，审阅者 E08）；Job 终态 conditions 为 Complete/Failed、backoffLimit 为限额（Job 概念页，审阅者 E07）；HealthCheckProgram 在 slurmd 首次启动注册前执行＋周期触发（slurm.conf L1379–1395，审阅者 E10）。以上锚点由审阅者独立重开、作者本轮采纳并改写正文。

## 修订轮二补充（2026-10-18，复核轮发现处理）

- C01：读一致性改为"未设 RV＝Most Recent（quorum/一致）、RV=\"0\"＝Any"。
- C02：补缓存重建的对象级验证（恢复前后对象清单 RV 比对＋观察窗口动作抽查＋无法解释漂移即停止）；"会触发重放"改为"存在重放风险，须验证后关闭"。
- C03/C04：执行身份映射补运行时 containerID 与应用 attempt；Job 侧补 status.succeeded/failed 计数与 JobPodReplacementPolicy/JobManagedBy 门控时序（门取值未知按 unknown）。
- C06：testsuite 定位到 test37.5（federated requeue，DBD 状态断言＋重启计数断言；非切换专项），范围如实；控制器切换专项仍缺证。
- R01：恢复输入工件分三类（快照文件/离线 member/snap/db 单文件含 WAL 缺口/输出目录）；--skip-hash-check 仅限第二类。
- R02：新登记 src.kubernetes.core-v1-types-v1.32.0（SHA 与两轮独立取回一致）并补入 source_refs。

## 修订轮三补充（2026-10-19，复核第二轮发现处理）

- C02：REVISION 差值改"提示"语义；补"缺证/无法判断缓存一致性＝恢复验证不通过"；skip-hash-check 措辞降为语义说明；etcd 端点/证书按部署布局区分（步骤 unknown）。
- C04：接入 v1.32 门控的终态时序（终态 condition 延迟至全部 Pod 终止；`status.terminating`=0；更早信号；引用生命周期正文与其登记的 TestDelayTerminalPhaseCondition）。
- C06：官方故障材料改为按分支交付表——Slurm 侧新增 testsuite/python/tests/test_102_5.py `test_qos_removal_single`（SHA-256 ae908d7c1f66ad9f02f307bc7ade74ffc7930a390e7828a67c4ef31f27edd757，本轮作者亲核：停 DBD→作业→停 ctld→启 DBD→改库→重启 ctld，断言旧运行/旧等待/新提交三分支）；K8s 侧具名 TestJobFailedWithInterrupts/TestDelayTerminalPhaseCondition/TestJobPodsCreatedWithExponentialBackoff（集成）与 TestJobBackoff 族（单测，SHA-256 b78d06e36bc9562a21546ea5b097997ab76f9d0507ba8dbf359d6659b99fbf31 本轮亲核 L6993/L7041/L7401）；etcd 灾备自动化测试负结果保留。
- R01：registry etcd 条目 notes 同步三类工件口径。

## 修订轮四补充（2026-10-19，复核第三轮发现处理）

- C02：验证分层重写（快照身份/全局 revision 记录、对象比对仅查身份与内容差异、消费者记录独立、缺证不放行）。
