from Coches import CruceModel, Coche, Camino, Banqueta, RayoMcqueen
import mesa.visualization

def agent_portrayal(agent):
    if isinstance(agent, Coche) or isinstance(agent, RayoMcqueen):
        portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5, "Layer": 1}
        portrayal["Color"] = "red" if agent.crashed else agent.color
        if agent.crashed:
            portrayal["text"] = "💥"  # Ícono de choque
            portrayal["text_color"] = "black"
        return portrayal
    if isinstance(agent, Coche):
        return {"Shape": "circle", "Filled": "true", "r": 0.5, "Color": "blue", "Layer": 1}
    elif isinstance(agent, RayoMcqueen):
        return {"Shape": "circle", "Filled": "true", "r": 0.5, "Color": "red", "Layer": 1}
    elif isinstance(agent, Camino):
        return {"Shape": "rect", "Filled": "true", "w": 1, "h": 1, "Color": "grey", "Layer": 0}
    elif isinstance(agent, Banqueta):
        return {"Shape": "rect", "Filled": "true", "w": 1, "h": 1, "Color": "green", "Layer": 0}

grid = mesa.visualization.CanvasGrid(agent_portrayal, 20, 6, 500, 300)

server = mesa.visualization.ModularServer(CruceModel,
                                          [grid],
                                          "Car Crossing Simulation",
                                          {"width": 20, "height": 6})
server.port = 8521
server.launch()