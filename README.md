# CultSynth-WVS Dataset

## Overview
The CultSynth-WVS dataset is a comprehensive collection of culturally-aware reasoning data derived from the World Values Survey (WVS), designed to support the paper **"Bridging Cultural Gaps: CultSynth Framework for Enhanced Reasoning in Equitable Global Survey Simulation"** submitted to KDD 2026. This dataset enables the training of language models that can generate culturally-aligned responses to survey questions across different countries and regions.

## Dataset Structure
The dataset is provided in JSON format and includes the following files:

| File Name | Description |
|-----------|-------------|
| `sft_wvs_train_combined_clean.json` | Training data with culturally-aware reasoning |
| `sft_wvs_valid_combined_clean.json` | Validation data for model evaluation |
| `sft_wvs_test_combined_clean.json`  | Test data for final assessment |

### Data Format
Each entry in the dataset follows this structure:

```json
{
  "id": "unique_identifier",
  "instruction": "How would someone from [Country] answer the following question:",
  "input": "Survey question text with response options",
  "options": ["(A)Option 1", "(B)Option 2", ...],
  "options_dist": {
    "A": percentage_value,
    "B": percentage_value,
    ...
  },
  "data_type": "train/valid/test",
  "thinking": {
    "thinking_processes": [
      {
        "perspective": "Perspective name",
        "thinking_process": "Detailed cultural reasoning"
      }
    ]
  }
}
```

## Data Processing Workflow

### 1. Data Conversion
To process the raw dataset for training, use the `data/SFT_data_format.py` script:

```bash
# Example: Convert training data
python data/value_alignment_json/SFT_data_format.py \
  -i data/value_alignment_json/final/sft_wvs_train_combined_clean.json \
  -o data/value_alignment_json/sft_wvs_train_aug_convert.json \
  --thinking-start "Here are my reasoning steps:" \
  --thinking-end "\n[BEGIN FINAL RESPONSE]"

# Convert validation data
python data/value_alignment_json/SFT_data_format.py \
  -i data/value_alignment_json/final/sft_wvs_valid_combined_clean.json \
  -o data/value_alignment_json/sft_wvs_valid_aug_convert.json \
  --thinking-start "Here are my reasoning steps:" \
  --thinking-end "\n[BEGIN FINAL RESPONSE]"

# Convert test data
python data/value_alignment_json/SFT_data_format.py \
  -i data/value_alignment_json/final/sft_wvs_test_combined_clean.json \
  -o data/value_alignment_json/sft_wvs_test_aug_convert.json \
  --thinking-start "Here are my reasoning steps:" \
  --thinking-end "\n[BEGIN FINAL RESPONSE]"
```

### 2. Dataset Registration
The dataset is already registered in `data/dataset_info.json` with the following entries:

```json
{
  "wvs_train_aug": {
    "file_name": "value_alignment_json/sft_wvs_train_aug_convert.json",
    "columns": {
      "prompt": "instruction",
      "response": "output"
    }
  },
  "wvs_valid_aug": {
    "file_name": "value_alignment_json/sft_wvs_valid_aug_convert.json",
    "columns": {
      "prompt": "instruction",
      "response": "output"
    }
  },
  "wvs_test_aug": {
    "file_name": "value_alignment_json/sft_wvs_test_aug_convert.json",
    "columns": {
      "prompt": "instruction",
      "response": "output"
    }
  }
}
```

## Training Configuration

The training setup is configured in `config/lora_sft_3090.yaml` (config for [LlamaFactory](https://github.com/hiyouga/LLaMAFactory)):

### Key Configuration Parameters
- **Model**: Qwen3-14B with 4-bit quantization
- **Training Method**: SFT (Supervised Fine-Tuning) with LoRA
- **LoRA Configuration**: Rank 16, target all layers
- **Dataset**: `wvs_train_aug` for training, `wvs_valid_aug` for validation
- **Batch Size**: 8 per device with 8 gradient accumulation steps
- **Learning Rate**: 1e-4 with cosine scheduler and 0.1 warmup ratio
- **Output**: Save checkpoints every 20 steps to `saves/qwen3-14b/qlora/sft`

## Running Training

To run the training, execute the following script:

```bash
# Set CUDA visible devices
export CUDA_VISIBLE_DEVICES=0,1,2,3

# Run training
llamafactory-cli train config/lora_sft.yaml
```

## Dataset Features

### Cultural Reasoning
Each entry includes detailed thinking processes that explain the cultural context behind survey responses, enabling models to generate culturally-aware answers.

### Survey Response Distributions
The dataset provides actual response distributions from the World Values Survey, allowing models to learn cultural preferences and norms.

### Multi-Country Coverage
The dataset covers responses from various countries, providing a diverse cultural perspective for model training.

## Citation

If you use this dataset in your research, please cite the following paper:

```
TODO
```

## Contact

For questions about the dataset or paper, please contact the authors at [alecliu@ontoweb.wust.edu.cn](mailto:alecliu@ontoweb.wust.edu.cn).

---

© 2026 ONTOWEB Team. All rights reserved.