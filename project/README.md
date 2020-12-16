This repository includes code to extract-transform-load records of Toronto restaurants from the Yelp dataset of businesses, reviews, and users data from Kaggle. The repo also includes files that include statistical analysis and machine learning on restaurant data.

Requirements [It is recommended to download the latest stable version of each software]  

Applications:
   * Python: https://www.python.org/  
   * Spark: https://spark.apache.org/  

Libraries:
  *  Pandas: https://pandas.pydata.org/
  *  NumPy: https://numpy.org/
  *  Scipy: https://www.scipy.org/
  *  Matplotlib: https://matplotlib.org/
  *  Seaborn: https://seaborn.pydata.org/
  *  Sklearn: https://scikit-learn.org/
  *  Statsmodels: https://www.statsmodels.org/stable/index.html

Dataset:
    The following link contains the download for the raw dataset: https://www.kaggle.com/yelp-dataset/yelp-dataset
    Once downloaded, you should have a zip file named ‘archive’. Create a folder name ‘0-raw_data’ and drag the following files from the ‘archive’ zip into the newly created       folder: ‘yelp_academic_dataset_business.json’, ‘yelp_academic_dataset_review.json’, ‘yelp_academic_dataset_user.json’



Code Organization
    The folders are listed in numerical order of execution. Detailed instructions are provided below. None of the files require any arguments to run. Simply run each code with     the command ‘python filename’. The main folder must contain the following folders:
    0-raw_data
    1-processing_cleaning
    2-cleaned_data
    3-analyses
    4-figures



Code Execution
1. Folder: ../1-processing_cleaning  
    A) File: clean_business.py  
        Reads: ../0-raw_data/yelp_academic_dataset_business.json  
        Command: python clean_business.py  
        Output: ../2-cleaned_data/business_clean.csv  

    B) File: all_data_merge.py [will take a few minutes to run]
        Reads: ../0-raw_data/yelp_academic_dataset_review.json,  
        ../0-raw_data/yelp_academic_dataset_user.json,  
        ./2-cleaned_data/business_cleaned.csv  
        Command: spark-submit all_data_merge.py  
        Output: business_reviews_users_merged.csv  


2. Folder: ../3-analyses  
    A) File: restaurant_popularity.py  
        Reads: ../2-cleaned_data/business_reviews_users_merged.csv  
        Command: python restaurant_popularity.py  
        Output: ../4-figures/restaurant_popularity/unadj_week.png,  
        ../4-figures/restaurant_popularity/adj_week.png,  
        ../4-figures/restaurant_popularity/unadj_hol.png,  
        ../4-figures/restaurant_popularity/adj_hol.png,  
        statistics on command line

    B) File: nationality_comparison.py  
        Reads: ../2-cleaned_data/business_cleaned.csv  
        Command: python nationality_comparison.py  
        Output: ../4-figures/nationality_comparison/nationality_ratings.png,  
        statistics on command line  

    C) File: user_review_trend.py  
        Reads: ../2-cleaned_data/business_reviews_users_merged.csv  
        Command: python user_review_trend.py  
        Output: ../4-figures/user_review_trend/user_rating.png,  
        ../4-figures/user_review_trend/non_elite_rating.png,  
        ../4-figures/user_review_trend/elite_rating.png  

    D) File: restaurant_score_classify.py  
        Reads: ../2-cleaned_data/business_cleaned.csv  
        Command: python restaurant_score_classify.py  
        Output: classifier accuracy score on command line  
