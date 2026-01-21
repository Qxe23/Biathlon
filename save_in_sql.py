from sqlalchemy import create_engine
import pandas as pd

# Step 1: Connect to PostgreSQL
username = "postgres"      # default user
password = "PostgreSQL"              # the password you set during installation
host = "localhost"         # if running locally
port = "5432"              # default PostgreSQL port
database = "biathlon"    # the database you created earlier

engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")


# Step 2: Load the DataFrame into PostgreSQL
table_name = "results_2122"
df = pd.read_csv("all_races_2122.csv")
df.to_sql(table_name, engine, if_exists="replace", index=False)

print(f"✅ Data successfully loaded into table '{table_name}' in database '{database}'.")