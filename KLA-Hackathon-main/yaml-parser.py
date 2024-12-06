from fileinput import filename
from matplotlib.pyplot import table
import yaml
from yaml.loader import SafeLoader
import datetime
import time as t
import threading
import sys
import pandas as pd
import numpy as np

class Logger:
    
    data = {}
    cur = ''
    concur = False
    threadLock = threading.Lock()
    def __init__(self,data,cur = '',concurrent = False):
        global time
        self.data = data
        self.cur = cur
        self.concur = concurrent
        threads = []
        self.threadLock.acquire()
        print(str(datetime.datetime.now())+';'+self.cur+' Entry')
        self.threadLock.release()
        k = data['Activities']
        
        for j in k:
            if k[j]['Type'] =='Task':
                if self.concur:
                    t_temp = threading.Thread(target = self.exec_func,args=(j,k))
                    threads.append(t_temp)
                    t_temp.start()
                else:
                    self.exec_func(j,k)
            else:
                #print(k[j])
                l = k[j]['Execution'] == 'Concurrent'
                if self.concur:
                    t_temp = threading.Thread(target=Logger, args = (k[j],self.cur+'.'+j,l))
                    threads.append(t_temp)
                    t_temp.start()
                else:
                    Logger(data = k[j],cur = self.cur+'.'+j,concurrent = l)
                    #del next
        for x in threads:
            x.join()

    def __del__(self):
        self.threadLock.acquire()
        print(str(datetime.datetime.now())+';'+self.cur+' Exit')
        self.threadLock.release()

    #Time Func
    def TimeFunction(self,i):
        t.sleep(int(i))
    
    #Dataload func
    def DataLoad(self,filename):
        df = pd.read_csv(filename)
        defects = len(df.index)
        return {'DataTable' : df,'NoOfDefects': defects}
    
    #Condition check function
    def conditions(self,con):
        global ops
        var = ''
        st = 0
        ed = 0
        gr = True
        f = 0
        for i in range(len(con)):
            if con[i] == '(':
                st = i
            if con[i] == ')':
                ed = i
            if con[i] == '<':
                gr = False
                f = i+1
            if con[i] == '>':
                f = i+1
        var = con[st+1:ed]
        n = int(con[f+1:])
        while var not in ops:
            h = 0
        if gr:
            if ops[var]> n:
                return True
        else:
            if ops[var]< n:
                return True

        return False

    def Binning(self,rule_file,dataset):
        
        rl = pd.read_csv(rule_file)
        #print(rl)
        rule = rl['RULE'][0]
        bin = rl['BIN_ID'][0]
        greater = -1
        lesser = -1
        rule = rule.split(' ')
        ln = len(rule)
        for i in range(len(rule)):
            if rule[i] == '>':
                greater = int(rule[i+1])
            if rule[i] == '<':
                lesser = int(rule[i+1])
        d_copy = dataset.copy()
        
        if greater != -1 and lesser != -1:
            bin_col = np.where((d_copy['Signal'] > greater) & (d_copy['Signal'] < lesser),bin,0)
        elif greater != -1:
            bin_col = np.where(d_copy['Signal'] > greater,bin,0)
        else:
            bin_col = np.where(d_copy['Signal'] < lesser,bin,0)

        #self.threadLock.acquire()
        #print(bin_col)
        #self.threadLock.release()
        
        d_copy['Bincode'] = bin_col
        self.threadLock.acquire()
        #print(d_copy)
        self.threadLock.release()

        return {'BinningResultsTable':d_copy,'NoOfDefects':ln}

    def MergeResults(self,precedence, datasets):
        f = open(precedence, "r")
        order = f.read()
        order = order.split(' ')
        order = [value for value in order if value != '>>']
        bin_col = np.zeros(len(datasets[0]))
        for i in range(len(datasets[0])):
            for j in range(len(datasets)):
                if datasets[j].iloc[i]['Bincode'] != 0:
                    if bin_col[i] == 0:
                        bin_col[i] = datasets[j].iloc[i]['Bincode']
                    else:
                        if order.index(bin_col) > order.index(datasets[j].iloc[i]['Bincode']):
                            bin_col[i] = datasets[j].iloc[i]['Bincode']
        ds = datasets[0].copy()
        ds['Bincode'] = bin_col
        #print(ds)
        return {'MergedResults':ds , 'NoOfDefects':len(bin_col)}

    def ExportResults(self,FileName,dt):
        dt.to_csv(FileName,  index = False)

    def exec_func(self,name,k):
        global path,ops,dts
        func = k[name]['Function']
        inputs = k[name]['Inputs']
        self.threadLock.acquire()
        print(str(datetime.datetime.now())+';'+self.cur+'.'+name+' Entry')
        self.threadLock.release()

        if 'Condition' in k[name]:
            if not self.conditions(k[name]['Condition']):
                self.threadLock.acquire()
                print(str(datetime.datetime.now())+';'+self.cur+'.'+name+' Skipped' )
                self.threadLock.release()

                self.threadLock.acquire()
                print(str(datetime.datetime.now())+';'+self.cur+'.'+name+' Exit')
                self.threadLock.release()

                return
            
        if func == "TimeFunction":
            f_input = inputs['FunctionInput']
            if '$' in inputs['FunctionInput']:
                st = 0
                ed = 0
                for i in range(len(f_input)):
                    if f_input[i] == '(':
                        st = i
                    if f_input[i] == ')':
                        ed = i
                f_input = ops[f_input[st+1:ed]]
            self.threadLock.acquire()
            print(str(datetime.datetime.now())+';'+self.cur+'.'+name+' Executing '+func+' ('+str(f_input)+' , '+inputs['ExecutionTime']+')' )
            self.threadLock.release()

            self.TimeFunction(inputs['ExecutionTime'])

        if func == "DataLoad":
            self.threadLock.acquire()
            print(str(datetime.datetime.now())+';'+self.cur+'.'+name+' Executing '+func+' ('+inputs['Filename']+')' )
            self.threadLock.release()
            
            temp = self.DataLoad(path+'/'+inputs['Filename'])
            ops[self.cur+'.'+name+'.NoOfDefects'] = temp['NoOfDefects']
            dts[self.cur+'.'+name+'.DataTable'] = temp['DataTable']
            #print(dts)

        if func == 'Binning':
            ds_input = inputs['DataSet']
            if '$' in inputs['DataSet']:
                st = 0
                ed = 0
                for i in range(len(ds_input)):
                    if ds_input[i] == '(':
                        st = i
                    if ds_input[i] == ')':
                        ed = i
                ds = dts[ds_input[st+1:ed]]
            self.threadLock.acquire()
            print(str(datetime.datetime.now())+';'+self.cur+'.'+name+' Executing '+func+' ('+inputs['RuleFilename']+','+inputs['DataSet']+')' )
            self.threadLock.release()
            temp = self.Binning(path+'/'+inputs['RuleFilename'],ds)
            dts[self.cur+'.'+name+'.BinningResultsTable'] = temp['BinningResultsTable']
            ops[self.cur+'.'+name+'.NoOfDefects'] = temp['NoOfDefects']

        if func == 'MergeResults':
            pr = inputs['PrecedenceFile']
            datasets = []
            for i in inputs:
                if 'DataSet' in i:
                    if '$' in inputs[i]:
                        ds_input = inputs[i]
                        st = 0
                        ed = 0
                        for i in range(len(ds_input)):
                            if ds_input[i] == '(':
                                st = i
                            if ds_input[i] == ')':
                                ed = i
                    datasets.append(dts[ds_input[st+1:ed]])
            self.threadLock.acquire()
            print(str(datetime.datetime.now())+';'+self.cur+'.'+name+' Executing '+func+' ('+inputs['PrecedenceFile']+')' )
            self.threadLock.release()
            temp = self.MergeResults(path+'/'+pr,datasets)
            dts[self.cur+'.'+name+'.MergedResults'] = temp['MergedResults']
            ops[self.cur+'.'+name+'.NoOfDefects'] = temp['NoOfDefects']

        if func == 'ExportResults':
            filename = inputs['FileName']
            ds_input = inputs['DefectTable']
            if '$' in inputs['DefectTable']:
                st = 0
                ed = 0
                for i in range(len(ds_input)):
                    if ds_input[i] == '(':
                        st = i
                    if ds_input[i] == ')':
                        ed = i
                ds = dts[ds_input[st+1:ed]]
            self.threadLock.acquire()
            print(str(datetime.datetime.now())+';'+self.cur+'.'+name+' Executing '+func+' ('+inputs['FileName']+')' )
            self.threadLock.release()
            self.ExportResults(path+'/'+filename,ds)

        self.threadLock.acquire()
        print(str(datetime.datetime.now())+';'+self.cur+'.'+name+' Exit')
        self.threadLock.release()

##----------------------------Class Finish-----------------------------------------------------
## -------------------Milestoone 1A-----------------------------
#with open('Milestone1\Milestone1A.yaml','r') as f:
#    data = yaml.load(f, Loader=SafeLoader)

#orig_stdout = sys.stdout
#f = open('ml1a.txt', 'w')
#sys.stdout = f

#for i in data:
    #print(i)
#    if data[i]['Execution'] =='Sequential':
#        p1 = Logger(data[i],i)
#        del p1

#sys.stdout = orig_stdout
#f.close()

## -------------------Milestoone 1B-----------------------------
#with open('Milestone1\Milestone1B.yaml','r') as f:
#   data = yaml.load(f, Loader=SafeLoader)

#orig_stdout = sys.stdout
#f = open('ml1b.txt', 'w')
#sys.stdout = f

#for i in data:
    #print(i)
#    if data[i]['Execution'] =='Sequential':
#        p1 = Logger(data[i],i)
#        del p1

#sys.stdout = orig_stdout
#f.close()

## -------------------Milestoone 2A-----------------------------
#dts = {}
#ops = {}
#path = "Milestone2"

#with open('Milestone2\Milestone2A.yaml','r') as f:
#    data = yaml.load(f, Loader=SafeLoader)

#orig_stdout = sys.stdout
#f = open('ml2a.txt', 'w')
#sys.stdout = f

#for i in data:
    #print(i)
#    if data[i]['Execution'] =='Sequential':
#        p1 = Logger(data[i],i)
#        del p1

#sys.stdout = orig_stdout
#f.close()

## -------------------Milestoone 2B-----------------------------
#dts = {}
#ops = {}
#path = "Milestone2"

#with open('Milestone2\Milestone2B.yaml','r') as f:
#    data = yaml.load(f, Loader=SafeLoader)

#orig_stdout = sys.stdout
#f = open('ml2b.txt', 'w')
#sys.stdout = f

#for i in data:
    #print(i)
#    if data[i]['Execution'] =='Sequential':
#        p1 = Logger(data[i],i)
#        del p1

#sys.stdout = orig_stdout
#f.close()

## -------------------Milestoone 3A-----------------------------
dts = {}
ops = {}
path = "Milestone3"

with open('Milestone3\Milestone3A.yaml','r') as f:
    data = yaml.load(f, Loader=SafeLoader)

for i in data:
    #print(i)
    if data[i]['Execution'] =='Sequential':
        p1 = Logger(data[i],i)
        del p1
#print(dts)