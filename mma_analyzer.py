from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = Path(__file__).resolve().parent / "fighters.csv"

def load_data():
    df = pd.read_csv(DATA_FILE)
    df["name"] = df["first_name"] + " " + df["last_name"]
    df["total_fights"] = df["wins"] + df["losses"] + df["draws"]
    df["win_rate"] = df["wins"] / df["total_fights"] * 100
    df["finish_rate"] = (df["ko_wins"] + df["submission_wins"]) / df["wins"] * 100
    df["ko_rate"] = df["ko_wins"] / df["wins"] * 100
    df["sub_rate"] = df["submission_wins"] / df["wins"] * 100
    df["score"] = df["win_rate"] * .5 + df["finish_rate"] * .3 + df["ko_rate"] * .1 + df["sub_rate"] * .1
    return df.fillna(0)

def search_fighter(df):
    text = input("\nSearch fighter: ").strip().lower()
    matches = df[df["name"].str.lower().str.contains(text, na=False)]
    if matches.empty:
        print("No fighters found.")
        return None
    print("\nMatches:")
    for i, name in enumerate(matches["name"], 1):
        print(f"{i}. {name}")
    choice = input("Choose a fighter number: ")
    try:
        return matches.iloc[int(choice)-1]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return None

def show_profile(f):
    print("\n" + "="*42)
    print(f["name"].upper())
    print("="*42)
    print(f"Division:       {f['weight_class']}")
    print(f"Record:         {int(f['wins'])}-{int(f['losses'])}-{int(f['draws'])}")
    print(f"Reach:          {f['reach_in']:.1f} in")
    print(f"Stance:         {f['stance']}")
    print(f"Win Rate:       {f['win_rate']:.1f}%")
    print(f"Finish Rate:    {f['finish_rate']:.1f}%")
    print(f"KO Rate:        {f['ko_rate']:.1f}%")
    print(f"Submission Rate: {f['sub_rate']:.1f}%")
    print(f"Overall Score:  {f['score']:.1f}")

def compare(df):
    print("\nFIGHTER 1")
    a = search_fighter(df)
    if a is None: return
    print("\nFIGHTER 2")
    b = search_fighter(df)
    if b is None: return

    labels = ["Win Rate", "Finish Rate", "KO Rate", "Submission Rate"]
    av = [a["win_rate"], a["finish_rate"], a["ko_rate"], a["sub_rate"]]
    bv = [b["win_rate"], b["finish_rate"], b["ko_rate"], b["sub_rate"]]

    x = range(len(labels))
    width = .38
    plt.figure(figsize=(9,5))
    plt.bar([i-width/2 for i in x], av, width, label=a["name"])
    plt.bar([i+width/2 for i in x], bv, width, label=b["name"])
    plt.xticks(list(x), labels)
    plt.ylabel("Percentage")
    plt.title(f"{a['name']} vs {b['name']}")
    plt.ylim(0, max(max(av), max(bv)) + 15)
    plt.legend()
    plt.tight_layout()
    plt.show(block=False)

    print(f"\nOverall score: {a['name']} {a['score']:.1f} | {b['name']} {b['score']:.1f}")
    winner = a if a["score"] > b["score"] else b if b["score"] > a["score"] else None
    print("Statistical advantage:", winner["name"] if winner is not None else "Tie")

def top_fighters(df):
    top = df.sort_values("score", ascending=False).head(10)
    print("\nTOP 10 BY CUSTOM SCORE")
    print("-"*42)
    for i, (_, f) in enumerate(top.iterrows(), 1):
        print(f"{i:2}. {f['name']:<22} {f['score']:.1f}")

def division_chart(df):
    avg = df.groupby("weight_class")["score"].mean().sort_values()
    plt.figure(figsize=(10,6))
    avg.plot(kind="barh")
    plt.xlabel("Average Custom Score")
    plt.title("Average Fighter Score by Weight Class")
    plt.tight_layout()
    plt.show(block=False)

def main():
    df = load_data()

    while True:
        print("\n" + "="*42)
        print("       MMA FIGHTER ANALYTICS")
        print("="*42)
        print("1. Search fighter")
        print("2. Compare two fighters")
        print("3. Top 10 fighters")
        print("4. Weight-class chart")
        print("5. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            fighter = search_fighter(df)
            if fighter is not None:
                show_profile(fighter)
        elif choice == "2":
            compare(df)
        elif choice == "3":
            top_fighters(df)
        elif choice == "4":
            division_chart(df)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
