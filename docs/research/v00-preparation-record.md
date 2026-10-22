# V00 准备实例交付与审计记录

交付日期：2026-10-22。本记录对应**独立验证轨道首轮交付**（用户会话称 Batch 33；验证工作包不计入内容批次，内容批次终止于 Batch 32）。交付物为 [plans/v00-preparation-instances.yaml](../../plans/v00-preparation-instances.yaml)：执行 [验证清单](../../plans/validation-backlog.yaml) 中 V00 的"先收集已知字段，未知项在该实例保留"步骤，为 12 个验证包整理 **19 个准备实例骨架**——V01–V05、V07–V09、V12 各一；V06 按其 phase gates 拆两实例（CPU direct-set missing-FQN 组、DCP callback 与多 rank 身份组）；V10 按四后端 subrun 拆四实例（ext4/NVMe、NFSv4.1、Ceph RGW/S3、Lustre）；V11 按四 subrun 拆四实例（共享与租户隔离、节点变更与回退、控制面恢复与账本、服务发布与请求恢复）。

## 定位与边界

- **只整理，不执行**：所有实例 `instance_status: skeleton_prepared`、`readiness: not_ready`。未取得任何独立资源与授权（`resources_available`/`authorization_scope` 全 null），未冻结任何脚本/输入，未建立外置脱敏证据位置，未指定清理/恢复负责人。
- **不改变任何状态**：12 个 V 包 `status` 均保持 planned、`executed_at` 保持 null；既有七份方案真实执行仍为 **0/7**；01.6 实测 gap（V08）、08.7 真实执行（V01–V07）、V12 独立评测集缺证据均维持 open。
- **不构成执行授权**：validation-backlog 的 notice（本文件不提供硬件/集群/生产执行授权）继续适用；实例通过各自验收"只使相应验证子组就绪，不代表所有验证资源准备完成"。
- **已知字段不是新主张**：每实例的 known_fields 是对既有方案条目（experiment）与正文方法锚点的概述＋指向，技术细节以所引条目为准；V03 实例明确 HCCL Test 配套发行物缺口与 03.5-BLOCKED-1 同源。

## 已知字段来源

| 包 | 既有方案条目（scheme_refs） | 方法锚点正文 | 来源锚点 |
|---|---|---|---|
| V01 | `software-stack.ascend-version-mismatch-experiment` | ascend-version-mismatch-triage、environment-installation-and-upgrade | torch-npu 固定配套、CANN 8.3.RCX 安装前提 |
| V02 | `cluster-platform.ascend-device-visibility-experiment` | device-resource-chain | K8s v1.32 Device Plugin、MindCluster v26.1.1、vLLM Ascend #2557/#2541 |
| V03 | `communication.hccl-timeout-experiment` | hccl-timeout-triage、bandwidth-baselines | HCCL 用户指南 8.1.RC1.alpha001、cann-hccl 2d685b08 |
| V04 | `communication.nccl-timeout-experiment` | nccl-timeout-triage、bandwidth-baselines | NCCL 2.27.5、nccl-tests b4d5beeb、PyTorch 2.8 变量页 |
| V05 | `training.gpu-npu-precision-difference-experiment` | gpu-npu-precision-difference-triage、mixed-precision-and-convergence | msprobe 固定指南、PyTorch 2.6 数值/状态文档 |
| V06×2 | `training.checkpoint-state-recovery-experiment` | checkpoint-state-consistency | PyTorch DCP 2.6、Issue #164257、修订 edd8d35 |
| V07 | `inference.ascend-inference-tail-latency-experiment` | latency-metrics、execution-and-kv-cache | vLLM v0.14、vllm-ascend v0.14.0rc1 |
| V08–V12 | 无既有方案 | 各包 existing_content_prerequisites / 方法正文（验收、RDMA、存储、平台与服务、评测方法） | 无新增 |

## 账面

- **registry 无新增**（577 维持）：全部 source_anchors 复用既有登记；本交付为既有知识的重组，不产生新来源需求。
- **内容条目无变化**（135 维持）：不新增/修订任何 knowledge/ 与 paths/ 条目；内容覆盖统计 62/1/0 不受影响。
- **实例引用**：validation-backlog.yaml 的 V01–V12 `preparation_instance_ref` 已指向实例文件（fragment 约定＝package id，经 package_index 解析到该包全部实例）；V00 自身保持 null（V00 不为自己准备实例）。top-level 新增 `preparation_delivery` 块记录交付事实；V00 `preparation_note` 追加一行交付说明。
- **机器可读性**：实例文件经 YAML 解析与内部一致性自检——19 实例；package_index 与实例 id 集合一致；`instance_schema` 声明的字段在 19 个实例全部存在（含 `source_anchors`，无锚点者为显式空列表）；全部 `source_anchors` 可对 registry 解析、无未登记 ID；`common_pass_floor` 引用项 19/19；readiness 全 not_ready。初审发现该自检首版口径不足（V00R-C01 五处来源 ID 错拼、V00R-C02 六实例缺 `source_anchors` 键），修订后自检扩为上述逐字段＋registry 交叉核对。
- `make check` / `make build` 通过（结构与引用校验；不证明技术主张或资源就绪，也不校验 plans/ 内字段契约——该缺口由审阅弥补）。

## 审阅账面

- **初审**（2026-10-22，`gpt-6.1-sol / xhigh`，报告见[独立审阅报告](v00-preparation-review.md)；调用方经 `~/.codex/sessions` turn_context 核验单一模型/档位/cwd）：结论"修订后通过"，发现 7 项——P2×6（V00R-C01 五处来源 ID 将点号误写为短横线致 4 个 registry ID 不可解析、C02 六实例缺 `source_anchors` 键且自检账面不实、C03 V00 附语误设"全体实例通过才可推进"总门槛、C04 V06 第二实例环境清单未分列端到端 B 组（P/F/2.8.0）与多 rank C 组（2.6.0）、C05 V02 判据丢失 N1 条件性、C06 各实例通过清单缺共同验收兜底）＋P3×1（C07 V11 节点变更 B0/N/R 表述缺方法出处）。
- **修订**：C01 五处恢复既有稳定 ID（不新增别名）并自检全量解析；C02 六实例补 `source_anchors: []`、自检口径扩为逐字段；C03 附语改为"本次交付不改变状态＋按各实例独立验收与推进、不阻塞其他子组"；C04 端到端 B 组复用 V06-CPU 的 P/F 不可变制品并另列 H0 的 2.8.0 身份、多 rank C 组单列 2.6.0 环境与启动方式、未覆盖组明确保持未就绪；C05 判据恢复"若执行 N1"限定与 H3 未验证范围；C06 新增 `common_pass_floor`（环境身份/脚本输入冻结/授权与资源/停止清理恢复负责人/外置证据位置五项共同门槛＋缺项保留与不适用理由规则）、schema 定义局部清单为其上增量、19/19 实例追加门槛引用项、V12 补冻结评测执行件与案例集治理增量；C07 改用本子组方法正文自身的变更档案/预检/逐层三态判据表述并注明 B0/N/R 仅作跨域参照。
- **定向复核**（同会话 resume，显式携带 `gpt-6.1-sol / xhigh`；报告见[定向复核](v00-preparation-recheck.md)，调用方独立核验 rollout JSONL 最新 turn_context＝gpt-6.1-sol/xhigh/cwd 一致）：V00R-C01–C07 **7/7 全部 CLOSED**，修订未引入新问题；按初审报告要求重跑 C01/C02 全量交叉核对（22/22 来源引用可解析、19/19 字段齐备）、C03/C05 条件分支纸面检查（含"V06 CPU 已验收、其他资源仍未知"与"V10 一后端已验收、其余仍 planned"场景）、C04 B/C 环境对照、C06 逐实例验收覆盖（19/19 恰有一次共同门槛引用、重点四例覆盖）、C07 方法定位。**终态：审阅通过**——该结论仅覆盖准备实例骨架的编辑与结构审阅，19 实例仍为 skeleton_prepared/not_ready，各 V 包 planned，七份方案真实执行 0/7，不构成执行授权。`make check`/`make build` 复跑通过（135/577 维持）。

## 写作轮次自记

- 实例骨架的字段结构对齐 V00 验收句"真实环境、来源/脚本/输入/判据、已有授权范围与清理恢复条件可审阅；缺项逐条保留"：known_fields 覆盖判据/设计/停止恢复要求（来自方案），unknown_fields 逐项保留环境身份、冻结件、重复与阈值、授权与证据位置等缺项。
- V06 第三阶段（存储后端/设备扩展）与 V09 的条件扩展（特定 collective/AMD/HCCL、路由/rail）按 backlog 语义"选定后另建实例"，未建占位实例。
- 概括性表述（如"四步执行方法"）均指向方案条目相应章节，不复制正文，避免转写走样；数字计数（19 个实例、12 个包、0/7）与文件实际内容核对后填写。
