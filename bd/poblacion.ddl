DO $$
DECLARE
    v_conf_id UUID := uuid_generate_v4();
    v_fecha_base TIMESTAMPTZ := '2026-05-20 09:00:00+00';
    v_track_id UUID;
    v_sesion_id UUID;
    i INT;
    j INT;
BEGIN
    -- Validar si ya existen datos para no volver a poblar y evitar errores
    IF EXISTS (SELECT 1 FROM content.conferencia LIMIT 1) THEN
        RETURN;
    END IF;
    
    -- Inserción de Conferencia
    INSERT INTO content.conferencia (id, nombre, fecha_inicio, fecha_fin, fecha_creacion, fecha_modificacion)
    VALUES (v_conf_id, 'Global Developer Summit 2026', '2026-05-20', '2026-05-22', NOW(), NOW());

    -- Inserción de 700 Usuarios
    INSERT INTO content.usuario (id, nombre, apellido, fecha_creacion, fecha_modificacion)
    SELECT uuid_generate_v4(), 'Usuario_' || s.i, 'Apellido_' || s.i, NOW(), NOW()
    FROM generate_series(1, 700) AS s(i);

    -- Inserción de 100 Ponentes
    INSERT INTO content.ponente (id, id_usuario, descripcion, fecha_creacion, fecha_modificacion)
    SELECT uuid_generate_v4(), id, 'Experto internacional en tecnología.', NOW(), NOW()
    FROM content.usuario
    ORDER BY id
    LIMIT 100;

    FOR i IN 1..10 LOOP
        -- Insertar 10 Tracks
        INSERT INTO content.track (id, id_conferencia, nombre, fecha_creacion, fecha_modificacion)
        VALUES (uuid_generate_v4(), v_conf_id, 'Track Tecnológico ' || i, NOW(), NOW())
        RETURNING id INTO v_track_id;

        -- Insertar 30 Sesiones por Track (TOTAL: 300 Sesiones, requisito cumplido)
        FOR j IN 1..30 LOOP
            INSERT INTO content.sesion (id, id_track, titulo, descripcion, hora_inicio, hora_fin, capacidad, fecha_creacion, fecha_modificacion)
            VALUES (
                uuid_generate_v4(), v_track_id, 'Sesión Especializada ' || j || ' (Track ' || i || ')',
                'Exploración profunda sobre tendencias. Charla ' || j,
                v_fecha_base + ((j - 1) * interval '2 hours'), v_fecha_base + ((j - 1) * interval '2 hours') + interval '90 minutes',
                600, NOW(), NOW()
            ) RETURNING id INTO v_sesion_id;

            -- Asignar Ponentes
            INSERT INTO content.sesion_ponente (id_sesion, id_ponente)
            SELECT v_sesion_id, id FROM content.ponente ORDER BY random() LIMIT 2;
        END LOOP;
    END LOOP;

    -- Insertar 500 Oyentes por cada Sesión
    INSERT INTO content.oyente (id, id_sesion, id_usuario, fecha_creacion, fecha_modificacion)
    SELECT uuid_generate_v4(), s.id, u.id, NOW(), NOW()
    FROM content.sesion s
    CROSS JOIN LATERAL (
        SELECT id FROM content.usuario ORDER BY random() LIMIT 500
    ) u
    ON CONFLICT DO NOTHING;

END $$;