# 第三十一批 T02-12 来源记录

任务：T02-12（三平台安装基线、迁移升级与回退验证；**new** `knowledge/02-software-stack/environment-installation-and-upgrade.md`，主题 02.7）。取证轮次：主会话作者角色首轮（2026-10-21；前置 T02-01/03/04/05/08/09/10/11、T06-05、T06-09、T07-04/05、T07-12 均已交付）。

## 新增来源与主张定位

| 主张 | 登记 ID | 精确位置 | 支持范围 |
|---|---|---|---|
| 预安装检查/冲突方法处理；cuda-toolkit-X.Y 并列安装且锁定 release；cuda-uninstaller（runfile 卸载）；验证走 deviceQuery/bandwidthTest（非 nvidia-smi/nvcc -V；/dev/nvidia* 缺失与 SELinux 提示）；Ch.11 通配 purge＋autoremove | ~~src.nvidia.cuda-128-install-guide-linux（本轮新增）~~ **ID 已废止**：C13 复核起并入既有 src.nvidia.cuda-12-8-installation-guide-linux（Batch 31 补读段） | [CUDA 12.8 Installation Guide for Linux](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-installation-guide-linux/index.html)（archive 版本化页，Ch.2/3.12.3.7/5.4/10.2.2/11） | CUDA 12.8 文档线；非部署证明 |
| Ubuntu 驱动安装（linux-headers；local repo 装 nvidia-driver-local-repo 包并复制 keyring、network repo 装 cuda-keyring 包，两种路径不同；apt install nvidia-open、dist-upgrade 升级）；version-locking（nvidia-driver-pinning-<分支/版本> 锁包、Pin-Priority>=1000 允许降级、Debian 示例 580.103→570.199 降 57 包、DNF versionlock/Zypper addlock 排除式、Ubuntu 580 及以前包名带分支/590 起去分支化） | src.nvidia.driver-installation-guide-latest-2026-10-21（**本轮新增**） | [Driver Installation Guide](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/latest/index.html)（latest 可变页，Ubuntu 与 version-locking 两节，2026-10-21 读取） | latest 可变页非固定快照；固定 580 README 语义另条目分立 |
| 升级前必读（instg_0028：禁止其他维护操作/业务中断/高→低回退须卸载重装/latest 软链接/固件>驱动>CANN 顺序）；固件驱动 .run --upgrade＋reboot＋npu-smi info（instg_0029）；CANN 升级（instg_0030：yum/conda 版本号、磁盘"可用>已占用+10G"、跟随宿主包安装的 Kernels 自动卸载须重装）；卸载（instg_0032 按包分列完整路径、instg_0033 驱动/固件完整路径，R05 更正后口径） | src.huawei.cann-83rcx-upgrade-uninstall-2026-10-21（**本轮新增**） | [安装指南目录](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/83RC1/softwareinst/instg/instg_0098.html) 及 instg_0027/0028/0029/0030/0031/0032/0033（doc_center/source 静态镜像核读；页头 8.3.RCX/URL 83RC1 沿既有边界） | CANN community 8.3.RCX 文档线 |
| ~~ROCm 10.1 安装页补读：……无专门卸载章节~~ **已被取代**（复核轮 R04：Uninstalling 节存在，含包管理器卸载/Remove ROCm repositories/缓存清理及 venv/tarball/runfile 分支；未知项收窄为"完整版本回退与依赖恢复"）；runfile gpu-access=user/all、"7.2.4 或更旧须先卸载"、pip 验证命令仍有效 | src.amd.rocm-install-docs-10.1.0（**既有条目本轮补读**，notes 的 Batch 31 段已按 R04 更正并留误记痕迹） | [Install ROCm 10.1.0](https://rocm.docs.amd.com/en/docs-10.1.0/install/rocm.html)（2026-10-21 补读＋原始 HTML 复核 Uninstalling） | docs-10.1.0 版本化页 |

## 复用来源与主张定位

| 主张 | 登记 ID | 精确位置 | 支持范围 |
|---|---|---|---|
| npu-smi info 驱动就绪前置、CANN 快速安装（conda/yum/run 命令、Toolkit+Kernels+NNAL 配套） | src.huawei.cann-83rcx-install-2026-09-29 | instg_quick/instg_0005（第九批已核） | 8.3.RCX 安装线 |
| 安装场景选择（物理机/虚拟机/容器）；torch_npu 配套（驱动固件+CANN 版本配套另查） | src.ascend.torch-npu-7.2.0-install-guide-2026-10-09 | insg_0001/0002（第九批已核） | Pytorch/720 文档树 |
| 设备文件语义（/dev/nvidiactl 等、0666 默认） | src.nvidia.driver-readme-580.105.08 | README Ch17B/Ch7（第九批已核） | 580.105.08 固定 README |
| cuda-compat 前向兼容矩阵（R545 不在列、限定对象） | src.nvidia.cuda-forward-compatibility-2026-10-09 | Table 3（第九批已核） | 可变页＋观察日期 |
| minor version compatibility 大类边界 | src.nvidia.cuda-compatibility-latest-2026-09-30 | 页面（第九批已核） | latest 可变页 |
| 容器"驱动不入镜像"、宿主/镜像职责 | src.nvidia.framework-containers-user-guide-2026-09-30 | 指南（第九批已核） | 方法层 |
| bandwidthTest 样例 | src.nvidia.cuda-samples-bandwidthtest-2026-10-08 | 样例页（第九批已核；master 树入口本轮连接器读取不稳定） | 正文一律用 v12.8 固定 tag 树；master 入口留 registry |
| MI300X OS/内核兼容（Ubuntu 24.04.5 GA 6.8 等） | src.amd.rocm-compatibility-matrix-10.1.0 | 矩阵选择器页条件块（第九批已核） | 选择器页＋观察日期 |
| 10.1.0 OS 支持窗口变化 | src.amd.rocm-release-notes-10.1.0 | release notes（第九批已核） | docs-10.1.0 |
| rocm_bandwidth_test 样例 | src.amd.rocm-bandwidth-test-d7f5efe | 固定 commit（第九批已核） | 固定快照 |
| video/render 组与 udev 语义 | src.amd.rocm-install-linux-prerequisites-7.2.4 | prerequisites（第九批已核） | docs-7.2.4 页（版本映射随页注明） |
| 版本化安装建议的现实错配例子 | src.vllm-ascend.issue-1188 | Issue（第九批已核） | 用户内容＋成员建议，非配套证明 |
| 安装后配置（set_env.sh、依赖库 protobuf==3.20.0/numpy<=1.24.0、推理样例 top1–top5） | src.huawei.cann-83rcx-upgrade-uninstall-2026-10-21（instg_0094 一并核读，随升级/卸载条目登记） | instg_0094 | 同上 |

## 本文原创部分

七层安装验证梯子（含每层停止条件与"失败时进入"映射）、三平台按梯子组织的步骤表、迁移升级变化矩阵（改变项×三平台×检查层）、回退与不可逆边界小节（制品保留/平台回退路径/不可逆/恢复门槛）、与相邻正文的连接。

## unknown 清单

1. 全部命令未执行；本文为文档档案，非可直接部署环境（applicability.environment_refs 空）。
2. NVIDIA 驱动指南为 latest 可变页（2026-10-21 观察）；固定 580.105.08 README 与之分立，不合并成同版本证据。
3. CANN 页头 8.3.RCX/URL 83RC1 版本标识不一致沿既有登记边界；OS×机型具体兼容结果未取得（交互查询工具静态抓取只得外壳）。
4. ~~ROCm 安装页无专门卸载/回退章节~~ **已被取代**（R04：Uninstalling 节含卸载与仓库/缓存清理，按安装方式分列）；仍 unknown 的是完整版本回退与依赖恢复能力。
5. 固件层回退（升级后降固件）无公开路径，保持 unknown，变更前须向支持渠道确认。
6. MindIE/MindSpeed/上层框架与引擎的安装不在本文（属 06/07 域各自档案）。

## 复核轮修订记录（初审后）

- C01：梯子表加"所需证据/能证明/不能证明"三列语义；L2 拆驱动加载与版本身份证据；L4 改为"环境脚本=必要条件，实载按运行时篇方法另记，无法采集即未完成"。
- C02：新增"最小算子/同步与结果契约"小节——三平台样例判据=样例自带校验（deviceQuery/bandwidthTest/形态比对/传输测量），计算正确性契约须另行冻结输入与预期，未冻结即无法判断，由验证轨道承接。
- C03：变化矩阵扩为十一行（hardware/OS/驱动/runtime/library/framework/backend/engine/model+config+input/不变项），每行约束来源就近定位；新增 B0/N/R 三状态对照方法表（同负载同判据，首次安装以安装前状态替代，不虚构基线）。
- C04：新增"变更前准入门禁"小节（三类缺项停止）；不可逆扩展至数据/模型转换/状态格式；恢复门槛改"按实际受影响层重查＋与 B0 同判据对比"。
- C05：制品保全与全量卸载分列；CUDA §11 通配会命中并列旧版标注为命令模式语义推断（未执行）；删除 CANN"旧版本目录仍在"承诺，改 unknown＋自留 .run 制品。
- C06：ROCm"无专门卸载章节"为误记（两轮网页转换漏读；原始 HTML 复核 Uninstalling 节存在，10-09 既有登记已有 autoremove 命令）——正文改"页内 Uninstalling 节给包管理器卸载；完整回退/依赖恢复/仓库清理 unknown"，registry Batch 31 补读段同步更正并留误记痕迹。
- C07：固件卸载完整路径 /usr/local/Ascend/firmware/script/uninstall.sh；CANN 卸载脚本路径按包分列（Toolkit/NNRT arch 目录、NNAE、Kernels、NNAL scripts）。
- C08：cuda-toolkit-12-8 具体坐标＋上游 X.Y/X-Y 模板冲突照录（registry 同步）；local repo（nvidia-driver-local-repo 包＋复制 keyring）与 network repo（cuda-keyring 包）分别描述。
- C09：Kernels 自动卸载加前提"跟随 Toolkit/NNAE/NNRT 安装的"；独立安装（8.0.0 起）另判。
- C10：L1/门禁改"查不到＝操作不放行；证据状态 unknown；仅封闭全集表或明确否定才记不支持"。
- C11：02 index 阅读顺序 14 的"审阅已闭环"改为"审阅修订中"（待定向复核通过后再更新）。
- C12：升级矩阵与回退各条补就近来源（节名）；instg_0094 并入 CANN 条目 revision；7.2.4 prerequisites 与 cuda-samples-v12.8 补入 source_refs；bandwidth-test URL 钉固定 commit 树；06/07 恢复入口给具体正文。
- C13：删除重复身份 src.nvidia.cuda-128-install-guide-linux，Batch 31 核读并入既有 src.nvidia.cuda-12-8-installation-guide-linux（含 §3.12.3.7 双模板、§11 通配语义）；正文/取证 source_refs 同步替换。

## 第二轮修订记录（复核后）

（待审阅后回填）

## 第三～四轮修订记录（复核 R08–R14）

- R08/R13：三平台 L2 的"安装身份/已加载身份/固件信息"分项落字段。NVIDIA 已加载身份首稿误写"文档线无查询命令"——第三轮复核指出驱动指南 Post-installation Actions 有 "Verify the Driver Version"（`cat /proc/driver/nvidia/version`），本轮作者独立核读该节后修正正文并补入 registry（首登仅核读 Ubuntu/version-locking 两节的范围限制如实保留）。AMD 加 rocminfo 为文档线自身 L2/L5 合并确认＋固件字段 unknown；Ascend npu-smi info 为已加载证据、固件/驱动两包分别登记。
- R09：方法表加版本范围注（运行时篇样板 8.2.RC1.alpha001/HIP 6.3.42134 与本文档线不同，入口仅旧版样板）。
- R10：registry ROCm unknown 收窄为"完整版本回退与依赖恢复"，仓库/缓存清理步骤补记。
- R11：取证 NVIDIA 驱动行 local/network 分列。
- R12/R14：正文 bandwidthTest 链接改 v12.8 固定 tag 树；扩展 src.nvidia.cuda-samples-v12.8 核读范围至同 tag bandwidthTest（README 实读：传输测量、无显式通过阈值、CUDA Toolkit 12.5 原文照录）；首轮"本轮新增"已废止 ID 行标注并入既有条目。
- R15：registry/取证两处 "CUDA Toolkit 12.5+" 改为 README 原文照录 "CUDA Toolkit 12.5"，不外推更高版本要求。
