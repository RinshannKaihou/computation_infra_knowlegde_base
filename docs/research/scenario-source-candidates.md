# 问题专题的来源候选

2026-09-29，主任务在批次审阅期间做发现与初筛。本文件不是正式案例、支持矩阵或已完成来源登记；候选只有通过对应任务的完整核查后才能进入 `knowledge/`。

| 候选 | 已读内容 | 可研究的主题 | 缺口与取舍 |
|---|---|---|---|
| [vLLM Ascend #9490](https://github.com/vllm-project/vllm-ascend/issues/9490) | Issue 正文：作者报告 Ascend 910、v0.18.0rc1 镜像、Kubernetes/KServe、TP=2；非 root 身份初始化失败，修改派生镜像后能够启动 | 容器身份/用户态条件与 HCCL 初始化；可作为设备资源链的边界反例 | 派生镜像同时改变用户条目与环境变量，不能确认单一变量因果；这是初始化失败，不是已证明的设备不可见。问题处于 open，不宜硬套 T02-C 标题或作为通用处方 |
| [vLLM Ascend #1955](https://github.com/vllm-project/vllm-ascend/issues/1955) | Issue 正文给单机 910B2C×16、v0.9.2rc1 镜像、启动配置与 socket timeout 片段；页面显示 closed 和 wait-feedback | T03-C 的 HCCL 超时候选 | 尚未取得完整评论、关闭理由、明确修正与复验；不能把 closed 视为修复。正文中的清日志等命令没有执行，也不纳入操作步骤 |
| [vLLM Ascend #14296](https://github.com/vllm-project/vllm-ascend/issues/14296) | Issue 正文给硬件/OS/Python/CANN/TorchNPU/vLLM 标识、启动期 AIV timeout、日志片段及作者的并发通信组解释 | T03-C 的通信等待与配置分支候选 | 正文前段称只关闭 enable_dsa_cp 有效，末段又列同时关闭 enable_flashcomm1；变量控制存在差异，根因仍是报告者判断。未取得维护者评论、修复 commit 或发行记录，不能宣告通用修复 |

三个 Issue 的正文均经精确 URL 打开；未引用搜索摘要作为案例证据。尝试只读获取 #14296、#1955 的公开 GitHub API 评论时返回 HTTP 403，因此评论和关闭原因仍未知，没有把读取失败解释为“没有评论”。后续可通过可访问的官方页面完整核查；需记录实际访问时点和永久评论链接。

补充的训练恢复发现入口：[PyTorch 2.6 DCP](https://docs.pytorch.org/docs/2.6/distributed.checkpoint.html)已读取并用于 F10；MindIO 当前网页入口有静态读取失败，F10 最终改用已核查的 MindCluster 固定 README。二者属于机制来源，不能改写为真实事故。

这些候选尚未下载或保存大日志、运行脚本、改动集群或发送任何外部消息。后续案例应保存原创精简时间线和近旁引用，控制引用长度，并单独登记 Issue 内容的复用范围。
