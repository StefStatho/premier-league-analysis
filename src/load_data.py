
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Find the project folder and the CSV file
project_dir = Path(__file__).resolve().parent.parent
data_path = project_dir / "data" / "raw" / "E0.csv"

# Load the CSV into a pandas DataFrame
df = pd.read_csv(data_path, encoding="utf-8-sig")

# Display the first 5 rows
print(df.head())

print("\nDataset dimensions:")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist()[:20])

print("\nMissing values in the first 10 columns:")
print(df.isnull().sum().head(10))

# Calculate total goals scored by each team

home_goals = df.groupby("HomeTeam")["FTHG"].sum()
away_goals = df.groupby("AwayTeam")["FTAG"].sum()

total_goals = home_goals.add(away_goals, fill_value=0)

# Display the top 10 teams by goals scored
top_scorers = total_goals.sort_values(ascending=False).head(10)

print("\nTop 10 teams by total goals:")
print(top_scorers)

print("\nTotal goals in the entire league:")

league_goals = df["FTHG"].sum() + df["FTAG"].sum()

print(league_goals)

# Calculate goals conceded by each team
home_conceded = df.groupby("HomeTeam")["FTAG"].sum()
away_conceded = df.groupby("AwayTeam")["FTHG"].sum()

# Calculate total goals conceded
total_conceded = home_conceded.add(away_conceded, fill_value=0)

# Create a team statistics table
team_stats = pd.DataFrame({
    "Goals Scored": total_goals,
    "Goals Conceded": total_conceded
})

# Calculate goal difference
team_stats["Goal Difference"] = (
    team_stats["Goals Scored"] - team_stats["Goals Conceded"]
)

print("\nTeam Statistics - Top 10 by Goals Scored:")
print(team_stats.sort_values("Goals Scored", ascending=False).head(10))


# Check missing values in important match columns
important_columns = [
    "Date",
    "HomeTeam",
    "AwayTeam",
    "FTHG",
    "FTAG",
    "FTR"
]

missing_values = df[important_columns].isnull().sum()

print("\nMissing values in important columns:")
print(missing_values)

# Check for duplicate matches
duplicate_matches = df.duplicated(
    subset=["Date", "HomeTeam", "AwayTeam"]
).sum()

print("\nDuplicate matches:")
print(duplicate_matches)


# Check for invalid negative goal values
negative_home_goals = (df["FTHG"] < 0).sum()
negative_away_goals = (df["FTAG"] < 0).sum()

print("\nNegative home goals:", negative_home_goals)
print("Negative away goals:", negative_away_goals)

# Calculate matches by each team
home_matches = df["HomeTeam"].value_counts()
away_matches = df["AwayTeam"].value_counts()

matches_played = home_matches.add(
    away_matches, fill_value=0
).astype(int)

print("\nMatches played by each team:")
print(matches_played.sort_values)


# Calculate wins, draws, and losses

# Wins at home and away
home_wins = df[df["FTR"] == "H"].groupby("HomeTeam").size()
away_wins = df[df["FTR"] == "A"].groupby("AwayTeam").size()
wins = home_wins.add(away_wins, fill_value=0).astype(int)

# Draws at home and away
home_draws = df[df["FTR"] == "D"].groupby("HomeTeam").size()
away_draws = df[df["FTR"] == "D"].groupby("AwayTeam").size()
draws = home_draws.add(away_draws, fill_value=0).astype(int)

# Losses at home and away
home_losses = df[df["FTR"] == "A"].groupby("HomeTeam").size()
away_losses = df[df["FTR"] == "H"].groupby("AwayTeam").size()
losses = home_losses.add(away_losses, fill_value=0).astype(int)

# Add results to the team statistics table
team_stats["Wins"] = wins
team_stats["Draws"] = draws
team_stats["Losses"] = losses

# Calculate league points
team_stats["Points"] = team_stats["Wins"] * 3 + team_stats["Draws"]

# Display the top 10 teams by points
print("\nTop 10 teams by points:")
print(team_stats.sort_values("Points", ascending=False).head(10))

#Validate match result for every team
total_results = (
    team_stats["Wins"]
   +team_stats["Draws"]
   +team_stats["Losses"]

)

print("\nDo results add up to 38 matches for every team?")
print((total_results==matches_played).all())

#Calculate win percentage for each team
team_stats["Win Percentage"] = (
    team_stats["Wins"] / matches_played * 100
).round(2)

#Display the top 10 teams by points
print("\nTop 10 teams by points with wint percentage:")
print(
    team_stats.sort_values("Points", ascending=False)[
        ["Wins","Draws","Losses","Points","Win Percentage"]
    ].head(10)
)
      

# Save the complete team statistics
output_path = project_dir / "data" / "processed" / "team_stats.csv"

team_stats.sort_values(
    "Points",
    ascending=False
).to_csv(output_path, index=True)

print(f"\nUpdated team statistics saved to: {output_path}")


# Display the 10 teams that conceded the fewest goals
print("\nTop 10 teams by fewest goals conceded:")

print(
    team_stats.sort_values(
        "Goals Conceded",
        ascending=True
    )[["Goals Conceded", "Goals Scored", "Goal Difference"]].head(10)
)


# Display the top 5 teams by goal difference
print("\nTop 5 teams by goal difference:")

print(
    team_stats.sort_values(
        "Goal Difference",
        ascending=False
    )[["Goals Scored", "Goals Conceded", "Goal Difference"]].head(5)
)


# Save the complete team statistics to a CSV file
output_path = project_dir / "data" / "processed" / "team_stats.csv"

team_stats.sort_values(
    "Points",
    ascending=False
).to_csv(output_path, index=True)

print(f"\nUpdated team statistics saved to: {output_path}")



# Create a bar chart of the top 10 teams by points
top_10_points = team_stats.sort_values(
    "Points",
    ascending=False
).head(10)

plt.figure(figsize=(10, 6))


bars = plt.bar(
    top_10_points.index,
    top_10_points["Points"]
)

plt.bar_label(bars, padding=3)


plt.title("Top 10 Premier League Teams by Points (2024-25)")
plt.xlabel("Team")
plt.ylabel("Points")
plt.xticks(rotation=45)
plt.tight_layout()

# Save the chart as a PNG image
chart_path = project_dir / "images" / "top_10_teams_by_points.png"
plt.savefig(chart_path, dpi=300, bbox_inches="tight")

plt.show()
