def calculate(data, findall):
    matches = findall(r"([abc])([+-]{0,1})[=]{1}([abc]{0,1}[0-9]{0,})([0-9-+]{0,})")
    print(matches)
    for v1, s, v2, n in matches:
        if 'abc'.count(v2) == 1:
            g = data[v2]
            if n != '':
                g += int(n)
        else:
            if v2 == '':
                g = int(n)
            elif n == '':
                g = int(v2)
            else:
                g = int(v2) + int(n)

        if s == '+':
            data[v1] += g
        elif s == '-':
            data[v1] -= g
        else:
            data[v1] = g

    return data
