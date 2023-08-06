"Creates file in .ipython\profile_default\startup that adds package to path."
#FIXME: Generalize the following code as an extendible funcion or class.

import os

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.join(dir_path)
#
dir_path = dir_path.encode('unicode_escape').decode('latin1')
usr_path = os.path.expanduser('~')
ipython_startup = os.path.join(usr_path, '.ipython', 'profile_default', 'startup')

print(ipython_startup)

# code="""
# from notebook_mapper import append_mapped
# append_mapped(path={}, server={})
# """
#
# path='Pics\Kittens'
# server='vmw-mysmb'
#
# print(os.path.realpath(path))

# code ="""
# import sys
# sys.path.append("{}")
# """.format(dir_path)



# if os.path.exists(ipython_startup):
#     with open(os.path.join(ipython_startup, 'noteboook_mappings.py'), 'w') as f:
#         f.write(code)
# else:
#     print('Could not find:', ipython_startup)
