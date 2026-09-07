Smart Question Paper Analyzer

Student Details

- Name: Kritika Limje
- Roll No.: BT240035ET
- Branch: Electronics and Telecommunication Engineering
- Semester: V Semester
- Course: Natural Language Processing (ET5M004)

1. Problem Statement / Objective

The Smart Question Paper Analyzer is an NLP-based application designed to analyze question papers using Natural Language Processing techniques.

The main objective of the project is to automatically process question paper text and extract useful information such as frequently used keywords, topics, questions, and similar or repeated questions.

2. Introduction

Question papers contain a large amount of textual information. Manually analyzing them to identify important topics, frequently used keywords, question patterns, and similar questions can be time-consuming.

This project uses Natural Language Processing techniques to analyze question paper data and present the results in a structured and understandable form.

The application helps in understanding the distribution and characteristics of questions in a question paper.

3. NLP Techniques / Methods Used

The project uses the following NLP techniques and methods:

- Text preprocessing
- Text normalization
- Tokenization
- Stop-word removal
- Keyword frequency analysis
- Question extraction
- Similar question detection
- Topic identification
- Data visualization

4. Dataset / Source of Data

The project uses a sample question paper as the input dataset.

The dataset is stored in:

dataset/Sample_question_paper.txt

The question paper text is processed by the NLP application to perform analysis and generate useful results.

5. Software, Tools and Libraries Used

Software / Tools

- Python
- Visual Studio Code
- Jupyter Notebook
- Git and GitHub

Python Libraries

- Regular Expressions ("re")
- Collections ("Counter")
- Difflib ("SequenceMatcher")
- Matplotlib
- Jupyter
- IPykernel

6. Methodology / Workflow

The project follows the following workflow:

Question Paper
      ↓
Text Input
      ↓
Text Preprocessing
      ↓
Text Normalization
      ↓
Tokenization
      ↓
Stop-word Removal
      ↓
Keyword Frequency Analysis
      ↓
Question Extraction
      ↓
Similar Question Detection
      ↓
Topic Analysis
      ↓
Visualization
      ↓
Results / Report

7. Project Features

The Smart Question Paper Analyzer provides the following features:

- Cleans and normalizes question paper text
- Tokenizes the input text
- Removes common stopwords
- Identifies frequently occurring keywords
- Extracts questions from the question paper
- Detects highly similar questions
- Identifies predefined topics
- Generates keyword frequency visualization
- Generates topic frequency visualization
- Produces structured analysis results

8. Project Structure

NLP_Smart_Question_Paper_Analyzer/
│
├── dataset/
│   └── Sample_question_paper.txt
│
├── output/
│   └── analysis_report.txt
│
├── screenshots/
│   ├── screenshot_1.png
│   ├── screenshot_2.png
│   └── ...
│
├── notebooks/
│   └── question_paper_analyzer.ipynb
│
├── question_paper_analyzer.py
├── README.md
├── requirements.txt
└── .gitignore

9. Steps to Execute the Project

Step 1: Install Python

Install Python on the system.

Step 2: Install Required Libraries

Open the terminal in the project folder and run:

py -m pip install -r requirements.txt

Step 3: Run the Python Application

Run the main Python source code:

py question_paper_analyzer.py

Step 4: Run the Jupyter Notebook

Open:

notebooks/question_paper_analyzer.ipynb

Select the Python kernel and execute the cells sequentially.

10. Sample Input

The input is a text-based question paper stored in:

dataset/Sample_question_paper.txt

Example:

1. Define Natural Language Processing.
2. Explain text preprocessing.
3. What is tokenization?
4. Explain the applications of NLP.

11. Sample Output

The analyzer generates information such as:

Total words: ...
Meaningful words: ...
Total questions: ...

Top 10 Keywords:
keyword1 : ...
keyword2 : ...
keyword3 : ...

Topics detected:
NLP : ...
Python : ...

The project also generates visualizations for:

- Top 10 keyword frequency
- Topic frequency

Similar questions are also identified using text similarity analysis.

12. Results / Observations

The Smart Question Paper Analyzer successfully processes the question paper and extracts useful information.

The analysis provides:

- Frequently occurring keywords
- Extracted questions
- Similar question pairs
- Detected topics
- Keyword frequency visualization
- Topic frequency visualization

The results demonstrate that NLP techniques can be used to analyze and organize information from question papers automatically.

13. Conclusion

The Smart Question Paper Analyzer demonstrates the application of Natural Language Processing techniques to question paper analysis.

The project performs text preprocessing, tokenization, stop-word removal, keyword analysis, question extraction, similarity detection, topic identification, and visualization.

The system provides a structured way to understand the content and patterns present in a question paper and reduces the effort required for manual analysis.

14. Resources / References

- Python Documentation
- Jupyter Notebook Documentation
- Matplotlib Documentation
- Natural Language Processing learning resources
- Git and GitHub documentation