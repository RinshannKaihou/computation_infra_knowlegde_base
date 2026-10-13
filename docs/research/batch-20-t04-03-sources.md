# 第二十批 T04-03 来源记录

任务：T04-03（新建 `object-and-parallel-storage.md`）。作者取证轮次：首轮（Squid S3 三页、Lustre 手册全文；latest/dev 反例；取证日 2026-10-13）＋第二轮（v19.2.7 tag 与 src/rgw 定位、RGW 索引部署入口、latest objectops 反例登记、wiki LTS 2.15.8、手册节表明文；独立复核初审取证点）。页面 SHA-256（作者实开）：S3 索引 e48b4d87/serviceops a2fe21b0/bucketops 3f2a9d0d/objectops 14f5689f、Lustre 手册 63b09d06、RGW 索引 695cd90d、latest objectops a394e115（前缀 8 位；全文见复核报告一次源表）；wiki 为动态页，作者快照前缀仅作当时记录，不可复现。releases 页仅浏览版本映射，未登记。

## 主张—来源定位表（ID—精确页面/节—字段/支持范围）

| 主张 | 已登记 ID | 精确页面/节 | 支持范围 / 未覆盖 |
|---|---|---|---|
| RGW S3 接口 | src.ceph.docs-rgw-s3-squid | [S3 索引](https://docs.ceph.com/en/squid/radosgw/s3/)（Features 表/兼容模型）＋ serviceops（`GET /?usage`）/bucketops（版本化三态/ETag MD-5措辞/`allow-unordered`/Object Lock）/objectops（multipart/`content-md5`/Append/409） | Squid 分支文档（取证日），点版本 unknown |
| RGW 实现/部署 | src.ceph.repo-v19.2.7 / src.ceph.docs-rgw-index-squid | [src/rgw](https://github.com/ceph/ceph/tree/v19.2.7/src/rgw)（rgw_op.cc multipart/ETag；rgw_rest_s3.cc versionId；定位未逐行审计）/[RGW 索引](https://docs.ceph.com/en/squid/radosgw/)（librados/HTTP前端/池/索引/zone） | 测试文件未定位 unknown；细节 unknown |
| Lustre 语义 | src.lustre.ops-manual-2x | [手册](https://doc.lustre.org/lustre_manual.xhtml)（§1.1.1/§1.2.2/§1.3.1/§12/§19/§20/§22/§23.1/§23.5.1/§34.8/§34.10/§39/术语表；DoM/FLR 2.11、PFL 2.10、默认 count 1/size 1MB） | 2.x 滚动手册；稳定锚 LTS 2.15.x；精确小版本 unknown |
| 反例边界 | src.ceph.docs-rgw-s3-latest-boundary | [latest objectops](https://docs.ceph.com/en/latest/radosgw/s3/objectops/)（development 提示） | 仅边界；dev scrub 引用已移除 |

## unknown 清单

1. Ceph 点版本行为差异；2. RGW 测试文件；3. Lustre 精确小版本/源码；4. RGW 管理统计端点；5. Lustre 计数器含义；6. 版本化启用细节；7. 现场默认值；8. 全部实测（未执行）。
