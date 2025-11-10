# author : @nlkguy

import os, json, subprocess
from datetime import datetime, timedelta



"""

    1 - get text , turn it to list
    2 - for each char in list , get the 7x7 grid
            get_char_grid() 
                returns a dict/list of char grids
    3 - combine the char grids into a full grid 7x49
            combine_char_grids()
                returns full 7x49 grid of text
    4 - transpose the full_text_grid to github grid
            transpose_to_gh()
                return the gh_grid
    5 - commitment is a huge thing

"""


alph_codes = {
    "A" : [10,16,18,22,26,29,30,31,32,33,36,40],
    "B" : [8,9,10,11,15,19,22,24,25,26,29,33,36,37,38,39],
    "C" : [9,10,11,12,15,22,29,37,38,39,40],
    "D" : [8,9,10,15,18,22,26,29,32,36,37,38],
    "E" : [8,9,10,11,12,15,22,23,24,25,29,36,37,38,39,40],
    "F" : [8,9,10,11,12,15,22,23,24,25,29,36],
    "G" : [9,10,11,12,15,22,24,25,26,29,33,37,38,39],
    "H" : [8,12,15,19,22,23,24,25,26,29,33,36,40],
    "I" : [9,10,11,17,24,31,37,38,39],
    "J" : [8,9,10,11,12,17,24,31,36,37,38],
    "K" : [8,11,12,15,17,22,23,29,31,36,39,40],
    "L" : [8,15,22,29,36,37,38,39,40],
    "M" : [8,12,15,16,18,19,22,24,26,29,33,36,40],
    "N" : [8,12,15,16,19,22,24,26,29,32,33,36,40],
    "O" : [9,10,11,15,19,22,26,29,33,37,38,39],
    "P" : [8,9,10,11,15,19,22,23,24,25,26,29,36],
    "Q" : [9,10,11,15,19,22,26,29,32,37,38,40],
    "R" : [8,9,10,11,15,19,22,23,24,25,29,32,36,40],
    "S" : [8,9,10,11,12,15,22,23,24,25,26,33,36,37,38,39,40],
    "T" : [8,9,10,11,12,17,24,31,38],
    "U" : [8,12,15,19,22,26,29,33,37,38,39],
    "V" : [8,12,15,19,22,26,30,32,38],
    "W" : [8,12,15,17,19,22,24,26,29,30,32,33,36,40],
    "X" : [8,12,16,18,24,30,32,36,40],
    "Y" : [8,12,16,18,24,31,38],
    "Z" : [8,910,11,1218,24,30,36,37,38,39,40],
    "1" : [10,16,17,24,31,37,38,39],
    "2" : [],
    "3" : [],
    "4" : [],
    "5" : [],
    "6" : [],
    "7" : [],
    "8" : [],
    "9" : [],
    "0" : []
}


# helper functions
# find next sunday to start grid fresh @ 0
    # add padding logic ode later
def next_sunday(date):
    wd = date.weekday()
    return date if wd == 6 else date + timedelta(days=(6 - wd))

# check if commits folder exists
def commits_dir():
    if not os.path.exists("commits"):
        os.makedirs("commits")

# manage liberal arts history major and find a job in mcD
def append_history(artname, savepoint_commit, start_date):
    entry = {
        "name": artname,
        "savepoint": savepoint_commit,
        "start_date": start_date,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    if os.path.exists("history.json"):
        hist = json.load(open("history.json"))
    else:
        hist = []

    hist.append(entry)
    json.dump(hist, open("history.json", "w"), indent=4)

# todo : create helpers  to manage history
# todo : menu for delete/restore commits


# major functions 

# convert alph code into 7x7 array grid
def conv_alph(alph):
    char_3d, ln = [], []
    for i in range(49):
        ln.append(1 if i in alph else 0)
        if (i + 1) % 7 == 0:
            char_3d.append(ln)
            ln = []
    return char_3d

"""
0	1	2	3	4	5	6
7	8	9	10	11	12	13
14	15	16	17	18	19	20
21	22	23	24	25	26	27
28	29	30	31	32	33	34
35	36	37	38	39	40	41
42	43	44	45	46	47	48
"""

# stich all the characters into single 7x49 grid
# gh is 7x53 , leave 4 ass padding - thefo - 7x7x7
def stich_grid(char_list):
    full = [[0 for _ in range(53)] for _ in range(7)]
    col_offset = 0
    for char_grid in char_list:
        for r in range(7):
            for c in range(7):
                if col_offset + c < 53:
                    full[r][col_offset + c] = char_grid[r][c]
        col_offset += 7
    return full


# generate commits based on the grid 0-1
def commitment(gh_grid, start_date_str):
    commits_dir()

    start_date = next_sunday(datetime.strptime(start_date_str, "%Y-%m-%d"))
    print("commits starts on sunday:", start_date.date())

    for col in range(53):
        for row in range(7):
            if gh_grid[row][col] == 0:
                continue

            days_offset = col * 7 + row
            commit_date = start_date + timedelta(days=days_offset)
            ds = commit_date.strftime("%Y-%m-%d")

            filename = f"commits/{ds}.txt"
            subprocess.run(["bash", "-c", f"echo 'Commit {ds}' > '{filename}'"])
            subprocess.run(["git", "add", filename], check=True)

            env = dict(os.environ)
            env["GIT_AUTHOR_DATE"] = f"{ds} 12:00:00"
            env["GIT_COMMITTER_DATE"] = f"{ds} 12:00:00"

            subprocess.run(
                ["git", "commit", "-m", f"commit for {ds}"],
                env=env,
                check=True
            )

            print("commits done succesfully", ds)
    
    subprocess.run(["git", "push","--force"], check=True)
    # force commit to deal with simple co


##############################################################


def main():
    text = input("Text: ").strip()
    if not text:
        print("Empty input. Abort.")
        return

    # checkpoint commit - to log the hash
    savepoint_msg = f"[SAVEPOINT] ART:{text}"
    subprocess.run(["git", "commit", "--allow-empty", "-m", savepoint_msg], check=True)
    savepoint_hash = (
        subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    )
    print("savepoint:", savepoint_hash)
    # save into file - hisory
    start_date = input("Start date (YYYY-MM-DD): ").strip()
    append_history(text, savepoint_hash, start_date)

    # generate character grids 
    # shorten from double loop
    char_grids = [conv_alph(alph_codes[c.upper()]) for c in text]
    stitched = stich_grid(char_grids)

    # print preview in full grid
    for r in stitched:
        print("".join("X" if x else " " for x in r))

    # commitment
    commitment(stitched, start_date)


    print(f"""    
        $ git reset --hard {savepoint_hash}
        $ delete commits
        $ cleanup commit
        """)

# -------------------------------

if __name__ == "__main__":
    main()
