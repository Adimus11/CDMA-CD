from medium import Medium
from host import Host

def main():
    medium = Medium(20, 0.05)
    medium.add_host(Host("12", 20, medium, "A"), 0)
    medium.add_host(Host("34", 20, medium, "B"), 10)
    medium.add_host(Host("56", 20, medium, "C"), 19)
    medium.start()
    pass

if __name__ == "__main__":
    main()