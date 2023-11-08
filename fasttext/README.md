# Used dataset
This model is based on wikipedia dump file. If you want to make model with our code, please follow this process.

> ## 0. Prerequisite
> To make model, you should install java in your local environment.
> ```
> sudo apt-get update && sudo apt-get install -y openjdk-8-jdk g++ build-essential autoconf automake
> ```
> Also, you can use conda for executing word2vec
> ```
> conda env create --file ./environment.yml
> conda activate word2vec
> ```
> For making model, you should have some directories
> ```
> mkdir data
> mkdir models
> mkdir parsed_data
> mkdir preprocess
> ```
   
> ## 1. Download dump file & locate in ./data directory
> You can download files in https://dumps.wikimedia.org/kowiki/
   
> ## 2. Parse dumpfile with wikiextractor
> ```
> pip install wikiextractor
> cd data
> python -m wikiextractor.WikiExtractor <your_dump_file>
> ```
   
> ## 3. Run python file sequently
> ```
> python load_data.py
> python preprocess.py
> python make_model.py
> ```
> Model will be located in ./models

> ## 4. Run model
> ```
> python main.py
> ```


# Gensim warning
If you use gensim 4.x.x, error will happen. Please install gensim==3.8.3
