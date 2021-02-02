import tensorflow as tf
import pandas as pd
from url import get_embedding, char_dict
import numpy as np

from tensorflow.keras import Sequential
from tensorflow.keras.layers import Convolution1D, Dense, MaxPool1D, LSTM, Reshape, Dropout, Embedding
from tensorflow.keras.models import Model

url_df = pd.read_csv('data.csv')

url_df = url_df.sample(frac=1).reset_index(drop=True)
url_df = url_df.truncate(after=1500)
url_df.loc[url_df['label'] == 'good', 'label'] = 0
url_df.loc[url_df['label'] == 'bad', 'label'] = 1
batch_size = 64

good_df = url_df[url_df.label == 0].to_numpy()
bad_df = url_df[url_df.label == 1].to_numpy()

url_df = url_df.to_numpy()

print(good_df)
print(bad_df)

# url = Url(url_df.loc[url_df.index[93], 'url'], 200)
# url_ts = url.get_embedding()
# exit()
#
# print(url_ts)


def create_model(url_len):

    model = Sequential()
    model.add(Convolution1D(200, 2, 1, padding='same', activation=tf.nn.relu))
    model.add(MaxPool1D(pool_size=2))
    model.add((LSTM(units=100, dropout=0.3, recurrent_dropout=0.3)))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='softmax'))

    inputs = tf.keras.layers.Input(shape=(200, 64))
    outputs = model(inputs)

    model.summary()

    return Model(inputs=inputs, outputs=outputs)


data = [get_embedding(url, 200) for url in url_df[:, 0]]
# print(data)
# print(url_df[:, 1])
# print(np.asarray(url_df[:, 1]).astype('float32'))

model = create_model(200)
opt = tf.keras.optimizers.Adam(learning_rate=0.1)
model.compile(optimizer=opt, loss=tf.keras.losses.BinaryCrossentropy(), metrics=['accuracy'])
model.fit(np.asarray(data), np.asarray(url_df[:, 1]).astype('float32'), epochs=150, batch_size=64)

accuracy = model.evaluate(np.asarray(data), np.asarray(url_df[:, 1]).astype('float32'))
print('Accuracy: %.2f' % (accuracy*100))


# for i in range(0, 1000):
#     # Take a random sample of the good batch to train
#     idx = np.random.randint(0, len(good_df), batch_size)
#     good_batch = np.array(good_df)[idx]
#     good_batch = np.array([Url(x, 200).get_embedding() for x in good_batch])
#
#     idx = np.random.randint(0, len(bad_df), batch_size)
#     bad_batch = np.array(bad_df)[idx]
#     bad_batch = np.array([Url(x, 200).get_embedding() for x in bad_batch])
#
#     loss_real = model.train_on_batch(good_batch, np.zeros((batch_size, 1)))
#     loss_fake = model.train_on_batch(bad_batch, np.ones((batch_size, 1)))
#
#     print("\n%d Iterations [Real loss: %f, Fake loss: %f]" % (i, loss_real, loss_fake))
