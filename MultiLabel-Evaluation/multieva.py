import pandas as pd
#Evaluate the predictive performance of the model on each SDG category
def accuracy(prediction,labels,sdg):
    minus=prediction["SDG"+str(sdg)]-labels["SDG"+str(sdg)]
    sample_num=len(minus) #the number of samples
    zero_num= minus.tolist().count(0) #the number of zero, i.e. cases predicted correctly.
    return zero_num/sample_num #accuracy

def precision(prediction,labels,sdg):
    tpPlusfp=0
    tp=0
    for i in range(len(prediction)):
        if prediction.loc[i,"SDG"+str(sdg)]==1:
            tpPlusfp = tpPlusfp+1
            if labels.loc[i,"SDG"+str(sdg)]==1:
                tp = tp+1
    try:
        return tp/tpPlusfp #precision
    except: #Denominator is 0
        return "tp=fp=0"

def recall(prediction,labels,sdg):
    fn=0
    tp=0
    for i in range(len(prediction)):
            if prediction.loc[i,"SDG"+str(sdg)]==1:
                if labels.loc[i,"SDG"+str(sdg)]==1:
                    tp = tp+1
            elif prediction.loc[i,"SDG"+str(sdg)]==0:
                if labels.loc[i,"SDG"+str(sdg)]==1:
                    fn = fn+1
    try:
        return tp/(tp+fn) #recall
    except:#Denominator is 0
        return "tp=fn=0"

def f1fun(prediction,labels,sdg):
    p=precision(prediction,labels,sdg)
    r=recall(prediction,labels,sdg)
    try:
        return 2*p*r/(p+r)
    except: #Denominator is 0
        return ("p=0,r=0")

def evaluate_on_each_SDG(labels,prediction):
    sdg_num=len(prediction.columns.values.tolist()) #how many sdgs in the dataset
    result=pd.DataFrame(columns=('Accuracy','Precision','Recall','F1'),index=["SDG"+str(i)for i in range(1,sdg_num+1)])
    for i in range(1,sdg_num+1):#evaluate each sdg class
        acc=accuracy(prediction,labels,i)
        pre=precision(prediction,labels,i)
        rec=recall(prediction,labels,i)
        f1=f1fun(prediction,labels,i)
        result.loc["SDG"+str(i)]=[acc,pre,rec,f1]
    return result