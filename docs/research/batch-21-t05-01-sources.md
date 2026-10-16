# T05-01 来源记录（Batch 21 补交）

任务：T05-01（新建 `container-image-runtime-baseline.md`；Batch 21 遗漏项补交）。作者取证轮次：首轮（OCI 双规范 tag、Toolkit 1.20.0 四页、设备插件 v0.20.1 README、复用 MindCluster/NGC 登记）＋第二轮（annotations/config 明文、containerd/runc/CDI tag 解引用、Toolkit 安装固定包版本、插件策略/time-slicing、Ascend plugin.go 路径）＋第三轮（k8s 拉取策略/torch 可见集/syft/cosign/runc 手册/containerd CRI/CDI SPEC 正文、common.go 输出字段；独立复核 codex 初审/复核取证点）＋第四轮（2026-10-17，对应 C32–C34 关闭：syft v1.54.1 源码 scope.go/catalog.go/syft-json 模型/coordinates.go/constants.go（sparse clone 只读）、Toolkit CDI 页 JIT-CDI/mode 显式设定节、排障页 legacy 措辞与 Affected Environments、k8s Pod resize v1.32 页、Ascend api/consts.go Env 段与 runtime/hook process.go 全文重读）＋第五轮（2026-10-17，对应第 29 次复核剩余项：syft debian cataloger（package.go/parse_dpkg_db.go/parse_dpkg_info_files.go）与 model/file.go、filecataloging/config.go、options/file.go、file/selection.go（包证据位置 vs 成员文件、文件编目 selection）、插件 server.go envvar 直写段、man-pages 6.19 proc_pid_mountinfo(5)（挂载关联字段语义））。

## 主张—来源定位表（ID—精确页面/节—字段/支持范围）

| 主张 | 登记 ID | 精确页面/节 | 支持范围 / 未覆盖 |
|---|---|---|---|
| 镜像身份/构建方法 | src.oci.image-spec-v1.1.1 | [annotations.md](https://github.com/opencontainers/image-spec/blob/v1.1.1/annotations.md)（MUST 规则/SHOULD 关系）/[config.md](https://github.com/opencontainers/image-spec/blob/v1.1.1/config.md)（diff_ids 必填/history 可选）/manifest（subject 可选） | 方法层；构建工具 unknown |
| 运行时版本基线 | tag 解引用（containerd v2.4.1/runc v1.5.2/CDI 仓库 v1.1.1）＋CRI config.md 全文（v3 独立 images/runtime 插件、default_runtime_name、runtimes.<handler>.runtime_type/options.SystemdCgroup、cdi_spec_dirs、RuntimeClass handler）＋runc state.go/list.go（JSON 字段/--root 作用域/stopped-PID-zero） | 见登记注 | 固定点；消费端输出 unknown |
| GPU 层间机制（含 Allocate 实现位置） | src.nvidia.container-toolkit-1.20.0 / src.nvidia.k8s-device-plugin-v0.20.1（server.go L280–438/L448–481：DevicesIds 校验→策略转换去重→qualified 名→CdiDevices） / src.oci.runtime-spec-v1.3.0 | 安装指南（1.20.0-1）/CDI 页/docker-specialized/排障四分支；插件配置策略；config-linux Devices/Allowed list | 机制分开；调度/兼容 unknown |
| 昇腾样板 | src.ascend.device-plugin-pkg-44385c13 / src.ascend.device-plugin-common-44385c13 / src.ascend.docker-runtime-44385c13 / src.ascend.docker-hook-44385c13 / src.ascend.docker-install-44385c13 / src.ascend.mind-cluster-v26.1.1 | [plugin.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go)（L1087 挂载函数/L1161–1169 分支判断/Allocate L1296；common.go 静态输出已读）＋[process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go)（VIRTUAL 提前返回/CreateVDevice 条件/设备非空分支/env 与库路径分开）＋[api/consts.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/api/consts.go) Env 段（worker 7 键字符串） | 已读：环境键完整链（worker 键 consts.go／控制键 default_name.go）/hook 白名单机制与 CLI 参数构造/默认 base.list 5 项与安装选择规则/所选示例基线条件/逐对象对应规则与逐库 M-LIB（含 mountinfo 来源—挂载关联判据）已交付（正文 §3）；未读（K1）：5 份产品变体内容/vdevice 切分/dcmi 完整实现；未采（K2）：逐对象/逐库 filled 值与实际挂载证据（mountinfo 条目/宿主 st_dev）；未执行（K3）：CLI 执行与部署产物核对。四分见正文 §3 |
| 清单/异常/对照 | 上列复用 | 正文 §4（可填写清单/分支表/对照方案） | 只设计未执行 |

## unknown 清单（按 K1 缺方法/K2 缺采样/K3 未执行分列）

1. containerd/runc 消费端交集（K2）；2. 构建输入工具（格式已交付，选型 K1）；3. 昇腾：机制已读＝默认 base/hook/CLI 消费链、白名单源码链、worker/控制键定义位置；K1＝5 份产品变体 `.list` 内容、vdevice 切分、dcmi 完整实现；K2＝逐对象/逐库记录 filled 值与实际挂载证据（mountinfo 条目/宿主 st_dev）；K3＝CLI 执行与部署产物核对；4. 调度策略（T05-05）；5. 框架枚举顺序语义与宿主节点↔UUID 复核方法（K1，多卡出所选范围；单卡范围 M-ID 已闭合）；6. 全部实测（K3）。

## 第四轮增补（对应 C32–C34 关闭修订）

| 主张 | 登记 ID | 精确页面 |
|---|---|---|
| SBOM 扫描范围与输出字段 | src.anchore.syft-v1.54.1 | [scope.go L8–24](https://github.com/anchore/syft/blob/v1.54.1/syft/source/scope.go)（squashed/all-layers/deep-squashed 语义）、[catalog.go L41/L78/L228–233](https://github.com/anchore/syft/blob/v1.54.1/cmd/syft/internal/options/catalog.go)（--scope flag、默认 squashed）、[model/package.go](https://github.com/anchore/syft/blob/v1.54.1/syft/format/syftjson/model/package.go)（name/version/type/foundBy/locations）、[coordinates.go](https://github.com/anchore/syft/blob/v1.54.1/syft/file/coordinates.go)（JSON 键 path/layerID）、[location.go](https://github.com/anchore/syft/blob/v1.54.1/syft/file/location.go)（镜像源 layerID＝层 digest）、[constants.go L6](https://github.com/anchore/syft/blob/v1.54.1/internal/constants.go)（schema 16.1.11） |
| 两端消费配置对 | src.nvidia.container-toolkit-1.20.0 | [CDI 页](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html)（原生消费/非原生 cdi mode/JIT-CDI/`nvidia-container-runtime.mode` 显式设定节）、[排障页](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html)（"legacy mode" 措辞、访问丢失 Affected Environments） |
| 资源更新接口 | src.k8s.pod-resize-v1.32 | [resize 页 v1.32](https://v1-32.docs.kubernetes.io/docs/tasks/configure-pod-container/resize-container-resources/)（/resize 子资源、InPlacePodVerticalScaling v1.27 alpha 默认关、requests/limits.cpu 可变与单位、status.resize/containerStatuses[].resources、restartCount 不变） |

## 第三轮增补（对应第二次定向复核 C30–C34）

| 主张 | 登记 ID | 精确页面 |
|---|---|---|
| 拉取策略字段 | src.k8s.images-v1.32 | [Images v1.32](https://v1-32.docs.kubernetes.io/docs/concepts/containers/images/)（imagePullPolicy/默认化/缓存） |
| 框架可见集 | src.pytorch.cuda-notes-2.14 | [CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html)（CUDA_VISIBLE_DEVICES） |
| SBOM/签名工具 | src.anchore.syft-v1.54.1 / src.sigstore.cosign-docs / src.sigstore.cosign-cli-v3.1.3 | syft README（Features/基础示例范围）/ cosign signing overview＋verifying（未固定修订）/ CLI v3.1.3 同修订 verify.go L1–220、options/verify.go L1–195、options/certificate.go L1–155 |
| runc 实现 | src.opencontainers.runc-man-v1.5.2 | [man/runc.8.md@v1.5.2](https://github.com/opencontainers/runc/blob/v1.5.2/man/runc.8.md) |
| containerd CRI | src.containerd.cri-config-v2.4.1 | [config.md@v2.4.1](https://github.com/containerd/containerd/blob/v2.4.1/docs/cri/config.md)（版本头/cdi_spec_dirs） |
| CDI 规范身份 | src.cdi.spec-1.1.0 | [SPEC.md@cb98bcf6](https://github.com/cncf-tags/container-device-interface/blob/cb98bcf66dc68530012483bd56e33e14d815e167/SPEC.md#version)（规范 1.1.0） |

## 第五轮增补（对应第 29 次复核剩余子项）

| 主张 | 登记 ID | 精确页面 |
|---|---|---|
| 包证据位置 vs 成员文件语义 | src.anchore.syft-v1.54.1 | [debian/package.go L163–193](https://github.com/anchore/syft/blob/v1.54.1/syft/pkg/cataloger/debian/package.go)（成员文件入 metadata.Files）、[parse_dpkg_db.go L36–49](https://github.com/anchore/syft/blob/v1.54.1/syft/pkg/cataloger/debian/parse_dpkg_db.go)（dpkg 数据库读入位置入包 Locations） |
| 文件编目输出与选择 | src.anchore.syft-v1.54.1 | [model/file.go](https://github.com/anchore/syft/blob/v1.54.1/syft/format/syftjson/model/file.go)（files[] 条目 location.path/layerID＋digests）、[filecataloging/config.go](https://github.com/anchore/syft/blob/v1.54.1/syft/cataloging/filecataloging/config.go)（Selection 默认 owned-by-package）、[options/file.go L34–47](https://github.com/anchore/syft/blob/v1.54.1/cmd/syft/internal/options/file.go)（CLI 默认 selection/digests）、[selection.go](https://github.com/anchore/syft/blob/v1.54.1/syft/file/selection.go)（all/owned-by-package/none） |
| 单卡 envvar 直写分配 ID | src.nvidia.k8s-device-plugin-v0.20.1 | [server.go](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go)（`updateResponseForDeviceListEnvVar`：`NVIDIA_VISIBLE_DEVICES`＝分配 ID 逗号串；`uniqueDeviceIDsFromAnnotatedDeviceIDs` uuid/index 策略分支） |
| 挂载关联字段语义 | src.linux-man-pages.proc-pid-mountinfo-6.19 | [proc_pid_mountinfo(5)](https://man7.org/linux/man-pages/man5/proc_pid_mountinfo.5.html)（field 3 major:minor＝st_dev、field 4 root＝bind 源子路径、field 5 挂载点、field 9/10 fs 类型/源） |
