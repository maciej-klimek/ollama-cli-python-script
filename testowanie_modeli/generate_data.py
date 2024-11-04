import random
import string


def generate_random_text(lines, words_per_line):
    data = []
    for _ in range(lines):
        line = ' '.join(''.join(random.choices(string.ascii_letters + string.digits, k=5))
                        for _ in range(words_per_line))
        data.append(line)
    return '\n'.join(data)


file_sizes = {
    'data1.txt': (50, 8),   # 50 lines, 8 words per line
    'data2.txt': (500, 15),  # 500 lines, 15 words per line
    'data3.txt': (2000, 20)  # 2000 lines, 20 words per line
}

for filename, (lines, words_per_line) in file_sizes.items():
    with open(filename, 'w') as f:
        f.write(generate_random_text(lines, words_per_line))

print("Data files generated: data1.txt, data2.txt, data3.txt")
