Loan Approval Prediction with NB, KNN, and LR




This repository contains the code, documentation, and resources for the project titled "Loan Approval Prediction with NB, KNN, and LR." This project leverages machine learning methodologies to improve the loan approval process using Naive Bayes (NB), K-Nearest Neighbors (KNN), and Logistic Regression (LR) algorithms.

Table of Contents
Introduction
Project Structure
Installation
Usage
Algorithms
Dataset
Model Development
Performance Evaluation
Results
Conclusion and Future Work
Acknowledgements
References
Introduction
This project aims to enhance the efficiency of loan approval processes in financial institutions by applying machine learning algorithms. The study focuses on analyzing diverse customer data, including age, income, and education, to develop predictive models that can forecast loan approval outcomes. The performance of these models is evaluated based on accuracy, precision, and recall, with an exploration of ensemble methods to further improve overall accuracy.

Project Structure
The repository is structured as follows:
├── data
│   └── bank_loans.csv
├── src
│   ├── data_preprocessing.py
│   ├── model_training.py
│   ├── model_evaluation.py
│   └── predict.py
├── notebooks
│   └── Loan_Approval_Prediction.ipynb
├── results
│   └── model_performance_metrics.csv
├── README.md
└── requirements.txt


Installation
To install the necessary dependencies for this project, run the following command: pip install -r requirements.txt

Usage
To run the project, follow these steps:

Data Preprocessing: Prepare the dataset by executing the data preprocessing script.-(python src/data_preprocessing.py)

Model Training: Train the predictive models using the prepared dataset.(python src/model_training.py)

Model Evaluation: Evaluate the performance of the trained models.(python src/model_evaluation.py)

Prediction: Use the trained models to predict loan approval outcomes for new customer data. (python src/predict.py)

Algorithms
The project employs three machine learning algorithms:

Naive Bayes (NB): Simple and efficient for classification tasks, modeling the probability of loan approval based on customer attributes.
K-Nearest Neighbors (KNN): Classifies data points based on the majority class of their nearest neighbors, capturing local patterns and relationships.
Logistic Regression (LR): Effective for binary classification tasks, modeling the probability of loan approval as a function of customer attributes.
Dataset
The dataset used in this project is the "Universal Bank customer information dataset" from Kaggle. It contains data on over 5,000 customers, including features such as age, income, family size, education level, and financial behaviors.

Model Development
The development of predictive models involves the following steps:

Data Collection and Preprocessing: Gathering and preparing the dataset for analysis.
Algorithm Application: Applying NB, KNN, and LR algorithms to the dataset.
Parameter Tuning: Optimizing algorithm parameters to improve model performance.
Model Training: Training the models on the preprocessed dataset.
Performance Evaluation
Model performance is evaluated using key metrics, including accuracy, precision, and recall. Ensemble methods are explored to enhance overall accuracy by combining the strengths of individual models.

Results
The results of the model evaluation are summarized as follows:

Logistic Regression: Accuracy of 95.5%
Multinomial Naive Bayes (NB): Accuracy of 89.5%
K-Nearest Neighbors (KNN): Accuracy of 96%
Conclusion and Future Work
The project demonstrates the potential of machine learning techniques in improving loan approval predictions. Future enhancements may include incorporating more diverse datasets, refining feature engineering, exploring ensemble methods, and leveraging advanced techniques such as deep learning.

Acknowledgements
We would like to acknowledge the valuable insights and resources provided by the GitHub community, which have significantly contributed to the development of this project.

References
Supriya, Pidikiti, et al. (2019). Loan prediction using machine learning models. International Journal of Engineering and Techniques, 5(2), 144-147.
G. Arutjothi, Dr C. Senthamarai, “Prediction of Loan Status in Commercial Bank using Machine Learning Classifier,” Proceedings of the International Conference on Intelligent Sustainable Systems, (2017).
P. Supriya, M. Pavani, N. Saisushma, N. Kumari and K. Vikas, “Loan Prediction by using Machine Learning Models,” International Journal of Engineering and Techniques, (2019).
B. Srinivasan, N. Gnanasambandam, S. Zhao, R. Minhas, “Domain-specific adaptation of a partial least squares regression model for loan defaults prediction,” 11th IEEE International Conference on Data Mining Workshops, (2011).
M. V. Reddy, Dr B. Kavitha, “Neural Networks for Prediction of Loan Default Using Attribute Relevance Analysis,” International Conference on Signal Acquisition and Processing, (2010).
Ndayisenga, Theoneste. Bank Loan Approval Prediction Using Machine Learning Techniques. Diss. 2021.
Tejaswini, J., et al. "Accurate loan approval prediction based on machine learning approach." Journal of Engineering Science vol. 11, no.4, pp. 523-532. 2020.
Karthiban, R. M. Ambika and K. E. Kannammal, "A Review on Machine Learning Classification Technique for Bank Loan Approval," 2019 International Conference on Computer Communication and Informatics (ICCCI), pp. 1-6, 2019, doi: 10.1109/ICCCI.2019.8822014.
Y. Shi and P. Song, "Improvement Research on the Project Loan Evaluation of Commercial Bank Based on the Risk Analysis," 2017 10th International Symposium on Computational Intelligence and Design (ISCID), Hangzhou, 2017, pp. 3-6.doi: 10.1109/ISCID.2017.60.
For further details, please refer to the project documentation and code provided in this repository.
