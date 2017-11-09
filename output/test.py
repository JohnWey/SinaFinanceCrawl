wordlist = [l.split(" ") for l in open('file1.txt', 'r')]
fd = open('file2.txt', 'w')
for line in zip(*wordlist): 
    fd.write(' '.join(line) + '\n')
    fd.close()