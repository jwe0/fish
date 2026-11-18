import json, time
from core.modules.logging import info, success

class Phone:
    def __init__(self, args):
        self.number = args[0]

        self.report = {}

        self.carriers_file = "core/dependencies/carriers.json"
        self.country_code_file = "core/dependencies/callingcodes.json"

    def init_values(self):
        self.report["basic"] = {
            "number" : self.number
        }

    def find_carrier(self):
        carriers = json.load(open(self.carriers_file))
        number = self.number.removeprefix("+")
        start = time.time()
        for x, carrier in enumerate(carriers):
            for i in range(len(self.number)):
                car = carriers.get(number[:x])
                if car:
                    end = time.time()
                    taken = end - start
                    self.report["carrier"] = {
                        "count" : carrier,
                        "searched" : x,
                        "time taken" : f"{taken}s",
                    }
                    for key, value in car.items():
                        if key == "en":
                            key = "carrier"
                        self.report["carrier"][key] = value

    def country_code_info(self):
        number = self.number.removeprefix("")
        code_info = json.load(open(self.country_code_file))
        for i in range(3, 0, -1):
            info = code_info.get(number[:i])
            if info:
                self.report["code info"] = info




    def run(self):
        self.init_values()

        info("Searching for carrier (this may take several seconds)...")
        self.find_carrier()
        success("Carrier lookup completed!")

        info("Searching country code...")
        self.country_code_info()
        success("Completed country code lookup!")

        input()
        return self.report