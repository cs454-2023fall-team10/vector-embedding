## 0. Prerequisite
```
$ conda env create --file environment.yml
```

## 1. Run
For <json_file_path> and <intents_file_path>, relative path should be used
```
$ python main.py <json_file_path> <intents_file_path> <NUM_OUTPUTS> <DEPTH_THRESHOLDS> <(Optional) model_name>
```

# Gensim warning
If you use gensim 4.x.x, error will happen. Please install gensim==3.8.3
