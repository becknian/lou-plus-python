import sys
import getopt
import csv
import os
from multiprocessing import Process, Queue
from datetime import datetime
import configparser

#多进程
class Args(object):
    cityname = ''
    configfile = ''
    userfile = ''
    resultfile = ''
    def __init__(self):
        self.args = sys.argv[1:]
        self._read_args(self.args)
    def _read_args(self, args):
        try:
            opts, arg = getopt.getopt(args, 'hC:c:d:o:', ['help', 'output='])
            for name, value in opts:
                if name in ('-h', '--help'):
                    print('Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata')
                    sys.exit(0)
                elif name == '-C':
                    self.cityname = value
                elif name == '-c':
                    self.configfile = value
                elif name == '-d':
                    self.userfile = value
                elif name == '-o':
                    self.resultfile = value

        except:
            #print('Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata')
            sys.exit(-1)
    def cfg_path(self):
        try:
            index = self.args.index('-c')
            configfile = self.args[index + 1]        
            return configfile
        except:
            print("Parameter Error1")
            sys.exit(-1)
    def user_path(self):
        try:
            index = self.args.index('-d')
            userfile = self.args[index + 1]
            return userfile
        except:
            print("Parameter Error2")
            sys.exit(-1)
    def output_path(self):
        try:
            index = self.args.index('-o')
            outputfile = self.args[index + 1]
            return outputfile
        except:
            print("Parameter Error3")
            sys.exit(-1)

class Config(object):
    def __init__(self, path, cityname):
        self.config = self._read_config(path, cityname)
    def _read_config(self, path, cityname):
        config = {}
        configfile = configparser.ConfigParser()
        if not os.path.exists(path):
            print('config path does not exist')
            sys.exit(-1)
        try:
            configfile.read(path)
            config = configfile[cityname.upper()]
            return config
        except KeyError:
            config = configfile['DEFAULT']
            return config

    def get_config(self, name):
        return float(self.config[name])
    def get_ratio(self):
        return float(self.config['YangLao']) + \
               float(self.config['YiLiao']) + \
               float(self.config['ShiYe']) + \
               float(self.config['GongShang']) + \
               float(self.config['ShengYu']) + \
               float(self.config['GongJiJin'])

class UserData(Process):
    def __init__(self, path):
        self.path = path
        #self.userdata = self._read_users_data(path)
        #super(UserData, self).__init__()
        super().__init__()

    def read_users_data(self, path):
        userdata = {}
        try:
            with open(path) as file:
                for line in file:
                    cur_line = line.strip().split(',')
                    userdata[cur_line[0]] = int(cur_line[1])
            queue1.put(userdata)
            
        except:
            print("Parameter Error5")
            sys.exit(-1)
    def run(self):
        self.read_users_data(self.path)

        
class IncomeTaxCalculator(Process):
    def __init__(self, high, low, ratio, path):
        #super(IncomeTaxCalculator, self).__init__()
        self.high = high
        self.low = low
        self.ratio = ratio
        self.path = path
        super().__init__()
        
    def cala_for_all_userdata(self, high, low, ratio):
        results = []
        userdata = queue1.get()
        for id, salary in userdata.items():
            if salary <= low:
                shebao = low * ratio
            elif salary >= high:
                shebao = high * ratio
            else:
                shebao = salary * ratio
            cal_salary = salary - shebao - 3500
            tax = self.cal_tax(cal_salary)
            final_salary = salary - shebao - tax
            time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            result = [id, salary, format(shebao, ".2f"), format(tax, ".2f"), format(final_salary, ".2f"), time]
            results.append(result)
        #return results
        queue2.put(results)
        
    def export(self, path):
        results = queue2.get()
        with open(path, 'w') as file:
            writer = csv.writer(file)
            writer.writerows(results)
            
    def run(self):
        self.cala_for_all_userdata(self.high, self.low, self.ratio)
        self.export(self.path)
        
    def cal_tax(self, salary):
        if salary > 80000:
            return salary * 0.45 - 13505
        elif salary > 55000:
            return salary * 0.35 - 5505
        elif salary > 35000:
            return salary * 0.3 - 2755
        elif salary > 9000:
            return salary * 0.25 - 1005
        elif salary > 4500:
            return salary * 0.2 - 555
        elif salary > 1500:
            return salary * 0.1 - 105
        elif salary < 0:
            return 0
        else:
            return salary * 0.03


if __name__ == '__main__':
    queue1 = Queue()
    queue2 = Queue()
   
    argument = Args()
    cityname = argument.cityname
    cfg_path = argument.configfile
    user_path = argument.userfile
    output_path = argument.resultfile

    cfg = Config(cfg_path, cityname)
    high = cfg.get_config('JiShuH')
    low = cfg.get_config('JiShuL')
    ratio = cfg.get_ratio()

    #userdata = UserData(user_path).userdata
    
    user = UserData(user_path)
    user.start()
    user.join()
    calculator = IncomeTaxCalculator(high, low, ratio, output_path)
    calculator.start()        
    calculator.join()


    #results = calculator.cala_for_all_userdata(userdata, high, low, ratio)
    #calculator.export(results, output_path)
