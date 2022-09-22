fonts = ["Times New Roman", "Helvetica", "Fira Code"]
categories = ["Serif", "Sans Serif", "Monospaced"]

for i, font in enumerate(fonts):
    print(
        "{}. {} is a {} font.".format(
            i, font, categories[i]
        )
    )