# Sonic Atlas Sound Corpus

> 标准化声音语料库，服务于 Sonic Atlas 音频特征研究。
>
> **当前位置**: betelgeuse:~/sonic-atlas/data/corpus/
> **本地副本**: sonic-atlas/data/corpus/（gitignored）

## 概览

| 指标 | 值 |
|:---|:---|
| 总条数 | 54,316 |
| 总大小 | ~16 GB |
| 格式 | WAV, 22050 Hz, mono, PCM 16-bit |
| 时长范围 | 0.5s – 70s（mean ~4s） |
| 分类体系 | 4 大类 / 20 子类 / 100+ 乐器/声源 |

## 目录结构

```
data/corpus/
├── manifest.csv              # 全局 manifest（54,316 行）
├── music/                    # 21,805 条
│   ├── string_bowed/         # 6,051 (violin, viola, cello, double_bass)
│   ├── electronic/           # 4,099 (synthesizer, music_generic)
│   ├── percussion/           # 3,420 (snare_drum, hihat, cymbal, gong…)
│   ├── brass/                # 3,002 (trumpet, tuba, trombone, french_horn)
│   ├── string_plucked/       # 2,495 (guitar, electric_guitar, bass_guitar, mandolin, banjo)
│   ├── keyboard/             # 1,321 (piano, organ, accordion)
│   ├── woodwind/             # 796 (harmonica, flute, clarinet, oboe, bassoon, sax)
│   └── voice/                # 658 (singing, female_singing, male_singing, choir)
├── nature/                   # 17,282 条
│   ├── human/                # 9,765 (speech, laughing, coughing, breathing…)
│   ├── animal/               # 3,532 (bird, insect, mammal, frog)
│   ├── water/                # 1,679 (ocean, stream, rain, splash)
│   ├── weather/              # 1,367 (thunder, rain, wind)
│   ├── fire/                 # 682 (crackling, fire)
│   └── texture/              # 254 (whoosh)
├── urban/                    # 15,205 条
│   ├── impact/               # 5,688 (explosion, squeak, shatter, door, glass)
│   ├── alarm/                # 2,195 (alarm, bell, chime, siren, ringtone)
│   ├── machine/              # 1,992 (engine, tools, revving, fan)
│   ├── domestic/             # 1,904 (cutlery, zipper, dishes, vacuum)
│   ├── transport/            # 1,790 (car, train, airplane, bus)
│   └── human/                # 1,602 (footsteps, typing, clapping)
└── texture/                  # 24 条
    ├── noise/                # 15 (white, pink, brown × 5 variants)
    └── tone/                 # 9 (sine sweep C2→C7)
```

## Manifest Schema

`manifest.csv` 包含 54,316 行，每行一个音频文件。字段说明：

| 字段 | 类型 | 说明 | 示例 |
|:---|:---|:---|:---|
| `sample_id` | string | 唯一标识符 | `fsd50k_37199`, `music_brass_trumpet_0042` |
| `file_path` | string | 相对于仓库根的路径 | `data/corpus/music/brass/music_brass_trumpet_0042.wav` |
| `category` | string | 大类 | `music`, `nature`, `urban`, `texture` |
| `subcategory` | string | 子类 | `brass`, `animal`, `impact` |
| `instrument` | string | 具体乐器/声源 | `trumpet`, `bird`, `engine` |
| `tags` | string | 多标签（分号分隔） | `forte;normal`, `bird;chirp` |
| `duration` | float | 时长（秒） | `3.456` |
| `sample_rate` | int | 采样率 | `22050` |
| `source` | string | 数据来源 | `FSD50K`, `Philharmonia`, `ESC-50` |
| `source_id` | string | 原始文件名 | `37199.wav`, `TpC-ord-C4-mf-1a.wav` |
| `license` | string | 许可证 | `CC-BY`, `CC`, `CC-BY-NC` |
| `pitch` | string | 音高（乐器用） | `C4`, `A#5` |
| `dynamic` | string | 力度 | `forte`, `mf`, `pp` |
| `technique` | string | 演奏技法 | `normal`, `muted`, `trill` |
| `description` | string | 描述 | `trumpet C5 forte normal` |

## 数据来源

| 来源 | 条数 | 占比 | 许可证 | 内容 |
|:---|:---:|:---:|:---|:---|
| **FSD50K** | 43,515 | 80.1% | CC-BY | Freesound 用户上传，人工标注，200 类 |
| **Philharmonia** | 6,669 | 12.3% | CC | 专业管弦乐单音采样（铜管/弦乐/吉他） |
| **LibriSpeech** | 2,703 | 5.0% | CC-BY 4.0 | 有声书朗读，干净语音 |
| **TinySOL** | 752 | 1.4% | CC-BY 4.0 | 乐器单音采样（木管/手风琴） |
| **ESC-50** | 653 | 1.2% | CC-BY-NC | 环境声分类数据集 |
| **Synthetic** | 24 | <0.1% | Public Domain | 合成噪声/音调 |

## 分类体系

### 大类定义

| 大类 | 定义 | 典型声源 |
|:---|:---|:---|
| `music` | 乐器演奏、人声演唱 | piano, guitar, drum, singing |
| `nature` | 自然环境声、动物声、人体声 | bird, rain, thunder, laughing |
| `urban` | 城市/机械/人造声 | engine, alarm, door, typing |
| `texture` | 抽象声纹理、合成声 | noise, tone, drone |

### 子类定义

#### music

| 子类 | 包含乐器 |
|:---|:---|
| `keyboard` | piano, organ, accordion, harpsichord |
| `string_bowed` | violin, viola, cello, double_bass |
| `string_plucked` | guitar, electric_guitar, bass_guitar, mandolin, banjo, harp |
| `brass` | trumpet, french_horn, trombone, tuba |
| `woodwind` | flute, clarinet, oboe, bassoon, saxophone, harmonica |
| `percussion` | drum, snare_drum, cymbal, hi-hat, gong, marimba, xylophone |
| `voice` | singing, female_singing, male_singing, choir, rapping |
| `electronic` | synthesizer, sampler, music_generic |

#### nature

| 子类 | 包含声源 |
|:---|:---|
| `animal` | bird, insect, mammal, frog, dog, cat |
| `weather` | rain, thunder, wind, thunderstorm |
| `water` | ocean, stream, splash, drip, pour |
| `fire` | crackling, fire |
| `human` | speech, laughing, coughing, breathing, crying |
| `texture` | whoosh, swoosh |

#### urban

| 子类 | 包含声源 |
|:---|:---|
| `alarm` | alarm, bell, siren, chime, ringtone, horn |
| `machine` | engine, tools, fan, chainsaw, revving |
| `transport` | car, train, airplane, helicopter, bus |
| `impact` | door, glass, explosion, shatter, knock |
| `domestic` | vacuum, washing, dishes, cutlery, zipper |
| `human` | footsteps, typing, clapping, writing |

## 数据质量说明

### 优势

- **单音采样（Philharmonia/TinySOL）**: 专业录音室条件，干净无混响，适合 timbre 分析
- **FSD50K**: 人工标注，多标签，覆盖 200 个细分类别
- **格式统一**: 全部 WAV 22050Hz mono PCM 16-bit
- **无重复**: sample_id 全局唯一，无重复条目

### 局限

- **录音质量参差**: FSD50K 来自 Freesound 用户上传，部分有背景噪声或压缩伪影
- **标签噪声**: FSD50K 虽为人工标注，但部分 clip 标签可能不准确
- **时长不一致**: 0.5s–70s，部分短 clip 可能不足以提取稳定特征
- **类别平衡**: music 占 40%，nature 32%，urban 28%，texture <0.1%
- **speech 偏多**: nature/human 中 3,170 条为 speech（LibriSpeech），但本项目不以 speech 为重点

### 已知问题

- `music/electronic` 中 215 条 `instrument=music_generic`，仅有 "Musical_instrument" 标签，无更细分类
- `nature/texture` 中 254 条来自 FSD50K 的 "Whoosh_and_swoosh_and_swish"，分类边界模糊
- LibriSpeech 的 speech 条目未标注说话人性别/年龄

## 许可证汇总

| 许可证 | 条数 | 说明 |
|:---|:---:|:---|
| CC-BY | 43,515 | FSD50K (Creative Commons Attribution) |
| CC | 6,669 | Philharmonia Orchestra (Creative Commons) |
| CC-BY 4.0 | 3,455 | TinySOL + LibriSpeech |
| CC-BY-NC | 653 | ESC-50 (非商业用途) |
| Public Domain | 24 | 合成声 |

**注意**: CC-BY-NC 条目（ESC-50）不可用于商业用途。如需全商业许可，需替换这 653 条。

## 使用方法

### 加载 manifest

```python
import csv

with open('data/corpus/manifest.csv') as f:
    corpus = list(csv.DictReader(f))

# 按类别筛选
music = [r for r in corpus if r['category'] == 'music']
nature = [r for r in corpus if r['category'] == 'nature']
urban = [r for r in corpus if r['category'] == 'urban']

# 按乐器筛选
piano = [r for r in corpus if r['instrument'] == 'piano']
drums = [r for r in corpus if r['subcategory'] == 'percussion']
```

### 加载音频

```python
import librosa

# 加载单个文件
entry = corpus[0]
y, sr = librosa.load(entry['file_path'], sr=22050, mono=True)
```

### 批量特征提取

```python
from experiments.creative_features.01_baseline_features.schemas import P0_FEATURE_COLUMNS

# 只处理 music 子集
music_entries = [r for r in corpus if r['category'] == 'music'][:100]
for entry in music_entries:
    y, sr = librosa.load(entry['file_path'], sr=22050)
    # 提取特征...
```

## 构建脚本

各数据集的下载链接、许可证与获取方式详见 [docs/data_sources.md](../../docs/data_sources.md)。

```bash
# 从原始数据源重新构建 corpus
uv run python experiments/build_corpus.py \
  --output data/corpus \
  --source-dir /tmp/sonic-atlas-sources \
  --sources ESC-50 TinySOL Philharmonia FSD50K LibriSpeech synthetic
```

## 同步到 betelgeuse

```bash
rsync -az data/corpus/ betelgeuse:~/sonic-atlas/data/corpus/
```
