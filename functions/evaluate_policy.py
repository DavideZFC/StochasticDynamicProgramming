import numpy as np

def evaluate_policy(policy, env, T=364, seeds=1, first_seed=1):

    reward_matrix = np.zeros((seeds, T))
    np.random.seed(first_seed)

    for seed in range(seeds):

        env.reset()

        for t in range(1,T):
            arm = policy.act(env.s)
            reward = env.step(arm)
            reward_matrix[seed, t] = reward_matrix[seed, t-1] + reward
    
    return reward_matrix