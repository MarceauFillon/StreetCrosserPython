import numpy as np


def create_row_d(arr1):
    arr2 = []
    for matrix in arr1:
        first_row = np.ravel(matrix[0].getA())
        for matrix2 in arr1:
            second_row = np.ravel(matrix2[0].getA())
            arr2.append(np.matrix([first_row, second_row]))

    # print(len(arr2))
    return arr2


class StateHandler:
    def __init__(self, filename=None):
        self.states = []

        if not filename:
            self.generate_states()
        else:
            self.load_states(filename)
    
    def generate_states(self): 
        states = []

        # State 1 to 20 and 51 to 70 and 74 to 80

        A1 = [np.matrix([[0, 0, 4, 4, 4], [0, 0, 4, 4, 4]])]  # = B1 = F1 = G1
        A2 = [np.matrix([[0, 4, 4, 4, 4], [0, 4, 4, 4, 4]])]  # = B2 = F2 = G2
        A3 = [np.matrix([[4, 4, 4, 4, 4], [4, 4, 4, 4, 4]])]  # = A4 = A5 = A6 = A7 = A8 = B3 = B4 = B5 = B6 = B7 = B8
        G3 = [np.matrix([[4, 4, 4, 4, 4], [4, 4, 4, 4, 4]])]  # = G4 = G5 = G6 = G7 = G8 = F3 = F4 = F5 = F6 = F7 = F8
        A9 = [np.matrix([[4, 4, 4, 4, 0], [4, 4, 4, 4, 0]])]  # = B9 = F9 = G9
        A10 = [np.matrix([[4, 4, 4, 0, 0], [4, 4, 4, 0, 0]])]  # = B10 = F10 = G10

        states.extend(A1)
        states.extend(A2)
        states.extend(A3)
        states.extend(G3)
        states.extend(A9)
        states.extend(A10)

        # State 21
        C1 = []
        C1.append(np.matrix(([[0, 0, 1, 1, 2], [0, 0, 4, 4, 4]])))
        C1.append(np.matrix(([[0, 0, 3, 1, 2], [0, 0, 4, 4, 4]])))
        C1.append(np.matrix(([[0, 0, 1, 3, 2], [0, 0, 4, 4, 4]])))
        C1.append(np.matrix(([[0, 0, 1, 1, 3], [0, 0, 4, 4, 4]])))
        C1.append(np.matrix(([[0, 0, 3, 1, 3], [0, 0, 4, 4, 4]])))

        # State 22
        C2 = []
        C2.append(np.matrix(([[0, 1, 1, 2, 1], [0, 4, 4, 4, 4]])))
        C2.append(np.matrix(([[0, 3, 1, 2, 1], [0, 4, 4, 4, 4]])))
        C2.append(np.matrix(([[0, 1, 3, 2, 1], [0, 4, 4, 4, 4]])))
        C2.append(np.matrix(([[0, 1, 1, 3, 1], [0, 4, 4, 4, 4]])))
        C2.append(np.matrix(([[0, 1, 1, 2, 3], [0, 4, 4, 4, 4]])))
        C2.append(np.matrix(([[0, 3, 1, 3, 1], [0, 4, 4, 4, 4]])))
        C2.append(np.matrix(([[0, 3, 1, 2, 3], [0, 4, 4, 4, 4]])))
        C2.append(np.matrix(([[0, 1, 3, 2, 3], [0, 4, 4, 4, 4]])))

        # State 23
        C3 = []
        C3.append(np.matrix(([[1, 1, 2, 1, 1], [4, 4, 4, 4, 4]])))
        C3.append(np.matrix(([[3, 1, 2, 1, 1], [4, 4, 4, 4, 4]])))
        C3.append(np.matrix(([[1, 3, 2, 1, 1], [4, 4, 4, 4, 4]])))
        C3.append(np.matrix(([[1, 1, 3, 1, 1], [4, 4, 4, 4, 4]])))
        C3.append(np.matrix(([[1, 1, 2, 3, 1], [4, 4, 4, 4, 4]])))
        C3.append(np.matrix(([[1, 1, 2, 1, 3], [4, 4, 4, 4, 4]])))
        C3.append(np.matrix(([[3, 1, 3, 1, 1], [4, 4, 4, 4, 4]])))
        C3.append(np.matrix(([[3, 1, 2, 3, 1], [4, 4, 4, 4, 4]])))
        C3.append(np.matrix(([[3, 1, 2, 1, 3], [4, 4, 4, 4, 4]])))
        C3.append(np.matrix(([[1, 3, 2, 3, 1], [4, 4, 4, 4, 4]])))
        C3.append(np.matrix(([[1, 3, 2, 1, 3], [4, 4, 4, 4, 4]])))
        C3.append(np.matrix(([[1, 1, 3, 1, 3], [4, 4, 4, 4, 4]])))
        C3.append(np.matrix(([[3, 1, 3, 1, 3], [4, 4, 4, 4, 4]])))

        # State 24
        C4 = []
        C4.append(np.matrix(([[1, 2, 1, 1, 1], [4, 4, 4, 4, 4]])))
        C4.append(np.matrix(([[3, 2, 1, 1, 1], [4, 4, 4, 4, 4]])))
        C4.append(np.matrix(([[1, 3, 1, 1, 1], [4, 4, 4, 4, 4]])))
        C4.append(np.matrix(([[1, 2, 3, 1, 1], [4, 4, 4, 4, 4]])))
        C4.append(np.matrix(([[1, 2, 1, 3, 1], [4, 4, 4, 4, 4]])))
        C4.append(np.matrix(([[1, 2, 1, 1, 3], [4, 4, 4, 4, 4]])))
        C4.append(np.matrix(([[3, 2, 3, 1, 1], [4, 4, 4, 4, 4]])))
        C4.append(np.matrix(([[3, 2, 1, 3, 1], [4, 4, 4, 4, 4]])))
        C4.append(np.matrix(([[3, 2, 1, 1, 3], [4, 4, 4, 4, 4]])))
        C4.append(np.matrix(([[1, 3, 1, 3, 1], [4, 4, 4, 4, 4]])))
        C4.append(np.matrix(([[1, 3, 1, 1, 3], [4, 4, 4, 4, 4]])))
        C4.append(np.matrix(([[1, 2, 3, 1, 3], [4, 4, 4, 4, 4]])))
        C4.append(np.matrix(([[3, 2, 3, 1, 3], [4, 4, 4, 4, 4]])))

        # State 25
        C5 = []
        C5.append(np.matrix(([[2, 1, 1, 1, 1], [4, 4, 4, 4, 4]])))
        C5.append(np.matrix(([[3, 1, 1, 1, 1], [4, 4, 4, 4, 4]])))
        C5.append(np.matrix(([[2, 3, 1, 1, 1], [4, 4, 4, 4, 4]])))
        C5.append(np.matrix(([[2, 1, 3, 1, 1], [4, 4, 4, 4, 4]])))
        C5.append(np.matrix(([[2, 1, 1, 3, 1], [4, 4, 4, 4, 4]])))
        C5.append(np.matrix(([[2, 1, 1, 1, 3], [4, 4, 4, 4, 4]])))
        C5.append(np.matrix(([[3, 1, 3, 1, 1], [4, 4, 4, 4, 4]])))
        C5.append(np.matrix(([[3, 1, 1, 3, 1], [4, 4, 4, 4, 4]])))
        C5.append(np.matrix(([[3, 1, 1, 1, 3], [4, 4, 4, 4, 4]])))
        C5.append(np.matrix(([[2, 3, 1, 3, 1], [4, 4, 4, 4, 4]])))
        C5.append(np.matrix(([[2, 3, 1, 1, 3], [4, 4, 4, 4, 4]])))
        C5.append(np.matrix(([[2, 1, 3, 1, 3], [4, 4, 4, 4, 4]])))
        C5.append(np.matrix(([[3, 1, 3, 1, 3], [4, 4, 4, 4, 4]])))

        # State 26
        C6 = []
        for matrix in C5:
            C6.append(np.fliplr(matrix))

        # State 27
        C7 = []
        for matrix in C4:
            C7.append(np.fliplr(matrix))

        # State 28
        C8 = []
        for matrix in C3:
            C8.append(np.fliplr(matrix))

        # State 29
        C9 = []
        for matrix in C2:
            C9.append(np.fliplr(matrix))

        # State 30
        C10 = []
        for matrix in C1:
            C10.append(np.fliplr(matrix))

        states.extend(C1)
        states.extend(C2)
        states.extend(C3)
        states.extend(C3)
        states.extend(C4)
        states.extend(C5)
        states.extend(C6)
        states.extend(C7)
        states.extend(C8)
        states.extend(C9)
        states.extend(C10)

        # State 31
        D1 = create_row_d(C1)

        # State 32
        D2 = create_row_d(C2)

        # State 33
        D3 = create_row_d(C3)

        # State 34
        D4 = create_row_d(C4)

        # State 35
        D5 = create_row_d(C5)

        # State 36
        D6 = create_row_d(C6)

        # State 37
        D7 = create_row_d(C7)

        # State 38
        D8 = create_row_d(C8)

        # State 39
        D9 = create_row_d(C9)

        # State 40
        D10 = create_row_d(C10)

        states.extend(D1)
        states.extend(D2)
        states.extend(D3)
        states.extend(D3)
        states.extend(D4)
        states.extend(D5)
        states.extend(D6)
        states.extend(D7)
        states.extend(D8)
        states.extend(D9)
        states.extend(D10)

        # State 41
        E1 = []
        for matrix in C1:
            E1.append(np.flipud(matrix))

        # State 42
        E2 = []
        for matrix in C2:
            E2.append(np.flipud(matrix))

        # State 43
        E3 = []
        for matrix in C3:
            E3.append(np.flipud(matrix))

        # State 44
        E4 = []
        for matrix in C4:
            E4.append(np.flipud(matrix))

        # State 45
        E5 = []
        for matrix in C5:
            E5.append(np.flipud(matrix))

        # State 46
        E6 = []
        for matrix in C6:
            E6.append(np.flipud(matrix))

        # State 47
        E7 = []
        for matrix in C7:
            E7.append(np.flipud(matrix))

        # State 48
        E8 = []
        for matrix in C8:
            E8.append(np.flipud(matrix))

        # State 49
        E9 = []
        for matrix in C9:
            E9.append(np.flipud(matrix))

        # State 50
        E10 = []
        for matrix in C10:
            E10.append(np.flipud(matrix))

        states.extend(E1)
        states.extend(E2)
        states.extend(E3)
        states.extend(E3)
        states.extend(E4)
        states.extend(E5)
        states.extend(E6)
        states.extend(E7)
        states.extend(E8)
        states.extend(E9)
        states.extend(E10)

        # State 71 to 80
        H1 = [np.matrix([[0, 0, 5, 4, 4], [0, 0, 4, 4, 4]])]
        H2 = [np.matrix([[0, 5, 4, 4, 4], [0, 4, 4, 4, 4]])]
        H3 = [np.matrix([[5, 4, 4, 4, 4], [4, 4, 4, 4, 4]])]
        H4 = [np.matrix([[4, 4, 4, 4, 4], [4, 4, 4, 4, 4]])]  # = H5 = H6 = H7 = H8
        H9 = [np.matrix([[4, 4, 4, 4, 0], [4, 4, 4, 4, 0]])]
        H10 = [np.matrix([[4, 4, 4, 4, 0], [4, 4, 4, 4, 0]])]

        states.extend(H1)
        states.extend(H2)
        states.extend(H3)
        states.extend(H3)
        states.extend(H4)
        states.extend(H9)
        states.extend(H10)

        # State 81 to 100
        I1 = [np.matrix([[0, 0, 0, 0, 0], [0, 0, 5, 4, 4]])]
        I2 = [np.matrix([[0, 0, 0, 0, 0], [0, 5, 4, 4, 4]])]
        I3 = [np.matrix([[0, 0, 0, 0, 0], [5, 4, 4, 4, 4]])]
        I4 = [np.matrix([[0, 0, 0, 0, 0], [4, 4, 4, 4, 4]])] # = I5 = I6 = I7 = I8
        I9 = [np.matrix([[0, 0, 0, 0, 0], [4, 4, 4, 4, 0]])]
        I10 = [np.matrix([[0, 0, 0, 0, 0], [4, 4, 4, 0, 0]])]

        states.extend(I1)
        states.extend(I2)
        states.extend(I3)
        states.extend(I3)
        states.extend(I4)
        states.extend(I9)
        states.extend(I10)

        # State 91 to 100
        J1 = [np.matrix([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])]  # = J2 = J3 = J4 = J5 = J6 = J7 = J8 = J9 = J10

        states.extend(J1)

        final_states = []

        for matrix in states:
            if final_states.__len__():
                duplicate = False

                for matrix2 in final_states:
                    if np.equal(matrix, matrix2).all():
                        duplicate = True
                        break

                if not duplicate:
                    final_states.append(matrix)

            else:
                final_states.append(matrix)

        self.states = final_states

    def get_states_length(self):
        return self.states.__len__()

    def save_states(self, filename):
        file = open(filename, "w+")

        for state in self.states:

            for i in range(0, 2):
                for number in np.ravel(state[i].getA()):
                    file.write("%s " % number)
                file.write("\n")

        file.close()

    def load_states(self, filename):
        try:
            file = open(filename, "r+")

            line0 = []
            index = 0

            for line in file:
                if index % 2 != 0:
                    line1 = [int(s) for s in line.split() if s.isdigit()]
                    matrix = np.matrix([line0, line1])
                    self.states.append(matrix)
                else:
                    line0 = [int(s) for s in line.split() if s.isdigit()]

                index += 1

        except IOError:
            print("File doesn't exist, generation of states")
            self.generate_states()

