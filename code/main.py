import os
import Environment as env

str_intro = f"""
      _ _                     
     | (_)                    
   __| |_ _ __ __ _ _ __ ___  
  / _` | | '__/ _` | '_ ` _ \ 
 | (_| | | | | (_| | | | | | |
  \__,_|_|_|  \__,_|_| |_| |_|
                              
{env.APP_NAME} - {env.VERSION}
Presione cualquier tecla para continuar...
"""

print(str_intro)
input()

if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')

exit()