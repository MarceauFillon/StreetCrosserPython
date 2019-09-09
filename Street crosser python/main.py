from interface import *

from world import World

from state_generator import StateHandler

if __name__ == '__main__':
    # stateHandler = StateHandler()
    # stateHandler.save_states("states.txt")
    world = World(10, 10, 2, 2)
    world.add_elements()

    world.set_goal(0, 0)

    tk = Tk()
    gui = InterfaceGui(tk, world)
    try:
        gui.mainloop()
    except:
        gui.plot(10, "Gamma")
