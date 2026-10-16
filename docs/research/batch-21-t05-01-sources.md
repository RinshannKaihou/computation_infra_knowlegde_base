# T05-01 来源记录（Batch 21 补交）

任务：T05-01（新建 `container-image-runtime-baseline.md`；Batch 21 遗漏项补交）。作者取证轮次：首轮（OCI 双规范 tag、Toolkit 1.20.0 四页、设备插件 v0.20.1 README、复用 MindCluster/NGC 登记）＋第二轮（annotations/config 明文、containerd/runc/CDI tag 解引用、Toolkit 安装固定包版本、插件策略/time-slicing、Ascend plugin.go 路径）＋第三轮（k8s 拉取策略/torch 可见集/syft/cosign/runc 手册/containerd CRI/CDI SPEC 正文、common.go 输出字段；独立复核 codex 初审/复核取证点）。

## 主张—来源定位表（ID—精确页面/节—字段/支持范围）

| 主张 | 登记 ID | 精确页面/节 | 支持范围 / 未覆盖 |
|---|---|---|---|
| 镜像身份/构建方法 | src.oci.image-spec-v1.1.1 | [annotations.md](https://github.com/opencontainers/image-spec/blob/v1.1.1/annotations.md)（MUST 规则/SHOULD 关系）/[config.md](https://github.com/opencontainers/image-spec/blob/v1.1.1/config.md)（diff_ids 必填/history 可选）/manifest（subject 可选） | 方法层；构建工具 unknown |
| 运行时版本基线 | tag 解引用（containerd v2.4.1/runc v1.5.2/CDI 仓库 v1.1.1）＋CRI config.md 全文（v3 独立 images/runtime 插件、default_runtime_name、runtimes.<handler>.runtime_type/options.SystemdCgroup、cdi_spec_dirs、RuntimeClass handler）＋runc state.go/list.go（JSON 字段/--root 作用域/stopped-PID-zero） | 见登记注 | 固定点；消费端输出 unknown |
| GPU 层间机制（含 Allocate 实现位置） | src.nvidia.container-toolkit-1.20.0 / src.nvidia.k8s-device-plugin-v0.20.1（server.go L280–438/L448–481：DevicesIds 校验→策略转换去重→qualified 名→CdiDevices） / src.oci.runtime-spec-v1.3.0 | 安装指南（1.20.0-1）/CDI 页/docker-specialized/排障四分支；插件配置策略；config-linux Devices/Allowed list | 机制分开；调度/兼容 unknown |
| 昇腾样板 | src.ascend.device-plugin-pkg-44385c13 / src.ascend.device-plugin-common-44385c13 / src.ascend.docker-runtime-44385c13 / src.ascend.docker-hook-44385c13 / src.ascend.docker-install-44385c13 / src.ascend.mind-cluster-v26.1.1 | [plugin.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go)（L1087 挂载函数/L1161–1169 分支判断/Allocate L1296；common.go L90–150 静态输出已读）＋[process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go)（VIRTUAL 提前返回/CreateVDevice 条件/设备非空分支/env 与库路径分开） | 已读：环境键完整链/hook 白名单机制与 CLI 参数构造/默认 base.list 5 项与安装选择规则/所选示例基线条件；未读：产品变体内容/逐库身份版本/dcmi 实现；未执行：实际挂载结果。机制已读、所选记录 filled 值未交付、现场未采三分见正文 §3 |
| 清单/异常/对照 | 上列复用 | 正文 §4（可填写清单/分支表/对照方案） | 只设计未执行 |

## unknown 清单

1. containerd/runc 消费端交集；2. 构建输入工具（格式已交付）；3. 昇腾实际库挂载/白名单/hook 可执行/dcmi 完整实现（入口与条件链已读，见上）；4. 调度策略（T05-05）；5. 全部实测（未执行）。

## 第三轮增补（对应第二次定向复核 C30–C34）

| 主张 | 登记 ID | 精确页面 |
|---|---|---|
| 拉取策略字段 | src.k8s.images-v1.32 | [Images v1.32](https://v1-32.docs.kubernetes.io/docs/concepts/containers/images/)（imagePullPolicy/默认化/缓存） |
| 框架可见集 | src.pytorch.cuda-notes-2.14 | [CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html)（CUDA_VISIBLE_DEVICES） |
| SBOM/签名工具 | src.anchore.syft-v1.54.1 / src.sigstore.cosign-docs / src.sigstore.cosign-cli-v3.1.3 | syft README（Features/基础示例范围）/ cosign signing overview＋verifying（未固定修订）/ CLI v3.1.3 同修订 verify.go L1–220、options/verify.go L1–195、options/certificate.go L1–155 |
| runc 实现 | src.opencontainers.runc-man-v1.5.2 | [man/runc.8.md@v1.5.2](https://github.com/opencontainers/runc/blob/v1.5.2/man/runc.8.md) |
| containerd CRI | src.containerd.cri-config-v2.4.1 | [config.md@v2.4.1](https://github.com/containerd/containerd/blob/v2.4.1/docs/cri/config.md)（版本头/cdi_spec_dirs） |
| CDI 规范身份 | src.cdi.spec-1.1.0 | [SPEC.md@cb98bcf6](https://github.com/cncf-tags/container-device-interface/blob/cb98bcf66dc68530012483bd56e33e14d815e167/SPEC.md#version)（规范 1.1.0） |
