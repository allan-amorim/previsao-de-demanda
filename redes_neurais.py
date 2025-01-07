import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Gerar dados artificiais com tendência e sazonalidade
np.random.seed(42)
n_samples = 1000

# Tendência de crescimento
tendencia = np.linspace(50, 200, n_samples)

# Sazonalidade mensal (aproximadamente 30 dias)
sazonalidade = 20 * np.sin(2 * np.pi * np.arange(n_samples) / 30)

# Outros fatores
preco = np.random.uniform(10, 30, size=n_samples)  # Preços variando entre 10 e 30
promocao = np.random.choice([0, 1], size=n_samples)  # Promoção: Sim ou Não
feriado = np.random.choice([0, 1], size=n_samples, p=[0.95, 0.05])  # Feriados esparsos

# Calcular vendas com base nos fatores
vendas = (
    tendencia + sazonalidade - 0.8 * preco + promocao * 25 + feriado * 30 +
    np.random.normal(0, 5, size=n_samples)  # Ruído normal
).clip(min=0)

# Criar DataFrame
df = pd.DataFrame({
    'data': pd.date_range(start='2023-01-01', periods=n_samples, freq='D'),
    'preco': preco,
    'promocao': promocao,
    'feriado': feriado,
    'vendas': vendas.astype(int)
})

# Visualizar os primeiros registros
print(df.head())

# Preparar os dados
X = df[['preco', 'promocao', 'feriado']].values
y = df['vendas'].values

# Dividir em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalizar os dados
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Criar o modelo
model = Sequential([
    Dense(32, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(16, activation='relu'),
    Dense(1)  # Saída para previsão de demanda
])

model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Treinar o modelo
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2, verbose=1)

# Avaliar o modelo
loss, mae = model.evaluate(X_test, y_test)
print(f'MAE no conjunto de teste: {mae:.2f}')

# Fazer previsões
y_pred = model.predict(X_test)

# Visualizar resultados
plt.figure(figsize=(10, 5))
plt.plot(y_test[:100], label='Verdadeiro', marker='o')
plt.plot(y_pred[:100], label='Previsto', marker='x')
plt.title('Comparação de vendas reais vs previstas')
plt.xlabel('Exemplos')
plt.ylabel('Vendas')
plt.legend()
plt.show()
