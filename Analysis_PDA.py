# First let's import all the necassary libraries and dependecies 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import re


df = pd.read_csv("Fortune_1000.csv")


# Let's see first few rows of the data in dataset
df.head()


# let's see a brief overview of the data first , so that we can move on
df.describe()


# Let's see some info about the dataset next .
df.info()


# Now that we know some basic info about the dataset , let's see columns name and data types of columns of our dataset
df.dtypes


print(df.columns)


# Now that we have an idea of what the data looks like , let's start with data cleaning
# First let's remove the Ticker columns as it is really unnecassary for our analysis
df.drop(columns=["Ticker"], inplace=True)


# Now let's drop the rows with missing values in the dataset, also drop the duplicate rows in the dataset
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)


# Now let's change the data type of columns to numeric where necassary
df["rank_change"] = df["rank_change"].astype(int)
df["num. of employees"] = df["num. of employees"].astype(int)


# Now let's change the name of the column from num of employees to num_employees so that it would be easier
df = df.rename(columns={"num. of employees": "num_employees"})


# now let's reset the index of the dataset
df = df.reset_index(drop=True)


# Now let's fill the null value in the revenue column with the mean of sector and revenue
df["revenue"] = df.groupby("sector")["revenue"].transform(
    lambda x: x.fillna(x.median())
)


# Now let's remove ',' and also the '$' signs from the profit columns as this would make it easier for calculation
df["profit"] = (
    df["profit"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.replace("$", "", regex=False)
    .astype(float)
)


# Now let's create a new column called revenue per companies so that we will know how much does the company pulls off per employee
df["revenue_per_employee"] = df["revenue"] / df["num_employees"]


# Let's create a bin for revenue and save it in revenue_Group columns so that it would be easier for the analysis
df["revenue_group"] = pd.cut(
    df["revenue"], bins=5, labels=["Very Low", "Low", "Medium", "High", "Very High"]
)


# let's change all the test in city columns to lowercase so that it would be easier to read and perform analysis on
df["city"] = df["city"].astype(str).str.lower()


# Let's detect outliers in the data using the z_score methods

z_scores = np.abs(stats.zscore(df["profit"]))
df = df[(z_scores < 3)]


# now let's remove all the special characters in the website columns

df["Website"] = df["Website"].apply(lambda x: re.sub(r"[^\w\s.]", "", x))


# Let's delete duplicate rows but also keeping the first occurance of the data
df = df.drop_duplicates(subset=["company", "revenue"], keep="first")


# Let's create a new columns that holds the profit margin data and name it simply profit margin
df["profit_margin"] = df["profit"] / df["revenue"]


# Now taht we are done with data cleanign we can move on to exploration
df.head()


# Now let's create a visualization that shows the porportion of male and female CEOs in Fortune 1000 Companies in The us
# we will be creating a pie-chart that shows what porpotion of CEOs are wome nand what propotion are male in those companies
female_ceo_counts = df["ceo_woman"].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(
    female_ceo_counts, labels=female_ceo_counts.index, autopct="%1.1f%%", startangle=140
)
plt.title("Proportion of Female CEOs", fontsize=14)
plt.show()


# From the above pie chart we can see that in the fortune 100 companies , only 8.3% CEOs are Female,
# This indicates a huge Gender Gap in leadership positions in the corporate world.


# Now let's create a histogram of revenue
plt.figure(figsize=(10, 6))
plt.hist(df["revenue"], bins=20, edgecolor="k")
plt.xlabel("Revenue", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.title("Distribution of Revenue", fontsize=14)
plt.show()


# This historgram of revenue distribution we can clearly see that very few companies hold alot of Revenue
# We can say that even among top 1000 companies top 100 companies holds more revenue than all of other 900 combined


# Top 10 sectors by number of companies in the list
top_sectors = df["sector"].value_counts().head(10)
plt.figure(figsize=(12, 6))
top_sectors.plot(kind="bar")
plt.xlabel("Sector", fontsize=12)
plt.ylabel("Number of Companies", fontsize=12)
plt.title("Top 10 Sectors by Number of Companies", fontsize=14)
plt.xticks(rotation=45)
plt.show()


# From teh above bar chart we can clearly see that Technology Fianance and Energy are the leading top secotrs in the list
# While financials leads the pact , Food . Bevrages and tobacco are at the bottom of the top 10


# Scatter plot of revenue Vs profit
plt.figure(figsize=(10, 6))
plt.scatter(df["revenue"], df["profit"], alpha=0.5)
plt.xlabel("Revenue", fontsize=12)
plt.ylabel("Profit", fontsize=12)
plt.title("Relationship between Revenue and Profit", fontsize=14)
plt.show()


# The scatter plot clearly states that the companies with highest revenues have highest profit
# but also there are a few anamolies where compnies with high revenue have low profit , Companies with low revenue also have very high profit.


# Revenue by sector
plt.figure(figsize=(12, 8))
df.boxplot(column="revenue", by="sector", vert=False)
plt.xlabel("Revenue", fontsize=12)
plt.ylabel("Sector", fontsize=12)
plt.title("Revenue Distribution by Sector", fontsize=14)
plt.suptitle("")
plt.show()


# Even though Retailing sector was one of the bottom 5 companies it leads as the sector with the highest revenue.
# and on the contrary Eventhough financials was leading with most number of companies in the fortune 1000s list, it is one of the sectors with least revenue


# Histogrma of number of employee
plt.figure(figsize=(10, 6))
plt.hist(df["num_employees"], bins=20, edgecolor="k")
plt.xlabel("Number of Employees", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.title("Distribution of Number of Employees", fontsize=14)
plt.show()


# From the above Histogram we can clearly see that as with revenue , Some companies at the top employees
# The most people ,for example Walmart employs more than 2 million people all by themselves


# Top 10 cities with most companies
top_cities = df["city"].value_counts().head(10)
plt.figure(figsize=(12, 6))
top_cities.plot(kind="bar")
plt.xlabel("City", fontsize=12)
plt.ylabel("Number of Companies", fontsize=12)
plt.title("Top 10 Cities by Number of Companies", fontsize=14)
plt.xticks(rotation=45)
plt.show()


# From above bar chart we can clearly see that new york has the highest number of companies in the Fortuen 100 companies
# Followed by Houston and Chicago , With Charlotte and Columbus right at the end of the top 10.


# Number of companies by state
companies_by_state = df["state"].value_counts()
plt.figure(figsize=(12, 6))
companies_by_state.plot(kind="bar")
plt.xlabel("State", fontsize=12)
plt.ylabel("Number of Companies", fontsize=12)
plt.title("Number of Companies by State", fontsize=14)
plt.xticks(rotation=45)
plt.show()


# above bar chart clearly shows us that Chicago and Texas and New York are top 3 states, while chicago being the top as it have more than 127 companies in Fortune 1000 list.
# Also we can see that Puerto Rico has the least number of companies in the fortune 1000 companies


profitability_by_sector = (
    df.groupby("sector")["profitable"].value_counts(normalize=True).unstack()
)
plt.figure(figsize=(12, 6))
profitability_by_sector.plot(kind="bar", stacked=True, color=["skyblue", "lightcoral"])
plt.xlabel("Sector", fontsize=12)
plt.ylabel("Proportion of Companies", fontsize=12)
plt.title("Profitability by Sector", fontsize=14)
plt.legend(["Not Profitable", "Profitable"])
plt.xticks(rotation=45)
plt.show()


# From the above stacked barchart we can clearly notice that although companies make billions in revenue not all of them gurantee profit.
# as evident from chart , Mining and Energy makes billion of dollars in revenue it is the least profitable sector , joined by media , which also makes billions in revenue but has little no negligable profit margin
# Also wholesalers and Retailers May have the one of the least revenue , It has the highest profit margin and is the best sector to start working , investing or Starting a business
