# 音源数据

Sonic Atlas 声音语料库获取指南。完整语料包含约 54,000 条音频（16 GB），来自六个数据源。音频文件**不**纳入 Git 跟踪——请按本指南下载并重建语料库。

## 快速开始

```bash
# 1. 下载所有数据源到临时目录
mkdir -p /tmp/sonic-atlas-sources

# 2. 构建语料库
uv run python experiments/build_corpus.py \
  --output data/corpus \
  --source-dir /tmp/sonic-atlas-sources \
  --sources ESC-50 TinySOL Philharmonia FSD50K LibriSpeech synthetic
```

## 数据源

### 1. FSD50K

| 字段 | 值 |
|---|---|
| 内容 | 51,197 条 Freesound 音频，人工标注，200 类 |
| 语料库中使用 | 43,515 条 |
| 许可证 | CC-BY |
| 论文 | Eduardo Fonseca et al., "FSD50K: An Open Dataset of Human-Labeled Sound Events" (arXiv 2010.14761) |

**下载**

1. 访问 <https://zenodo.org/record/4060432>
2. 下载 `FSD50K.dev_audio.zip` 和 `FSD50K.eval_audio.zip`
3. 下载 `FSD50K.ground_truth.zip`（包含标签）
4. 解压至以下目录结构：
   ```
   /tmp/sonic-atlas-sources/FSD50K/
   ├── FSD50K.dev_audio/    # 40,966 条
   ├── FSD50K.eval_audio/   # 10,231 条
   └── ground_truth/        # 标签
   ```

> **注意**：需要 Zenodo 账号。压缩包总计约 23 GB。

### 2. Philharmonia Orchestra

| 字段 | 值 |
|---|---|
| 内容 | 专业管弦乐单音采样（铜管、弦乐、吉他） |
| 语料库中使用 | 6,669 条 |
| 许可证 | Creative Commons (CC) |
| 来源 | Philharmonia Orchestra, London |

**下载**

```bash
# 音频样本以 MP3/WAV 格式单独提供：
# https://www.philharmonia.co.uk/explore/sound-samples

# 建议使用批量下载工具
mkdir -p /tmp/sonic-atlas-sources/philharmonia
# 期望的目录结构：
# philharmonia/
# ├── Brass/Brass/{trumpet,french horn,trombone,tuba}/
# ├── Strings/Strings/{violin,viola,cello,double bass,guitar}/
# └── ...
```

1. 访问 <https://www.philharmonia.co.uk/explore/sound-samples>
2. 进入各乐器页面
3. 下载每种乐器的所有 MP3 样本
4. 按上述目录结构整理

### 3. TinySOL

| 字段 | 值 |
|---|---|
| 内容 | 2,940 条管弦乐器单音采样（木管 + 手风琴） |
| 语料库中使用 | 752 条 |
| 许可证 | CC-BY 4.0 |
| 论文 | Gómez-García et al., "TinySOL: A Tiny Dataset of Solo Instrument Notes" (ISMIR 2019 Late-Breaking Demo) |

**下载**

1. 访问 <https://zenodo.org/record/3685367>
2. 下载 `TinySOL.tar.gz`（约 500 MB）
3. 解压至：
   ```
   /tmp/sonic-atlas-sources/TinySOL2020/
   ├── Flute/
   ├── Clarinet_Bb/
   ├── Oboe/
   ├── Bassoon/
   ├── Sax_Alto/
   └── Accordion/
   ```

### 4. LibriSpeech

| 字段 | 值 |
|---|---|
| 内容 | 有声书英文朗读语音 |
| 语料库中使用 | 2,703 条（clean 子集） |
| 许可证 | CC-BY 4.0 |
| 论文 | Vassil Panayotov et al., "Librispeech: An ASR Corpus Based on Public Domain Audio Books" (ICASSP 2015) |

**下载**

```bash
cd /tmp/sonic-atlas-sources

# 下载 clean 训练集（100 小时子集即可）
wget https://www.openslr.org/resources/12/train-clean-100.tar.gz
tar xzf train-clean-100.tar.gz

# 期望结构：
# LibriSpeech/
# ├── train-clean-100/
# │   └── {speaker_id}/{chapter_id}/*.flac
```

来源：<https://www.openslr.org/12>

### 5. ESC-50

| 字段 | 值 |
|---|---|
| 内容 | 2,000 条环境声，50 类 |
| 语料库中使用 | 653 条 |
| 许可证 | CC-BY-NC（非商业用途） |
| 论文 | Karol J. Piczak, "ESC: Dataset for Environmental Sound Classification" (ACM MM 2015) |

**下载**

1. 访问 <https://github.com/karolpiczak/ESC-50>
2. 下载数据集：
   ```bash
   cd /tmp/sonic-atlas-sources
   wget https://github.com/karoldvl/ESC-50/archive/master.zip
   unzip master.zip
   mv ESC-50-master ESC-50
   ```
3. 期望结构：
   ```
   ESC-50/
   ├── audio/       # 2,000 个 WAV 文件
   └── meta/        # esc50.csv
   ```

### 6. Synthetic

| 字段 | 值 |
|---|---|
| 内容 | 24 条合成音频（噪声 + 正弦扫频） |
| 语料库中使用 | 24 条 |
| 许可证 | Public Domain |

**无需下载** — `build_corpus.py` 在指定 `--sources synthetic` 时自动生成：

- `texture/noise/` — 15 条：白噪声、粉噪声、布朗噪声（各 5 个变体）
- `texture/tone/` — 9 条：C2→C7 正弦扫频（3 速度 × 3 时长）

## 部分重建

只重建指定数据源：

```bash
uv run python experiments/build_corpus.py \
  --output data/corpus \
  --source-dir /tmp/sonic-atlas-sources \
  --sources ESC-50 TinySOL
```

脚本会跳过 `--source-dir` 中不存在的数据源并给出警告。

## 许可证汇总

| 数据源 | 许可证 | 商业用途 |
|---|---|---|
| FSD50K | CC-BY | ✅（需署名） |
| Philharmonia | CC | ✅ |
| TinySOL | CC-BY 4.0 | ✅（需署名） |
| LibriSpeech | CC-BY 4.0 | ✅（需署名） |
| ESC-50 | CC-BY-NC | ❌ |
| Synthetic | Public Domain | ✅ |

> **注意**：653 条 ESC-50 音频受 CC-BY-NC 限制。商业用途需移除或替换。

## 在其他机器上重建

完整语料库维护在 `betelgeuse` 上：

```bash
rsync -az betelgeuse:~/sonic-atlas/data/corpus/ data/corpus/
```

或按上述步骤从头重建——仓库中的 manifest（`data/corpus_fsd50k/manifest.csv` 等）提供了完整索引。
