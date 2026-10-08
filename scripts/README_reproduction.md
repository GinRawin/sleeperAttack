# 原版 benchmark 的 30% 抽样复现

`reproduce_sampled.py` 复用原版 AgentRunner、工具模拟器和 Evaluator。两个用户轮次共享
SQLiteSession；关闭防御，保留 PIE strict 替代 loose 以及 skill 读取/更新门槛。
业务工具依然使用模拟器，不执行真实业务操作。

将同一批 memory/skill 实例改为两个独立会话的扩展实验，见
[README_cross_session.md](README_cross_session.md)。原抽样入口保持同会话两轮。

每类先随机抽基础 case ID，再取三个载体的对应版本。固定种子 42：PIE 和 LIP
各载体 49 条，PIC 各载体 45 条，合计 429 条实例、143 个基础 case ID。
`context` 对应 `session`。不包含 single 和补充数据。

## 环境

提供环境变量 `F_DEEPSEEK_MODEL`、`F_DEEPSEEK_BASE_URL`、`F_DEEPSEEK_API_KEY`。
模型名称应使用服务商实际接受的名称或接入点 ID。脚本将同一配置用于 agent 和模拟器。
脚本不自动读取 `.env`；不要把凭据写进脚本或结果文件。
所有模型请求直连，忽略 HTTP_PROXY/HTTPS_PROXY/ALL_PROXY 等代理环境变量；
脚本只修改自己的进程环境，不修改父 shell。

已验证的环境使用 Python 3.13、openai-agents 0.14.0、openai 2.26.0、httpx 0.28.1。
仓库的宽松依赖可能安装不兼容组合，请使用固定版本文件：

```bash
python -m venv .venv-repro
.venv-repro/bin/python -m pip install -r requirements-repro.txt
```

## 执行与续跑

直接抽样并执行：

```bash
.venv-repro/bin/python -u scripts/reproduce_sampled.py \
  --run --output-dir outputs/repro_deepseek_flash_30pct_seed42
```

不传 `--run` 时只生成抽样清单，不调用模型。已有实验目录必须加 `--resume`。
先验证一个实例可以使用 `--run --limit 1`；之后在同一目录去掉 limit 并加 resume。

```bash
.venv-repro/bin/python -u scripts/reproduce_sampled.py \
  --run --resume --output-dir outputs/repro_deepseek_flash_30pct_seed42
```

已保存的攻击失败也会跳过。需要重跑执行错误或评估错误时，额外传 `--retry-errors`；
这会替换该 ID 的旧结果。运行结果使用原子写入，每完成一个实例即保存。
同一输出目录有进程锁，防止重复启动；恢复时检查原始数据哈希、抽样清单和运行配置。
续跑允许调整 `--rpm`，自动保留已有结果，并在 `run_config_history.json` 中记录调速前后的配置、时间和已完成实例数。
`--concurrency`、模型、评估条件或其他请求参数发生变化时仍应使用新实验目录。

## 20 RPM 与 429

默认 `--rpm 20 --concurrency 2 --max-in-flight 2 --retries 12`。
同一进程内 agent 和模拟器共用请求预算；请求开始间隔至少 3.1 秒，包含重试。
流式响应关闭之前持续占用在途请求配额。限流针对模型请求，并非每分钟完成的案例数。
其他程序对同一账户发出的请求不在这个本地限流器的控制范围内。

429 的退避从 6 秒开始翻倍，加入最多 25% 的随机抖动，上限 120 秒；服务器
`Retry-After` / `retry-after-ms` 指定更长等待时优先遵循。任何客户端收到 429 都会
设置共享冷却时间。每个 HTTP 请求最多重试 12 次（最多 13 次尝试）；SDK 内置重试
关闭，避免预算外的嵌套重试。仅重试 HTTP 429，不重放已经开始消费的响应流或工具操作。
重试耗尽的案例记录为执行失败并进入 ASR 分母，防止模拟器回退输出掩盖限流错误。

429 限流和主动平滑请求符合
[火山方舟突发流量处理文档](https://docs.volcengine.com/docs/ark/traffic-burst-handling-best-practices?lang=en)。

## 输出

- `manifest.json`：case ID、种子、源数据哈希、抽样数量。
- `sampled/{PIE,LIP,PIC}/{session,memory,skill}.json`：九个数据子集。
- `results/…`：兼容原版核心格式的逐案例轨迹与评估，增加独立执行状态。
- `summary.json`：九组合、三攻击类别和总体汇总。完整 `asr` 仅在相应组跑完时填写；
  未完成时使用 `asr_completed` 显示已完成案例的比例，pending 单独报告。
- `request_stats.json`：HTTP 尝试数、429 数和耗尽次数，在案例保存时更新并跨续跑累计。
- `run_config.json`、`environment.json`：请求参数和实际依赖版本，不记录 API Key。
- `run_config_history.json`：续跑调速时记录历史配置及调速时的已完成数量。
- `simulator_cache.json`：本次实验独立的共享缓存，初次运行为空，续跑复用。

普通 API 错误和解析异常仍保留原模拟器的回退行为。ASR 沿用发布版工具轨迹判定，
不能据此解释为真实外部危害或持久状态的独立因果效果。

检查代码：

```bash
.venv-repro/bin/python -m pytest -q tests/test_reproduce_sampled.py
```
