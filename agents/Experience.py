class Experience(object):
    def __init__(self):
        self.attempts = 0
        self.success = 0.0
        self.reward = 0
        self.total_attempts = 0
        self.total_success = 0.0
        self.total_reward = 0

    def add_reward(self, reward):
        self.total_reward += reward
        self.reward += reward
        self.incr_attepmts()

    def incr_attepmts(self):
        self.total_attempts += 1
        self.attempts += 1

    def reset_attempts(self):
        self.attempts = 0
        self.success = 0

    def get_success_rate(self):
        if self.attempts == 0:
            return 0
        return self.success / self.attempts

    def get_avg_success_rate(self):
        if self.total_attempts == 0:
            return 0
        return self.total_success / self.total_attempts

    def __add__(self, other):
        result = Experience()
        result.attempts = self.attempts + other.attempts
        result.success = self.success + other.success
        result.reward = self.reward + other.reward
        result.total_attempts = self.total_attempts + other.total_attempts
        result.total_success = self.total_success + other.total_success
        result.total_reward = self.total_reward + other.total_reward

        return result

