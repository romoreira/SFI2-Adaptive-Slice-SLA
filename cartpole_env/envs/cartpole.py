from enum import Enum
import gymnasium as gym
from gymnasium import spaces
import pygame
import numpy as np


class Actions(Enum):
    right = 0
    left = 1


class CartPoleEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}

    def __init__(self, render_mode=None):
        self.window_size1 = 600
        self.window_size2 = 400

        self.gravity = 9.8
        self.mass_cart = 1.0
        self.mass_pole = 0.1
        self.total_mass = self.mass_cart + self.mass_pole

        self.length = 0.5
        self.tau = 0.02

        self.x_threshold = 2.4
        self.theta_threshold_radians = np.pi / 15

        self.observation_space = spaces.Box(
            low=np.array([-self.x_threshold, -np.inf, -self.theta_threshold_radians, -np.inf]),
            high=np.array([self.x_threshold, np.inf, self.theta_threshold_radians, np.inf]),
            dtype=np.float32
        )
        self.action_space = spaces.Discrete(2)

        self.state = None
        self.render_mode = render_mode
        self.window = None
        self.clock = None

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.state = np.array([
            self.np_random.uniform(low=-0.05, high=0.05),  # Posição do carrinho
            0.0,  # Velocidade do carrinho
            self.np_random.uniform(low=-0.05, high=0.05),  # Ângulo do mastro
            0.0  # Velocidade do mastro
        ])

        if self.render_mode == "human":
            self._render_frame()

        return self.state, {}

    def step(self, action):
        x, x_dot, theta, theta_dot = self.state

        # Calcula a força
        force = 1.0 if action == Actions.right.value else -1.0  # Ação 1: direita, 0: esquerda
        costheta = np.cos(theta)
        sintheta = np.sin(theta)

        temp = (force + self.mass_pole * theta_dot ** 2 * sintheta) / self.total_mass
        theta_acc = (self.gravity * sintheta - costheta * temp) / (
                    self.length * (4.0 / 3.0 - (self.mass_pole * costheta ** 2) / self.total_mass))
        x_acc = temp - self.mass_pole * theta_acc * costheta / self.total_mass

        # Atualiza o estado
        x += self.tau * x_dot
        x_dot += self.tau * x_acc
        theta += self.tau * theta_dot
        theta_dot += self.tau * theta_acc

        self.state = np.array([x, x_dot, theta, theta_dot])

        # Condições de término
        done = x < -self.x_threshold or x > self.x_threshold or theta < -self.theta_threshold_radians or theta > self.theta_threshold_radians
        reward = 1.0 if not done else 0.0

        if self.render_mode == "human":
            self._render_frame()

        return self.state, reward, done, False, {}

    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()

    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_size1, self.window_size2))
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((self.window_size1, self.window_size2))
        canvas.fill((255, 255, 255))

        # Desenho do carrinho
        cart_x = 300 + self.state[0] * 100
        cart_width = 50
        cart_height = 30
        pygame.draw.rect(canvas, (0, 0, 255),
                         pygame.Rect(cart_x - cart_width // 2, 400 - cart_height, cart_width, cart_height))

        # Desenho do mastro
        pole_x = cart_x
        pole_length = 100
        pole_width = 10
        pole_y = 400 - cart_height
        pygame.draw.line(canvas, (255, 0, 0), (pole_x, pole_y),
                         (pole_x + pole_length * np.sin(self.state[2]), pole_y - pole_length * np.cos(self.state[2])),
                         pole_width)

        # Atualiza a janela
        if self.render_mode == "human":
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            return np.transpose(np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2))

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
