# We are gonna do some data cleaning then we are gonna do some data analysis and then data visualization #let's import necassary libraries and dependencies
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# Now let's read the data into the datafrane
df = pd.read_csv("Fortune_1000.csv")

pd.set_option(
    "display.max_rows", None
)  # This code will let us view the entire data when not just some preview
df  # Let's see some simple information about the data
df.info()  # Now let's see some simple description of the data that we have
df.describe()  # Now that w completly understand the data , Let's do some data cleaning which will make the data easy to interpret
# First let's have a look at the propotion of the missing values in the data frame
for (
    col
) in (
    df.columns
):  # this will loop through the columns and find the propotion of the data
    pct_missing = np.mean(df[col].isnull())
    print("{} - {:.2f}%".format(col, pct_missing * 100))
# So this will loop through all the columns nad print the proportion of missing value in total value #Okay alot of null values in the dataframe , first let's take care of that shall we.
# well et's try to use forward fill and then we can continue with the data
df.fillna(method="bfill", inplace=True)
# Okay now that's taken care of #to make analysis easier let's cahne the name of some columns first.
df.rename(columns={"num. of employees": "employees"}, inplace=True)
# This is the only columns name that could be some problems #Now that's done , I wanna change the yes to 1 and no to 0 , so that it will be easier later.
df.replace(
    {"yes": 1, "no": 0}, inplace=True
)  # This should change all the yes to 1 and no to 0 #Now that that's taken care of we can move on , we also dont need the Website and Ticker columns as they are useless for our analysis
df.drop(
    columns=["Website", "Ticker"], inplace=True
)  # This should delete both columns #Now that we are done with it , Let's move on with the data cleaning.
# all the columns that hold monetary values are in manitute of million which can be very hard to so let's change them into their full value
# as the value of each of each monetary column we can just loop along with it
columns = ["revenue", "profit", "Market Cap"]

# Iterate over each column in the list
for col in columns:
    # Multiply the values in the current column by 1,000,000
    df[col] *= 1000000
    # now that we are done with that , let's move on to anotehr data cleaning step ,
# let's detect and remove outliers if there are any. df.describe()#Next step in finding an outlier would be to plot the data , let's plot the proit and revenue columns as they are most likely to have outliers
# Set up the matplotlib figure
plt.figure(figsize=(14, 6))

# Plot the revenue distribution plot
plt.subplot(1, 2, 1)
sns.histplot(df["revenue"], kde=True)
plt.title("Revenue Distribution")
plt.xlabel("Revenue")
plt.ylabel("Density")

# Plot the profit distribution plot
plt.subplot(1, 2, 2)
sns.histplot(df["profit"], kde=True, color="orange")
plt.title("Profit Distribution")
plt.xlabel("Profit")
plt.ylabel("Density")

# Adjust layout to make room for the plots
plt.tight_layout()
plt.show()  # Let's use a boxplot to make it much easier
sns.boxplot(
    df["revenue"]
)  # THis data set doesn't seem to have much of an outliers here, as the copmpanies revenue and profit have been growing in similiar rate, also it seems like
# The revenue and profit also align with the result we get from a simple google search . Now we can move on to analysis part ## Analysis #let's have a look at the data
df  # Now let's create a dataframe that holds the data of top 10 largest companies based on revenue
revenue = df.sort_values(by="revenue", ascending=False).head(10)
revenuedfemployee = df.sort_values(by="employees", ascending=False)[
    ["company", "employees"]
].head(10)
employee  # Now let's see how many companies are there from each sector, and maybe create a dataframe that holds that data
sector_counts = df["sector"].value_counts().reset_index()
sector_counts  # Now we can see the companies where ceo are women
ceo_women = df.loc[df["ceo_woman"] == "yes", ["company", "revenue", "Market Cap"]]
ceo_womensector_market_cap = (
    df.groupby("sector")["Market Cap"].sum().sort_values.reset_index()
)
sector_market_capwomen_marketcap = (
    df[df["ceo_woman"] == 1]
    .groupby("company")["Market Cap"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
men_marketcap = (
    df[df["ceo_woman"] == 0]
    .groupby("company")["Market Cap"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
women_marketcap  # Now that we know how many companies who have women as CEO of the companies.
# Now let's see all the companies and their market cap who are new commenrs to the list.
new_comers = (
    df.loc[df["newcomer"] == "yes", ["company", "revenue", "Market Cap"]]
    .sort_values(by="Market Cap", ascending=False)
    .reset_index(drop=True)
)
new_comers  # Now let's see which cities has the most numbers of fortuen 1000 companies
cities = df["city"].value_counts().reset_index()
cities  # Now that we hae the data for the cities with the most number of these companies , now let's create a dataframe that holds the data of top 10 countries
# with the highest profit
profit = (
    df.sort_values(by="profit", ascending=False)[
        ["company", "sector", "revenue", "profit", "Market Cap"]
    ]
    .head(10)
    .reset_index(drop=True)
)
profit  # Let's see how many companies rank increased compared to previous year
rank_increase = df.loc[
    df["rank_change"] > 0, ["rank", "prev_rank", "company", "revenue", "Market Cap"]
].reset_index(drop=True)
rank_increase  # Now that we are done with this wecan continue towards data visualization
# We are gonna use matplotlib  and seaborn to visualize the data #Let's create a barchart using the sector_counts dataframe so that we will have a better idea of the data
sector_counts = sector_counts.head(10)
plt.figure(figsize=(10, 15))  # Adjust the size of the figure as needed
plt.bar(sector_counts["sector"], sector_counts["count"], color="skyblue")
plt.title("Sector Counts Bar Chart")
plt.xlabel("Sectors")
plt.ylabel("Counts")
plt.xticks(fontsize=5)
plt.yticks(fontsize=5)
plt.show()  # Now let's create a plot that shows top 10 companies with largest employees count
plt.figure(figsize=(10, 15))
plt.plot(employee["company"], employee["employees"], color="skyblue")
plt.xlabel("Companies")
plt.ylabel("Employees count")
plt.xticks(fontsize=5)
plt.show()  # Now let's plot another plot that will show line chart of both GDP
df  # Now let's make dual line chart that will show market cap of men and women companies side by side
men_marketcap.plot.bar()
plt.show()  # Now let's plot a pie-chart of companies according to sectors.
# Plotting the pie chart
plt.figure(figsize=(10, 10))
plt.pie(
    sector_counts["count"],
    labels=sector_counts.sector,
    autopct="%1.1f%%",
    startangle=140,
)
plt.title("Companies according to sector ")
plt.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

# Display the plot
plt.show()
