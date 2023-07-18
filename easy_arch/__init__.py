#! /bin/python3
import argparse, argcomplete
import gettext
import pacman
import logging
logging.basicConfig(level=logging.INFO)

locale_path = './locale/'
gettext.bindtextdomain('internation', locale_path)
gettext.textdomain('internation')
_ = gettext.gettext

def pak_exist(pak_name):
    for pacman_pak in pacman.get_available():
        if pacman_pak['id'] == pak_name:
            return True
    return False

def install_pak(args):
    pak_list = args.pak_name
    logging.info(_("Start search pacman"))
    for pak_name in pak_list:
        pacman.set_bin('pacman')
        if pak_exist(pak_name):
            logging.info(_("Found in pacman, use pacman"))
            pacman.install(pak_name)
        else:
            logging.info(_("Not found in pacman, use yay"))
            pacman.set_bin('yay')
            print(pacman.get_bin())
            use_bin = bool(input(_(
                "use (0){1} or (1){0}?".format(pak_name + '-bin', pak_name))))
            if use_bin:
                pacman.install(pak_name + '-bin')
            else:
                pacman.install(pak_name)
    
def remove_pak(args):
    pacman.set_bin('pacman')
    pak_list = args.pak_name
    for pak_name in pak_list:
        pacman.remove(pak_name)

def search_pak(args):
    pak_list = args.pak_name
    pacman.set_bin('pacman')
    pacman.pacman('-Ss', pak_list, print_r=True)
    pacman.set_bin('yay')
    pacman.pacman('-Ss', pak_list, print_r=True)

def upgrade(args):
    logging.info(_("Start upgrade pacman"))
    pacman.set_bin('pacman')
    pacman.upgrade()
    logging.info(_("Start upgrade yay"))
    pacman.set_bin('yay')
    pacman.upgrade()

parser = argparse.ArgumentParser(prog = "easy_arch", 
                                 description = _("A arch package management helper for beginner"))
argcomplete.autocomplete(parser)
subparsers = parser.add_subparsers()

com_install = subparsers.add_parser("install", help = _("install package"))
com_install.add_argument('pak_name', nargs='+')
com_install.set_defaults(func=install_pak)

com_update = subparsers.add_parser("update", help = _("resynchronize the package index files from sources"))
com_update.set_defaults(func=lambda args:pacman.refresh())

com_remove = subparsers.add_parser("remove", help = _("remove package"))
com_remove.add_argument('pak_name', nargs='+')
com_remove.set_defaults(func=remove_pak)

com_search = subparsers.add_parser("search", help = _("search package"))
com_search.add_argument('pak_name', nargs='+')
com_search.set_defaults(func=search_pak)

com_upgrade = subparsers.add_parser("upgrade", help = _("install the newest versions of all packages "))
com_upgrade.set_defaults(func=upgrade)

args = parser.parse_args()
if not hasattr(args, 'func'):
    args = parser.parse_args(['-h'])
args.func(args) 