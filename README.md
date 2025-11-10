# MovieDude ![Movie Recommendation System](https://img.shields.io/badge/Movie%20Recommendation%20System-orange?style=flat-square)

An advanced "content-based filtering" movie recommendation system built with Python, scikit-learn, and SQLite.<br>
It provides personalized movie suggestions based on user preferences through data analysis, and also allows users to search by a specific movie title or keyword to find similar recommendations.

<img src="https://github.com/user-attachments/assets/163c4a81-32d4-4b16-bce8-367f3ecabcc0">

---

### Work Flow Sessions

- <strong>On Users Table Flow </strong>>>><br>
  Extract and analyze user activity data from the database to determine personal preferences.

  1. Apply Min–Max data normalization
  2. Extract top favorite movies by normalized score
  3. Use quasi-NLP to extract movie attributes
  4. Return finall result processed matrix ready for model use

- <strong>Main Engine Processes</strong> >>><br>
  Performs similarity analysis and recommendation generation based on user preferences and the database contents.

  1. Pre-processing validation check
  2. Multi-binary encoding
  3. Apply selected options #1 (filter out watched movies)
  4. Execute engine process
  5. Apply selected options #2 (filter for high-rated movies)
  6. Return final result as a list (array)
  
---

### Requirements

After installing `Python 3.x` you can install the required packages by running the following command in the terminal.<br>
_Using a virtual environment is recommended._

```
pip install pandas==2.3.3 scikit-learn==1.7.2 numpy==2.3.3 termcolor==3.2.0
```

Alternatively, you can install all dependencies from the included `requirements.txt` file, simply open your terminal in the project directory and run:

```
pip install -r requirements.txt
```
