# 第二十批 T04-04 来源记录

任务：T04-04（新建 `artifact-transfer-and-publication.md`）。作者取证轮次：首轮（两仓库 tag/commit/LICENSE/下载指南/README；取证日 2026-10-13）＋第二轮（v0.33.0 版指南页、file_download/_snapshot_download/测试行号、tensor.rs 错误枚举、safetensors 组织迁移；独立复核初审取证点）。

## 主张—来源定位表（ID—精确页面/行—字段/支持范围）

| 主张 | 已登记 ID | 精确页面/行 | 支持范围 / 未覆盖 |
|---|---|---|---|
| 传输实现 | src.hf.huggingface-hub-v0.33.0 | [file_download.py@commit](https://github.com/huggingface/huggingface_hub/blob/d5dff4efd9187cc5c56246f416d666ea1f808cb0/src/huggingface_hub/file_download.py)（Range L406-407/重试 L500-517/长度 L444-445/ETag L232-234/弃用 L942-947/incomplete L1160-1163/move L1684-1693/1735/1776；无 hashlib/fsync）＋[setup.py L17](https://github.com/huggingface/huggingface_hub/blob/d5dff4efd9187cc5c56246f416d666ea1f808cb0/setup.py)（hf-xet 默认安装）＋[_snapshot_download.py](https://github.com/huggingface/huggingface_hub/blob/d5dff4efd9187cc5c56246f416d666ea1f808cb0/src/huggingface_hub/_snapshot_download.py)（L264-267/283/305）＋[测试](https://github.com/huggingface/huggingface_hub/blob/d5dff4efd9187cc5c56246f416d666ea1f808cb0/tests/test_file_download.py)（L514/536/798-806，L804 缺 assert） | v0.33.0 commit d5dff4ef；磁盘不足仅警告；Xet 路径未核 unknown |
| 制品格式 | src.hf.safetensors-v0.7.0 | [README §Format](https://github.com/safetensors/safetensors/blob/v0.7.0/README.md)（8 字节头/JSON/数据区；字段仅 dtype/shape/data_offsets/__metadata__）＋[tensor.rs](https://github.com/safetensors/safetensors/blob/fa27fa835a466cb50d07696ec20b94f46aed0e31/safetensors/src/tensor.rs)（错误枚举） | 无校验和字段；读写测试 unknown |
| 后端承诺 | T04-02/03 登记复用 | rename/fsync、multipart/版本化 | 见各自主文 |

选版理由：v0.33.0/0.7.0 为取证时已发布一段时间的固定版本（非最新，取证时 latest 为 hub 2.2.0/safetensors 0.8.0），结论不外推到 1.x/2.x。页面/文件 SHA-256（作者实开，前缀 8 位）：file_download a973d198/_snapshot e9747ac/测试 f19f048c/setup 27aa7974、README e430910c/tensor.rs f94ad16f、v0.33.0 指南 fcb88d5f（全文与复核报告一次源表比对一致处以复核记录为准）。

## unknown 清单

1. Xet 路径行为细节（除 setup/file 行号外）；2. safetensors 读写测试；3. hub 续传之外中断语义；4. T07-01 实现；5. 全部实测（未执行）。
