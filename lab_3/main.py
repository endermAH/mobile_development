#!/usr/bin/python
# -*- coding: utf-8 -*-
# lab 3

import csv
from jinja2 import Template
import pdfkit

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
            data_file_path='./nf_decoded',
            factor=1,
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
        self.data_file_path = data_file_path
        self.factor = factor

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

    def generate_pdf(self, output, bik, src_num ,inn ,kpp, dst, number, date, customer, tel, sms, net):

        tmplt_file = open('./invoice.html.j2', 'r')
        template = tmplt_file.read()
        tmplt_file.close()

        invoice = Template(template)
        invoice_content = invoice.render(
            BIK=bik,
            SRC_NUM=src_num,
            INN=inn,
            KPP=kpp,
            DST_NUM=dst,
            NUMBER=number,
            DATE=date,
            CUSTOMER=customer,
            TEL=tel,
            SMS=sms,
            NET=net,
            SUM=tel+sms+net,
        )

        invoice_html = open('tmp_html.html', 'w')
        invoice_html.write(invoice_content)
        invoice_html.close()
        pdfkit.from_url('./tmp_html.html', output)


if __name__ == '__main__':

    # Init work class

    counter = tarificator()

    tel = counter.tarificate_tel('911926375')
    net = counter.tarificate_net('192.168.250.41')
    sms = counter.tarificate_sms('911926375')
    print('Стоимость звонков абонента: ' + str(tel))
    print('Стоимость SMS абонента: ' + str(sms))
    print('Стоимость услуг интернет: ' + str(net))

    counter.generate_pdf('./invoice.pdf', '123123123', '1234123451234', '123123123', '1231231231', '12341234123412341', '1', '26.10.1999', 'Пупкин В. В.', tel, sms, net)
