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
| 03_senales · ¿Tu web te trae clientes, o solo está ahí? | — |
| 09_proceso · Así trabajo, paso a paso | Disseny Web PM |
| 12_clinica · Nadie elige dentista a ciegas | Clínica Dental Fulanito |
| 13_reformas · Si haces reformas, enseña esto | Reformas Fulanito |
| 14_rural · Reservas directas para tu casa rural | Mas Fulanito |
| 15_gimnasio · Antes de apuntarse, mira esto | Gimnasio Fulanito |
| 17_asesoria · Tu web dice lo mismo que todas | Asesoría Fulanito |
| 18_estetica · Tu carta, sin «consultar» | Centro de Estética Fulanita |
| 23_busca · Lo que mira un cliente antes de llamarte | Peluquería Fulanito |
| 28_bienvenidos · Si tu web empieza con «Bienvenidos» | Can Fulanito |
| 29_movil · Abre tu web en el móvil | Fisioterapia Fulanito |
| 30_taller · Así te busca quien tiene una avería | Taller Fulanito |
| 31_tienda · Tu tienda cierra. Tu web, no. | Ferretería Fulanito |

Fuente: Montserrat (licencia OFL, en `fuentes/`). `.env` no se sube nunca.
