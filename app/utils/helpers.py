def set_bins(length):
    if length <= 100:
        bins = int(length ** 0.5)
    else:
        bins = int(length ** (1 / 3))
    return max(bins, 1)