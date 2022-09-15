# Measure some strings:
words = ['cat', 'window', 'defenestrate']
for w in words:
    if len(w) > 8:
        break
    else:
        print(w, len(w))
print("The end: break 1")


# Measure some strings:
words = ['cat', 'window', 'defenestrate']
for w in words:
    if len(w) < 8:
        break
    else:
        print(w, len(w))
print("The end: break 2")

# Measure some strings:
words = ['cat', 'window', 'defenestrate']
for w in words:
    if len(w) < 8:
        continue
    else:
        print(w, len(w))
print("The end: continue")
