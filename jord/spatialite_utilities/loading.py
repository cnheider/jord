__all__ = ["load_spatialite"]


def load_spatialite(dbapi_conn, connection_record):
    dbapi_conn.enable_load_extension(True)
    dbapi_conn.load_extension("mod_spatialite")
