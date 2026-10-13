# 第十九批 T03-05 RCCL 来源记录

任务：T03-05（`rccl-runtime-and-verification.md`，reference）。取证日期 2026-10-14。

## 候选来源（2 项新登记 + 复用）

新登记：rocm-systems-therock-10.1（tag 固定源码，rccl/rccl-tests 各自 LICENSE.txt；仓库根许可 unknown）、rocm-systems-pr-9745（主案例，merged 2026-08-09；最早入版与 hang 机理 unknown）。复用：rccl-docs-10.1.0、rocm-compatibility-matrix-10.1.0、rocm-release-notes-10.1.0、instinct-mi300x-system-acceptance-2026-10-09。

## 主张—来源定位表（可逐项复核）

固定 commit：`7da43026e4f2ef7600433c38c820732f7a205d22`（tag therock-10.1）；文档别名 `docs-10.1.0`（RCCL 站标 2.30.7）。

| 主张 | 精确页面/源码与定位 | 支持范围 / 不支持 |
|---|---|---|
| 样板五元各自支持 | [兼容矩阵](https://rocm.docs.amd.com/en/docs-10.1.0/compatibility/compatibility-matrix.html) 系统需求三表（MI300X/CDNA3/gfx942；Ubuntu 24.04.5；amdgpu 31.60.0）＋ Communication libraries 行（RCCL 2.30.7→therock-10.1 树） | 各维度支持集；无整栈已测组合（U1） |
| 初始化映射 | [library-specification](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/api-reference/library-specification.html) Communicator functions 节（UniqueId/InitRank/InitAll/Count/CuDevice/UserRank） | "CUDA device"残留措辞冲突照录（U4） |
| 原语名单与 deprecated | [api-library](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/api-reference/api-library.html) Operations 节；`ncclAllToAll`→`ncclAlltoAll`、`ncclBcast`→`ncclBroadcast` | P2P 初步支持口径 |
| 返回五态/恢复前提 | [fault-tolerance](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/how-to/fault-tolerance.html) Note（config.blocking=0）、Error handling（9 码）、Asynchronous errors（poll）、Recovering（Abort 线程前提、deadline）、对称内存 abort 节；[group.cc L919–958](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl/src/group.cc#L919-L958) 后台 job + ncclInProgress | 未运行故障注入 |
| NCCL 对照五点 | fault-tolerance 首段；[env-variables](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/api-reference/env-variables.html) NCCL_PXN_C2C/NVLS 行；[CHANGELOG](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl/CHANGELOG.md) 2.30.4/2.28.3 Removed 节 | 对照专用，不作等价证据 |
| 日志变量全名与目的集 | env-variables NCCL_DEBUG_SUBSYS 节（默认 INIT,BOOTSTRAP,ENV；`SUBSYS=` 零命中）；INIT/TUNING/COLL 目的集 | MPI 远端传递按 launcher 条件 |
| 采集清单与 Replayer | [troubleshooting](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/how-to/troubleshooting-rccl.html) Collect RCCL information、Replayer 三步、NIC counts 节 | 日志行格式无规范（U10） |
| 通道版本行为 | [usage-tips](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/how-to/rccl-usage-tips.html) MI350X 通道段、CPX/DPX 段、对称内存四前提 | MI350X 行为作版本差异证据 |
| 计时口径（us） | [common.cu L1070–1087/L1259–1266](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/common.cu#L1259-L1266)（×1.0E6）；[util.cu L780–787](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/util.cu#L780-L787) `(us)` 表头；PERFORMANCE.md ms 记来源冲突 | 默认模式；-C/-I/-G/device 另口径 |
| 校验默认与门限 | [README L163–187](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/README.md#L163-L187)（-c 默认 1、-n 20、-w 1、-a 聚合、-T 禁用）；[common.cu L1192–1256](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/common.cu#L1192-L1256) 重跑校验；[common.cu L2757–2788](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/common.cu#L2757-L2788)（MIN_BW 继承、0.9 系数、退出）；[util.cu L500–514/L799–806](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/util.cu#L799-L806)（N/A vs wrong） | 重跑≠全迭代证明；门限随环境 |
| PR #9745 四分 | [PR 页](https://github.com/ROCm/rocm-systems/pull/9745)（merged 2026-08-09，commit 5bc651a）；[RegisterTests.cpp L55–66/L574–581/L671](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl/test/RegisterTests.cpp) | 最早入版（U7）与 hang 机理（U8）unknown |

## unknown 清单

U1 整栈已测组合；U2 仓库根许可；U3 latest/别名 diff；U4 CUDA 措辞澄清；U5 MI350 LL 影响面；U6 CHANGELOG 版本标注冲突；U7 主案例最早入版；U8 hang 机理；U9 rccl-tests 官方门限（本库 P1/判据四分为方法选择，非上游门限）；U10 日志行格式；U11 API 限流未查；U12 四元组 documented 非 reproduced。
