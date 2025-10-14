from sklearn import metrics



# todo Read the label


# compute db result










y_true = [0, 1, 2, 2, 2]
y_pred = [0, 0, 2, 2, 1]
target_names = ['class 0', 'class 1', 'class 2']
print(metrics.classification_report(y_true, y_pred, target_names=target_names))

acc = metrics.accuracy_score(y_true, y_pred)

f1_score = metrics.f1_score(y_true, y_pred, average='weighted')
macro_f1_score = metrics.f1_score(y_true, y_pred, average='macro')
micro_f1_score = metrics.f1_score(y_true, y_pred, average='micro')
#target_names = ['class 0', 'class 1', 'class 2']
#score = metrics.classification_report(y_true, y_pred,target_names)

print(acc)
print(f1_score)
print(macro_f1_score)
print(micro_f1_score)
#print(score)
