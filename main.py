import math
from collections import Counter
import matplotlib.pyplot as plt


def file_open(name):
    data = []
    with open(name, 'r') as f:
        data = f.readlines()

    for i in range(len(data)):
        data[i] = data[i].strip().split(',')

    for d in data:
        for i in range(len(d) - 1):
            d[i] = float(d[i])

    return data


def knn(k, test, train):
    distances = []

    for t in train:
        train_v = t[:-1]  # cechy
        label = t[-1]     # klasa

        distance = 0
        for i in range(len(train_v)):
            distance += (train_v[i] - test[i]) ** 2

        distance = math.sqrt(distance)

        distances.append((distance, label))

    distances.sort(key=lambda x: x[0])

    return distances[:k]


def commonest(k, test, train):
    nearest = knn(k, test, train)
    # print(nearest)
    labels = [nearest[i][1] for i in range(len(nearest))]
    counter = Counter(labels)

    return counter.most_common(1)[0][0]


def accuracy(k, test, train):
    points = 0
    for test_v in test:
        if test_v[-1] == commonest(k, test_v[:-1], train):
            points += 1
            # print(points, test_v, commonest(k, test_v[:-1], train))
    return points / len(test)


def looped(train):
    print("User input mode")
    print("Input template <k>[space]<vector>. Example: 3 1,2,3,4. To end type 'exit'.")
    while True:
        user = input(": ")
        if user.lower() == "exit" or user == "":
            break
        else:
            user = user.split()
            user_k = int(user[0])
            user_v = user[1].split(',')
            user_v = list(map(int, user_v))
            # print(user, user_k, user_v)
            print(commonest(user_k, user_v, train))


def k_dependence(n, test, train):
    acc_result = [accuracy(i, test, train) for i in range(1, n + 1)]
    plt.plot([i for i in range(1, n + 1)], acc_result)

    plt.title("K-dependence")
    plt.xlabel("k")
    plt.ylabel("accuracy")
    plt.grid()

    plt.show()


def main():
    # import files

    train = file_open("wdbc.data")
    test = file_open("wdbc.test.data")

    # Accuracy
    print("Accuracy k=3:", accuracy(3, test, train))

    # User input
    looped(train)

    # Plot
    k_dependence(11, test, train)

if __name__ == "__main__":
    main()