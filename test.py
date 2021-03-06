import numpy as np
import pymysql.cursors
import pymysql
from numpy.linalg import inv
from sympy import symbols, diff
from sympy.parsing.sympy_parser import parse_expr


class Model:



    def input(self):
        self.R = int(input("Enter the number of Measurements:"))
        self.C = int(input("Enter the number of state variables:"))


        self.Y=np.zeros((self.R, 1))
        print("Input the measurement Values:")
        for i in range(self.R):
            for j in range(1):
                self.Y[i][j]=float(input())
        print(self.Y)

        self.X = np.zeros((self.C, 1))
        print("Input initial assumption values:")
        for i in range(self.C):
            for j in range(1):
                self.X[i][j] = float(input())
        print(self.X)

        x1, x2 = symbols("x1 x2")

        self.H = []
        self.S = []
        for i in range(0, self.R):
            self.F = input("Enter the function:")
            (self.H).append(self.F)



    def partial(self):
        self.J = []
        self.partial = []
        for j in range(1, self.C + 1):
            for i in range(0, self.R):
                self.partial1 = diff(self.H[i], "x" + str(j))
                self.partial.append(self.partial1)
        print("partial", self.partial)
        self.J = np.array(self.partial).reshape(self.C, self.R)
        self.G = np.transpose(self.J)
        # print("G=",self.G)

    def update(self):
        self.S=[]
        for i in range(self.R):
            (self.S).append(parse_expr(self.H[i]))
        c = {}
        count = 1
        for i in range(self.C):
            c["x" + str(count)] = self.X[i][0]
            count += 1

        # print("c=", c)
        for i in range(self.R):
            self.S[i] = self.S[i].evalf(subs=c)
        # print(self.S)
        self.D = np.array(self.S).reshape(self.R,1)
        self.D = self.D.reshape(self.R, 1)
        # print("D=", self.D)


        # print(type(G))
        # print("G=", self.G)
        d = {}
        count = 1
        for i in range(self.C):
            d["x" + str(count)] = self.X[i][0]
            count += 1

        # print("d=", d)
        for i in range(self.R):
            for j in range(self.C):
                self.G[i][j] = self.G[i][j].evalf(subs=d)
        #print(self.G)

    def calculation(self):
        for i in range(100):
            Gtranspose=np.transpose(self.G)
            x=np.array(np.dot(Gtranspose, self.G),dtype="float")
            x = np.linalg.inv(x)
            # print(x)
            # print(self.Y)
            # print(self.D)

            # print(self.Y-self.D)
            c=np.dot(Gtranspose, (self.Y-self.D))
            # print(c)
            x=np.dot(x, c)
            # print(x)
            self.X=self.X+x

            self.update()
        print("X=",self.X)









#     def create_table(self):
#         conn = pymysql.connect(host="localhost", user="root", passwd="", db="final")
#
#         myCursor = conn.cursor()
#
#         myCursor.execute("""CREATE TABLE state_variable
#             (
#             id int,
#             position int,
#             value float
#             )
#
#             """)
#         conn.commit()
#         conn.close()
#
#     def fill_table(self):
#         conn = pymysql.connect(host="localhost", user="root", passwd="", db="final")
#
#         myCursor = conn.cursor()
#
#         # mat = np.array([5.9,8,7.9,4.3])
#         id = 11
#         counter = 1
#         x = list(self.X)
#         for i in x:
#             sql = f"INSERT INTO state_variable VALUES ({id},{counter},{i[0]})"
#             myCursor.execute(sql)
#             counter = counter +1
#             conn.commit()
#         conn.close()
my_model=Model()
# my_model.create_table()

# my_model.table()
# my_model.insert_data()
my_model.input()
my_model.partial()
my_model.update()
my_model.calculation()
# my_model.fill_table()

