import numpy as np
import math


class Library:

    def __init__(self, book_ids, max_books_scanned_per_day):
        self.book_ids = book_ids
        self.max_books_scanned_per_day = max_books_scanned_per_day

    def __repr__(self):
        return self.book_ids.__str__()


def sort_libraries_greedy(p=1):
    indices = set([i for i in range(len(libraries))])
    sort_indices = []
    d=0
    books_scanned = set()
    score = 0
    max_score = -math.inf
    signup_library = -1
    for x in indices:
        k = (D - d - libraries_signup_days[x])*libraries[x].max_books_scanned_per_day
        l_score = 0
        i=0
        while i < len(libraries[x].book_ids) and i < k:
            l_score += book_scores[libraries[x].book_ids[i]] #/ (books_frequencies[libraries[x].book_ids[i]])
            i+=1
        l_score /= (libraries_signup_days[x])**p
        if l_score > max_score:
            max_score = l_score
            signup_library = x
    indices.remove(signup_library)
    sort_indices.append(signup_library)
    signup_time = libraries_signup_days[signup_library]
    library_out = []

    while d<D:
        k = (D - d - signup_time)*libraries[signup_library].max_books_scanned_per_day
        i = 0
        s = 0
        library_out.append([signup_library,0,[]])
        while i < len(libraries[signup_library].book_ids) and s < k:
            if libraries[signup_library].book_ids[i] not in books_scanned:
                books_scanned.add(libraries[signup_library].book_ids[i])
                score += book_scores[libraries[signup_library].book_ids[i]]
                library_out[L - len(indices) - 1][1]+=1
                library_out[L - len(indices) - 1][2].append(libraries[signup_library].book_ids[i])
                s+=1
            i+=1


        d+=signup_time
        
        if len(indices) > 0:
            max_score = 0
            signup_library = -1
            for x in indices:
                k = (D - d - libraries_signup_days[x])*libraries[x].max_books_scanned_per_day
                l_score = 0
                i=0
                s=0
                while i < len(libraries[x].book_ids) and s < k:
                    if libraries[x].book_ids[i] not in books_scanned:
                        l_score += book_scores[libraries[x].book_ids[i]] #/ (books_frequencies[libraries[x].book_ids[i]])
                        s+=1
                    i+=1
                l_score /= (libraries_signup_days[x])**p
                if l_score > max_score:
                    max_score = l_score
                    signup_library = x
            if signup_library == -1:
                sort_indices += list(indices)
                break
            signup_time = libraries_signup_days[signup_library]
            sort_indices.append(signup_library)
            indices.remove(signup_library)
            print('libraries left unsorted',' '*(6 - len(str(len(indices)))),len(indices),end='\r')
        else:
            break

    print()
    print('total score',score)
    with open(filename+"_out.txt","w+") as f:
        f.write(str(len(library_out))+"\n")
        for line in library_out:
            f.write(str(line[0])+" "+str(line[1])+"\n")
            f.write(' '.join(map(str, line[2]))+"\n")

    return sort_indices


filename = "c_incunabula"
file = filename+'.txt'

with open(file, "r") as f:
    content = f.read().splitlines()
print(file)
B, L, D = list(map(int, content[0].split(' ')))

book_scores = np.array(list(map(int, content[1].split(' '))))
pos = 1

libraries_signup_days = np.zeros(L)

libraries = []


for i in range(L):
    pos += 1
    n, t, m = list(map(int, content[pos].split(' ')))
    libraries_signup_days[i] = t
    pos += 1
    book_ids = np.array(list(map(int, content[pos].split(' '))))
    libraries.append(Library(book_ids, m))

for i in range(L):
    libraries[i].book_ids = np.array(sorted(libraries[i].book_ids, key = lambda x: -book_scores[x]),dtype=int)

for p in [0.95]:
    greedy_permutation = sort_libraries_greedy(p)
