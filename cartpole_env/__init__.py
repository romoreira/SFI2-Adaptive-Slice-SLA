from gymnasium.envs.registration import register

register(
    id="gymnasium_env/CartPole-v0",
    entry_point="gymnasium_env.envs.cartpole_env:CartPoleEnv",
)
