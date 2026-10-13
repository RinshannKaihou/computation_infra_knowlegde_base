# 第二十批审阅修订映射

## T04-02 修订（claude-opus-5-5 初审 B20-C01–C10 → 本轮处理全部 10 项）

- C01：补本地提交语义行（data= 三模式/commit 5 s/barrier/auto_da_alloc 启发式≠fsync）；rename 改引 rename(2) 并修正条件；journal 链 globals §3.6；登记 rename(2)＋admin-guide/ext4。
- C02：两侧锁行（NFS NLM/NSM＋v4 内置/advisory/flock 转换/nolock；本地 flock/fcntl 登记）；恢复拆协议层与实现层。
- C03：CTO 归属纠正（本地页缓存可见 vs NFS CTO＋缓存窗口）；close-to-open 措辞；可见性与持久性分列。
- C04：写入→提交→稳定行（回写触发/UNSTABLE/COMMIT/verifier/导出 sync-async/hard-soft）；客户端/服务器 sync 区分；Checkpoint 发布配置。
- C05：drop_caches 非破坏性纠正＋引 sysctl vm；回写行；冷热分层（服务器侧 unknown）。
- C06：特性位逐项条件；delalloc 后果改引 admin-guide/fsync。
- C07：选型表五列补齐（后端 knfsd-stats、客户端 unknown、hard/sync、异常列、对象行边界）。
- C08：方法四栏（前置/预期/实际留空/授权）＋CTO 前置。
- C09：pNFS 服务器侧收敛、knfsd-stats 收敛；登记补快照日期。
- C10：交叉链接补齐、T04-04 标注计划中、记录细化到节/锚点。

## T04-02 第二轮修订（claude-opus-5-5 定向复核 5/5 → 处理 C01/C02/C03/C05/C10）

- C01：barrier 全条件行；ordered 措辞纠正（数据直写主 fs）；登记同步；auto_da_alloc 补 truncate。
- C02："均为 advisory"删除（v3 NLM advisory；v4 字节锁可 mandatory；share reservation mandatory；flock 模拟细节）；两侧故障→锁结果（§8.4.1/§8.4.3/Linux 丢锁/nfsv4leasetime 90 s；grace 时长 unknown；主机崩溃不保留标推论）；登记 fcntl_locking(2)，fcntl-6.19 备注索引定位。
- C03："v4 类似"改"此节仅 v3＋v4 见 RFC＋Linux v4 CTO unknown"（初审前提错误由复核更正，不归责作者）。
- C05：NFS 客户端冷条件（本地 drop_caches＋属性/委托 unknown）；特权标推论；drop-caches 锚点。
- C10：nfs 登记写明实际三子页；evidence_refs 补 sysctl-vm/fsync/rename/flock/fcntl/fcntl-locking。
- 非阻断同轮采纳：§18.26.4 RENAME 原子、`hard` 标本库约束、iostat 方法层标注。

### T04-02 改动位置索引（行号为编写时现行版，不冻结；以节名为准）

- C01：正文 L61–64（data=/commit=/barrier/auto_da_alloc/rename/jbd2）＋ admin-guide/ext4、rename(2) 登记；L68–69 特性位/故障域。
- C02：正文 L66（本地锁：传统/OFD/flock 分列）＋ fcntl_locking(2) 登记；L77–84（NFS 锁/提交/恢复，RFC §8.4.1/§8.4.2.1/§8.4.3/§9/§18 锚点）。
- C03：正文 L76（CTO 归属）＋ RFC §10.3.1/§10.4。
- C04：正文 L78–81（提交链/sync 区分/rename/Checkpoint 发布）。
- C05：正文 L67（回写）、L105/L113/L116（冷基线/drop_caches 锚点）＋ sysctl vm 登记。
- C06：正文 L68（特性位逐项）。
- C07：正文 L88–95（选型五列）＋ knfsd-stats。
- C08：正文 L99–106（方法四栏）。
- C09：正文 L53/L83（pNFS/knfsd-stats 收敛）；登记快照日期。
- C10：正文交叉链接；来源记录节/锚点；evidence_refs 补齐。

## T04-02 第三轮修订（claude-opus-5-5 第二次定向复核 7/3 → 处理 C01/C02/C10）

- 登记三处文字同步真实落盘（此前脚本缺 write 未写入，已补写并复核）：nfs 实际三子页、fcntl-6.19 索引备注、admin-guide ordered 措辞。
- 映射去重（第二轮节重复）＋改动位置索引。
- C02：本地锁传统/OFD/flock 三分列；NFS 证据列补 §8.4.1/§8.4.2.1/§8.4.3/§9 锚点；L116 特权标推论。

## T04-02 第四轮修订（claude-opus-5-5 第三次定向复核 8/2 → 处理 C01/C02）

- C01：登记 auto_da_alloc 补 truncate。
- C02：§8.4.1/§8.4.2.1 锚点纠正；证据列补 §9.1.2/flock NFS details/fcntl_locking NFS 节；flock 登记注补模拟细节；fcntl-locking 登记注限定传统锁；L113 去重。

## T04-02 第五轮修订（claude-opus-5-5 第四次定向复核 9/1 → 处理 C02）

- C02：§8.4.2.1 锚点纠正为 #section-8.4.2.1（上一轮只改了 §8.4.1，映射误称两处均改，特此纠正）。

## T04-03 修订（claude-opus-5-5 初审 B20-C11–C21 → 本轮处理全部 11 项）

- C11：登记 v19.2.7 tag（src/rgw 定位，未逐行审计；测试未定位）；Lustre 源码未取记 unknown＋影响范围；两侧部署组成行（RGW 索引/Lustre §1.2.2）。
- C12：Ceph 分支文档＋点版本 unknown；Lustre 滚动手册＋LTS 2.15.x 锚（主张只用 ≤2.15 特性）；反例换 latest objectops（dev scrub 引用移除）；releases 锚澄清（版本映射见实现锚）。
- C13：ETag 行如实转述 MD-5 措辞＋本库不用及理由；合成规则 unknown；content-md5 可选项；登记同步。
- C14：版本化三态改引 bucketops；versionId 返回 unknown；读旧版本改待判定；Append 409 约束。
- C15：multipart 按页拆分；可见性/列举一致性 unknown；Retention/Object Lock 分列；range/条件读/列举参数/allow-unordered。
- C16：子集改兼容模型＋Features 表＋扩展清单（Append/allow-unordered/Appendable）。
- C17：LDLM/§34.10/Extent/§34.8；glimpse 删除；DoM/FLR 2.11＋MDT 5%；默认条带 1/1MB＋-1 语义；§1.2.2。
- C18：GET /?usage；Jobstats/Ch12/Ch39 入口；错误码；BAD WRITE CHECKSUM；Full OST。
- C19：三层定义表；区间写/大小覆盖/负向用例；content-md5 与读回哈希分开。
- C20：索引改审阅中；verification 只写已核对条目（复核确认）。
- C21：登记同步；Lustre https；滚动手册注；releases 说明。

## T04-03 第二轮修订（claude-opus-5-5 定向复核 4/7 → 处理 C11/C12/C13/C15/C16/C19/C21）

- 登记真实落盘复核（grep 确认）：rgw-s3 分支＋点版本 unknown、lustre 滚动＋LTS 锚、repo commit 9ec952b9 纠正、ETag 措辞同步；新增 wiki LTS 登记。
- C11：commit 纠正为 9ec952b9（tag 对象≠commit）。
- C12：LTS 2.15.8 登记 mapping；分支/滚动口径保持。
- C13：登记 ETag 措辞同步（前轮已在正文，登记本次落盘）。
- C15：NoSuchUpload 触发条件纠正（upload-id 不匹配）。
- C16：Features 表逐项状态＋large subset 回应。
- C19：Abort 负向用例改预期栏；FID 不含（设计决定＋理由）；端到端哈希设计约定；versionId 获取与 unknown。
- C21：记录补日期＋SHA；releases 未登记说明。

## T04-03 第三轮修订（claude-opus-5-5 第二次定向复核 7/4 → 处理 C12/C16/C19/C21）

- C12：正文 LTS 引 wiki（下载页仅版本号说明）；source_refs/evidence_refs 补 release-info-wiki。
- C16：Features 表精确行（List Buckets 单列）；large subset/非子集/条件读/列举标推论。
- C19：versionId 获取 unknown＋未启用版本化身份；Abort 独立行（前置/预期/判据）；端到端哈希已在第二轮约定。
- C21：登记 lustre https 落盘确认；记录 wiki SHA 不可复现说明；releases 未登记说明保持。

## T04-03 第四轮修订（claude-opus-5-5 第三次定向复核 8/3 → 处理 C12/C16/C19）

- C12：LTS 引文补取证日（wiki 动态页）。
- C16：Features 表"实测行"改"声明状态"；对象列举改引 bucketops GET Bucket；条件读以 GET 的 range/if-modified-since/if-unmodified-since 为据（标推论）。
- C19：未启用版本化身份加内容哈希；Suspended 归无有效版本；L88 判据按 versionId 可获得性区分。

## T04-03 第五轮修订（claude-opus-5-5 第四次定向复核 9/2 → 处理 C16/C19）

- C16：条件读改五项请求头直接引用（作者此前窗口截断误判，特此纠正）；L56/L60 统一集合；wiki 链接 https。
- C19：L88 按身份分支改写（Enabled-versionId/其他-SHA-256）＋对象不可见即失败。

## T04-04 修订（claude-opus-5-5 初审 B20-C22–C31 → 本轮处理全部 10 项）

- 报告坏链机械修复（C30 五处相对链接；见审计）。
- C22：data_offsets 单文件区间；分片索引 unknown；清单集合成员＋SHA-256。
- C23：指南改 v0.33.0 版页；选版理由＋不外推；登记同步。
- C24：续传/5 次/长度判据/无哈希；版本记解析 commit；50k 窗口；读回本地重算；unknown 清单删 hub 续传。
- C25：三栏拆分＋NFS 条件引入；fsync 次序；T04-03 归属修正；hub 落地边界。
- C26：集合级提交点＋读者协议；目录 rename 条件；对象无多原子性 unknown；设计/上游分开标。
- C27：版本字段按 T04-03 分支；删"版本号未推进"；旧/混合按三态＋链接。
- C28：§4 阶段表（锚点/计时起止/失败信号；计时未执行）；L804 缺 assert 说明；磁盘不足仅警告；safetensors 测试 unknown＋检索范围。
- C29：格式门全条件＋NaN 分界；正确性门形式＋T07-01；重试清理分侧残留物。
- C30：四主文相对链接＋节；T07-01＋07 索引。
- C31：source_refs 删 dcp/mindio；verification 重写；safetensors URL 迁组织；L48 格式无校验和字段确定；记录补日期/SHA/行号。

## T04-04 第二轮修订（claude-opus-5-5 定向复核 1/9 → 处理 C22/C23/C24/C25/C26/C27/C29/C30/C31）

- 登记落盘复核：safetensors notes（单文件区间/无校验和字段）、hub notes（plain HTTP 限定＋Xet 行）；safetensors URL 迁组织。
- C22/C13类比项：分片索引 unknown；清单集合成员。
- C23：指南 v0.33.0 版；选版理由＋不外推。
- C24：Xet 路径例外行（setup L17/file L530/618/1708-1710）；plain HTTP 限定。
- C25：fsync/rename 就近引用；NFS 条件改引 §4；hub 落地边界。
- C26：集合级提交点标本库设计（两处）。
- C27：版本字段按三态；旧/混合按三态＋链接。
- C29：格式门/正确性门/重试清理分侧。
- C30：链接精确到节名；T07-01＋07 索引。
- C31：verification 重写待复核；记录补日期/SHA/行号。

## T04-04 第三轮修订（claude-opus-5-5 第二次定向复核 4/6 → 处理 C24/C25/C26/C29/C30）

- C24：L35 加 plain HTTP 限定；RGW 栏去"同左"（上传无续传语义）；Xet 锚点纠正 L600-603/L627-633。
- C25/C26/C31：NFS 条件补 §3 引用；rename(2) 就近链接；Complete 加 T04-03 §2 链接（Ceph 登记正文引用落盘）。
- C29：L70 方法标注；锁文件删除记 unknown；README L89/L94 锚点。
- C30：T04-03 引用改链接。
- 附带：映射第二轮节去重；rename-6.19 登记注复核为 rename 内容，无错位。

## T04-04 第四轮修订（claude-opus-5-5 第三次定向复核 8/2 → 处理 C24/C30）

- C24：Xet 证据列锚点纠正 L600-603/L627-633；RGW 上传续传语义改 unknown（分片可列举续传，文档未用"续传"字样）。
- C30：L53 T04-03 §2 改链接。
- 附带：磁盘检查锚点纠正 L799（登记同步）；映射节标题补全。

## T04-04 第五轮修订（claude-opus-5-5 第四次定向复核 9/1 → 处理 C24）

- C24：L55 RGW 栏改 unknown 措辞（与 L53 一致）；Xet 证据列补 L530/L1708-1710。
- 报告坏链机械修复（code span 化）；L57 正文去词重复。

## T04-05 修订（首轮交付，待 claude-opus-5-5 初审）

- 只做加法：新增 §5 校验原语对照、§6 后端读路径责任、§7 验证链、§8 反例与证据保留；front matter 补 5 个复用 ID 与核对注。
- 无新增远程取证，仅复用已核对来源；签名机制记 unknown。

## T04-05 第二轮修订（claude-opus-5-5 初审 B20-C32–C40 → 本轮处理全部 9 项）

- 登记新增 BlueStore 页（32-bit 量级）；lustre revision 补 §23.5.1。
- C32：恢复诊断指南三节链接；存储 repair 归 T04-07 unknown；顺序标设计约定＋SRE 引文；repair 证据 unknown。
- C33：NFS 读路径三列（UDP/krb5i/soft；无端到端断言）；COMMIT＋verifier；CTO v3/v4 边界；source_refs 补 nfs-5/rfc-8881。
- C34：RGW 读路径 RADOS/语义分列；BlueStore＋读修复；pre-OSD 推论；Squid 适用说明。
- C35：§23.5.1 全文（两类/两向/重试/EIO/adler32）；ldiskfs 限定；e2fsck/ZFS/LFSCK；证据链接＋登记。
- C36：碰撞分随机/对抗；去循环引用；签名格式无字段；清单信任锚。
- C37：缺片措辞；DCP 实例化；正确性门分训练/推理；错误×步骤对照。
- C38：hub 期望值措辞；Ceph/Lustre 移检测信号；SRE 案例＋原则引用。
- C39：记录逐主张定位；NFS ID 修正；SRE 落点；notes 如实改写。
- C40：来源节合并；定义/边界/待确认同步；related_ids；计划 ID 改链接；索引摘要。

## T04-05 第三轮修订（claude-opus-5-5 定向复核 5/4 → 处理 C33/C35/C39/C40）

- C33：TCP checksum 错误删除（TCP 16-bit 弱校验＋原文 65536 误匹配概率）；端到端不断言；后端 unknown。
- C35/C39：登记 lustre revision 补 §23.5.1 全文要素。
- C40：定义尾句修正；L121/L127 链接化（L121 已带链，复核确认）。
- 附带：登记 forty  typo；报告 SHA 乱码机械修复。

## T04-05 第四轮修订（claude-opus-5-5 第二次定向复核 8/1 → 处理 C33）

- C33："弱"字删除，传输层 checksum 细节改 unknown（nfs(5) 只述 UDP）。
- 报告末行"见下行"补结果（机械修复）。
