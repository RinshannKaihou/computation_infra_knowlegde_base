# 第二十批 T04-05 来源记录

任务：T04-05（修订 `checkpoint-integrity-evidence.md`，新增 §5–§8；定义/边界/待确认最小同步获初审 C40 许可）。作者取证轮次：首轮（复用 T04-02/03/04 登记＋既有 SRE/DCP/MindIO/Ceph/zipfile 登记；取证日 2026-10-13）＋第二轮（SRE 章 validator/案例原文、Squid BlueStore/读修复原文、Lustre §23.5.1 全文、nfs(5) 传输损坏与 krb5i；独立复核初审取证点；BlueStore 页新登记）。

## 主张—来源定位表（ID—精确页面/节/行—字段/支持范围）

| 主张 | 登记 ID | 精确页面/节/行 | 支持范围 / 未覆盖 |
|---|---|---|---|
| 校验原语/碰撞边界 | src.ceph.docs-bluestore-squid / src.hf.safetensors-v0.7.0 | [BlueStore Checksums](https://docs.ceph.com/en/squid/rados/configuration/bluestore-config-ref/)（32-bit 约四十亿分之一）；README §Format（无校验和字段） | 随机漏检量级；对抗碰撞 unknown |
| NFS 读路径责任 | src.nfs-utils.nfs-5-man7 / src.ietf.rfc-8881 | [nfs(5)](https://man7.org/linux/man-pages/man5/nfs.5.html)（UDP 损坏/krb5i/soft） | 端到端内容校验 unknown |
| RGW 读路径责任 | src.ceph.docs-bluestore-squid / src.ceph.docs-rgw-s3-squid | 上页＋health-checks 读修复（见 T04-04 记录） | 到达 OSD 前 unknown（推论） |
| Lustre 读路径责任 | src.lustre.ops-manual-2x | 手册 §23.5.1（两类 checksum/读写两向/五次重试/EIO/adler32；ldiskfs 范围） | ZFS 行为 unknown |
| 验证链/DCP 实例 | src.pytorch.dcp-2.6（复用） | §7（storage_data/MindIO 个数） | 按 offset 读≠全哈希 unknown |
| 反例与原则 | src.hf.huggingface-hub-v0.33.0 / src.google.sre-data-integrity | hub 测试 L798-806（缺 assert）；[SRE 章](https://sre.google/sre-book/data-integrity/)（validator/两案例/两原则） | 不外推 AI checkpoint |
| 恢复流程链接 | 现行草稿 | [恢复诊断指南](../../knowledge/06-training/checkpoint-state-recovery-triage.md)（前置/停止/完成判据）；T04-07 未交付 | 存储侧 repair unknown |

## unknown 清单

1. 签名机制；2. 对抗碰撞来源；3. ZFS 行为；4. 端到端内容校验（NFS）；5. T07-01/T04-07 实现；6. 全部实测（未执行）。
