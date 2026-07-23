## Data Science Project Template

# Wearable Workout Data Visualization

This project provides an automated Python pipeline for visualizing wearable sensor data (Accelerometer and Gyroscope). It is designed to analyze 3D movement during strength training exercises (like squats, bench presses, and rows) and automatically generate performance dashboards for different participants and workout sets.

## Features

- **Data Ingestion:** Loads pre-processed time-series sensor data from a Pandas Pickle (`.pkl`) format.
- **Granular Filtering:** Easily isolate data by exercise type (`label`), user (`participant`), or workout set (`set`).
- **Multi-Axis Plotting:** Visualizes movement in 3D space by mapping `acc_x`, `acc_y`, and `acc_z` (or gyroscope equivalents) on shared axes.
- **Automated Dashboard Generation:** Uses loops to automatically generate, format, and save 2-panel subplots (Accelerometer vs. Gyroscope) for every participant and exercise combination.
- **High-Quality Export:** Plots are styled using the `seaborn-v0_8-deep` theme and exported as high-resolution (100 DPI) PNG files.

## Project Structure

Because the script uses relative file paths, ensure your project directory looks like this before running the code:

├── LICENSE
├── Makefile           <- Makefile with commands like `make data` or `make train`
├── README.md          <- README for using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default Sphinx project; see sphinx-doc.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.py           <- Make this project pip installable with `pip install -e`
├── src                <- Source code for use in this project.
│   ├── __init__.py    <- Makes src a Python module
│   │
│   ├── data           <- Scripts to download or generate data
│   │   └── make_dataset.py
│   │
│   ├── features       <- Scripts to turn raw data into features for modeling
│   │   └── build_features.py
│   │
│   ├── models         <- Scripts to train models and then use trained models to make
│   │   │                 predictions
│   │   ├── predict_model.py
│   │   └── train_model.py
│   │
│   └── visualization  <- Scripts to create exploratory and results oriented visualizations
│       └── visualize.py
│
└── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io
```

## Prerequisites

To run this script, you will need Python installed along with the following libraries:

- `pandas`
- `matplotlib`

You can install them via pip:

```bash
pip install pandas matplotlib

```

## Usage

1. Ensure your processed data file is located at `../../data/interim/01_data_processed.pkl` relative to where you run the script.
2. Ensure the destination folder `../../reports/figures/` exists, or the script will throw a "File Not Found" error when saving the images.
3. Run the script in your IDE, Jupyter Notebook, or via the command line.
4. The script will display individual plots dynamically and save the final combined dashboard images into the `reports/figures/` directory.

## Known Data Requirements

The input `.pkl` file must be a Pandas DataFrame containing at least the following columns:

- `set`: (int) The workout set number.
- `label`: (str) The name of the exercise (e.g., 'squat', 'bench', 'row').
- `participant`: (str) The ID of the person performing the exercise (e.g., 'A', 'B').
- `category`: (str) Weight category (e.g., 'heavy', 'medium').
- `acc_x`, `acc_y`, `acc_z`: (float) Accelerometer readings.
- `gyro_x`, `gyro_y`, `gyro_z`: (float) Gyroscope readings.
