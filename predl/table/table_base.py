import gym
import torch
import random

from predl import RLBase


class TableBase(RLBase):
    def __init__(self, env_name, num_episodes, alpha, gamma, epsilon, policy, **kwargs):
        """
        base class for RL using lookup table
        :param env_name: name of environment, currently environments whose observation space and action space are
        both Discrete are supported. see https://github.com/openai/gym/wiki/Table-of-environments
        :param num_episodes: number of episode for training
        :param alpha:
        :param gamma:
        :param epsilon:
        :param kwargs: other arguments.
        """
        super(TableBase, self).__init__(env_name, num_episodes, alpha, gamma, policy, epsilon=epsilon, **kwargs)

        if not isinstance(self.env.action_space, gym.spaces.Discrete) or \
                not isinstance(self.env.observation_space, gym.spaces.Discrete):
            raise NotImplementedError("action_space and observation_space should be Discrete")

        self.obs_size = self.env.observation_space.n
        self.action_size = self.env.action_space.n
        self.q_table = torch.zeros(self.obs_size, self.action_size)

    def test(self, init_state=-1):
        """
        testing the trained model
        :param init_state: the initial state
        """
        done = False
        total_reward, reward, counter = 0, 0, 0
        state = self.env.reset() if init_state is -1 else init_state
        while not done:
            self.env.render()
            action = self.argmax(self.q_table[state])
            state, reward, done, _ = self.env.step(action)
            total_reward += reward
            counter += 1
        print(f"total reward {total_reward} in {counter} steps")

    @property
    def epsilon_greedy(self) -> int:
        """
        epsilon greedy method
        :return: action (int)
        """
        _epsilon = self.epsilon * (1 - 1 / self.action_size)
        if random.random() > _epsilon:
            action = self.argmax(self.q_table[self.state])
        else:
            action = random.randrange(0, self.action_size)
        return action


class Array2D(object):
    def __init__(self, row, column):
        self._index = []
        self._array = [[None for _ in range(column)] for _ in range(row)]

    def __getitem__(self, key):
        if key not in self._index:
            raise ValueError(f"No value in {key}")
        row, column = key
        return self._array[row][column]

    def __setitem__(self, key, val):
        if key not in self._index:
            self._index.append(key)
        row, column = key
        self._array[row][column] = val

    def sample(self):
        return self[random.choice(self._index)]

    def __repr__(self):
        s = [str(row) for row in self._array]
        return "_2DArray:[\n" + "\n".join(s) + "]"
