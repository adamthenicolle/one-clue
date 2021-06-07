## I owe so much to Brooke Husic and Adam Aaronson for teaching me code and helping me with this script

import sys
import re

cfp_lines = []
cfp_file = open("/Users/steven/Desktop/CROSSWORDS ORGANIZED/LUCKYSTREAK PLUS/REDSTONE SECOND PACKL/SQUISHMALLOWS.cfp",encoding="utf-8").readlines()
end_file = "/Users/steven/Desktop/CROSSWORDS ORGANIZED/LUCKYSTREAK PLUS/REDSTONE SECOND PACKL/SQUISHMALLOWS.txt"
for line in cfp_file:
    line_no_n = line.replace("\n", "")
    cfp_lines.append(line_no_n)

# getting puzzle title
for line in cfp_lines:
    if "<TITLE" in line:
        result = re.search(r">.*<", line)
        title_with_brackets = result.group(0)
        puzzle_title = title_with_brackets.replace("<", "").replace(">", "")

# getting author
for line in cfp_lines:
    if "<AUTHOR" in line:
        result = re.search(r">.*<", line)
        author_with_brackets = result.group(0)
        puzzle_author = author_with_brackets.replace("<", "").replace(">", "")

# getting copyright
for line in cfp_lines:
    if "<COPYRIGHT" in line:
        result = re.search(r">.*<", line)
        copyright_with_brackets = result.group(0)
        puzzle_copyright = copyright_with_brackets.replace("<", "").replace(">", "")

# getting grid width
for line in cfp_lines:
    if "<GRID width" in line:
        result = re.search(r"<GRID width=\".*\">", line)
        width_with_brackets = result.group(0)
        grid_width = int(width_with_brackets.replace("<GRID width=\"", "").replace("\">", ""))

this_is_a_grid_entry = False
this_is_an_across_clue = False
this_is_a_down_clue = False
grid_entries = []
across_clues = []
down_clues = []

for line in cfp_lines:
    if "</GRID>" in line:
        this_is_a_grid_entry = False
    if "dir=\"DOWN\"" in line:
        this_is_an_across_clue = False
    if "</WORDS>" in line:
        this_is_a_down_clue = False

    if this_is_a_grid_entry and len(line) > 0:
        grid_entries.append(line)

    if "dir=\"ACROSS\"" in line:
        across_clues.append(line)
        this_is_an_across_clue = True
    elif "dir=\"DOWN\"" in line:
        this_is_a_down_clue = True
        down_clues.append(line)
    elif line == "<GRID width=\"15\">":
        this_is_a_grid_entry = True

    # sanity checking
    if this_is_an_across_clue == True and this_is_a_down_clue == True:
        raise RuntimeError('This shouldnt happen')
    if this_is_a_grid_entry == True and this_is_a_down_clue == True:
        raise RuntimeError('This shouldnt happen')
    if this_is_a_grid_entry == True and this_is_a_down_clue == True:
        raise RuntimeError('This shouldnt happen')


grid_height = int(len(grid_entries))

across_clue_numbers_raw = []
across_clue_numbers = []
for line in across_clues:
    result = re.search(r"num=\".*\"", line)
    clue_number_with_brackets = result.group(0)
    clue_number_no_brackets = clue_number_with_brackets.replace("num=\"", "").replace("\"", "")
    across_clue_numbers_raw.append(clue_number_no_brackets)
for line in across_clue_numbers_raw:
    if ">" in line:
        get_the_number = line.split(">")
        across_clue_numbers.append(get_the_number[0])
    else:
        across_clue_numbers.append(line)

across_just_clues = []
for line in across_clues:
    result = re.search(r">.*<", line)
    clue_with_brackets = result.group(0)
    clue_no_brackets = clue_with_brackets.replace("<", "").replace(">", "")
    across_just_clues.append(clue_no_brackets)

down_clue_numbers_raw = []
down_clue_numbers = []
for line in down_clues:
    result = re.search(r"num=\".*\"", line)
    down_clue_number_with_brackets = result.group(0)
    down_clue_number_no_brackets = down_clue_number_with_brackets.replace("num=\"", "").replace("\"", "")
    down_clue_numbers_raw.append(down_clue_number_no_brackets)
for line in down_clue_numbers_raw:
    if ">" in line:
        get_the_number = line.split(">")
        down_clue_numbers.append(get_the_number[0])
    else:
        down_clue_numbers.append(line)

down_just_clues = []
for line in down_clues:
    result = re.search(r">.*<", line)
    clue_with_brackets = result.group(0)
    clue_no_brackets = clue_with_brackets.replace("<", "").replace(">", "")
    down_just_clues.append(clue_no_brackets)

across_words = []
for line in grid_entries:
    row_words = line.split(".")
    number_of_black_squares = line.count(".") + 1
    for i in range(number_of_black_squares):
        if len(row_words[i]) == 0:
            continue
        across_words.append(row_words[i])

across_dictionary = dict(zip(across_words, across_just_clues))

def parsedowns(grid_entries):
    rows = len(grid_entries)
    cols = len(grid_entries[0])

    downs = []

    
    for row in range(rows):
        for col in range(cols):
            if grid_entries[row][col] != '.' and (row == 0 or grid_entries[row - 1][col] == '.'):
                newword = grid_entries[row][col]
                letterrow = row + 1
                while letterrow < rows and grid_entries[letterrow][col] != '.':
                    newword += grid_entries[letterrow][col]
                    letterrow += 1
                downs.append(newword)

    return downs

down_words = parsedowns(grid_entries)
down_dictionary = dict(zip(down_words, down_just_clues))

clues_and_words = []
clues_and_words.append("Across")
for line in across_words:
    clues_and_words.append(line + "\t" + across_dictionary[line])
clues_and_words.append("Down")
for line in down_words:
    clues_and_words.append(line + "\t" + down_dictionary[line])

# # fuck yeah!!! now let's make files

# ## across lite txt file
# creates an across lite puz file
puz_txt = []
puz_txt.append("<ACROSS PUZZLE V2>")
puz_txt.append("<TITLE>")
puz_txt.append(puzzle_title)
puz_txt.append("<AUTHOR>")
puz_txt.append(puzzle_author)
puz_txt.append("<COPYRIGHT>")
puz_txt.append(puzzle_copyright)
puz_txt.append("<SIZE>")
puz_txt.append(str(grid_width) + "x" + str(grid_height))
puz_txt.append("<GRID>")
for line in grid_entries:
    puz_txt.append(line)
puz_txt.append("<ACROSS>")
for line in across_words:
    puz_txt.append(across_dictionary[line])
append = puz_txt.append("<DOWN>")
for line in down_words:
    puz_txt.append(down_dictionary[line])


ncw_txt = []
ncw_txt.append("Across")
for line in across_clue_numbers:
    across_clue_number = line
    for line in across_words:
        across_word = line
        ncw_txt.append(across_clue_number + "\t" + line + "\t" + across_dictionary[line])
    break

ncw_txt.append("Down")
for line in down_clue_numbers:
    down_clue_number = line
    for line in down_words:
        down_word = line
        ncw_txt.append(down_clue_number + "\t" + line + "\t" + down_dictionary[line])
    break

puz_txt = puz_txt
ncw = ncw_txt
clues_list = []

# for line in ncw:
#     if "\t" in line:
#         parts = line.split("\t")
#         clue_number = parts[0]
#         clue = parts[1]
#         entry = parts[2]
#         if clue == "":
#             pattern = sys.argv[1] if len(sys.argv) > 1 else input(entry)
#             newline = pattern, "\n"
#             # print(newline)
#             clues_list.append(newline)
#         else:
#             oldline = clue, "\n"
#             # print(oldline)
#             clues_list.append(oldline)
#     if "Down" in line:
#         nothing_line = "", "\n"
#         # print(nothing_line)
#         clues_list.append(nothing_line)


written_clues = []
written_clues_lines = clues_list
for line in written_clues_lines:
    if line == '\t\n':
        written_clues.append("")
        continue
    clue_parts = line.split('\n')
    clue_line = clue_parts[0]
    written_clues.append(clue_line)

pre_update = []
for line in puz_txt:
    puz_parts = line.split('\n')
    doc_line = puz_parts[0]
    pre_update.append(doc_line)

my_puz_file = {}
my_puz_file['title'] = pre_update[2]
my_puz_file['author'] = pre_update[4]
my_puz_file['copyright'] = pre_update[6]
my_puz_file['size'] = pre_update[8]

this_is_a_grid_entry = False
this_is_an_across_clue = False
this_is_a_down_clue = False
grid_entries = []
across_clues = []
down_clues = []

for line in pre_update:
    if line == '<ACROSS>':
        this_is_a_grid_entry = False
    if line == '<DOWN>':
        this_is_an_across_clue = False

    if this_is_a_grid_entry and len(line) > 0:
        grid_entries.append(line)
    if this_is_an_across_clue and len(line) > 0:
        across_clues.append(line)
    if this_is_a_down_clue and len(line) > 0:
        down_clues.append(line)

    if line == '<ACROSS>':
        this_is_an_across_clue = True
    elif line == '<DOWN>':
        this_is_a_down_clue = True
    elif line == '<GRID>':
        this_is_a_grid_entry = True

    # sanity checking
    if this_is_an_across_clue == True and this_is_a_down_clue == True:
        raise RuntimeError('This shouldnt happen')
    if this_is_a_grid_entry == True and this_is_a_down_clue == True:
        raise RuntimeError('This shouldnt happen')
    if this_is_a_grid_entry == True and this_is_a_down_clue == True:
        raise RuntimeError('This shouldnt happen')

my_puz_file['grid'] = grid_entries
my_puz_file['across'] = across_clues
my_puz_file['down'] = down_clues

are_we_across = True
new_across_clues = []
new_down_clues = []
for line in written_clues:
    if len(line) == 0:  # this is how we indicate the transition
        are_we_across = False
    if are_we_across == True and len(line) > 0:
        new_across_clues.append(line)
    if not are_we_across and len(line) > 0:
        new_down_clues.append(line)

if len(my_puz_file['across']) == len(new_across_clues):
    my_puz_file['across'] = new_across_clues
else:
    print('you did something wrong!')

if len(my_puz_file['down']) == len(new_down_clues):
    my_puz_file['down'] = new_down_clues
else:
    print('you did something wrong!')

with open(end_file,"w") as puz_final:
    puz_final.write('<ACROSS PUZZLE V2>\n')
    puz_final.write('<TITLE>\n')
    puz_final.write(my_puz_file['title'] + '\n')
    puz_final.write('<AUTHOR>\n')
    puz_final.write(my_puz_file['author'] + '\n')
    puz_final.write('<COPYRIGHT>\n')
    puz_final.write(my_puz_file['copyright'] + '\n')
    puz_final.write('<SIZE>\n')
    puz_final.write(my_puz_file['size'] + '\n')
    puz_final.write('<GRID>' + '\n')
    for grid_answer in my_puz_file['grid']:
        puz_final.write(grid_answer + '\n')
    puz_final.write('<ACROSS>' + '\n')
    for across_clue in my_puz_file['across']:
        puz_final.write(across_clue + '\n')
    puz_final.write('<DOWN>' + '\n')
    for down_clue in my_puz_file['down']:
        puz_final.write(down_clue + '\n')

print(puz_final)
