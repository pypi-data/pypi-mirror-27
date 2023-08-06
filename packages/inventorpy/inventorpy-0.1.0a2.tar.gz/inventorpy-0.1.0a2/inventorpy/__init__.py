import importlib
import pkgutil


# PLUGINS = [
#     importlib.import_module(name)
#     for finder, name, ispkg
#     in pkgutil.iter_modules()
#     if name.startswith('inventorpy_')
# ]
#
#
# REPOSITORIES = dict()
# def init_repositories():
#     imported = {
#         'remote': [
#             plugin.repository.Repository()
#             for plugin in PLUGINS
#             if plugin.__plugin__ == 'remote-repository'
#         ],
#         'disk': [
#             plugin.repository.Repository()
#             for plugin in PLUGINS
#             if plugin.__plugin__ == 'disk-repository'
#         ],
#         'memory': MemoryRepo()
#     }
#     REPOSITORIES.update(imported)
#     return
#
#