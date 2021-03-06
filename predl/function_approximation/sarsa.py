import matplotlib.pyplot as plt

from predl import FABase


class Sarsa(FABase):
    def __init__(self, env_name, num_episodes=50000, alpha=0.9, gamma=0.9, epsilon=1e-1, min_alpha=1e-3,
                 decay_freq=1000):
        super(Sarsa, self).__init__(env_name, num_episodes, alpha, gamma, epsilon, policy="epsilon_greedy",
                                    min_alpha=min_alpha, decay_freq=decay_freq)

    def _loop(self):
        done = False
        total_reward, reward = 0, 0
        self.state = self.env.reset()
        action = self.policy()
        while not done:
            _state, reward, done, _ = self.env.step(action)
            _action = self.argmax([self.app_q(_state, a) for a in range(self.action_size)])
            q = self.app_q(self.state, action)
            target = reward + self.gamma * self.app_q(_state, _action)
            # todo use autograd instead
            self.weight -= self.alpha * (target - q) * self.feature(self.state, action)
            total_reward += reward
            self.state = _state
            action = _action
        return total_reward

    def schedule_alpha(self, episode):
        if self.alpha > self.min_alpha and episode % self.decay_freq == 0 and episode != 0:
            self.alpha = self.alpha / (episode / self.decay_freq)


def main(plot=True, env_name='CartPole-v0'):
    print("start training")
    sarsa = Sarsa(env_name, num_episodes=int(1e5))

    # training
    sarsa()
    if plot:
        plt.plot(sarsa.rewards)
        plt.show()
    sarsa.test()
    sarsa.test()
    sarsa.test()


if __name__ == '__main__':
    main()
