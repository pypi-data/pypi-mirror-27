import sklearn
from sklearn.preprocessing import MultiLabelBinarizer


def accuracy_score(TP, FP, TN, FN):
    return round((TP + TN) / (TP + FP + TN + FN), 2)


def precision_score(TP, FP, TN, FN):
    try:
        return round(TP / (TP + FP), 2)
    except:
        return 0


def recall_score(TP, FP, TN, FN):
    try:
        return round(TP / (TP + FN), 2)
    except:
        return 0


def f1_score(TP, FP, TN, FN):
    p = precision_score(TP, FP, TN, FN)
    r = recall_score(TP, FP, TN, FN)
    try:
        f1 = round((2 * p * r) / (p + r), 2)
    except:
        f1 = 0
    return f1


def analyze_multilabel(X_test, y_test, y_pred):
    labels = set(sum(y_test + y_pred, ()))
    score = {}
    for label in labels:
        score[label] = {}
        TP, FP, TN, FN = (0, 0, 0, 0)

        for i in range(len(y_test)):
            if label in y_test[i]:
                if label in y_pred[i]:
                    TP += 1
                else:
                    FN += 1
            else:
                if label in y_pred[i]:
                    FP += 1
                else:
                    TN += 1
        score[label] = {
            "TP": TP,
            "FP": FP,
            "TN": TN,
            "FN": FN,
            "accuracy": accuracy_score(TP, FP, TN, FN),
            "precision": precision_score(TP, FP, TN, FN),
            "recall": recall_score(TP, FP, TN, FN),
            "f1": f1_score(TP, FP, TN, FN),
        }
    f1_weighted = f1_all_labels(y_test, y_pred)
    result = {
        "X_test": X_test,
        "y_test": y_test,
        "y_pred": y_pred,
        "score": score,
        "f1_weighted": f1_weighted
    }
    return result


def f1_all_labels(y_test, y_pred):
    binarizer = MultiLabelBinarizer()
    y = [{i for sub in y_test for i in sub}.union(
        {i for sub in y_pred for i in sub})]
    binarizer.fit_transform(y)
    y_test = binarizer.transform(y_test)
    y_pred = binarizer.transform(y_pred)
    return sklearn.metrics.f1_score(y_test, y_pred, average='weighted')
