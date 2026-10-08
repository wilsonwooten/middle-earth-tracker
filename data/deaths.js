// Chapter in which a character dies, per book. From that chapter on, the list and the
// character result say "died" with the chapter and place instead of "off the map". Only for
// deaths the text makes plain; leaving the story alive (Gollum in The Hobbit, Melian) is a
// plain "" retirement in the chapter data, not an entry here.
window.DEATHS = {
  hobbit: { "Smaug": "14" },
  lotr: { "Boromir": "III.1", "Theoden": "V.6", "Halbarad": "V.6", "Denethor": "V.7", "Gollum": "VI.3", "Saruman": "VI.8" },
  silm: {
    "Finwe": "8", "Denethor of the Laiquendi": "10", "Feanor": "13", "Angrod": "18", "Aegnor": "18", "Fingolfin": "18",
    "Barahir": "19a", "Gorlim": "19a", "Finrod": "19b", "Huan": "19d", "Carcharoth": "19d", "Huor": "20", "Fingon": "20",
    "Beleg": "21b", "Orodreth": "21c", "Gwindor": "21c", "Finduilas": "21d", "Glaurung": "21e", "Turin": "21e", "Nienor": "21e",
    "Thingol": "22", "Dior": "22", "Celegorm": "22", "Curufin": "22", "Caranthir": "22",
    "Turgon": "23", "Maeglin": "23", "Ecthelion": "23", "Gothmog": "23", "Glorfindel": "23",
    "Amrod": "24a", "Maedhros": "24b", "Ar-Pharazon": "Ak.3", "Celebrimbor": "RoP.2", "Anarion": "RoP.3", "Gil-galad": "RoP.4", "Elendil": "RoP.4", "Isildur": "RoP.4",
  },
  ut: {
    "Lalaith": "I.2a", "Saeros": "I.2d", "Beleg": "I.2g", "Orodreth": "I.2h", "Gwindor": "I.2h", "Finduilas": "I.2i", "Aerin": "I.2i",
    "Glaurung": "I.2m", "Turin": "I.2m", "Nienor": "I.2m", "Brandir": "I.2m",
    "Veantur": "II.2b", "Meneldur": "II.2d", "Isildur": "III.1", "Elendur": "III.1", "Theodred": "III.5",
  },
};
