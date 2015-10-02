#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import print_function

# Importar librerías requeridas
import cPickle as pickle
import scipy
import numpy as np
import argparse
import os


from sklearn.metrics.metrics import accuracy_score
from sklearn.cross_validation import KFold


# Variables de configuaración
NAME='develop'

if __name__ == "__main__":
    # Las opciones de línea de comando
    p = argparse.ArgumentParser(NAME)
    p.add_argument("DIR",default=None,
        action="store", help="Directory with corpus")
    p.add_argument("-m", "--mode",type=str,
        action="store", dest="mode",default="gender",
        help="Mode (gender|age|extroverted|stable|agreeable|conscientious|open) [gender]")
    p.add_argument("-f", "--folds",type=int,
        action="store", dest="folds",default=20,
        help="Folds during cross validation [20]")
    p.add_argument("-d", "--dir",
        action="store_true", dest="dir",default="feats",
        help="Default directory for features [feats]")
    p.add_argument("-v", "--verbose",
        action="store_true", dest="verbose",
        help="Verbose mode [Off]")
    p.add_argument("--estimators",
        action="store", dest="estimators",default=10000,type=int,
        help="Define el valor para n_estimators")
    opts = p.parse_args()


    # prepara función de verbose
    if opts.verbose:
        def verbose(*args):
            print(*args)
    else:
        verbose = lambda *a: None

    feats=['1grams','tfidf','lb_reyes','lb_hu','lf_reyes','lf_hu','whissell_t']

    if opts.mode=="gender":
        index_y=0
    elif opts.mode=="age":
        index_y=1
    elif opts.mode.startswith("ex"):
        index_y=2
    elif opts.mode.startswith("st"):
        index_y=3
    elif opts.mode.startswith("agre"):
        index_y=4
    elif opts.mode.startswith("co"):
        index_y=5
    elif opts.mode.startswith("op"):
        index_y=6



    # Carga etiquetas
    truth={}
    for line in open(os.path.join(opts.DIR,'truth.txt')):
        bits=line.split(':::')
        truth[bits[0]]=bits[1:]


    # Carga las matrices
    x=[]
    feats_=[]
    for feat in feats:
        verbose('Loading:', feat)
        # Lee los indices de los rengloes
        try:
            with open(os.path.join(opts.dir,feat+'.idx'),'rb') as idxf:
                ids = pickle.load(idxf)
        except IOError:
            verbose('Warning, no features...')
            continue

        # Lee la matrix de features de disco
        with open(os.path.join(opts.dir,feat+'.dat'), 'rb') as infile:
            x_ = pickle.load(infile)
            if type(x_) is scipy.sparse.csr.csr_matrix:
                x_ = x_.toarray()
        x.append(x_)
        feats_.append(feat)

    verbose("Loaded",len(x),"matrix features")
    for feat,x_ in zip(feats_,x):
        verbose('Sumary', feat)
        verbose("Rows     :", x_.shape[0] )
        verbose("Features :", x_.shape[1] )
        verbose('----------\n')


    x=np.hstack(x)

    # Checa que etiquetas e identificatores coincidan
    if not x.shape[0]==len(ids):
        print("Error con matrix de features {0} e identificadores {1}".
            format(len(x.shape), x.shape[0]))


    verbose("Truth    :", len(truth) )
    verbose("Ids      :", len(ids) )
    verbose("Rows     :", x.shape[0] )
    verbose("Features :", x.shape[1] )
    verbose('----------\n')

    # recuperando las etiquetas
    try:
        y_labels= [truth[id_usuario][index_y] for idd,id_usuario in ids]
    except ValueError:
        y_labels= [truth[id_usuario][index_y] for id_usuario in ids]

    # Pasando etiquetas a números
    if opts.mode in ['age','gender']:
        labels={}
        for label in y_labels:
            try:
                labels[label]+=1
            except KeyError:
                labels[label]=1

        labels=labels.keys()
        for label in labels:
            verbose("Label",label,"-->",labels.index(label))
        verbose('----------\n')

        # Creando el vector de etiquetas
        y=np.array([ labels.index(label) for label in y_labels])
    else:
        y=np.array([float(l) for l in y_labels])
        print(y)
        



        
        #reducir x_train
        #aplicar la misma reduccion  y_test

    kf = KFold(len(y), n_folds=opts.folds)
    y_=[]
    prediction_=[]
    verbose("Cross validation:")
    for i,(train,test) in enumerate(kf):
        # Cortando datos en training y test
        from sklearn.decomposition import PCA
        pca = PCA(n_components=='mle')
        
        X_train, X_test, y_train, y_test = x[train],x[test],y[train],y[test]
        
        X_train = pca.transform_fit(X_train)
        X_test = pca.transform(X_test)
        
        if opts.mode in ['age','gender']:
            # Preparando la máquina de aprendizaje
            verbose("   Training fold   (%i)"%(i+1))
            from sklearn.svm import SVC
            from sklearn.ensemble import RandomForestClassifier
            classifier=RandomForestClassifier(n_estimators=10000, criterion='entropy')
            
            #classifier = SVC(C=10, kernel='linear', 
            #gamma=10, coef0=0.0, shrinking=True, 
            #probability=False, tol=0.001, cache_size=20000, 
            #class_weight='auto', verbose=False, max_iter=-1, 
            #random_state=None)
            # Aprendiendo
            classifier.fit(X_train, y_train)

            # Prediciendo
            verbose("   Predicting fold (%i)"%(i+1))
            prediction = classifier.predict(X_test)

            verbose('   Accuracy fold   (%i):'%(i+1), accuracy_score(y_test, prediction))
            y_.extend(y_test)
            prediction_.extend(prediction)

        else:
             # Preparando la máquina de aprendizaje
            verbose("   Regressing fold   (%i)"%(i+1))
            from sklearn.ensemble import RandomForestRegressor
            from sklearn.svm import SVR
            #regressor=RandomForestRegressor(n_estimators=opts.estimators)
            regressor = SVR(kernel='linear', degree=3, gamma=1.0, coef0=1.0, 
            tol=0.001, C=10, epsilon=0.1, shrinking=True, probability=False
            , cache_size=200, verbose=False, max_iter=-1, 
            random_state=None)
            
            # Aprendiendo
            regressor.fit(X_train, y_train)

            # Prediciendo
            verbose("   Predicting fold (%i)"%(i+1))
            prediction = regressor.predict(X_test)

            y_.extend(y_test)
            prediction_.extend(prediction)



    verbose('----------\n')
    verbose("Evaluation")

    if opts.mode in ['age','gender']:
        from sklearn.metrics.metrics import precision_score, recall_score, confusion_matrix, classification_report, accuracy_score, f1_score
        # Calculando desempeño
        print( 'Accuracy              :', accuracy_score(y_, prediction_))
        print( 'Precision             :', precision_score(y_, prediction_))
        print( 'Recall                :', recall_score(y_, prediction_))
        print( 'F-score               :', f1_score(y_, prediction_))
        print( '\nClasification report:\n', classification_report(y_,
                prediction_))
        print( '\nConfussion matrix   :\n',confusion_matrix(y_, prediction_))
    else:
        from sklearn.metrics.metrics import mean_absolute_error, mean_squared_error,r2_score
        print( 'Mean Abs Error        :', mean_absolute_error(y_, prediction_))
        print( 'Mean Sqr Error        :', mean_squared_error(y_, prediction_))
        print( 'R2 Error              :', r2_score(y_, prediction_))


    #plots:
    #import matplotlib.pyplot as plt
    #confusion_matrix_plot = confusion_matrix(y_test, prediction)
    #plt.title('matriz de confusion')
    #plt.colorbar()
    #plt.xlabel()
    #plt.xlabel('categoria de verdad')
    #plt.ylabel('categoria predecida')
    #plt.show()
