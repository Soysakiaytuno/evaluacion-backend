from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Puebla la base de datos con 300 sesiones y 500 oyentes por sesión (Requisito de la rúbrica)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Verificando si la base de datos ya tiene datos...'))
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM content.sesion")
            count = cursor.fetchone()[0]
            
            if count > 0:
                self.stdout.write(self.style.SUCCESS(f'La BD ya contiene {count} sesiones. Omitiendo seeding.'))
                return

            self.stdout.write(self.style.WARNING('Iniciando la inserción masiva de 150,000+ registros. Por favor espera...'))
            
            sql_seed = """
            DO $$
            DECLARE
                v_conf_id UUID := uuid_generate_v4();
                v_fecha_base TIMESTAMPTZ := '2026-05-20 09:00:00+00';
            BEGIN
                -- Conferencia
                INSERT INTO content.conferencia (id, nombre, fecha_inicio, fecha_fin, fecha_creacion, fecha_modificacion)
                VALUES (v_conf_id, 'Cumbre Global de Tecnología 2026', '2026-05-20', '2026-05-22', NOW(), NOW());

                -- Tracks
                INSERT INTO content.track (id, id_conferencia, nombre, fecha_creacion, fecha_modificacion)
                SELECT uuid_generate_v4(), v_conf_id, 'Track ' || i, NOW(), NOW() FROM generate_series(1, 10) s(i);

                -- Usuarios y Ponentes
                INSERT INTO content.usuario (id, nombre, apellido, fecha_creacion, fecha_modificacion)
                SELECT uuid_generate_v4(), 'UsuarioNombre' || i, 'UsuarioApellido' || i, NOW(), NOW() FROM generate_series(1, 700) s(i);

                INSERT INTO content.ponente (id, id_usuario, descripcion, fecha_creacion, fecha_modificacion)
                SELECT uuid_generate_v4(), id, 'Biografía generada automáticamente.', NOW(), NOW() FROM content.usuario ORDER BY random() LIMIT 100;

                -- Sesiones (300 Main Resources)
                INSERT INTO content.sesion (id, id_track, titulo, descripcion, hora_inicio, hora_fin, capacidad, fecha_creacion, fecha_modificacion)
                SELECT 
                    uuid_generate_v4(),
                    (SELECT id FROM content.track ORDER BY random() LIMIT 1),
                    'Título de Sesión ' || i,
                    'Descripción auto-generada para la sesión ' || i,
                    v_fecha_base + (i || ' hours')::interval,
                    v_fecha_base + ((i + 1) || ' hours')::interval,
                    600, NOW(), NOW()
                FROM generate_series(1, 300) s(i);

                -- Asignar Ponentes a Sesiones
                INSERT INTO content.sesion_ponente (sesion_id, ponente_id)
                SELECT s.id, p.id FROM content.sesion s
                CROSS JOIN LATERAL (SELECT id FROM content.ponente ORDER BY random() LIMIT 2) p
                ON CONFLICT DO NOTHING;

                -- Oyentes (500 Child Resources x 300 = 150,000 inscripciones)
                INSERT INTO content.oyente (id, id_sesion, id_usuario, fecha_creacion, fecha_modificacion)
                SELECT uuid_generate_v4(), s.id, u.id, NOW(), NOW() FROM content.sesion s
                CROSS JOIN LATERAL (SELECT id FROM content.usuario ORDER BY random() LIMIT 500) u
                ON CONFLICT DO NOTHING;
            END $$;
            """
            
            try:
                cursor.execute(sql_seed)
                self.stdout.write(self.style.SUCCESS('¡Seeding completado con éxito! Se han generado más de 150,000 registros.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error durante el seeding: {str(e)}'))