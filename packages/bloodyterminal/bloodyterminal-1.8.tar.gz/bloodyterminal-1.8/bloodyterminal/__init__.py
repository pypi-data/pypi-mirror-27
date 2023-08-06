from colorama import Fore, Style, init
from win10toast import ToastNotifier

init()
toaster = ToastNotifier()


class btext:

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

    def demo():
        btext.success("your string")
        btext.info("your string")
        btext.warning("your string")
        btext.debug("your string")
        btext.custom("your prefix", "your string")


class btoast:

    def success(str1, str2, int=10):
        toaster.show_toast(str1, str2, icon_path="ico/success.ico", duration=int)

    def info(str1, str2, int=10):
        toaster.show_toast(str1, str2, icon_path="ico/info.ico", duration=int)

    def warning(str1, str2, int=10):
        toaster.show_toast(str1, str2, icon_path="ico/warning.ico", duration=int)

    def debug(str1, str2, int=10):
        toaster.show_toast(str1, str2, icon_path="ico/debug.ico", duration=int)

    def custom(str1, str2, int=10):
        toaster.show_toast(str1, str2, icon_path="ico/custom.ico", duration=int)

    def demo():
        btoast.success("your title", "your message", 2)
        btoast.info("your title", "your message", 2)
        btoast.warning("your title", "your message", 2)
        btoast.debug("your title", "your message", 2)
        btoast.custom("your title", "your message", 2)
