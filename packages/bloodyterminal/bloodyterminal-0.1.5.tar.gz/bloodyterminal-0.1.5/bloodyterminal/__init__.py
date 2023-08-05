from colorama import Fore, Style


class bt:

    def __init__():
        print(Style.RESET_ALL)

    def info(str):
        print(Fore.YELLOW + '[INFO] ' + str)

    def warning(str):
        print(Fore.RED + '[WARNING] ' + str)

    def debug(str):
        print(Fore.MAGENTA + '[DEBUG] ' + str)

    def custom(str1, str2):
        print(Fore.GREEN + '[%s] ' % str1 + str2)
