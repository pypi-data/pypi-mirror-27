from colorama import Fore, Style, init

init()


class bt:

    def __init__():
        print(Style.RESET_ALL)

    def success(str):
        print(Fore.GREEN + '[SUCCESS] ' + str + Style.RESET_ALL)

    def info(str):
        print(Fore.YELLOW + '[INFO] ' + str + Style.RESET_ALL)

    def warning(str):
        print(Fore.RED + '[WARNING] ' + str + Style.RESET_ALL)

    def debug(str):
        print(Fore.MAGENTA + '[DEBUG] ' + str + Style.RESET_ALL)

    def custom(str1, str2):
        print(Fore.CYAN + '[%s] ' % str1 + str2 + Style.RESET_ALL)
