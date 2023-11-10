from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random

class Coche(Agent):
    def __init__(self, unique_id, model, color):
        super().__init__(unique_id, model)
        self.color = color
        self.crashed = False

    def move_forward(self):
        # Obtener movimientos posibles (hacia adelante, arriba-enfrente, abajo-enfrente)
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,  # Usar Moore para movimientos diagonales
            include_center=False)

        # Filtrar solo los pasos que están en el camino
        road_steps = [step for step in possible_steps if "Camino" in str(self.model.grid[step[0]][step[1]]) and step[0] > self.pos[0]]

        if road_steps:
            new_position = random.choice(road_steps)
            self.model.grid.move_agent(self, new_position)

    def step(self):
        if self.crashed:
            return

        self.move_forward()

        # Verificar colisiones
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for c in cellmates:
            if isinstance(c, Coche) and c != self:
                self.crashed = True
                c.crashed = True

class CocheFlexible(Coche):
    def __init__(self, unique_id, model, color):
        super().__init__(unique_id, model, color)

    def step(self):
        if self.crashed:
            return

        # Realiza dos movimientos en un turno
        for _ in range(2):
            self.move_forward()

            # Verificar colisiones después de cada movimiento
            cellmates = self.model.grid.get_cell_list_contents([self.pos])
            for c in cellmates:
                if isinstance(c, Coche) and c != self:
                    self.crashed = True
                    c.crashed = True
                    return  # Detener movimiento si hay colisión
  # Hacer que el otro coche también se detenga

class Camino(Agent):
    def step(self):
        pass

class Banqueta(Agent):
    def step(self):
        pass

class CruceModel(Model):
    def __init__(self, width, height):
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.current_id = 0

        # Crear Caminos y Banquetas
        for x in range(width):
            for y in range(height):
                if y == 2 or y == 3:  # Caminos
                    camino = Camino(self.next_id(), self)
                    self.grid.place_agent(camino, (x, y))
                else:  # Banquetas
                    banqueta = Banqueta(self.next_id(), self)
                    self.grid.place_agent(banqueta, (x, y))

        # Crear e inicializar los coches
        coche1 = Coche(self.next_id(), self, "blue")
        self.grid.place_agent(coche1, (0, 2))
        self.schedule.add(coche1)

        coche2 = CocheFlexible(self.next_id(), self, "red")
        self.grid.place_agent(coche2, (0, 3))
        self.schedule.add(coche2)

        self.running = True

    def step(self):
        self.schedule.step()

    def next_id(self):
        self.current_id += 1
        return self.current_id

# Inicialización y ejecución del modelo
model = CruceModel(10, 5)
for i in range(10):
    model.step()
