class SincronizacionRouter:
    """
    Router para manejar las operaciones de las tablas Sincronizacion y RegistroSincronizacion
    """
    TABLAS_BDSIAF = ['sincronizacion', 'registrosincronizacion', 'estadoproyectoinversion', 'proyectoinversion', 'programacionproyectoinversion' ]

    def db_for_read(self, model, **hints):
        if model._meta.model_name in self.TABLAS_BDSIAF:
            return 'BDSIAF'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.model_name in self.TABLAS_BDSIAF:
            return 'BDSIAF'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        # Permitir relaciones entre modelos de la misma base de datos
        if obj1._meta.model_name in self.TABLAS_BDSIAF and \
           obj2._meta.model_name in self.TABLAS_BDSIAF:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name in self.TABLAS_BDSIAF:
            return db == 'BDSIAF'
        return db == 'default'