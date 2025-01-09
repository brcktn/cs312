class Fermat():
    def find_repeating_length(a,b):
        l = []
        for i in range(100):
            l.append(a**i % b)
            if l[:len(l)//2] == l[len(l)//2:] and i != 0:
                return len(l) // 2 
        return 0

    def rep_matrix(rows, cols):
        matrix = []
        for i in range(rows):
            matrix.append([])
            for j in range(cols):
                matrix[i].append(Fermat.find_repeating_length(i+1, j+1))

        return matrix

    def print_matrix(matrix):
        for row in matrix:
            row_string = ""
            for col in row:
                row_string += f"{col:02}" + " "
            print(row_string)