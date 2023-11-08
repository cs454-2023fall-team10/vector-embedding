## 0. Prerequisite
```
$ conda env create --file environment.yml
```
If it doesn't work, do it manually
```
$ conda env create -n <conda_name> python=3.9
$ pip install sentence_transformers
```

## 1. Run
For <json_file_path> and <intents_file_path>, relative path should be used
```
$ python main.py <json_file_path> <intents_file_path> <NUM_OUTPUTS> <DEPTH_THRESHOLDS> <(Optional) model_name>
```
