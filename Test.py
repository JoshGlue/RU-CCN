from DQN import Estimator
import tensorflow as tf
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import spline
from stock_env import Stock

env = Stock()
VALID_ACTIONS = env.VALID_ACTIONS
experiment_dir = os.path.abspath("./experiments/{}".format(env.spec.id))

estimator = Estimator(scope="q", summaries_dir=experiment_dir)
experiment_dir = os.path.abspath("./experiments/{}".format(env.spec.id))
stocks_to_iterate = 1000
smoothing = 500
x = np.array(range(stocks_to_iterate))

def deep_q_investing():
    profit = 0
    stocks_invested = 0
    stocks_iterated = 0

    y = []
    with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())
        state = env.reset()
        while stocks_iterated < stocks_to_iterate:

            state = np.squeeze(np.reshape(state, [80, 80]))

            state = np.stack([state] * 4, axis=2)
            state = np.array([state])
            q_values = estimator.predict(sess, state)[0]
            best_action = np.argmax(q_values)
            action = VALID_ACTIONS[best_action]
            next_state, reward, done, _ = env.step(action)

            if done:
                profit += reward
                stocks_invested  += reward != 0
                y.append(profit/(stocks_invested or 1))
                state = env.reset()
                stocks_iterated += 1
                print ("Stock {}/{} , Profit: {}".format(stocks_iterated, stocks_to_iterate, profit/(stocks_invested or 1)))


            else:
                state = next_state
    x_new = np.linspace(x.min(),x.max(),smoothing)
    y = np.array(y)
    y_smooth = spline(x, y, x_new)
    return     [plt.plot(x_new, y_smooth, linewidth=2, label='Deep Q'),profit / (stocks_invested or 1)]

def random_investing():
    profit = 0
    stocks_invested = 0
    stocks_iterated = 0
    y = []
    state = env.reset()
    while stocks_iterated < stocks_to_iterate:
        action = np.random.choice(np.array(VALID_ACTIONS))
        next_state, reward, done, _ = env.step(action)

        if done:
            profit += reward
            stocks_invested += reward != 0
            y.append(profit / (stocks_invested or 1))
            state = env.reset()
            stocks_iterated += 1
            print(
                "Stock {}/{} , Profit: {}".format(stocks_iterated, stocks_to_iterate, profit / (stocks_invested or 1)))
        else:
            state = next_state
    x_new = np.linspace(x.min(),x.max(),smoothing)
    y = np.array(y)

    y_smooth = spline(x, y, x_new)
    return [plt.plot(x_new, y_smooth, linewidth=2, label='Random'),profit / (stocks_invested or 1)]



plt.clf()
deep_q_investing()
random_investing()
plt.legend(loc='upper left')
plt.show()
plt.ylabel("Profit")
plt.xlabel("Runs")



