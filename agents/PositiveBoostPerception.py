class PositiveBoostPerception(object):
    @staticmethod
    def get_perceived_observation(observation):
        return observation

    @staticmethod
    def get_perceived_reward(observation, reward):
        observation = PositiveBoostPerception.get_perceived_observation(observation)
        if reward > 0:
            reward = reward * 10
        if reward == 0:
            reward = -1

        return observation, reward
