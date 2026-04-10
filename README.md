# 🌊 EcoStream: River Health Prediction System

An intelligent, data-driven application designed to monitor and predict river ecosystem health. EcoStream utilizes a machine learning backend to estimate Dissolved Oxygen (DO) levels based on 7-day historical readings of various water pollutants. It includes a modern, user-friendly `tkinter` graphical interface for seamless data entry and analysis.

## Features

* **Advanced Feature Engineering:** Calculates rolling means, standard deviations, maximums, and trends across 7-day windows for multiple pollutants.
* **Ensemble Machine Learning:** Utilizes a robust `VotingRegressor` combining `ExtraTreesRegressor`, `RandomForestRegressor`, and `HistGradientBoostingRegressor` for high-accuracy predictions.
* **Health Status Classification:** Automatically categorizes river health into five distinct tiers based on WHO/EPA ecological standards.
* **Modern GUI:** A clean, grid-based interface built with standard Python libraries for zero-dependency frontend deployment.

## Project Structure

* `river_health_prediction.ipynb`: The core data science notebook containing exploratory data analysis (EDA), feature engineering logic, and model training/evaluation.
* `river_health_backend.py`: The machine learning logic extracted into a modular Python script. It handles feature generation, model loading, and DO prediction.
* `river_health_gui.py`: The frontend user interface. It provides a 5x7 grid for entering daily sensor readings and displays the predicted health status.
* `sample_submission.csv`: The training dataset containing historical sensor readings.

## River Health Classifications

The system classifies ecological health based on the predicted Dissolved Oxygen (mg/L) levels:

| DO Level (mg/L) | Health Status | Ecological Risk |
| :--- | :--- | :--- |
| ≥ 8 | Excellent 🟢 | Optimal for all aquatic life |
| 6 – 8 | Good 🟡 | Minor stress on sensitive species |
| 4 – 6 | Fair 🟠 | Moderate stress; early warning |
| 2 – 4 | Poor 🔴 | High stress; significant risk |
| < 2 | Critical ⚫ | Dead Zone; severe oxygen depletion |

## Installation & Setup

1. Clone this repository to your local machine.
2. Ensure you have Python 3.8+ installed.
3. Install the required data science packages:

```bash
pip install pandas numpy scikit-learn
```

## Usage

To launch the River Health Monitor GUI, run the following command in your terminal:
```
python river_health_gui.py
```
## How to add and push this to your repository
Run these commands in your terminal to save the file and push it to your main branch on GitHub:
```
git commit -m "Add requirements.txt"
```
