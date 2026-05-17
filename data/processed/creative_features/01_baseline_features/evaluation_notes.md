# Baseline Feature Evaluation Notes

> **评估工具**: [`demos/creative_features/evaluation.html`](../../../../demos/creative_features/evaluation.html)
>
> 打开交互式 HTML 工具完成所有听检与评分工作，评分结果自动保存到浏览器 localStorage，
> 点击 **Export Ratings JSON** 可导出为 `evaluation_ratings.json`。

---

## 评估流程

### Step 1: 打开评估工具

```bash
# 方式一：直接用浏览器打开（推荐）
xdg-open demos/creative_features/evaluation.html

# 方式二：用 Python 起本地服务器（音频播放更稳定）
cd /home/pulcerto/Workspace/exp_music/sonic-atlas
python3 -m http.server 8080
# 然后打开 http://localhost:8080/demos/creative_features/evaluation.html
```

### Step 2: 投影探索（RQ1）

在左侧 Sidebar 切换 **Method**（UMAP/PCA）和 **Feature Group**（All/Timbre/Texture/Temporal），观察：

- [ ] 三个 category 是否各自聚团？
- [ ] 哪两类最容易混淆？
- [ ] 哪些点是离群值？
- [ ] UMAP vs PCA 哪个聚类更清晰？
- [ ] 哪个 feature group 的组织最符合直觉？

### Step 3: 特征分析（RQ2）

在左侧 Sidebar 切换 **Category Summary** 的 feature，观察三类差异：

- [ ] 哪些特征区分力最强？（centroid? flatness? entropy?）
- [ ] 哪些特征三类几乎无差异？
- [ ] 查看 **High Correlations** 表，标记冗余对

### Step 4: 逐样本听检

点击散点图上的点，对每个样本：

- [ ] 播放音频，确认声音内容
- [ ] 填写 **Perceptual Rating**（7 轴 × 1-5 分）
- [ ] 填写 **Listening Checklist**（主声源、有无音高、有无纹理运动、创作联想）
- [ ] 可选：填写 **Notes**

### Step 5: 近邻评估（RQ3）

选中样本后，底层面板显示 **Nearest Neighbors**：

- [ ] 对每对近邻评分：acoustic similarity / semantic similarity / creative usefulness（各 1-5）
- [ ] 切换 Neighbors 的 feature group（All/Timbre/Texture/Temporal），对比检索质量
- [ ] 查看 **Cross-Category Neighbors**，记录跨类相似的创作价值

### Step 6: 导出与总结

- [ ] 点击 **Export Ratings JSON** 下载评分数据
- [ ] 将 JSON 文件保存到 `data/processed/creative_features/01_baseline_features/evaluation_ratings.json`
- [ ] 填写下方的总结 section

---

## RQ1 总结: 特征空间是否直觉合理？

**投影观察：**

<!-- 在评估工具中观察后填写 -->

| 问题 | 发现 |
|:---|:---|
| music 是否聚团？ | |
| nature 是否聚团？ | |
| urban_object 是否聚团？ | |
| 哪两类最容易混淆？ | |
| 最明显的离群点 | |

## RQ2 总结: 哪些特征解释力最强？

| 类型 | 特征 |
|:---|:---|
| 区分力最强（三类差异大） | |
| 区分力最弱（三类几乎相同） | |
| 高度冗余可合并的对 | |
| 需要重新实现的特征 | |

## RQ3 总结: 近邻是否有创作价值？

**有趣的近邻对（至少 5 对）：**

| Query | Neighbor | 距离 | 为什么有趣？ |
|:---|:---|:---|:---|
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |

**跨类近邻发现：**

<!-- 哪些跨类对意外地近？创作上能怎么用？ -->

## RQ4 总结: 基线描述符的局限性

**失败案例（至少 5 个）：**

| Sample A | Sample B | 问题描述 |
|:---|:---|:---|
| | | |
| | | |
| | | |
| | | |
| | | |

**缺失的感知维度（Phase 3 应补充）：**

- [ ] 空间感 / 立体声宽度
- [ ] 冷暖色调
- [ ] 紧张感 / 情绪色彩
- [ ] 节奏型 / 脉冲感
- [ ] 谐波丰富度
- [ ] 粒度感
- [ ] 密度
- [ ] 其他：____________

## Creative Insights

**可解释特征轴（至少 2 个）：**

1. **轴名**: ____________ — 涉及特征: ____________ — 听感变化: ____________
2. **轴名**: ____________ — 涉及特征: ____________ — 听感变化: ____________

**特征轨迹作曲草图（至少 1 个）：**

> 从 ____________ 出发，沿 ____________ 轴变化，经过 ____________，到达 ____________。
> 效果：____________

## Next Steps

- [ ] 导出 evaluation_ratings.json 并提交
- [ ] 确认 Phase 3 候选 embedding 模型
- [ ] 确认 feature-space browser 的 MVP 功能
- [ ] 基于评估结果调整 P0/P1 特征集
