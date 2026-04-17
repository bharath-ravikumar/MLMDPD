
import time
from . import conversion, createatoms, GA_model_selection

def main():
    print("Starting MLMDPD run...")
    start = time.time()
    conversion.run()
    createatoms.run(4536127)
    GA_model_selection.run()
    end = time.time()
    elapsed = int(end - start)
    minutes = elapsed // 60
    seconds = elapsed % 60
    print(f"MLMDPD run completed in {minutes}m {seconds}s.")

if __name__ == "__main__":
    main()
