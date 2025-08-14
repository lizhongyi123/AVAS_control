flowchart TD
    %% ============ 数据层 =============
    A0([原始公网视频\n20M?100M?clip])
    A1([帧抽样/遮挡?Pipeline])
    A2([自监督预训练\nVideo?ViT?Large])

    %% ============ 模仿层 =============
    B0([录制演示\nGUI?or?Robot\n10k?100k?traj])
    B1([latent?提取\n(冻结?ViT)])
    B2([行为克隆 / Decision?Transformer\n初始化策略])

    %% ============ 强化学习层 =============
    C0([真实或仿真环境\nMiniWoB/Isaac?Gym])
    C1([Offline?QL?(IQL?/?CQL)\n利用演示 buffer])
    C2([Online?RL?微调\nGUI→PPO?|?Robot→SAC])
    C3([Curiosity?+?层次奖励\n→?探索长链任务])

    %% ============ 部署层 =============
    D0([评估基准\n成功率 / 回报 / 泛化])
    D1([策略蒸馏?+?LoRA\n轻量部署])
    D2([持续在线学习\n数据回流 → C1])

    %% -------- 链接箭头 --------
    A0 --> A1 --> A2
    A2 --> B1
    B0 --> B1 --> B2
    B2 --> C1
    C1 --> C2 --> C3 --> D0
    D0 -->|指标未达标| C2
    D0 -->|指标达标| D1 --> D2 --> C1
