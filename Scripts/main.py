# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 17:51:49 2020

@author: Natan Steinbruch
"""

import process_dataset as pdt
import funcao_ativacao as fa
import funcao_custo as fc
import numpy as np
import random
import cv2
import matplotlib.pyplot as plt

def test_predict(teste,teste_saidas,pesos1,pesos2,pesos3,pesos4,bias1,bias2,bias3,bias4):
    inp1 = np.dot(teste,pesos1) + bias1
    camada_oculta1 = fa.sigmoid(inp1)

    inp2 = np.dot(camada_oculta1,pesos2) + bias2
    camada_oculta2 = fa.sigmoid(inp2)

    inp3 = np.dot(camada_oculta2,pesos3) + bias3
    camada_oculta3 = fa.sigmoid(inp3)

    inp4 = np.dot(camada_oculta3,pesos4) + bias4
    camada_saida = fa.sigmoid(inp4)
    #camada_saida = np.where(camada_saida > 0,1,0)

    custo = fc.mse(teste_saidas,camada_saida,198,False)
    #print("erro: %.10f"%(custo))
    
    return custo
#
#Bloco Principal
#
pesos1 = 2 * np.random.random((784, 53)) -1
pesos2 = 2 * np.random.random((53, 36)) -1
pesos3 = 2 * np.random.random((36, 25)) -1
pesos4 = 2 * np.random.random((25, 1)) -1

bias1 = np.zeros((1,53))
bias2 = np.zeros((1,36))
bias3 = np.zeros((1,25))
bias4 = np.zeros((1,1))


path = "C:\\Users\\natst\\OneDrive\\Natan Steinbruch\\IA-do-Ramo\\DataSet\\"
#Modifique o path para onde está a sua pasta DataSet

train,test,dataSet,train_saidas,test_saidas = pdt.process_data_set(path)

epochs = 10000
learning_rate = 0.3
erros =[]
erros2 = []
for epocas in range(epochs+1):
    
    inp1 = np.dot(train,pesos1) + bias1
    camada_oculta1 = fa.sigmoid(inp1)

    inp2 = np.dot(camada_oculta1,pesos2) + bias2
    camada_oculta2 = fa.sigmoid(inp2)

    inp3 = np.dot(camada_oculta2,pesos3) + bias3
    camada_oculta3 = fa.sigmoid(inp3)

    inp4 = np.dot(camada_oculta3,pesos4) + bias4
    camada_saida = fa.sigmoid(inp4)
    #camada_saida = np.where(camada_saida > 0,1,0)

    custo = fc.mse(train_saidas,camada_saida,616,False)
    erros.append(custo)
    erros2.append(test_predict(test,test_saidas,pesos1,pesos2,pesos3,pesos4,bias1,bias2,bias3,bias4))
    print("epoca: %d/%d erro: %f"%(epocas,epochs,custo))
    derivada_saida = fc.mse(train_saidas,camada_saida,616,True)
    
    dinp4 = fa.derivada_sigmoid(inp4) * derivada_saida
    derivada_oculta3 = np.dot(dinp4,pesos4.T)
    d_pesos4 = np.dot(dinp4.T,camada_oculta3)
    d_bias4 = 1.0 * dinp4.sum(axis=0,keepdims=True)
    
    dinp3 = fa.derivada_sigmoid(inp3) * derivada_oculta3
    derivada_oculta2 = np.dot(dinp3,pesos3.T)
    d_pesos3 = np.dot(dinp3.T,camada_oculta2)
    d_bias3 = 1.0 * dinp3.sum(axis=0,keepdims=True)
    
    dinp2 = fa.derivada_sigmoid(inp2) * derivada_oculta2
    derivada_oculta1 = np.dot(dinp2,pesos2.T)
    d_pesos2 = np.dot(dinp2.T,camada_oculta1)
    d_bias2 = 1.0 * dinp2.sum(axis=0,keepdims=True)
    
    dinp1 = fa.derivada_sigmoid(inp1) * derivada_oculta1
    derivada_entrada = np.dot(dinp1,pesos1.T)
    d_pesos1 = np.dot(dinp1.T,train)
    d_bias1 = 1.0 * dinp1.sum(axis=0,keepdims=True)
    
    pesos4 = pesos4 - learning_rate * d_pesos4.T
    pesos3 = pesos3 - learning_rate * d_pesos3.T
    pesos2 = pesos2 - learning_rate * d_pesos2.T
    pesos1 = pesos1 - learning_rate * d_pesos1.T
    
    bias4 = bias4 - learning_rate * d_bias4
    bias3 = bias3 - learning_rate * d_bias3
    bias2 = bias2 - learning_rate * d_bias2
    bias1 = bias1 - learning_rate * d_bias1

result = test_predict(test,test_saidas,pesos1,pesos2,pesos3,pesos4,bias1,bias2,bias3,bias4)
plt.plot(erros)
plt.plot(erros2)
plt.show()
