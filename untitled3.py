import numpy as np
import pandas as pd
import random
random.seed(40)

def gera_pontos(qtd, a, b):
  x = []
  for i in range(qtd):
    x.append(random.uniform(a, b))
  return x

qtd_pontos = 1000

x1 = gera_pontos(qtd_pontos, -4*np.pi, 4*np.pi)
x2 = gera_pontos(qtd_pontos, -4*np.pi, 4*np.pi)
print(x1)
print(x2)

def funcao_a(x1,x2):
  return 1 if (x1== 0 and x2 == 0) else\
   (np.sin(x1*np.pi)/(x1*np.pi)) if (x1 != 0 and x2 == 0) else\
   (np.sin(x2*np.pi)/(x2*np.pi)) if (x1 == 0 and x2 != 0) else\
   (np.sin(x1*np.pi)/(x1*np.pi))*(np.sin(x2*np.pi)/(x2*np.pi))

fx1x2_a = []
for i in range(qtd_pontos):
  fx1x2_a.append(funcao_a(x1[i], x2[i]))

print(fx1x2_a)

df = {"x1": x1, "x2": x2, "target": fx1x2_a}
df = pd.DataFrame(df)
df

X = df.iloc[:, 0 : df.shape[1] - 1]
Y = df.iloc[:, df.shape[1] - 1 : ]

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from matplotlib import pyplot as plt

#Separando dados de treinamento e teste
x_treinamento, x_teste, y_treinamento, y_teste = train_test_split(X, Y, test_size=0.3, random_state=40)

#Criação do modelo de regressão
model = keras.Sequential([layers.Dense(100, activation='relu', input_shape=[len(X.keys())]),
    layers.Dense(100, activation='relu'),
    layers.Dense(1)
])

optimizer = tf.keras.optimizers.RMSprop(0.001)

model.compile(loss='mse',
              optimizer=optimizer,
              metrics=['mae', 'mse'])

model.summary()

previsoes = model.predict(x_teste)

history = model.fit(X, Y, epochs=100, validation_split = 0.3, verbose=0)

hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch
hist

def plot_history(history):
  hist = pd.DataFrame(history.history)
  hist['epoch'] = history.epoch

  plt.figure()
  plt.plot(fx1x2_a[:299], color='red', label = 'função real')
  plt.plot(previsoes, color='blue', label = 'função aproximado pela rede')
  plt.xlabel('Atributos')
  plt.ylabel('função')
  plt.title("Curva da função")
  plt.legend()
  plt.savefig('função.png', format='png')
  plt.show()

  plt.figure()
  plt.xlabel('Épocas')
  plt.ylabel('Erro')
  plt.title("Curva do erro médio")
  plt.plot(hist['epoch'], hist['mse'], color="red", 
           label='Erro de treinamento')
  plt.plot(hist['epoch'], hist['val_mse'],
           label = 'Erro de validação')
  plt.ylim([-0.1,0.1])
  plt.legend()
  plt.savefig('erro.png', format='png')
  plt.show()

plot_history(history)

"""Como os dados foram divididos em 30% para teste e 70% de treinamento, mostramos apenas 300 pontos da função real."""
