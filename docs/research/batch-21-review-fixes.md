
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
