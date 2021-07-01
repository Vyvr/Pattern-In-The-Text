import matplotlib.pyplot as plt
import string, random

random.seed(random.randint(1, 1000000000)) # creating seed

counter_sunday = 0
counter_naive = 0
counter_KMP = 0

def matchesAt(T, p, W):
    global counter_naive
    global counter_sunday
    if (p+len(W)-1) >= len(T):
        print("searching word is bigger than text :(")
        return False
    for i in range(0, len(W)):
        counter_sunday += 1
        counter_naive += 1
        if W[i] != T[p+i]:
            return False
    return True


def naiveAlgorithm(T, W):
    report = []
    global counter_naive
    for p in range(0, len(T)-len(W)+1):
        counter_naive += 1
        if matchesAt(T, p, W):
            report.append(p)
    return report


def lastp(W, z):
    for i in reversed(range(0, len(W))):
        if z == W[i]:
            return i
    return -1


def sundayAlgorithm(T, W):
    report = []
    p = 0
    last_p = {}

    for value, key in enumerate(W):
        last_p[key] = value

    global counter_sunday
    while p <= len(T)-len(W):
        counter_sunday += 1
        if matchesAt(T, p, W):
            report.append(p)
        if p == len(T)-len(W):
            break
        z = T[p + len(W)]
        p = p + len(W) - last_p.get(z, -1)
    return report


def KMPPattern(W):  # returns KMP list of indexes
    indexing = [-1] * (len(W) + 1)
    pred = -1

    for i in range(1, len(W) + 1):
        while pred > -1 and W[pred] != W[i - 1]:
            pred = indexing[pred]

        pred += 1

        if i != len(W) and W[i] == W[pred]:
            indexing[i] = indexing[pred]
        else:
            indexing[i] = pred

    return indexing


def KMPAlgorithm(T, W):
    KMPPatternList = KMPPattern(W)
    b = 0
    patternsFound = []
    global counter_KMP
    for i, char_S in enumerate(T):
        counter_KMP += 1
        while b > -1 and W[b] != char_S:
            counter_KMP += 1
            b = KMPPatternList[b]
        b += 1
        if b == len(W):
            patternsFound.append(i - len(W) + 1)
            b = 0
    return patternsFound


def createText(text, alphabet, size, mode):
    if mode == 'append':
        for _ in range(size):
            text += alphabet[random.randint(0, 1000000) % len(alphabet)]
    elif mode == 'new':
        text = ''
        for _ in range(size):
            text += alphabet[random.randint(0, 1000000) % len(alphabet)]
    else:
        print('fun createText: wrong mode\nAvailable modes:\n-new --> new text\n-append --> appends new letter to exsisting text\n')
    return text


def createSearchedWord(text, size):
    if size >= len(text):
        modulo = len(text)
    else:
        modulo = len(text) - size
    random_starting_point = random.randint(0, 1000000) % (modulo)
    return text[random_starting_point : random_starting_point + size]


alphabet = string.ascii_letters + string.digits
T = ''
W = ''

speed_to_text_size_chart = False
speed_to_searched_word_size_chart = False
speed_to_alphabet_size_chart = True

if speed_to_text_size_chart:
    naive_counter_list = []
    sunday_counter_list = []
    kmp_counter_list = []
    text_length_list = []
    current_text_size = 0
    while current_text_size <= 1000:
        current_text_size += 1
        T = createText(T, alphabet, 1, 'append')
        W = createSearchedWord(T, 3)

        counter_naive, counter_sunday, counter_KMP = 0, 0, 0
        naiveAlgorithm(T, W)
        sundayAlgorithm(T, W)
        KMPAlgorithm(T, W)

        naive_counter_list.append(counter_naive)
        sunday_counter_list.append(counter_sunday)
        kmp_counter_list.append(counter_KMP)

        text_length_list.append(len(T))

    plt.title("Zależności między algorytmami szukającymi wzorca")
    plt.plot(text_length_list, naive_counter_list, 'green', label='Naive algorithm')
    plt.plot(text_length_list, sunday_counter_list, 'red', label='Sunday algorithm')
    plt.plot(text_length_list, kmp_counter_list, 'blue', label='KMP algorithm')
    plt.legend(loc='upper left')
    fig = plt.gcf()
    fig.set_size_inches(16, 9)
    fig.savefig('speed_to_text_size_chart.png', dpi=300)


if speed_to_searched_word_size_chart:
    naive_counter_list = []
    sunday_counter_list = []
    kmp_counter_list = []
    searched_word_length_list = []
    current_searched_size = 0
    T = createText(T, alphabet, 10_000, 'new')
    while current_searched_size <= 1_000:
        current_searched_size += 1
        W = createSearchedWord(T, current_searched_size)

        counter_naive, counter_sunday, counter_KMP = 0, 0, 0
        naiveAlgorithm(T, W)
        sundayAlgorithm(T, W)
        KMPAlgorithm(T, W)

        naive_counter_list.append(counter_naive)
        sunday_counter_list.append(counter_sunday)
        kmp_counter_list.append(counter_KMP)
        searched_word_length_list.append(len(W))

    plt.title("Zależności między algorytmami szukającymi wzorca")
    plt.plot(searched_word_length_list, naive_counter_list, 'green', label='Naive algorithm')
    plt.plot(searched_word_length_list, sunday_counter_list, 'red', label='Sunday algorithm')
    plt.plot(searched_word_length_list, kmp_counter_list, 'blue', label='KMP algorithm')
    plt.legend(loc='upper left')
    fig = plt.gcf()
    fig.set_size_inches(16, 9)
    fig.savefig('speed_to_searched_word_size_chart.png', dpi=300)


if speed_to_alphabet_size_chart:
    naive_counter_list = []
    sunday_counter_list = []
    kmp_counter_list = []
    alphabet_length_list = []
    current_alphabet_size = 20

    while current_alphabet_size <= len(alphabet):
        current_alphabet_size += 1
        current_alphabet = alphabet[0 : current_alphabet_size]

        T = createText(T, alphabet, 500, 'new')
        W = createSearchedWord(T, 5)

        counter_naive, counter_sunday, counter_KMP = 0, 0, 0
        naiveAlgorithm(T, W)
        sundayAlgorithm(T, W)
        KMPAlgorithm(T, W)

        naive_counter_list.append(counter_naive)
        sunday_counter_list.append(counter_sunday)
        kmp_counter_list.append(counter_KMP)
        alphabet_length_list.append(len(current_alphabet))

    plt.title("Zależności między algorytmami szukającymi wzorca")
    plt.plot(alphabet_length_list, naive_counter_list, 'green', label='Naive algorithm')
    plt.plot(alphabet_length_list, sunday_counter_list, 'red', label='Sunday algorithm')
    plt.plot(alphabet_length_list, kmp_counter_list, 'blue', label='KMP algorithm')
    plt.legend(loc='upper left')
    fig = plt.gcf()
    fig.set_size_inches(16, 9)
    fig.savefig('speed_to_alphabet_size_chart.png', dpi=300)