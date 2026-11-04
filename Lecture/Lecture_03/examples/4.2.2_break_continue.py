words = ['cat', 'window', 'defenestrate']

# Session 1:
print("begin of Session 1")
for w in words:
    if len(w) > 8:
        break
    else:
        print(w, len(w))
print("End of Session 1", end = "\n\n")


# Session 2:
print("begin of Session 2")
for w in words:
    if len(w) < 8:
        break
    else:
        print(w, len(w))
print("End of Session 2", end = "\n\n")

# Session 3:
print("begin of Session 3")
for w in words:
    if len(w) < 8:
        continue
    else:
        print(w, len(w))
print("End of Session 3")
