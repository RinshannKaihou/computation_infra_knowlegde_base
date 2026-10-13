# 第十九批 T04-01 修订来源记录

任务：T04-01（修订 `training-data-path.md`，只做加法 + 一处明确标注替换）。取证日期 2026-10-14。

## 候选来源（3 项新登记 + 复用）

新登记：sampler-source-v2.6.0、distributed-sampler-source-v2.6.0、stateful-dataloader-0.11.0（版本化文档 + 固定 tag 实现）。复用：data-loader-2.6、dataloader-source-v2.6.0（含 DataLoader 无 state_dict/set_epoch 否定证据）、cuda-semantics-2.6、torch-npu-v7.2.0-pytorch2.6.0、三 TorchNPU 快照、CANN 传输页组九项、dcp-2.6（含 stateful.py 补核）、mlcommons.storage-rules-v2.0、numerical-verification-2.6。

## 主张—来源定位表（可逐项复核）

固定 commit：PyTorch `1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340`（tag v2.6.0）；TorchData `377e64c1be69a9be6649d14c9e3664070323e464`（tag v0.11.0）；TorchNPU `bc51ab84cc6f35c77aab1c59886e0ea43681a317`；CANN 8.2.RC1.alpha001 静态页。

| 主张 | 精确页面/源码与定位 | 支持范围 / 不支持 |
|---|---|---|
| 概念关系（应用样板） | [randomness 多 RNG/worker 种子](https://docs.pytorch.org/docs/2.6/notes/randomness.html)（manual_seed 全设备、worker 重种算法、worker_init_fn+generator） | 实际清单格式 unknown |
| DCP 收窄 | [metadata.py L135–147](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/metadata.py#L135-L147)（storage_data: Any）；[filesystem.py L66–72](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/filesystem.py#L66-L72)（_StorageInfo 三字段）；[stateful.py](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/stateful.py)（两方法）；[state_dict_loader.py](https://github.com/pytorch/pytorch/blob/v2.6.0/torch/distributed/checkpoint/state_dict_loader.py)（Stateful 回调先于公共 load 返回）；[serialization.py L196–204](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/serialization.py#L196-L204)（set_crc32_options(False) 可加载） | 28 文件扫描历史沿用；不概括任意损坏可加载 |
| 三类验证表 | 上行定位；通过条件为正文方法选择 | 不定义通用清单格式 |
| RandomSampler/DistributedSampler | [sampler.py](https://github.com/pytorch/pytorch/blob/v2.6.0/torch/utils/data/sampler.py)（generator 可空）；[distributed.py](https://github.com/pytorch/pytorch/blob/v2.6.0/torch/utils/data/distributed.py)（seed+epoch、set_epoch警告、补齐） | 无 generator≠必然不可复现（全局 RNG 固定则可） |
| DataLoader 无游标 | [dataloader.py](https://github.com/pytorch/pytorch/blob/v2.6.0/torch/utils/data/dataloader.py)（77162 B，state_dict/set_epoch 零命中） | 所查文件否定证据 |
| StatefulDataLoader 分支 | [stateful_dataloader.py L334–346](https://github.com/pytorch/data/blob/377e64c1be69a9be6649d14c9e3664070323e464/torchdata/stateful_dataloader/stateful_dataloader.py#L334-L346)（默认 sampler）；[L496–577](https://github.com/pytorch/data/blob/377e64c1be69a9be6649d14c9e3664070323e464/torchdata/stateful_dataloader/stateful_dataloader.py#L496-L577)（序列化尝试＋fast-forward 回退）；[sampler.py L55–80](https://github.com/pytorch/data/blob/377e64c1be69a9be6649d14c9e3664070323e464/torchdata/stateful_dataloader/sampler.py#L55-L80)（iterator state）；[0.11.0 API](https://docs.pytorch.org/data/0.11/torchdata.stateful_dataloader.html) | 不跨 rank；同 num_workers；NPU 未验证 |
| NPU 三路表 | [CopyKernel.cpp L85–122](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/common/CopyKernel.cpp#L85-L122)（路径范围注释＋下发分支）；[CachingHostAllocator.cpp L181–205](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/CachingHostAllocator.cpp#L181-L205)（三路判定）/[L214–235](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/CachingHostAllocator.cpp#L214-L235)（processEvents） | 限该拷贝路径；条件接口≠目标能力 |
| CANN 0106/stream/event | [0106](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0106.html)（非 MallocHost 不报错＋业务不可预知，不作 SDC 断言）；[0076](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0076.html) stream 等待；[0086](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0086.html) event 查询（返回 0 仅查询成功，完成由 COMPLETE/NOT_READY 出参判断；跨线程乱序警告；0020/0086 版本绑定弱）；[0091](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0091.html) **stream 等待 event**（源 stream [RecordEvent](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0083.html) 在先，目标 stream WaitEvent；主机异步返回，须后接同步确认） | 0088/0089 未取证 |

## unknown 清单

U1 清单格式；U2 torch 精确游标；U3 TorchData/2.6 配套；U4 NPU 下行为；U5 C08 联动（例外清单）；U6 worker 崩溃游标；U7 缓存失效语义；U8 iterable 分片；U9 CANN 0088/0089；U10 跨平台重复性。
