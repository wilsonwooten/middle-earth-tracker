// Second-tier cast: Valar, Maiar, great beasts, and supporting characters.
// Merged into the chapter data at load time so the base files stay readable.
window.EXTRA_CAST = {
hobbit: {
  "6": {"Gwaihir": "Eagles' Eyrie"}, "7": {"Beorn": "Beorn's House", "Gwaihir": ""},
  "9": {"Thranduil": "Elvenking's Halls"}, "15": {"Thranduil": "Dale", "Dain": "Iron Hills"},
  "17": {"Beorn": "Erebor", "Thranduil": "Erebor", "Dain": "Erebor", "Gwaihir": "Erebor"},
  "18": {"Beorn": "Beorn's House", "Thranduil": "Forest Gate", "Dain": "Erebor", "Gwaihir": ""}, "19": {"Beorn": "", "Thranduil": ""}
},
lotr: {
  "I.6": {"Tom Bombadil": "Old Forest"}, "I.7": {"Tom Bombadil": "Bombadil's House", "Goldberry": "Bombadil's House"},
  "I.8": {"Tom Bombadil": "Barrow-downs"}, "I.9": {"Tom Bombadil": "", "Goldberry": "", "Butterbur": "Bree"},
  "I.12": {"Glorfindel": "Ford of Bruinen", "Butterbur": ""}, "II.1": {"Glorfindel": "Rivendell", "Arwen": "Rivendell", "Elladan and Elrohir": "Rivendell"},
  "II.3": {"Glorfindel": "", "Arwen": "", "Elladan and Elrohir": ""}, "II.6": {"Haldir": "Lorien", "Gwaihir": "Zirakzigil"},
  "II.8": {"Haldir": "Lorien", "Gwaihir": ""}, "II.9": {"Haldir": ""},
  "III.4": {"Treebeard": "Wellinghall"}, "III.8": {"Treebeard": "Isengard"}, "III.11": {"Treebeard": ""},
  "IV.9": {"Shelob": "Cirith Ungol"}, "IV.10": {"Shelob": ""},
  "V.1": {"Beregond": "Minas Tirith"}, "V.2": {"Halbarad": "Erech", "Elladan and Elrohir": "Erech"},
  "V.4": {"Imrahil": "Minas Tirith", "Halbarad": "Pelargir", "Elladan and Elrohir": "Pelargir"},
  "V.5": {"Ghan-buri-Ghan": "Druadan Forest"}, "V.6": {"Imrahil": "Pelennor", "Halbarad": "Pelennor", "Elladan and Elrohir": "Pelennor", "Ghan-buri-Ghan": ""},
  "V.7": {"Halbarad": ""}, "V.10": {"Imrahil": "Morannon", "Elladan and Elrohir": "Morannon", "Mouth of Sauron": "Morannon"},
  "VI.4": {"Mouth of Sauron": "", "Gwaihir": "Field of Cormallen"}, "VI.5": {"Imrahil": "Minas Tirith", "Beregond": "Minas Tirith", "Arwen": "Minas Tirith", "Elladan and Elrohir": "Minas Tirith", "Gwaihir": ""},
  "VI.6": {"Treebeard": "Isengard", "Elladan and Elrohir": "Rivendell", "Glorfindel": "Rivendell", "Arwen": "", "Imrahil": "", "Beregond": ""},
  "VI.7": {"Treebeard": "", "Glorfindel": "", "Elladan and Elrohir": "", "Butterbur": "Bree"}, "VI.8": {"Butterbur": ""}
},
silm: {
  "1": {"Manwe": "Taniquetil", "Varda": "Taniquetil", "Ulmo": "Ekkaia", "Aule": "Valmar", "Yavanna": "Pastures of Yavanna", "Orome": "Woods of Orome", "Mandos": "Halls of Mandos", "Nienna": "Halls of Nienna", "Tulkas": "Valmar", "Irmo": "Lorien (Valinor)", "Este": "Lorien (Valinor)", "Vaire": "Halls of Mandos", "Nessa": "Woods of Orome", "Vana": "Pastures of Yavanna", "Eonwe": "Taniquetil"},
  "2": {"Aule": "Valmar", "Yavanna": "Taniquetil", "Manwe": "Taniquetil"},
  "5": {"Osse": "Tol Eressea", "Uinen": "Tol Eressea", "Miriel": "Lorien (Valinor)", "Indis": "Tirion", "Ulmo": "Tol Eressea"},
  "6": {"Miriel": "Halls of Mandos", "Indis": "Tirion", "Mandos": "Halls of Mandos"},
  "8": {"Tulkas": "Valmar", "Orome": "Valmar", "Manwe": "Taniquetil", "Yavanna": "Two Trees", "Nienna": "Two Trees"},
  "9a": {"Mandos": "Araman", "Osse": "Alqualonde", "Uinen": "Alqualonde", "Olwe": "Alqualonde"},
  "9b": {"Amras": "Losgar"}, "10": {"Osse": "Falas"},
  "13": {"Gothmog": "Anfauglith", "Thorondor": "Thangorodrim"},
  "14": {"Huan": "Himlad", "Amras": "Amon Ereb", "Thorondor": "Crissaegrim", "Gothmog": "Angband"},
  "15": {"Ecthelion": "Gondolin", "Glorfindel": "Gondolin"}, "17": {"Haleth": "Thargelion"},
  "18": {"Haleth": "Brethil", "Gorlim": "Tarn Aeluin", "Thorondor": "Angband"},
  "19a": {"Gorlim": "Tol Sirion", "Daeron": "Menegroth", "Thorondor": "Crissaegrim"},
  "19b": {"Huan": "Tol Sirion", "Gorlim": "", "Daeron": "Menegroth"},
  "19c": {"Huan": "Dorthonion", "Carcharoth": "Angband", "Thorondor": "Angband"},
  "19d": {"Huan": "Neldoreth", "Carcharoth": "Neldoreth", "Daeron": "", "Thorondor": "Crissaegrim"},
  "20": {"Huan": "", "Carcharoth": "", "Gothmog": "Anfauglith", "Ecthelion": "Anfauglith", "Amras": "Amon Ereb"},
  "21a": {"Gothmog": "Angband", "Ecthelion": "Gondolin"}, "22": {"Amras": "Menegroth"},
  "23": {"Gothmog": "Gondolin", "Ecthelion": "Gondolin", "Glorfindel": "Cirith Thoronath", "Thorondor": "Cirith Thoronath"},
  "24a": {"Gothmog": "", "Ecthelion": "", "Glorfindel": "", "Amras": "Mouths of Sirion", "Eonwe": "Anfauglith", "Ancalagon": "Anfauglith", "Thorondor": "Anfauglith"},
  "24b": {"Eonwe": "Tirion", "Manwe": "Taniquetil", "Ulmo": "Valmar"},
  "Ak.2": {"Tar-Miriel": "Armenelos"}, "Ak.3": {"Tar-Miriel": "Armenelos"}, "Ak.3b": {"Manwe": "Taniquetil"}
},
ut: {
  "I.1b": {"Ulmo": "Mount Taras"}, "I.1c": {"Ulmo": ""}, "I.1d": {"Ecthelion": "Gondolin"}
}
};
window.EXTRA_NOTES = {
hobbit: {"7": {"Beorn": "Skin-changer; lends ponies as far as the forest."}, "17": {"Dain": "Arrives from the Iron Hills with five hundred dwarves.", "Thranduil": "Besieges, then fights beside the dwarves.", "Gwaihir": "The Eagles decide the battle."}},
lotr: {"I.7": {"Tom Bombadil": "The Ring does nothing to him.", "Goldberry": "River-daughter."}, "I.12": {"Glorfindel": "Lends Frodo his horse and faces the Nine at the ford."}, "III.4": {"Treebeard": "Calls the Entmoot."}, "IV.9": {"Shelob": "Stung by Sting and blinded by the Phial."}, "V.5": {"Ghan-buri-Ghan": "Guides the Rohirrim through the Stonewain Valley."}, "V.6": {"Halbarad": "Dies on the Pelennor bearing Arwen's standard.", "Imrahil": "Leads the knights of Dol Amroth."}, "V.10": {"Mouth of Sauron": "Shows Frodo's mithril coat and sword."}},
silm: {"1": {"Manwe": "King of Arda on Taniquetil.", "Ulmo": "Dwells in the Outer Sea and seldom comes to Valmar.", "Mandos": "Keeper of the Houses of the Dead."}, "8": {"Tulkas": "Pursues Melkor and is cheated by the Unlight."}, "9a": {"Mandos": "Pronounces the Doom of the Noldor from the shore."}, "13": {"Gothmog": "Lord of Balrogs; slays Feanor.", "Thorondor": "Carries Fingon to Maedhros on the cliff."}, "18": {"Thorondor": "Rescues Fingolfin's body and mars Morgoth's face.", "Gorlim": "Betrays Barahir's camp under Sauron's torture."}, "19b": {"Huan": "Defeats Sauron in wolf-form at the tower.", "Daeron": "Betrays Luthien's plans to Thingol."}, "19c": {"Carcharoth": "Bites off Beren's hand with the Silmaril."}, "19d": {"Huan": "Dies killing Carcharoth; speaks for the third time."}, "20": {"Gothmog": "Kills Fingon."}, "23": {"Gothmog": "Killed by Ecthelion in the Square of the King.", "Ecthelion": "Dies with Gothmog in the fountain.", "Glorfindel": "Fights the Balrog on Cirith Thoronath and falls."}, "24a": {"Eonwe": "Leads the host of the West.", "Ancalagon": "Breaks Thangorodrim in his fall."}, "24b": {"Eonwe": "Hails Earendil at the Calacirya."}, "Ak.3": {"Tar-Miriel": "Rightful Queen, dies climbing the Meneltarma as the wave comes."}},
ut: {"I.1b": {"Ulmo": "Rises from the sea in storm at Mount Taras to charge Tuor."}}
};
