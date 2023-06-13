import Render
import Simulation

import faulthandler

faulthandler.enable()

def main():
    render_info = Render.setup('assets/map_decision_equal.png')
    simulation_info = Simulation.setup(render_info)
    print(render_info)
    #print(simulation_info)
    
    render_process = Render.start_process(render_info)
    simulation_processes = Simulation.start_process(render_info['overlay-shm'])
    
    Simulation.join(simulation_processes)
    render_process.join()
    
    Simulation.close(simulation_info)
    Render.close(render_info)

if __name__ == '__main__':
    main()
    