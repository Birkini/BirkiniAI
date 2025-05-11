import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Database connection setup
DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///birkini.db")
engine = create_engine(DATABASE_URI)

def fetch_data(query: str) -> pd.DataFrame | None:
    """Execute SQL query and return the result as a DataFrame."""
    try:
        return pd.read_sql(query, engine)
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error fetching data: {e}")
    return None

def plot_data(data: pd.DataFrame, chart_type: str = "line", title: str = "Data Visualization", xlabel: str = "X", ylabel: str = "Y") -> None:
    """Plot data using seaborn with configurable chart types."""
    if data is None or data.empty:
        print("No data available for plotting.")
        return

    x_col, y_col = data.columns[:2]

    plt.figure(figsize=(10, 6))

    if chart_type == "line":
        sns.lineplot(x=x_col, y=y_col, data=data)
    elif chart_type == "bar":
        sns.barplot(x=x_col, y=y_col, data=data)
    elif chart_type == "scatter":
        sns.scatterplot(x=x_col, y=y_col, data=data)
    else:
        print(f"Unsupported chart type: {chart_type}")
        return

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    query = """
        SELECT date, revenue 
        FROM sales_data 
        WHERE date BETWEEN '2023-01-01' AND '2023-12-31'
    """
    data = fetch_data(query)
    plot_data(data, chart_type="line", title="Sales Revenue Over Time", xlabel="Date", ylabel="Revenue")

