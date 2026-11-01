# shiyan-baogao · 实验报告

一个可独立安装的 Agent Skill：从实验指导书、原始数据或观察、课堂材料和参考样例生成可追溯、可复算的实验报告，也可只完成数据处理。支持中文工作流，不依赖特定学校或云服务。

## 能做什么

- 先对照指导书、逐字稿、现场照片、本人观察和教师要求建立逐项要求矩阵，再决定报告结构、图表和必填字段。
- 支持物理实验的“仅数据处理、精炼完整报告、较全面完整报告”三种范围。
- 支持设计制造/材料类实验的操作规程、制样过程、现象与显微组织观察、图像或手绘要求及机理分析。
- 区分本人测量/观察、教师课件对照、教材解释和往届样例；缺失的真实结果不以典型图或示例补写。

它不自动提交报告，不补造数据、观察或图片。计算内核支持直接测量不确定度、常用独立传播、线性拟合、逐差法和有效数字；尚未实现相关量通用传播、加权拟合或通用有效自由度算法。

## 安装与迁移

需要 Python **3.10 或更新版本**。计算和测试仅用标准库；生成中文 PDF 另外需要 XeLaTeX，视觉检查需要 PDF 渲染工具。

将发行 ZIP 解压为完整的 `shiyan-baogao` 文件夹，放入所用 agent 的技能目录；不要只复制 `SKILL.md`。安装后使用 `$shiyan-baogao`，或直接提出“按指导书整理这次实验报告”。技能不会自动上传文件。

从旧版 `shiyan-shuju` 迁移时，先备份旧目录及 `.local/` 私有配置，将新技能安装为独立的 `shiyan-baogao` 目录并运行自检；确认新入口正常后再停用旧入口，避免两个技能同时触发。课程资料、身份信息和私人模板仍留在课程工作区或 `.local/`，不复制进公开源码。

## 两条报告路线

物理实验默认从原始读数和计算口径出发。用户只要数据时不扩写目的、仪器和步骤；用户要完整报告时，前置内容以本次教材、指导书和教师要求为依据，精炼整合，结果讨论绑定复算数据。

设计制造/材料实验先逐条读取指导书的“实验报告要求”，再用本次逐字稿、现场照片和本人观察核对实际对象与课堂变更；本次证据明确时，以实际执行为准并保留差异记录。既有报告只用于识别写法和版式，不能替换本次样品、组织、图数、尺寸、标注或问题。本人实验照片与教师课件图分别标记；没有可靠身份或观察依据的图不进入正式结果。

详见[完整报告工作流](references/full-report-workflow.md)、[物理实验报告](references/physics-report.md)、[设计制造与材料实验报告](references/design-manufacturing-report.md)和[结果讨论与分析](references/analysis-discussion.md)。

## 快速试算

用户完成誊抄或自主调整后，可另行提供手写报告、扫描件或照片，要求[独立事实复核](references/handwritten-review.md)。此模式可跨会话启动，回查原始依据，诊断与生成稿的实质差异，允许合理改动并优先报告事实错误；生成阶段不自动要求手写件。

```text
python -B scripts/uncertainty.py selftest
python -B examples/direct_measurement.py
python -B scripts/uncertainty.py round --value 123.456 --u 9.9 --sig 1
```

示例使用明确标注的合成数据。命令行参数、数学假设及兼容 API 见[计算契约](references/calculation-contract.md)。原有 `scripts/uncertainty.py` 导入接口及 `direct/bridge/boxerr/prop/fit/diff/round/selftest` 子命令继续保留。

## 开发与验证

```text
python -B -m unittest discover -s scripts -p test_uncertainty.py -v
python -B -m unittest discover -s tests -v
python -B scripts/check_release.py
python -B scripts/verify.py --template --package
python -B scripts/build_release.py --output build/shiyan-baogao.zip
```

`--template` 会真实编译并渲染统一的横向双框模板；没有 TeX 环境时可省略，但不能声称完成了 PDF 视觉验收。完整报告与仅数据处理报告共用该版式，只由要求矩阵决定正文内容。表格和曲线规范见[科研图表与数值表达](references/scientific-presentation.md)，开发边界见[贡献指南](CONTRIBUTING.md)和[维护流程](MAINTENANCE.md)。

## 来源与许可证

本项目按 [MIT](LICENSE) 提供代码与自写文档，材料边界见 [NOTICE](NOTICE.md)。不分发教材、学生报告、扫描纸、校徽或私人实验档案。数值处理参考 [NIST 不确定度传播](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty)和 [Python Decimal](https://docs.python.org/3/library/decimal.html)；课程特殊算法仍须由本次材料确认。
