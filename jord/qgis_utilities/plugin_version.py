from pyplugin_installer.installer_data import repositories, plugins


__all__ = ["plugin_status"]


def plugin_status(plugin_key) -> str:
    return plugins.all()[plugin_key]["status"]


# utils.reloadPlugin()
