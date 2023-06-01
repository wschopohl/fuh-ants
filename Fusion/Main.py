import Render
import Simulation

def main():
    shm, shm_info = Render.get_memory('assets/map_decision_equal.png')
    render_process = Render.start_process(shm_info)
    
    simulation_processes = Simulation.start_process(shm_info)
    
    Simulation.join(simulation_processes)
    render_process.join()
    
    Render.close(shm)

if __name__ == '__main__':
    main()
    