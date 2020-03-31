#!/usr/bin/python
# -*- coding: utf-8 -*-

class tarificator():

    def __init__(
        self,
        data_file_path='./nf_decoded',
        factor=1,
        ):

        self.data_file_path = data_file_path
        self.factor = factor
        self.target = target

    def tarificate_net(self, target):

        data_types = {
            "date": 0,
            "time": 1,
            "duration": 2,
            "portno": 3,
            "ip_src": 4,
            "arrow": 5, # :)
            "ip_dst": 6,
            "packets": 7,
            "bytes": 8,
            "flows": 9
        }

        data_file = open(self.data_file_path, 'r')

        cost = 0

        for line in data_file.readlines():

            # Prepare line to collect data

            endpoint = len(line)
            i = 0
            while i < endpoint:
                if ( line[i] == ' ' and line[i+1] == ' '):
                    line = line[:i]+line[i+1:]
                    endpoint -= 1
                else:
                    i+=1

            linedata = line.split(' ')

            if ( linedata[data_types["ip_src"]].split(':')[0] == target ):
                cost += self.factor * (float(linedata[data_types["bytes"]]) / 1024 / 1024)

        return cost

if __name__ == '__main__':

    net_tar = tarificator()
    print('Стоимость услуг интернет: ' + str(net_tar.tarificate_net('192.168.250.41')))
