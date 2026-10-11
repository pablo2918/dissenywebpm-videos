# Disseny Web PM · carruseles y vídeos con voz

## Dónde está cada cosa

```
carruseles/<tema>_<es|ca>.json   textos, maquetas, gancho y guion de cada carrusel
guiones/<tema>_<es|ca>.txt       guion de la voz (se genera desde el JSON)
salida/<tema>/
├── PUBLICAR.md                  textos para Instagram, Facebook, TikTok y Shorts
├── es/carrusel/                 las 7 láminas para subir como carrusel
├── es/gancho.png                pantalla de gancho (solo para el vídeo)
├── es/video.mp4                 vídeo con voz (Reels, TikTok, Shorts)
└── ca/ ...                      lo mismo en catalán
herramientas/                    los programas
```

## Hacer un tema entero (los dos idiomas)

    python3 herramientas/hacer.py 30_taller

Dibuja las láminas y el gancho, genera la voz (Azure), monta el vídeo y deja
hojas de revisión en `.tmp/revision/` que hay que **mirar** antes de entregar.

## Temas hechos

| Tema | Negocio de ejemplo |
|---|---|
| 13_reformas · Si haces reformas, enseña esto | Reformas Fulanito |
| 23_busca · Lo que mira un cliente antes de llamarte | Peluquería Fulanito |
| 28_bienvenidos · Si tu web empieza con «Bienvenidos» | Can Fulanito |
| 29_movil · Abre tu web en el móvil | Fisioterapia Fulanito |
| 30_taller · Así te busca quien tiene una avería | Taller Fulanito |
| 31_tienda · Tu tienda cierra. Tu web, no. | Ferretería Fulanito |

Fuente: Montserrat (licencia OFL, en `fuentes/`). `.env` no se sube nunca.
