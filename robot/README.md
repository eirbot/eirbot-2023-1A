
# Eirbot coupe 1A 2023 Demoul'eirb

A brief description of what this project does and who it's for


## Protocol de com rasp <-> nucleo

Les communcations entre la raspberrypi et la nucleo se font part usb par envoie de commande en hexa (cf tableau ci dessous).

| Commande hex | Description |
| --- | --- |
| \ | Controle stepper gauche |
| git diff | Controle stepper droit |