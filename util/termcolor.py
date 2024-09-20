from colorama import just_fix_windows_console, Fore, Style

# 使用colorama库的方法支持Windows的控制台显示彩色
just_fix_windows_console()

RESET = Style.RESET_ALL

RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
MAGENTA = Fore.MAGENTA
CYAN = Fore.CYAN

BRIGHT = Style.BRIGHT
ITALIC = '\033[3m'
INVERT = '\033[7m'
