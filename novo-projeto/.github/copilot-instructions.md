# AI Coding Agent Instructions: ModelLab Fine-Tuning Project

## Project Overview
This is a **model fine-tuning workspace** for **Microsoft Phi-Silica 3.6** using the ModelLab CLI. The project supports two fine-tuning approaches:
- **LoRA** (Low-Rank Adaptation) - memory-efficient training with small trainable layers
- **Soft Prompt** - prefix tuning for task-specific adaptation

## Project Structure

```
├── .model_lab/cli/              # ModelLab CLI tool (pipx package)
├── microsoft_phi-silica-3.6_v1/
│   ├── model_project.config      # Model workflows configuration
│   ├── lora/
│   │   ├── lora.yaml            # LoRA hyperparameters (learning rate, batch size, etc.)
│   │   ├── lora.yaml.config     # UI field definitions for LoRA parameters
│   │   └── infra/
│   │       ├── model.json       # Model metadata (name, version, host)
│   │       └── provision/
│   │           ├── finetuning.bicep        # Azure Container Apps infrastructure
│   │           ├── finetuning.config.json  # Azure resource names & commands
│   │           └── finetuning.parameters.json  # Bicep deployment parameters
│   └── soft_prompt/             # Same structure for soft prompt tuning
└── finetuning.workspace.config  # Workspace version marker
```

## Key Conventions

### 1. Configuration File Relationships
- **`lora.yaml`**: Training hyperparameters consumed by the fine-tuning job
- **`lora.yaml.config`**: JSON schema defining UI fields and validation for `lora.yaml` parameters
- **`infra/provision/finetuning.config.json`**: Maps to Azure resource names (storage, ACA job, etc.) populated during provisioning
- **Mount paths**: Use `mount/<run_id>/` prefix for dataset/output paths in YAML files

### 2. Dataset Format Requirements
Training and test datasets must be **JSONL** format (one JSON object per line):
```json
{"messages":[{"content":"Hello, bot.","role":"user"},{"content":"Hi! How can I assist?","role":"assistant"}]}
{"messages":[{"content":"Who are you?","role":"user"},{"content":"I am your assistant.","role":"assistant"}]}
```

### 3. Azure Infrastructure Pattern
Infrastructure uses **Azure Container Apps (ACA)** with GPU workload profiles:
- **Workload Profile**: `Consumption-GPU-NC24-A100` for training jobs
- **Storage**: Azure File Share (`Standard_LRS`) mounted to ACA environment
- **Logging**: Log Analytics workspace for job monitoring
- **Timeout**: Default 21600 seconds (6 hours) configurable in `finetuning.parameters.json`

## Developer Workflows

### ModelLab CLI Installation
```bash
# IMPORTANT: Use cmd, not PowerShell (PATH registration issues)
cd .model_lab/cli
python -m pip install pipx
python -m pipx install .

# Verify installation
modellab --help
```

### ModelLab CLI Commands

**Available Commands**:
- `modellab listModels` - List all available models for fine-tuning
- `modellab createWorkspace --path <dir>` - Create new workspace
- `modellab addModel --model_id <id>` - Add model to current workspace (auto-detects workspace path)
- `modellab listLocalModels` - List models in current workspace
- `modellab syncProjects [--update]` - Sync all projects, optionally update versions
- `modellab convert --model_id <id> --workflow <name> [--runtime <env>] [--name <output>]` - Run fine-tuning job
- `modellab cancelJob` - Cancel running job (auto-triggered on Ctrl+C)

**Key Behaviors**:
- Commands except `listModels`, `createWorkspace`, and `cancelJob` auto-detect workspace from current directory
- CLI communicates with VS Code extension via `vscode://` URI protocol
- Logs streamed to console with timestamps via local HTTP server (port 12432)

**Common Workflows**:
```bash
# Initialize workspace and add model
modellab createWorkspace --path c:/my-project
cd c:/my-project
modellab addModel --model_id microsoft/phi-silica-3.6

# List and run fine-tuning
modellab listLocalModels
modellab convert --model_id microsoft/phi-silica-3.6 --workflow LoRA
```

### Adding a New Fine-Tuning Approach
When adding a new tuning method (e.g., QLoRA, full fine-tuning):
1. Create new folder under `microsoft_phi-silica-3.6_v1/<method_name>/`
2. Add `<method>.yaml` with hyperparameters
3. Add `<method>.yaml.config` with UI field definitions
4. Copy and modify `infra/` directory structure
5. Update `model_project.config` workflows array with new entry

### Modifying Hyperparameters
- Edit `lora.yaml` or `soft_prompt.yaml` directly for quick changes
- Update corresponding `.yaml.config` if adding/removing parameters or changing validation rules
- Key LoRA parameters:
  - `learning_rate`: 0.0002 (2e-4) typical for LoRA
  - `lora_dropout`: 0.1 for regularization
  - `finetune_train_batch_size`: 2 (memory-constrained on A100)
  - `gradient_accumulation_steps`: Increase if batch size too small

### Soft Prompt Specifics
- `init_prompt`: Task-specific instruction prefix (e.g., sentiment classification)
- `number_of_virtual_tokens`: 64 (typical range: 20-100)
- Lower learning rate (3e-5) compared to LoRA due to smaller parameter space

## Critical Details

- **No README in root**: Project context lives in this file and `.model_lab/cli/README.md`
- **Config nulls**: `null` values in `finetuning.config.json` and `finetuning.parameters.json` are populated by ModelLab CLI during provisioning
- **Bicep resource naming**: Uses `resourceSuffix` (5-char unique string) to avoid naming collisions
- **Early stopping**: Both methods use `early_stopping_patience: 5` to prevent overfitting

## Common Tasks

**Update training dataset samples**:
```yaml
# In lora.yaml or soft_prompt.yaml
finetune_train_nsamples: 8000  # Change this value
```

**Change GPU timeout**:
```json
// In infra/provision/finetuning.parameters.json
"timeout": { "value": 21600 }  // Seconds
```

**Modify Azure region**:
```json
// In infra/provision/finetuning.parameters.json
"location": { "value": "eastus" }  // Default: resourceGroup().location
```
