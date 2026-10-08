# 第三批 F10 来源核查

日期：2026-09-29。主任务在通信和可靠性文章写作期间补充本页，供下一轮训练恢复一致性使用；纳入同轮 astra/xhigh 审阅。

| 已读取位置 | 支持的主张 | 边界 |
|---|---|---|
| [PyTorch 2.6 DCP](https://docs.pytorch.org/docs/2.6/distributed.checkpoint.html) | async_save 暂存后后台保存并返回 Future；AsyncStager 的视图隔离预期；StorageWriter 各 rank 写入与协调者 finish | 文档有实验性 API 警告；不证明 TorchNPU 支持或真实保存成功 |
| [固定 filesystem.py](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/filesystem.py) | sync_files 默认值与警告；326–336 行数据 fsync；574–595 行临时元数据、同步、改名 | 只说明该实现，不能宣布跨文件事务或所有后端的断电保证 |
| [Linux fsync(2)](https://man7.org/linux/man-pages/man2/fsync.2.html) | 文件数据与元数据同步；目录项需独立考虑；I/O/空间等同步错误 | 页面标注 man-pages 6.19、手册日期 2026-02-08、HTML 生成日期 2026-09-09；不是目标存储实际配置 |
| [MindIO ACP README](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/mindio/acp/README.md) | 数据先写训练服务器内存，再异步写后端存储 | 标题为 ockio；正文确实为 MindIO ACP。没有从本 README 推断确认 API、副本数量、掉电保障或整栈配套 |

PyTorch 与 MindCluster 的 GitHub 展示页未被读取工具正常返回时，主任务读取相同完整 commit 的官方 raw 文件；MindCluster 路径通过完整递归 tree（未截断）核实。没有运行上游代码、安装、保存、同步或故障注入命令。Linux 源码许可页此次不可达，保留许可 unknown，不以项目整体说明代替该材料的许可。

图、证据分类表、建议记录字段和验证要求为本库原创整理，不表述为上游统一规范。GPU/NPU 暂存及恢复状态的语义需要独立资料。

```yaml
- id: src.pytorch.dcp-2.6
  title: PyTorch 2.6 Distributed Checkpoint 文档与固定 FileSystemWriter 实现
  url: https://docs.pytorch.org/docs/2.6/distributed.checkpoint.html
  kind: documentation
  registered_at: "2026-09-29"
  revision: "2.6 documentation; source commit 1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340"
  license:
    status: partial
    scopes:
      - scope: PyTorch 固定 commit 根代码 LICENSE；生成站点及第三方材料另计
        identifier: BSD-3-Clause
        url: https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/LICENSE
    notes: 根许可沿用本库对 PyTorch v2.6.0 的已核对记录；不概括所有文档与发行包。仅原创归纳和链接。
  notes: 核对 async_save、AsyncStager、StorageWriter 和 filesystem.py 的 sync_files、写入、元数据提交；不是目标后端持久性或 TorchNPU 支持声明。
- id: src.linux-man-pages.fsync-6.19
  title: Linux man-pages 6.19 fsync(2)
  url: https://man7.org/linux/man-pages/man2/fsync.2.html
  kind: documentation
  registered_at: "2026-09-29"
  revision: "man-pages 6.19; manual date 2026-02-08; HTML generated 2026-09-09"
  license:
    status: unknown
    scopes: []
    notes: 本次未成功取得该手册源文件许可声明，只保存精确链接与原创解释。
  notes: 核对文件数据/元数据同步、目录项边界和错误返回；不据此推断网络或对象存储的完整协议及目标现场保障。
- id: src.ascend.mindio-acp-v26.1.1
  title: MindIO ACP v26.1.1 固定 README
  url: https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/mindio/acp/README.md
  kind: repository
  registered_at: "2026-09-29"
  revision: 44385c13d7b1d87def35f1604e8be4d16de6ca4e
  license:
    status: partial
    scopes:
      - scope: 固定 MindCluster commit 的根代码许可；组件文档与第三方材料仍需分别核查
        identifier: Apache-2.0
        url: https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/LICENSE
    notes: 沿用同 commit 已核对的根代码许可；没有把 docs/LICENSE 的范围自动延伸到 component 下 README，也未核验 wheel 和第三方内容。仅原创归纳与链接。
  notes: 只核对 README 的先内存暂存、再异步后端写入关系；未核对接口/副本/回退细节，未安装或运行，不构成与现有 TorchNPU 档案的整栈配套。
```
