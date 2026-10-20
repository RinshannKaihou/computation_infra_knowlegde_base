# 第二十七批 T07-05 来源记录

任务：T07-05（推理输出质量的对照评估方法与案例；**new** procedure `knowledge/07-inference/output-quality-evaluation.md`，主题 07.4）。取证轮次：主会话作者角色首轮（2026-10-21；前置 T07-04 已 done）。目标：固定输入身份、区分采样变化与计算差异的层次、主指标/容差/样本量预注册、基线→单变量→恢复对照 schema、官方评估例与论文质量证据的归属纪律。

版本线（沿用既有钉扎）：vLLM v0.14.0＝`b17039bc`；vLLM Ascend v0.14.0rc1＝`52d4acfa`；MindIE-LLM＝master@`69e5a5dd`（文档线 3.1.0）。评估框架按各官方指南口径引用，不运行。

## 本轮取回清单（2026-10-21，固定 commit 原文件；SHA-256 前 16 位）

本轮新增取回 MindIE 两文件（其余复用 T07-04 轮缓存）：

| 文件 | SHA-256 前 16 位 |
|---|---|
| docs/zh/faq/faq.md（936 行） | 3c4f5db3c425f401 |
| docs/zh/developer_guide/test.md（3 行，存根） | de6ea3dae38eeffc |

复用缓存（T07-04 轮已取回并登记哈希）：va-using_lm_eval.md（29da7eb7d0c595e3）、va-using_evalscope.md（8e8eaf625027a233）、va-using_ais_bench.md（19c3087e40c30cb5）、va-using_opencompass.md（13a4b8c035e3c673）、vl-quant-int8.md（2d0c66123da0334c）；论文三篇（AWQ/GPTQ/SmoothQuant，摘要级，registry 已登记）。

## 主张—来源定位表

| 主张 | 登记 ID | 精确位置 | 支持范围 / 未覆盖 |
|---|---|---|---|
| lm-eval 在线路径：docker 起 vllm-ascend 服务后，容器内 `pip install lm-eval[api]`，`lm_eval --model local-completions --model_args model=…,base_url=http://127.0.0.1:8000/v1/completions,tokenized_requests=False,trust_remote_code=True --tasks gsm8k`；演示约 30 分钟出结果；先以 curl /v1/completions 单请求核验（示例 temperature=0、max_completion_tokens=1、stop 词，输出含 usage 与 kv_transfer_params 字段） | 扩展 src.ascend.vllm-ascend-v0-14-0rc1 | using_lm_eval.md L44–105（curl 样例）、L107–120（安装与命令，命令在 L116–120）、L123（30 分钟说明）——修订轮更正坐标 | 官方指南命令口径；未运行 |
| lm-eval 离线路径：同 docker 样板，`pip install lm-eval`（不带 [api]），离线模型直连；任务 YAML 可自定义 data_files/doc_to_text/doc_to_target/metric_list（gsm8k 样例给 train/test arrow 路径与 fewshot_split） | 扩展 src.ascend.vllm-ascend-v0-14-0rc1 | using_lm_eval.md L135 起（Offline Server 节）、L230–260（任务 YAML 片段） | 文档口径 |
| EvalScope：独立 venv 安装（gradio plotly evalscope），`evalscope eval --model … --api-url http://localhost:8000/v1 --eval-type server --datasets gsm8k --limit 10`，输出表（Model/Dataset/Metric=AverageAccuracy/Subset/Num/Score）；另有 perf 压测模式（evalscope[perf]）；官方文档 evalscope.readthedocs.io | 扩展 src.ascend.vllm-ascend-v0-14-0rc1 | using_evalscope.md L55–90（安装/命令/输出表）、perf 节 | 文档口径；--limit 10 为演示样本量 |
| AISBench（gitee aisbench/benchmark）：精度＋性能评估；要求 `--max_model_len` 大于 35000 否则"精度评估可能受影响"（L41–45 指南自身示例＝35000 与注释要求＞35000 不一致，两说照录、指南限定——修订轮同步）；数据集逐个下载安装（C-Eval 从 ModelScope、MMLU/GPQA 从 opencompass OSS），每数据集有 README；attr="service" 服务评估路径 | 扩展 src.ascend.vllm-ascend-v0-14-0rc1 | using_ais_bench.md L3、L45、L56–111 | 文档口径；gitee 仓未取回 |
| OpenCompass：OpenAISDK 连服务评估——配置 meta_template（HUMAN/BOT 角色并保留 SYSTEM，L82–87——修订轮更正）、openai_api_base、tokenizer_path、query_per_second=1、rpm_verbose；数据集经 opencompass 配置 | 扩展 src.ascend.vllm-ascend-v0-14-0rc1 | using_opencompass.md L85–120 | 文档口径 |
| vLLM 上游的质量评估步骤：INT8 量化流程第四步"评估精度"，示例 `lm_eval`＋gsm8k（量化侧命令 L117–139）；"baseline 为未量化模型同任务结果"是本库方法要求非该页内容——修订轮归属更正 | 扩展 src.vllm.inference-v0-14 | int8.md L117–136（T07-04 轮已核） | 官方流程口径 |
| NIXL PD 正确性对照入口：tests/v1/kv_connector/nixl_integration/ 的 run_accuracy_test.sh、toy_proxy_server.py、test_accuracy.py——分布式（PD）场景的输出一致性验证样板 | 扩展 src.vllm.inference-v0-14 | nixl_connector_usage.md L179–183 | 脚本存在性与用途；脚本内容未逐行核 |
| **MindIE 确定性与精度浮动 FAQ**：①确定性计算定义（输入不变时多次运行输出一致）；②精度数据集结果浮动的两层原因——后处理 sampling→greedy 可基本保证文本稳定＋确定性计算本身的问题；③相同输入组 batch 顺序不同输出不同的根因＝matmul 算子不同行累加顺序不完全相同（FAQ 原文用词"浮点加法无交换律"术语有误，技术上应为浮点运算**非结合性**与运算重排的舍入影响，据 PyTorch 2.6 数值精度说明更正——修订轮同步主表），可设 `ATB_MATMUL_SHUFFLE_K_ENABLE=0` 关闭 shuffle k 保证各行累加顺序一致（性能降约 10%，文档声明）；④Server 调度不确定性＝CPU 负载影响请求到达时间→组 batch 差异（调度框架 block 查询模式本身可保证确定性，faq.md L221–223——修订轮更正坐标，原 L224–226 为空行） | 扩展 src.ascend.mindie-llm-docs-69e5a5dd | faq.md L205–213（确定性计算/精度浮动）、L215–222（batch 顺序/ATB_MATMUL_SHUFFLE_K_ENABLE）、L221–223（Server 调度） | FAQ 口径＋术语更正归属；数值未实测 |
| MindIE PD 相关性能 FAQ：单机 A3 PD 混部 chat 接口劣化（单卡专家多、token 少、精度有差异场景）；PD 分离 D 节点 "Pull kv failed"（ERROR 级，CANN status_code 含 timeout；根因为 P→D KV 传输超时/网络质量差）——T07-07 共用 | 扩展 src.ascend.mindie-llm-docs-69e5a5dd | faq.md L23–27、L270–280 | FAQ 口径 |
| MindIE developer_guide/test.md 为 3 行存根，（标题＋"设计指南"一句内容简介，无外链——修订轮撤回"指向外部设计指南"初记） | 扩展 src.ascend.mindie-llm-docs-69e5a5dd | test.md 全文（3 行） | 存根照录 |
| 论文质量证据（摘要级，registry 已登记）：GPTQ 报告量化后精度保持（作者报告）；SmoothQuant 报告 negligible accuracy loss（作者报告）；AWQ 报告量化误差降低机制——质量数字均属作者报告，本库未复现 | 复用三论文登记 | abs 页 | 摘要级；实验设置未读全文 |

## unknown 清单

1. 四份评估指南的完整命令参数族（批次大小、并发、随机种子控制位）未逐项核；lm-eval/EvalScope/AISBench/OpenCompass 框架本体的版本与采样参数透传行为未取证（指南未钉框架版本）。
2. MindIE 精度评估：本轮检索范围（docs/zh 目录树）内未取得官方评估专页；可用口径＝FAQ 确定性条目＋Qwen README 对话样板＋ModelTest 入口（examples/atb_models/tests/modeltest/，README 级登记）；test.md 存根无外链。
3. NIXL accuracy test 脚本内部（对照判据、容差）未读；作为入口登记。
4. logits/数值层核对的引擎接口（logprobs 输出格式在 vLLM v0.14 的字段）未从 API 文档取证——正文只按 lm_eval 指南 curl 样例的 logprobs=null 字段记录存在性。
5. 采样温度/top_p 对各评估工具默认值的透传（lm-eval local-completions 的默认采样参数）未核。
6. 未运行任何评估命令；全部为文档/FAQ/论文摘要口径。

## 集成轮结果（2026-10-21 已执行）

- 无新增来源条目（本轮文件均在三个既有固定快照登记 scope 内）。
- 扩展 3 项 notes：src.ascend.vllm-ascend-v0-14-0rc1（四份评估指南命令级细节）、src.vllm.inference-v0-14（NIXL accuracy 脚本入口）、src.ascend.mindie-llm-docs-69e5a5dd（FAQ 确定性/精度浮动/PD 条目＋test.md 存根）。
- registry 维持 542 sources；T07-05 正文进入撰写轮。

## 初审修订轮（2026-10-21，响应 batch-27-t07-05-codex-review.md 的 C01–C07）

- C01：固定清单补评估协议冻结（任务 YAML 本身：few-shot/答案抽取/filter/指标聚合/生成模式）、BOS 处理；上下文预算分列（输入截断/总上限/生成上限）；"评估用 greedy/低温"改标本库方法选择（AISBench 样例 0.6、OpenCompass 0.01）；max_model_len>35000 记录指南自身示例与注释不一致（两说照录＋指南限定）。
- C02："浮点加法无交换律"更正为非结合性与运算重排的舍入影响（PyTorch 2.6 数值精度说明为据），FAQ 原文用词照录并注明归属；registry MindIE notes 同步。
- C03：差异分层改"待检验的解释"，删"合法/真缺陷"二分；四层表各层"能支持/不能支持"分列；恢复对照改条件性表述（未恢复＝未决）。
- C04：预注册补差值口径、不确定性与判定规则（不确定范围跨界＝未决；未检出≠无差异）；三种结论范围分列。
- C05：schema 补 run_id/baseline_ref/prereg_ref、变量有效值对、完整固定配置引用、执行路径证据位置；结果补计数关系（提交＝完成＋失败＋超时＋空输出）、重试口径、恢复判据与未决处置。
- C06：撤回"存根指向外部设计指南"（test.md 无外链，仅标题＋一句内容简介）；登记 ModelTest 入口（README L236–283 下游数据集精度测试、L332–333 GSM8K 示例；README_NEW L267–328 任务 YAML/指标/截断/modeltest 命令、L178–184 shuffle-k 为 NPU 精度测试默认设置之一）——README 级登记，新旧接口/脚本判据/Server 端到端关系 unknown；registry notes 同步。
- C07：锚点更正——faq 调度段 L221–223（原 L224–226 为空行）；lm-eval 命令 L116–120、30 分钟 L123；OpenCompass 角色 HUMAN/BOT＋保留 SYSTEM（原摘要误写 SYSTEM/USER）；"baseline 为未量化模型同任务结果"改归本库方法（int8 页仅量化侧命令）；论文补版本化近邻链接（v6/v2/v7）。
- 附带（T07-07-C09）：正文 PD 提及处补 pd-disaggregation.md 普通链接。
