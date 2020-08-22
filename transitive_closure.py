import datetime
import matplotlib.pyplot as plt
import random

class TransitiveClosure:


    def generate_input_matrix(self, order):
        """
            generates random input relational matrix
        """
        weight = random.randrange(10, 90, 1)
        return [random.choices(population= [0,  1], weights= (100 - weight, weight), k = order) for x in range(order)]

    def naive_algo(self, inputRelationMatrix, n):
        """
            use naive algorithm to calculate transitive closure
        """
        transitive_matrix = self.matrix_multiply(inputRelationMatrix, inputRelationMatrix, n)
        start = datetime.datetime.now()    
        for i in range(n - 1):
            transitive_matrix = self.matrix_multiply(transitive_matrix, inputRelationMatrix, n)
        end = datetime.datetime.now() - start
        return { 'finalMatrix': transitive_matrix, 'timeTaken': end.total_seconds() }

    def warshall_algo(self, inputRelationMatrix, n):
        """
            use Warshall's algorithm to calculate transitive closure
        """
        final_matrix = [x [: ] for x in inputRelationMatrix]
        start = datetime.datetime.now()
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    final_matrix[j][k] = final_matrix[j][k] or (final_matrix[j][i] and final_matrix[i][k])
        end = datetime.datetime.now() - start
        return { 'finalMatrix': final_matrix, 'timeTaken': end.total_seconds() }



    def matrix_multiply(self, input_matrix_a, input_matrix_b, n):
        """
            takes an input matrix and multiplies the matrix with itself
        """
        final_matrix = [i[: ]for i in input_matrix_a]
        for i in range(n):
            for j in range(n):
                final_matrix[i][j] = 0
                for k in range(n):
                    final_matrix[i][j] = input_matrix_a[i][j] or input_matrix_b[i][j] or final_matrix[i][j] or(input_matrix_a[i][k] and input_matrix_b[k][j])
        return final_matrix

    def find_transitive_closure(self):
        """
            finds transitive closure 
            using naive algorithm & warshall algo
            after calculating the timetaken for each algo plots the graph and save it into 2 png files
        """
        naiveResultList = []
        warshallResultList = []
        maxRange = 91
        minRange = 10
        for i in range(maxRange):
            input_matrix = self.generate_input_matrix(minRange + i)
            n = len(input_matrix)
            naiveResultList.append(self.naive_algo(input_matrix, n))
            warshallResultList.append(self.warshall_algo(input_matrix, n))
        
        self.plot_log_log_graph({ 'responseMatrix': naiveResultList, 'title': 'Naive algorithm Transitive closure - Execution Time vs Matrix Size. Order=n^4', 'xLabel': 'Matrix Size', 'yLabel': 'Execution Time in MiliSeconds', 'fileName': 'naive-algo' })
        self.plot_log_log_graph({ 'responseMatrix': warshallResultList, 'title': 'Warshall’s algorithm Transitive closure - Execution Time vs Matrix Size. Order=(2*n^3 - 1)', 'xLabel': 'Matrix Size', 'yLabel': 'Execution Time in MiliSeconds', 'fileName': 'Warshall-algo' })
        self.printOutput(naiveResultList, warshallResultList)
        
    def printOutput(self, naiveResultList, warshallResultList):
        n = len(warshallResultList)
        with open('output.txt', 'w') as file:
            for i in range(n):
                result = self.checkIfTwoMatricesAreEqual(naiveResultList[i]['finalMatrix'], warshallResultList[i]['finalMatrix'], len(naiveResultList[i]['finalMatrix']))
                file.write('Input: {inputNo} : Matrix dimensions: {dimension}x{dimension} \n'.format(inputNo = i + 1, dimension = len(naiveResultList[i]['finalMatrix'])))
                file.write('Are matrices obtained using  Warshall and Naive algo equal: {result}\n'.format(result = result))
                file.write('Matrix obtained using Naive Algo \n')
                for item in naiveResultList[i]['finalMatrix']:
                    for y in item:
                        file.write(' {} '.format(y))
                    file.write('\n')
                file.write('\n')
                file.write('Matrix obtained using Warshall Algo \n')
                for item in warshallResultList[i]['finalMatrix']:
                    for y in item:
                        file.write(' {} '.format(y))
                    file.write('\n')
                file.write('\n')

            

    def checkIfTwoMatricesAreEqual(self, matrix_1, matrix_2, n):
        for i in range(n):
            for j in range(n):
                if (matrix_1[i][j] != matrix_2[i][j]):
                    return False
        return True

    def plot_log_log_graph(self, details):
        """
            plots the log log graph
        """
        plt.rcParams["figure.figsize"] = (20, 8)
        plt.rcParams["savefig.format"] = 'png'
        plt.scatter([len(x['finalMatrix']) for x in details['responseMatrix']], [y['timeTaken'] for y in details['responseMatrix']])
        plt.title(details['title'], fontsize = 20)
        plt.xlabel(details['xLabel'], fontsize = 12)
        plt.ylabel(details['yLabel'], fontsize = 16)# beautify the x - labels
        plt.gcf().autofmt_xdate()
        plt.savefig(fname = details['fileName'], dpi = 100)
        plt.show()


