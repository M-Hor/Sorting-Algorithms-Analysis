import random
import time
import csv
import matplotlib.pyplot as plt

class SortStats:
    def __init__(self):
        self.time_ms = 0.0
        self.comparisons = 0
        self.swaps = 0
        self.merges = 0
        self.pivots = []
        self.shell_gaps = []
    def reset(self):
        self.time_ms = 0.0
        self.comparisons = 0
        self.swaps = 0
        self.merges = 0
        self.pivots.clear()
        self.shell_gaps.clear()

def bubble_sort(arr, stats):
    start_time = time.perf_counter()
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            stats.comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                stats.swaps += 1
    stats.time_ms = (time.perf_counter() - start_time) * 1000
    return arr

def shell_sort_bubble(arr, stats):
    start_time = time.perf_counter()
    n = len(arr)
    gaps = [1]
    k = 1
    while True:
        gap = (2 ** k) + 1
        if gap >= n: break
        gaps.append(gap)
        k += 1
    for gap in reversed(gaps):
        stats.shell_gaps.append(gap)
        for i in range(n):
            for j in range(0, n - gap):
                stats.comparisons += 1
                if arr[j] > arr[j + gap]:
                    arr[j], arr[j + gap] = arr[j + gap], arr[j]
                    stats.swaps += 1
    stats.time_ms = (time.perf_counter() - start_time) * 1000
    return arr

def merge_sort_wrapper(arr, stats):
    start_time = time.perf_counter()
    sorted_arr = merge_sort(arr, stats)
    stats.time_ms = (time.perf_counter() - start_time) * 1000
    return sorted_arr

def merge_sort(arr, stats):
    if len(arr) <= 1: return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], stats)
    right = merge_sort(arr[mid:], stats)
    return merge(left, right, stats)

def merge(left, right, stats):
    stats.merges += 1
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        stats.comparisons += 1
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def heapify(arr, n, i, stats):
    largest = i
    l, r = 2 * i + 1, 2 * i + 2
    if l < n:
        stats.comparisons += 1
        if arr[i] < arr[l]: largest = l
    if r < n:
        stats.comparisons += 1
        if arr[largest] < arr[r]: largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        stats.swaps += 1
        heapify(arr, n, largest, stats)

def heap_sort(arr, stats):
    start_time = time.perf_counter()
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1): heapify(arr, n, i, stats)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        stats.swaps += 1
        heapify(arr, i, 0, stats)
    stats.time_ms = (time.perf_counter() - start_time) * 1000
    return arr

def quick_sort_recursive_wrapper(arr, stats):
    start_time = time.perf_counter()
    sorted_arr = quick_sort_recursive(arr, stats)
    stats.time_ms = (time.perf_counter() - start_time) * 1000
    return sorted_arr

def quick_sort_recursive(arr, stats):
    if len(arr) <= 1: return arr
    pivot = random.choice(arr)
    stats.pivots.append(pivot)
    stats.comparisons += len(arr)
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort_recursive(left, stats) + middle + quick_sort_recursive(right, stats)

def get_median_pivot(arr, low, high, stats):
    mid = (low + high) // 2
    candidates = [(arr[low], low), (arr[mid], mid), (arr[high], high)]
    stats.comparisons += 3
    candidates.sort()
    return candidates[1][1]

def quick_sort_iterative(arr, stats):
    start_time = time.perf_counter()
    size = len(arr)
    stack = [(0, size - 1)]
    while stack:
        low, high = stack.pop()
        if low < high:
            p_idx = get_median_pivot(arr, low, high, stats)
            arr[p_idx], arr[high] = arr[high], arr[p_idx]
            stats.swaps += 1
            pivot = arr[high]
            stats.pivots.append(pivot)
            i = low - 1
            for j in range(low, high):
                stats.comparisons += 1
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    stats.swaps += 1
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            stats.swaps += 1
            p = i + 1
            stack.append((low, p - 1))
            stack.append((p + 1, high))
    stats.time_ms = (time.perf_counter() - start_time) * 1000
    return arr

def generacja_ciagu(n, typ):
    max_value = n * 10
    if typ == 'losowy':
        return [random.randint(1, max_value) for i in range(n)]
    if typ == 'rosnacy':
        return sorted([random.randint(1, max_value) for i in range(n)])
    if typ == 'malejacy':
        return (sorted([random.randint(1, max_value) for i in range(n)]))[::-1]
    if typ == 'A':
        return sorted([random.randint(1, max_value) for i in range(n - n // 2)]) + (sorted([random.randint(1, max_value) for i in range(n - n // 2)]))[::-1]
    if typ == 'V':
        return sorted([random.randint(1, max_value) for i in range(n - n // 2)])[::-1] + (sorted([random.randint(1, max_value) for i in range(n - n // 2)]))
    return "nieznany kształt"

def czy_posortowana(arr):
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]: return False
    return True

def uruchom_testy():
    wartosci_n = [10, 20, 50, 100, 200, 500, 750, 1000]
    ksztalty = ['losowy', 'rosnacy', 'malejacy', 'A', 'V']
    algorytmy = [
        ("Bubble Sort", bubble_sort),
        ("Shell Sort", shell_sort_bubble),
        ("Merge Sort", merge_sort_wrapper),
        ("Heap Sort", heap_sort),
        ("Quick Sort (Rek)", quick_sort_recursive_wrapper),
        ("Quick Sort (Iter)", quick_sort_iterative)
    ]
    stats = SortStats()
    csv_dane = []
    dane_wykresy = {nazwa: {ksztalt: [] for ksztalt in ksztalty} for nazwa, _ in algorytmy}
    for n in wartosci_n:
        print(f"\n{'-' * 50}\nROZPOCZYNAM TESTY DLA n = {n}\n{'-' * 50}")
        for ksztalt in ksztalty:
            print(f" == Kształt ciągu: {ksztalt.upper()} ==")
            sumy_czasow = {nazwa: 0.0 for nazwa, _ in algorytmy}
            sumy_porownan = {nazwa: 0 for nazwa, _ in algorytmy}
            sumy_zamian = {nazwa: 0 for nazwa, _ in algorytmy}
            wszystko_poprawnie = True
            for proba in range(10):
                oryginalny_ciag = generacja_ciagu(n, ksztalt)
                for nazwa, funkcja in algorytmy:
                    kopia_ciagu = oryginalny_ciag.copy()
                    stats.reset()
                    posortowany_ciag = funkcja(kopia_ciagu, stats)
                    if proba == 0 and not czy_posortowana(posortowany_ciag):
                        wszystko_poprawnie = False
                        print(f"BŁĄD! {nazwa} nie posortował {ksztalt}!")
                    sumy_czasow[nazwa] += stats.time_ms
                    sumy_porownan[nazwa] += stats.comparisons
                    sumy_zamian[nazwa] += stats.swaps
                    if proba == 0:
                        csv_dane.append({
                            'n': n,
                            'ksztalt': ksztalt,
                            'algorytm': nazwa,
                            'czas_ms': stats.time_ms,
                            'porownania': stats.comparisons,
                            'zamiany': stats.swaps,
                            'scalenia': stats.merges,
                            'pivoty': str(stats.pivots[:5]) + "..." if stats.pivots else "",
                            'przyrosty': str(stats.shell_gaps) if stats.shell_gaps else ""
                        })
            if wszystko_poprawnie:
                print("Poprawność: ZALICZONA")
            for nazwa, _ in algorytmy:
                sredni_czas = sumy_czasow[nazwa] / 10
                dane_wykresy[nazwa][ksztalt].append(sredni_czas)
                print(f"{nazwa:20} | Czas: {sredni_czas:8.4f} ms | Porównania: {sumy_porownan[nazwa]//10:8}")

    with open('raport_sortowanie.csv', 'w', newline='', encoding='utf-8') as f:
        pola = ['n', 'ksztalt', 'algorytm', 'czas_ms', 'porownania', 'zamiany', 'scalenia', 'pivoty', 'przyrosty']
        writer = csv.DictWriter(f, fieldnames=pola)
        writer.writeheader()
        writer.writerows(csv_dane)
    for nazwa, _ in algorytmy:
        plt.figure(figsize=(10, 6))
        for ksztalt in ksztalty:
            plt.plot(wartosci_n, dane_wykresy[nazwa][ksztalt], marker='o', label=ksztalt)
        plt.title(f'Czas od n - {nazwa}'); plt.xlabel('n'); plt.ylabel('Czas [ms]'); plt.legend(); plt.grid(True)
        plt.savefig(f"wykres_algorytm_{nazwa.replace(' ', '_')}.png"); plt.close()
    for ksztalt in ksztalty:
        plt.figure(figsize=(10, 6))
        for nazwa, _ in algorytmy:
            plt.plot(wartosci_n, dane_wykresy[nazwa][ksztalt], marker='o', label=nazwa)
        plt.title(f'Efektywność dla - {ksztalt}'); plt.xlabel('n'); plt.ylabel('Czas [ms]'); plt.legend(); plt.grid(True)
        plt.savefig(f"wykres_ksztalt_{ksztalt}.png"); plt.close()

if __name__ == "__main__":
    uruchom_testy()