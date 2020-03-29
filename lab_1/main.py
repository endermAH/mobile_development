#!/bin/python

import csv

class tarificator(

    # Defaults

    outcome_limit = 0,
    income_limit = 50,
    k_income_prelimit = 1,
    k_outcome_prelimit = 1,
    k_income_postlimit = 1,
    k_outcome_postlimit = 1,
    free_sms_count = 5,
    data_file_path = './data.csv'

):

    def __init__(self):

        # Collect data from file

        data_file = open(self.data_file_path, 'r')
        self.reader = csv.DictReader(data_file, delimeter=',')
        data_file.close()

    def tarificate_tel(self, target):

        # Calculate calls cost

        cost = 0
        outcome_limit = self.outcome_limit
        income_limit = self.income_limit

        for line in self.reader:
            if ( line['msisdn_origin'] == target ):
                if ( outcome_limit - line['call_duration'] > 0 ):
                    outcome_limit -= line['call_duration']
                    cost += line['call_duration'] * self.k_outcome_prelimit
                else:
                    outcome_limit -= line['call_duration']
                    cost += (0 - outcome_limit)*self.k_outcome_postlimit + (line['call_duration'] + outcome_limit)*self.k_outcome_prelimit
                    outcome_limit = 0
            if ( line['msisdn_dest'] == target ):
                a = 0
                # cost += line['call_duration']

        print(cost)

    def tarificate_sms(self):
        print('sms')

if __name__ == '__main__':

    # Init work class

    counter = tarificator()
    counter.tarificate_tel('911926375')
