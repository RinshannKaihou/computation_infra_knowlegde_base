# 第十七批 C08 本地包取证记录

取证日期：2026-10-09。对象：用户提供的 CANN 安装包（`/Volumes/T7/work/cann/`），Mac 上只解包不安装。

## 包身份

- 外层：`Ascend-cann-toolkit_8.2.RC1.alpha001_linux-x86_64.run`（2.5GB，Makeself 2.5.0），`--noexec --extract` 解包。
- 内层组件版本（`version.info`）：`Version=7.7.T17.0.B106`，`version_dir=8.2.RC1.alpha001`——包内组件构建版本与外层版本名不一致，引用时分别记录。
- 另有 `Ascend-cann-nnal_8.2.RC1.alpha001_linux-x86_64.run`（642MB，NNAL 元包，内含 SIP/ATB 子包，无头文件文档，与本次无关）。
- 包内无 `doc/` 目录、无 PDF。

## 核对结果（与 C08 缺口逐项对照）

1. `aclnn_matmul.h`（`cann_opp/.../op_api/include/aclnnop/`，Apache-2.0）：两段式接口 + `cubeMathType` 参数存在，与官方文档接口 claims 互证；**无累加精度陈述**。
2. opp unified_bank matmul JSON（如 910B4 4.8MB）：cost-model 知识库（timing 数据），不是精度契约；未用作证据。
3. fixpipe 内核注释（`weight_quant_batch_matmul_v2_fixpipe.h`：“分配给累加后的 c 矩阵”配 float 缓冲）：单个量化算子实现的缓冲细节，**不能引用为通用累加精度契约**，未采用。
4. aclnn op 头文件在 OPP 包（`op_api/include/aclnnop/`），toolkit 主包 `include/` 仅 opdev/experiment，无逐算子头。

## 结论

本地包渠道已穷尽：**累加精度官方陈述在包内不存在**（头文件无、文档无、JSON 非契约）。C08 累加精度子项继续 OPEN。包内版本映射（外层 8.2.RC1.alpha001 / 内层 7.7.T17.0.B106）已记录，后续引用包内文件须带此双版本标识。

注：本地文件不符合 `sources/registry.yaml` 的 URL 登记模式（仅接受 http(s)），故不新增登记；本记录为作者取证说明，供复核判断引用边界。
