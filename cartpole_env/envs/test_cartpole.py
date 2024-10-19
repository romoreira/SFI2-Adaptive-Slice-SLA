# test_grid_world.py

import gym
from cartpole import CartPoleEnv
from enum import Enum

def main():
    env = CartPoleEnv(render_mode="human")

    observation, _ = env.reset()
    done = False

    while not done:
        env.render()

        # Escolhe uma ação aleatória
        action = env.action_space.sample()

        observation, reward, done, _, info = env.step(action)

        print(f"Observação: {observation}, Recompensa: {reward}, Done: {done}, Info: {info}")

    env.close()


if __name__ == "__main__":
    main()
