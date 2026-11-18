from core.modules.logging import *
from core.modules.general import *

from core.modules.networking.run_networking import Networking
from core.modules.social_media.run_social_media import Online
from core.modules.email.run_email import Email
from core.modules.domain_lookup.run_domain import Domain
from core.modules.page_fuzzer.run_fuzzer import Fuzzer
from core.modules.phone.run_phone import Phone

class Main:
    def __init__(self):
        self.modules = {
            "networking" : {
                "name" : "Networking",
                "description" : "Automated lookup for domains/IP hosts",
                "class" : Networking,
                "args" : {
                    "host" : True
                }
            },
            "social media" : {
                "name" : "Social media",
                "description" : "Automated social media OSINT",
                "class" : Online,
                "args" : {
                    "username" : True
                }
            },
            "email lookup" : {
                "name" : "Email lookup",
                "description" : "Pull basic email information",
                "class" : Email,
                "args" : {
                    "email" : True
                }
            },
            "domain lookup" : {
                "name" : "Domain lookup",
                "description" : "Scan for hidden subdomains/domains",
                "class" : Domain,
                "args" : {
                    "domain" : True
                }
            },
            "page fuzzer" : {
                "name" : "Page fuzzer",
                "description" : "Website page fuzzer",
                "class" : Fuzzer,
                "args" : {
                    "url" : True
                }
            },
            "phone lookup" : {
                "name" : "Phone lookup",
                "description" : "Pull public mobile phone info",
                "class" : Phone,
                "args" : {
                    "number" : True
                }
            }
        }

        self.conversion_table = {}

    def show_modules(self):
        print()
        for i, module in enumerate(self.modules):
            module_info = self.modules[module]

            name = module_info["name"]

            self.conversion_table[str(i + 1)] = name

            menu_option(name, i + 1)
        print()

    def select_module(self):
        user_choice = inpt("Option")

        while not user_choice.isdigit() or user_choice not in self.conversion_table:
            error("Please make a valid selection")
            user_choice = inpt("Press enter to continue")
        return user_choice

    def get_module_info(self, user_choice):
        selected_module = self.conversion_table[user_choice].lower()

        module_info = self.modules[selected_module]

        name = module_info["name"]
        desc = module_info["description"]
        clas = module_info["class"]
        arg_ = module_info["args"]

        return {
            "name" : name,
            "description" : desc,
            "class" : clas,
            "arg"   : arg_
        }

    def get_module_arg(self, args, description):
        args_report = []
        info(description)
        for arg in args:
            user_choice = inpt(arg)
            if args.get(arg):
                while not user_choice:
                    error("Please enter a value")
                    user_choice = inpt("Press enter to continue")
            args_report.append(user_choice)
        return args_report

    def main(self):
        while True:
            clear_screen()
            menu()
            self.show_modules()
            user_choice = self.select_module()
            print()
            module_info = self.get_module_info(user_choice)
            module_arg  = self.get_module_arg(module_info.get("arg"), module_info.get("description"))

            print()
            module_class = module_info["class"](module_arg)
            results      = module_class.run()

            if not results.get("error"):

                flatten_results(results)
            else:
                error(results.get("error"))

            inpt("Press enter to continue")


if __name__ == "__main__":
    main = Main()
    main.main()
            