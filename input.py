def get(file):
    def readline(line):
        return list(map(lambda i: int(i), line.split()))
    with open(file) as data:
        matrix = []
        for line in data:
            matrix.append(readline(line))
        return(matrix)
