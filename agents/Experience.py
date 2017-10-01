class Experience(object):
    attempts = 0
    success = 0.0
    reward = 0
    total_attempts = 0
    total_success = 0.0
    total_reward = 0
    success_rate = 0
    avg_success_rate = 0

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
