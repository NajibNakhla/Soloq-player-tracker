# 🎮 League of Legends Player Performance Analysis (Solo Queue)

## 👋 Motivation

As a League of Legends coach, tracking player performance is crucial for improving my team and preparing strategies against enemy teams during tournaments. This project helps me analyze detailed match data to gain insights on player behavior, strengths, and weaknesses.

---

## 📘 Notebook Purpose

This notebook is the **first step in the data science phase** of our League of Legends performance tracking project. The goal of this notebook is to:

- Understand the structure and content of the match data
- Explore key metrics for each game
- Identify and handle missing values
- Prepare the dataset for further **visualization**, **trend analysis**, and **modeling**

---

## 🧠 Project Context

This project aims to analyze a **specific player's Solo Queue performance** using match history data from the Riot Games API. Prior to this notebook, we built a full **data engineering pipeline** that:

1. ✅ Fetches player `PUUID` via Riot ID  
2. ✅ Collects up to 300 match IDs filtered for **Ranked Solo Queue (queueId = 420)**  
3. ✅ Paginates through Riot’s match history endpoint to stay within API limits  
4. ✅ Retrieves and processes match details for each game  
5. ✅ Extracts over 100 relevant metrics per match (KDA, CS, gold, wards, vision score, etc.)  
6. ✅ Saves the final dataset as a `.csv` file for analysis  

---

## 🛠️ This Notebook Covers

- Loading the cleaned dataset from `.csv`  
- Inspecting dataset shape, columns, and data types  
- Identifying missing values and outliers  
- Performing basic statistical summaries  
- Preparing the data for visualization and machine learning models  

---

## 🎯 Next Steps

After this notebook, we will move on to:

- Advanced visualizations (e.g., winrate by champion, gold trends, vision behavior)  
- Behavior-based performance analysis (early vs late game stats)  
- Predictive modeling (e.g., predicting win probability from early game state)  
- Dashboarding and reporting  

---

> 📌 Dataset Source: Riot Games Match API (Solo Queue)  
> 📁 File Used: `data/Nakla_EUW.csv`  
