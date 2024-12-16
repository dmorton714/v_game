# Video Game Sales Data Analysis Project

## Overview

This project is an on going analyzes video game sales data to gain insights into various factors, including console sales throughout their life cycles, top developers, and more. The ultimate goal is to generate a data dashboard that presents key findings and visualizations.

## Current state 
The project is currently being worked on in the `final_working.ipynb` notebook. It has been converted to a class and will soon have a UI added to it. Tweaks on the plots are the next step to make them a bit more visually appealing. 

## Data

The dataset used in this project contains information about video game sales, including details such as title, genre, publisher, developer, critic scores, total sales, release dates, and console information.
[Data](https://www.kaggle.com/datasets/asaniczka/video-game-sales-2024)

## Project Structure

The project is organized as follows:

- **Data Exploration:** Jupyter notebooks or scripts exploring and cleaning the dataset.
- **Analysis:** Notebooks or scripts focusing on specific analyses, such as console sales trends, top developers, etc.
- **Dashboard:** Code and files related to the generation of the data dashboard.

## Key Insights

Some of the key insights and analyses include:

- Console sales trends over different life cycles.
- Identification of top developers and their contributions.
- Genre-wise distribution of sales.

## Data Visualization

The project includes various visualizations, such as charts and graphs, to help communicate the findings effectively. The data dashboard will consolidate these visualizations for easy interpretation.

## Getting Started

To replicate or contribute to this project, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/your-project.git`
2. Install the necessary dependencies: `pip install -r requirements.txt`
3. Explore the Jupyter notebooks or scripts in the respective folders.
4. 1_user.ipynb is a interactive notebook without code blocks. 
5. test.ipynb is my learning book for adding new features. 
6. fun.py is the function file used to run the user notebook 
7. I have included a docker image to use if you dont wish to run locally on you base system. 

## Dependencies

List any dependencies or libraries used in the project.

## Contribution Guidelines

If you'd like to contribute to this project, please follow the contribution guidelines outlined in the [CONTRIBUTING.md](CONTRIBUTING.md) file.


###  Virutal Environment Instructions

1. After you have cloned the repo to your machine, navigate to the project 
folder in GitBash/Terminal.
1. Create a virtual environment in the project folder. 
1. Activate the virtual environment.
1. Install the required packages. 
1. When you are done working on your repo, deactivate the virtual environment.

Virtual Environment Commands
| Command | Linux/Mac | GitBash |
| ------- | --------- | ------- |
| Create | `python3 -m venv venv` | `python -m venv venv` |
| Activate | `source venv/bin/activate` | `source venv/Scripts/activate` |
| Install | `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| Deactivate | `deactivate` | `deactivate` |

|To Run In Docker|
| --- | 
| `docker build . --tag v_game:latest` |
| `docker run -it -p 8888:8888 v_game:latest` |