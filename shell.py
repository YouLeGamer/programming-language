import upita

while True:

    enter = input("Upita > ")
    result, error = upita.run("<stdin>", enter)

    if error:
        print(error.as_string())
    else:
        print(result)
