from langchain_agent import load_data  # replace with your actual script/module filename

#  Load merged dataframe from MongoDB + MySQL
merged_df = load_data()

# Print available columns to verify correct names
print(" Available columns in merged_df:", merged_df.columns.tolist())

#  Print first 10 rows as sample data check
print("\n First 10 rows of merged dataframe:")
print(merged_df.head(10))

#  Check portfolio value per relationship manager (dynamic column detection)
print("\n Portfolio value per relationship manager:")
if "relationship_manager_y" in merged_df.columns:
    print(merged_df.groupby("relationship_manager_y")["value"].sum())
elif "relationship_manager_x" in merged_df.columns:
    print(merged_df.groupby("relationship_manager_x")["value"].sum())
else:
    print("❌ No relationship manager column found in dataframe.")

#  Check top 5 portfolios by total value for validation
print("\n Top 5 portfolios by value:")
print(merged_df.groupby("client_name")["value"].sum().sort_values(ascending=False).head(5))
