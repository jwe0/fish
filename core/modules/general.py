import os
from pystyle import Colors, Colorate

def clear_screen():
    os.system("clear")

def menu():
    ascii_art = """
O     O           ,       
  o o          .:/    
    o      ,,///;,   ,;/ 
      o   o)::::::;;///
         >::::::::;;\\\ 
           ''\\\\\\\\\\'"';\ 
              ';\\

"""

    ascii_art_2 = """
 ______   __     ______     __  __       
/\  ___\ /\ \   /\  ___\   /\ \_\ \      
\ \  __\ \ \ \  \ \___  \  \ \  __ \     
 \ \_\    \ \_\  \/\_____\  \ \_\ \_\    
  \/_/     \/_/   \/_____/   \/_/\/_/    
                                         """
    print(Colorate.Color(Colors.cyan, ascii_art_2))
    print("[*] Automated OSINT toolkit for penetration testing")
    print("[*] Developed by /jwe0")
    print("[>] Made with love <3")

def flatten_results(results, base_indent=4):
    clear_screen()
    ascii_art_2 = """
 ______   __     ______     __  __       
/\  ___\ /\ \   /\  ___\   /\ \_\ \      
\ \  __\ \ \ \  \ \___  \  \ \  __ \     
 \ \_\    \ \_\  \/\_____\  \ \_\ \_\    
  \/_/     \/_/   \/_____/   \/_/\/_/
                                         """
    result = [Colorate.Color(Colors.cyan, ascii_art_2), "[*] Lookup results", ""]
    for section in results:
        info = results[section]
        result.append(f"├ {section.title().replace("_", " ")}")
        if type(info) == str:
            result.append(f"│{" " * base_indent}├ [{section}] | {info}")
            result.append(f"│{" " * base_indent}└")
            
        elif type(info) == dict:
            max_key = max([len(key) for key in info])
            for key, value in info.items():
                if type(value) != dict:
                    result.append(f"│{" " * (base_indent * 2)}├ [{key}] {" " * (max_key - len(key))} | {value}")
                elif type(value) == dict:
                    result.append(f"│{" " * (base_indent * 2)}├ {key}")
                    result.append(f"│{" " * base_indent * 2}└───┐")
                    max_key = max([len(A) for A in value])
                    for k, v in value.items():
                        result.append(f"│{" " * (base_indent * 3)}├ [{k}]{" " * (max_key - len(k))} | {v}")
                    result.append(f"│{" " * base_indent * 3}└")
            result.append(f"│{" " * base_indent * 2}└")
    result.pop(-1)
    result.append(f"└")
    print("\n".join(result))