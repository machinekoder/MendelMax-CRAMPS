#!/usr/bin/python

import bisect


class R2Temp:

    # Thermistor data is loaded at runtime from thermistor_tables folder
    Thermistor = {}

    thermistor = []
    R_Key = []

    def __init__(self, name):
        self.loadTable(name)

        if name not in self.Thermistor:
            print(("Thermistor table not found"))
            exit()

        # Shuffle array to make three lists of values (Temp, Resistane, Alpha)
        # so we can use bisect to efficiently do table lookups
        self.thermistor.insert(0, list(map(list, list(zip(*self.Thermistor[name])))))

        # Pull out the resistance values to use as a key for bisect
        self.R_Key.insert(0, self.thermistor[0][1])

    def loadTable(self, name):
        inputFile = "./python/thermistor_tables/" + name + ".txt"
        with open(inputFile, "r") as f:
            self.Thermistor[name] = []
            content = f.readlines()
            for line in content:
                line = ' '.join(line.split())
                if ((len(line) == 0) or (line[0] == '#')):
                    continue
                datas = line.split(' ')
                tableEntry = []
                for data in datas:
                    tableEntry.append(float(data))
                self.Thermistor[name].append(tableEntry)
        # Temperature table needs resistance to be ordered low [0] to high [n]
        if (self.Thermistor[name][0][0] < self.Thermistor[name][-1][0]):
            self.Thermistor[name].reverse()

    # Convert resistance value into temperature, using thermistor table
    def r2t(self, R_T):
        temp_slope = 0.0
        temp       = 0.0
        n = 0

        i = max(bisect.bisect_right(self.R_Key[n], R_T) - 1, 0)

        temp_slope = (self.thermistor[n][0][i] - self.thermistor[n][0][i + 1]) / (self.thermistor[n][1][i] - self.thermistor[n][1][i + 1])
        temp = self.thermistor[n][0][i] + ((R_T - self.thermistor[n][1][i]) * temp_slope)
        #print "Temp:", temp, "i.R_T:", i, R_T, "slope:", temp_slope,
        #print "Deg.left:", self.Thermistor["epcos_B57560G1104"][i], "Deg.right:", self.Thermistor["epcos_B57560G1104"][i+1]
        return temp

#r2temp = R2Temp("1")
#print r2temp.r2t(100000)