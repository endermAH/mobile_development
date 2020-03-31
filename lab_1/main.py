#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv

class tarificator():

    def __init__(
            self,
            # Defaults
            outcome_limit = 0,
            income_limit = 50,
            k_income_prelimit = 0,
            k_outcome_prelimit = 2,
            k_income_postlimit = 1,
            k_outcome_postlimit = 2,
            free_sms_count = 0,
            sms_cost = 1,
            data_file_path = './data.csv',
        ):

        # Initialise variables

        self.outcome_limit = outcome_limit
        self.income_limit = income_limit
        self.k_income_prelimit = k_income_prelimit
        self.k_outcome_prelimit = k_outcome_prelimit
        self.k_income_postlimit = k_income_postlimit
        self.k_outcome_postlimit = k_outcome_postlimit
        self.free_sms_count = free_sms_count
        self.data_file_path = data_file_path
        self.sms_cost = sms_cost

    def tarificate_tel(self, target):

        data_file = open(self.data_file_path, 'r')
        self.reader = csv.DictReader(data_file, delimiter=',')

        # Calculate calls cost

        cost = 0
        outcome_limit = self.outcome_limit
        income_limit = self.income_limit

        for line in self.reader:
            call_duration = float(line['call_duration'])

            if ( line['msisdn_origin'] == target ):
                if ( outcome_limit - call_duration > 0 ):
                    outcome_limit -= call_duration
                    cost += call_duration * self.k_outcome_prelimit
                else:
                    outcome_limit -= call_duration
                    cost += (0 - outcome_limit)*self.k_outcome_postlimit + (call_duration + outcome_limit)*self.k_outcome_prelimit
                    outcome_limit = 0

            if ( line['msisdn_dest'] == target ):
                if ( income_limit - call_duration > 0 ):
                    income_limit -= call_duration
                    cost += call_duration * self.k_income_prelimit
                else:
                    income_limit -= call_duration
                    cost += (0 - income_limit)*self.k_income_prelimit + (call_duration + income_limit)*self.k_income_prelimit
                    income_limit = 0

        data_file.close()

        return cost

    def tarificate_sms(self, target):

        data_file = open(self.data_file_path, 'r')
        self.reader = csv.DictReader(data_file, delimiter=',')

        # Calculate sms cost

        cost = 0
        free_sms_count = self.free_sms_count

        for line in self.reader:
            if ( line['msisdn_origin'] == target ): free_sms_count -= int(line['sms_number'])

        cost += (0 - free_sms_count)*self.sms_cost if ( free_sms_count < 0 ) else 0

        data_file.close()

        return cost

if __name__ == '__main__':

    # Init work class

    counter = tarificator()
    print('Стоимость звонков абонента: ' + str(counter.tarificate_tel('911926375')))
    print('Стоимость SMS абонента: ' + str(counter.tarificate_sms('911926375')))
