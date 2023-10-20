from Webscraper.Class import *

# Initialize Webscraper
scraper = Webscraper()

# Test URLs
file_path = '.../Utilities/Webscraper/Data/Input/Test_URL.csv'
urls = pd.read_csv(file_path)['url'].head(100).astype(str).tolist()


### Comparing Performance of Trafilatura and Beautiful Soup
results = []

for url in urls:

    # Trafilatura
    start_time = time.time()
    output = Webscraper.trafilatura_scraper(url)
    end_time = time.time()
    duration = end_time - start_time
    evaluation = evaluate_output(output)
    results.append({"URL": url, "Scraper": "Trafilatura", "Duration": duration, "Result": evaluation})

    # Beautiful Soup
    start_time = time.time()
    output = Webscraper.bs_scraper(url)
    end_time = time.time()
    duration = end_time - start_time
    evaluation = evaluate_output(output)
    results.append({"URL": url, "Scraper": "Beautiful Soup", "Duration": duration, "Result": evaluation})

df = pd.DataFrame(results)
df.head()

# save results
df.to_csv(".../Utilities/Webscraper/Data/Output/Performance_Results.csv", index=False)


### Removing Outliers 

# Calculate the IQR for the 'Duration' column
Q1 = df['Duration'].quantile(0.25)
Q3 = df['Duration'].quantile(0.75)
IQR = Q3 - Q1

# Define the bounds for the outliers
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filter out the outliers
df_filtered = df[(df['Duration'] >= lower_bound) & (df['Duration'] <= upper_bound)]


### Visualising Performance Results

import matplotlib.pyplot as plt
import seaborn as sns

# Set the style of visualization
sns.set_style("whitegrid")

# Duration Visualization
plt.figure(figsize=(10, 6))
sns.barplot(x='Scraper', y='Duration', data=df, estimator=sum)
plt.title('Average Duration for Each Scraper')
plt.ylabel('Average Duration (s)')
plt.show()

# Success Rate Visualization
scraper_names = df['Scraper'].unique()
for scraper in scraper_names:
    subset = df[df['Scraper'] == scraper]
    success_counts = subset['Result'].value_counts()
    success_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, figsize=(8, 6))
    plt.title(f'Success Rate for {scraper}')
    plt.ylabel('')  # Hide the 'Result' ylabel
    plt.show()

# Individual URL Performance
plt.figure(figsize=(12, 7))
sns.boxplot(x='Scraper', y='Duration', data=df)
plt.title('Box Plot of Duration for Each Scraper')
plt.show()


