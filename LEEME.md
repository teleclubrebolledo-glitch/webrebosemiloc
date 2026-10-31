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
- **Sin datos personales**: nada de formularios, comentarios, registros ni tablón con envíos de terceros (riesgo RGPD/LOPDGDD, difamación y localización de personas). Contacto solo por correo.
- **Sin cookies ni almacenamiento local, y sin contenido incrustado de terceros** (Google Maps, YouTube, redes, fuentes de Google, analítica). Así no hace falta banner de cookies (LSSI-CE art. 22.2). Si algún día se añade algo de eso, hay que actualizar la política de privacidad y añadir consentimiento *antes*.
- **Aviso legal con titular identificado** (LSSI-CE art. 10), aunque sea sin ánimo de lucro.
- **Accesibilidad** como mínimo WCAG 2.1 AA por buena práctica (obligatoria solo para el sector público: RD 1112/2018).
- Mapas: enlace a OpenStreetMap, no incrustado.

## Lo que se retiró de la versión anterior (en `main`)
- El tablón automático de Telegram con mensajes de prueba y avisos con coordenadas, sin moderación.
- Enlaces de mapa rotos.
Si se quiere recuperar un tablón o avisos de vecinos, hay que diseñarlo con moderación previa, base legal de tratamiento y política de privacidad.

## Diseño y cómo editarlo
- Diseño (v2, 2026-10-31): la **curvatura de los lóbulos del roble** como único motivo (`css/roble.css`): bordes festoneados por máscara SVG, rama de fondo que se dibuja con el scroll, submenús que crecen despacio como una rama (`<details>`), títulos con degradado y trazo que se dibuja, tarjetas con esquinas de hoja y revelado por scroll. Sin hojas dibujadas ni contenido dentro de hojas. Sin JavaScript; animaciones solo con soporte y sin «movimiento reducido»; `@view-transition` entre páginas.
- El contenido está en `construir.py` (lista `CONTENIDO`); `python3 construir.py` regenera `index.html`. La galería la regenera el bot de fotos.
- Contenido tomado de la web anterior (web-rebolledo.pages.dev: rutas, astroturismo, eclipse, canales de Telegram). **Verificar cada dato** antes de publicar (distancias, desnivel, iglesia románica del s. XII, etc.).
- Coordenadas corregidas: 42.6889, -4.2271 (las de Windy de la web anterior). Antes había puesto 42.7302, -3.8910, que venían de una entrada de prueba del tablón.

## Lo que NO se ha traído de la web anterior (y por qué)
- Incrustados de terceros (Windy, forecast7, widgets de Telegram, Wikiloc embebido): instalan cookies o cargan scripts de terceros → exigirían banner de consentimiento. Aquí se enlazan, no se incrustan.
- Textos tipo «Portal Municipal», «Ayuntamiento», «Horarios del Ayuntamiento/Iglesia»: parecen oficiales y los horarios eran de relleno.
- Carpeta `ChatExport` (fotos exportadas de Telegram): sin permiso documentado por foto. Las fotos nuevas entran por el bot, con permiso y autoría archivados.
