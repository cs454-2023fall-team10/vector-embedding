# Warning
Before you run pororo, be aware that this model uses only pytorch 1.6.0
You should install appropriate pytorch with conda.

## 0. Prerequisite
Install conda environment
```
conda env create --file environment.yml
conda activate pororo
```
Install pytorch in conda
(This is cpu-only version)
(If you want to use GPU that support pytorch 1.6.0, please install cuda version)
```
conda install pytorch==1.6.0 torchvision==0.7.0 cpuonly -c pytorch
```

## 1. Run
For <json_file_path> and <intents_file_path>, relative path should be used
```
$ python main.py <json_file_path> <intents_file_path> <NUM_OUTPUTS> <DEPTH_THRESHOLDS> <(Optional) model_name>
```
