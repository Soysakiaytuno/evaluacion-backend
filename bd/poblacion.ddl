DO $$
DECLARE
    -- Variables para controlar la ejecución
    v_conf_id UUID := uuid_generate_v4();
    v_fecha_base TIMESTAMPTZ := '2026-05-20 09:00:00+00';
    v_track_id UUID;
    v_sesion_id UUID;
    
    -- Contadores para los bucles
    i INT;
    j INT;
    k INT;
BEGIN
    
    INSERT INTO content.conferencia (id, nombre, fecha_inicio, fecha_fin)
    VALUES (v_conf_id, 'Global Developer Summit 2026', '2026-05-20', '2026-05-22');

    INSERT INTO content.usuario (nombre, apellido)
    SELECT 'Usuario_' || s.i, 'Apellido_' || s.i
    FROM generate_series(1, 700) AS s(i);

    INSERT INTO content.ponente (id_usuario, descripcion)
    SELECT id, 'Experto internacional en tecnología. Biografía generada automáticamente.'
    FROM content.usuario
    ORDER BY id  -- Usamos un orden consistente (podría ser aleatorio, pero id es más rápido)
    LIMIT 100;

    FOR i IN 1..10 LOOP
        
        -- Insertar 1 Track
        INSERT INTO content.track (id, id_conferencia, nombre)
        VALUES (uuid_generate_v4(), v_conf_id, 'Track Tecnológico ' || i)
        RETURNING id INTO v_track_id;

        -- Por cada Track, insertar 30 Sesiones consecutivas en el tiempo
        FOR j IN 1..30 LOOP
            
            INSERT INTO content.sesion (
                id, 
                id_track, 
                titulo, 
                descripcion, 
                hora_inicio, 
                hora_fin, 
                capacidad
            )
            VALUES (
                uuid_generate_v4(), 
                v_track_id, 
                'Sesión Especializada ' || j || ' (Track ' || i || ')',
                'Exploración profunda sobre las últimas tendencias de desarrollo. Charla ' || j,
                v_fecha_base + ((j - 1) * interval '2 hours'),      -- Cada charla dura 2h, una tras otra
                v_fecha_base + ((j - 1) * interval '2 hours') + interval '90 minutes', 
                600 -- Capacidad suficiente para alojar a los 500 oyentes obligatorios
            )
            RETURNING id INTO v_sesion_id;

            -- Inmediatamente después de crear la sesión, le asignamos 2 Ponentes al azar
            INSERT INTO content.sesion_ponente (id_sesion, id_ponente)
            SELECT v_sesion_id, id
            FROM content.ponente
            ORDER BY random()
            LIMIT 2;

        END LOOP;
        
    END LOOP;

    INSERT INTO content.oyente (id_sesion, id_usuario)
    SELECT s.id, u.id
    FROM content.sesion s
    CROSS JOIN LATERAL (
        -- Seleccionamos aleatoriamente 500 usuarios distintos para cada sesión
        SELECT id 
        FROM content.usuario 
        ORDER BY random() 
        LIMIT 500
    ) u
    ON CONFLICT DO NOTHING; -- Por si ocurre alguna colisión de la restricción UNIQUE

END $$;