import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sqlalchemy import create_engine

# Database URI
DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///birkini.db')
engine = create_engine(DATABASE_URI)

def fetch_data(query):
    """Fetch data from the database using SQL query."""
    try:
        data = pd.read_sql(query, engine)
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def plot_data(data, chart_type='line', title='Data Visualization', xlabel='X-Axis', ylabel='Y-Axis'):
    """Generate visualizations based on the data."""
    if data is None:
        print("No data to plot.")
        return
    
    plt.figure(figsize=(10, 6))
    
    if chart_type == 'line':
        sns.lineplot(x=data.iloc[:, 0], y=data.iloc[:, 1], data=data)
    elif chart_type == 'bar':
        sns.barplot(x=data.iloc[:, 0], y=data.iloc[:, 1], data=data)
    elif chart_type == 'scatter':
        sns.scatterplot(x=data.iloc[:, 0], y=data.iloc[:, 1], data=data)
    else:
        print("Unsupported chart type.")
        return
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    query = "SELECT date, revenue FROM sales_data WHERE date BETWEEN '2023-01-01' AND '2023-12-31'"
    data = fetch_data(query)
    
    if data is not None:
        plot_data(data, chart_type='line', title='Sales Revenue Over Time', xlabel='Date', ylabel='Revenue')
