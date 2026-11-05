# Rebolledo de la Torre · web comunitaria

Web estática (HTML + CSS, sin JavaScript, sin cookies, sin servicios de terceros) para GitHub Pages.
Rama de trabajo: `nueva-web`. No publicar en `main` hasta cerrar la lista de abajo.

## Antes de publicar (marcado con «Por completar» / «por definir» en las páginas)
- [x] Titular (TeleCluB Rebolledo de la Torre) y correo (teleclubrebolledo@gmail.com) incorporados.
- [x] Grupo informal sin actividad económica: sin NIF por ahora. **Al empezar a vender (camisetas, tazas…) hay que identificar al titular (LSSI-CE art. 10), darse de alta fiscalmente y revisar el Aviso legal.**
- [x] Sin nombres de personas por ahora (proyecto muy informal, poca gente). Revisar si el proyecto crece o hay actividad económica: un grupo informal no tiene personalidad jurídica y responde una persona física.
- [x] Reconocimiento por usos comerciales: se deja deliberadamente ambiguo («el reconocimiento que corresponda», a acordar por escrito con la persona autora).
- [x] Bot de Telegram: @rebolledodelatorre_bot (enlazado en `colabora.html`).
- [ ] Decidir si se publica como **proyecto comunitario no oficial** (como está redactado) o en coordinación con el Ayuntamiento. No hacerse pasar por la web oficial.
- [ ] Contenido de Naturaleza, Historia y Estrellas con **fuentes citadas** (nada de memoria).
- [x] Vídeo de portada (`media/cielo-nocturno.mp4`, recomprimido de 13,6 a 2,6 MB, sin audio): permiso confirmado por TeleCluB.
- [ ] Fotos: **autoría propia o permiso/licencia**, con crédito; texto alternativo en cada imagen; subtítulos o transcripción en vídeo. Sin personas reconocibles sin consentimiento por escrito (L.O. 1/1982).
- [ ] Revisión por un gestor o abogado del Aviso legal y de Privacidad (los textos son un borrador de buena fe, no asesoría jurídica).

## Reglas que mantiene esta web (para no incumplir normativa)
- **Sin datos personales**: nada de formularios, comentarios, registros ni tablón con envíos de terceros (riesgo RGPD/LOPDGDD, difamación y localización de personas). Contacto por el bot de Telegram (botón «Hablar con el equipo»); el correo solo en las páginas legales y sin enlace mailto, para evitar spam. Antes: contacto solo por correo.
- **Sin cookies ni almacenamiento local, y sin contenido incrustado de terceros** (Google Maps, YouTube, redes, fuentes de Google, analítica). Así no hace falta banner de cookies (LSSI-CE art. 22.2). Si algún día se añade algo de eso, hay que actualizar la política de privacidad y añadir consentimiento *antes*.
- **Aviso legal con titular identificado** (LSSI-CE art. 10), aunque sea sin ánimo de lucro.
- **Accesibilidad** como mínimo WCAG 2.1 AA por buena práctica (obligatoria solo para el sector público: RD 1112/2018).
- Mapas: enlace a OpenStreetMap, no incrustado.

## Lo que se retiró de la versión anterior (en `main`)
- El tablón automático de Telegram con mensajes de prueba y avisos con coordenadas, sin moderación.
- Enlaces de mapa rotos.
Si se quiere recuperar un tablón o avisos de vecinos, hay que diseñarlo con moderación previa, base legal de tratamiento y política de privacidad.

## Diseño y cómo editarlo
- Diseño (v2, 2026-10-31): la **curvatura de los lóbulos del roble** como único motivo (`css/roble.css`): bordes festoneados por máscara SVG, rama de fondo que se dibuja con el scroll, submenús que crecen despacio como una rama (`<details>`), títulos con degradado y trazo que se dibuja, tarjetas con esquinas de hoja y revelado por scroll. Sin hojas dibujadas ni contenido dentro de hojas. Sin JavaScript ajeno; animaciones solo con soporte y sin «movimiento reducido»; `@view-transition` entre páginas.
- El contenido está en `construir.py` (lista `CONTENIDO`); `python3 construir.py` regenera `index.html`. La galería la regenera el bot de fotos.
- Contenido tomado de la web anterior (web-rebolledo.pages.dev: rutas, astroturismo, eclipse, canales de Telegram). **Verificar cada dato** antes de publicar (distancias, desnivel, iglesia románica del s. XII, etc.).
- Coordenadas corregidas: 42.6889, -4.2271 (las de Windy de la web anterior). Antes había puesto 42.7302, -3.8910, que venían de una entrada de prueba del tablón.

## Lo que NO se ha traído de la web anterior (y por qué)
- Incrustados de terceros (Windy, forecast7, widgets de Telegram, Wikiloc embebido): instalan cookies o cargan scripts de terceros → exigirían banner de consentimiento. Aquí se enlazan, no se incrustan.
- Textos tipo «Portal Municipal», «Ayuntamiento», «Horarios del Ayuntamiento/Iglesia»: parecen oficiales y los horarios eran de relleno.
- Carpeta `ChatExport` (fotos exportadas de Telegram): sin permiso documentado por foto. Las fotos nuevas entran por el bot, con permiso y autoría archivados.


## Carrusel de secciones (2026-11-05)
- `index.html` lleva ahora UN carrusel dentro de una caja-arco: cada diapositiva enseña una subsección; cada vez que una sección vuelve a salir enseña la siguiente (y al acabar, empieza de nuevo). Flechas, teclado (← →), pausa y 12 s de avance automático (sin autoavance con «movimiento reducido»). Debajo, enlaces a cada sección completa (`#rutas`, `#astro`…, o `#astro-3` para una tarjeta) con la actual subrayada. Botón fijo «Volver al inicio» en todas las páginas.
- Lo hace `js/carrusel.js`: **script propio**, sin cookies, sin almacenamiento local, sin terceros ni analítica. Sin JavaScript, la web muestra todas las secciones una debajo de otra. `construir.py` genera las secciones en `#almacen`; el script mueve (no copia) la tarjeta activa a la caja. `?i=N` abre la diapositiva N (para pruebas).
- Nuevas secciones o tarjetas: se añaden en `CONTENIDO` y entran solas en el carrusel y en los enlaces.
- Barra superior: menús desplegables por sección (tarjetas enlazables, `#seccion-N`), con hiedra animada que baja al abrir; `barra_html()` la genera y `parchea_paginas()` la pone en todas las páginas fijas (y `barra-pagina.html` la usa la galería del bot).

## Huerta, Fauna y flora, tiempo (2026-11-05)
- **Huerta** (`huerta/datos.json`, copia pública de HuertaDigital: `python3 ~/Proyectos/huerto/exportar_a_web.py`; ficha mensual por la fecha de generación: el flujo diario la mantiene al día). Setas con avisos de seguridad y plantas peligrosas. Datos escritos de memoria, adaptados a ~958 m: orientativos.
- **Fauna y flora** (`naturaleza/datos.json` ← `naturaleza/crear_datos.py`): aves (con sección especial), mamíferos, reptiles y anfibios, insectos, árboles y flora. ★ = citado por fuentes del Geoparque; el resto, propio de la meseta norte (por contrastar con observaciones locales).
- **Tiempo en la cabecera** (`tiempo/tiempo.py` → `tiempo/tiempo.json`, leído por `js/tiempo.js`): Open-Meteo, consultado por el servidor (GitHub Actions cada 3 h, `.github/workflows/tiempo.yml`); las visitas no contactan con nadie. Se muestra el estado de ahora y «prev. mañana».
