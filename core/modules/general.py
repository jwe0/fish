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
    # I am fully aware how simple this should be, I am running on no sleep and it works so yk
    os.system("clear")
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
        result.append(f"├ [{section[0].title()}] {section.title().replace("_", " ")}")
        if type(info) == str:
            result.append(f"│{" " * base_indent}├ [{section}] | {info}")
            result.append(f"│{" " * base_indent}└")
            
        elif type(info) == dict:
            double_dic = False
            triple_dic = False
            max_key = max([len(key) for key in info])
            for key, value in info.items():
                if type(value) != dict:
                    result.append(f"│{" " * (base_indent * 2)}├ [{key}] {" " * (max_key - len(key))} | {value}")
                elif type(value) == dict:
                    double_dic = True
                    result.append(f"│{" " * (base_indent * 2)}├ {key}")
                    result.append(f"│{" " * base_indent * 2}└───┐")
                    max_key = max([len(A) for A in value])
                    for k, v in value.items():
                        if type(v) == dict:
                            max_key_2 = max([len(A) for A, B in value.items()]) + 2
                            triple_dic = True
                            result.append(f"│{" " * base_indent * 3}└───┐")
                            result.append(f"│{" " * (base_indent * 4)}├ {key}")
                            result.append(f"│{" " * base_indent * 4}└───┐")
                            for k_, v_ in v.items():
                                result.append(f"│{" " * (base_indent * 5)}├ [{k_}]{" " * (max_key_2 - len(k_))} | {v_}")
                        else:
                            triple_dic = False
                            result.append(f"│{" " * (base_indent * 3)}├ [{k}]{" " * (max_key - len(k))} | {v}")
                    if triple_dic:
                        result.append(f"│{" " * base_indent * 5}└")
                    else:
                        result.append(f"│{" " * base_indent * 3}└")
            if not double_dic:
                result.append(f"│{" " * base_indent * 2}└")
    result.append(f"│{" " * base_indent * 2}└")
    result.pop(-1)
    result.append(f"└")

    print("\n".join(result))