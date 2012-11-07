from django.utils.translation import ugettext_lazy as _

# Constants for all available difficulty types.
SIMPLE = 1
MEDIUM = 2
DIFFICULT = 3

# Names for all available difficulty types.
DIFFICULTIES = (
    (SIMPLE, _("simple")),
    (MEDIUM, _("medium")),
    (DIFFICULT, _("difficult")),
)


# Constants for all available unit types.
CUP = 11
BAG = 97
SHEET = 98
SHEETS = 179
BUNCH = 16
BUNDLE = 204
CL = 12
CM = 46
THICKNESS = 215
DL = 44
CAN = 166
CANS = 156
THIN = 100
BUCKET = 2
AFEW = 43
AFEWSTALKS = 30
TBS = 13
TBSH = 59
SOMETHING = 22
POSSIBLY = 120
EXTRA = 220
BOTTLE = 55
BOTTLES = 184
G = 3
GLASS = 31
GLASSES = 93
GREATCAN = 63
GREATBOTTLE = 124
GREATSHE = 21
GREAT = 213
GREATHE = 180
GREATIT = 42
HALF = 70
HANDFUL = 48
KG = 28
SMALLBUNCH = 127
SMALLCAN = 104
SMALLGLASS = 83
SMALLHEAD = 18
SMALLBOTTLE = 249
SMALLSHE = 24
SMALL = 168
SMALLHE = 52
SMALLIT = 131
TUBER = 153
HEAD = 19
BALL = 231
BALLS = 217
BALLS2 = 122
BOX = 74
HEADS = 77
CORN = 192
LITER = 165
MGREATSHE = 25
MGREATHE = 53
MGREATIT = 90
MORE = 227
MG = 228
ML = 4
MSP = 5
NB = 7
PAIR = 76
PACKAGE = 243
PCK = 169
PKT = 1
PLATE = 119
PORT = 72
PRISE = 106
PRISES = 238
RING = 130
RIB = 84
DISC = 32
DISCS = 252
SHOT = 126
TAPENADE = 78
SPLASH = 15
ROD = 149
STALK = 255
STALKS = 57
PIECE = 87
CULM = 47
CHALKBOARD = 218
CHALKBOARDS = 116
CUP2 = 224
CUPS = 29
PART = 146
TL = 14
HEAPEDTL = 58
LEVELTL = 164
POT = 175
DROP = 20
TUBE = 125
BAG2 = 141
LOTS = 136
FEW = 45
ROOT = 198
ROOTS = 161
CUBE = 89
TOE = 26
BRACE = 150

# Names for all available unit types.
UNITS = (
    (CUP, _("cup")),
    (BAG, _("bag")),
    (SHEET, _("sheet")),
    (SHEETS, _("sheets")),
    (BUNCH, _("bunch")),
    (BUNDLE, _("bundle")),
    (CL, _("cl")),
    (CM, _("cm")),
    (THICKNESS, _("thick")),
    (DL, _("dl")),
    (CAN, _("can")),
    (CANS, _("cans")),
    (THIN, _("thin")),
    (BUCKET, _("bucket")),
    (AFEW, _("a few")),
    (AFEWSTALKS, _("a few stalks")),
    (TBS, _("tbs")),
    (TBSH, _("level tbs.")),
    (SOMETHING, _("something")),
    (POSSIBLY, _("possibly")),
    (EXTRA, _("extra")),
    (BOTTLE, _("bottle")),
    (BOTTLES, _("bottles")),
    (G, _("g")),
    (GLASS, _("glass")),
    (GLASSES, _("glasses")),
    (GREATCAN, _("great can")),
    (GREATBOTTLE, _("great bottle")),
    (GREATSHE, _("great she")),
    (GREAT, _("great")),
    (GREATHE, _("great he")),
    (GREATIT, _("great it")),
    (HALF, _("half")),
    (HANDFUL, _("handful")),
    (KG, _("kg")),
    (SMALLBUNCH, _("small bunch")),
    (SMALLCAN, _("small can")),
    (SMALLGLASS, _("small glass")),
    (SMALLHEAD, _("small head")),
    (SMALLBOTTLE, _("small bottle")),
    (SMALLSHE, _("small she")),
    (SMALL, _("small")),
    (SMALLHE, _("small he")),
    (SMALLIT, _("small it")),
    (TUBER, _("tuber")),
    (HEAD, _("head")),
    (BALL, _("ball")),
    (BALLS, _("balls")),
    (BALLS2, _("some balls")),
    (BOX, _("box")),
    (HEADS, _("heads")),
    (CORN, _("corn")),
    (LITER, _("liter")),
    (MGREATSHE, _("medium she")),
    (MGREATHE, _("medium he")),
    (MGREATIT, _("medium it")),
    (MORE, _("more")),
    (MG, _("mg")),
    (ML, _("ml")),
    (MSP, _("msp.")),
    (NB, _("n. B.")),
    (PAIR, _("pair")),
    (PACKAGE, _("package")),
    (PCK, _("pck.")),
    (PKT, _("pkt.")),
    (PLATE, _("plate")),
    (PORT, _("port.")),
    (PRISE, _("prise")),
    (PRISES, _("prises")),
    (RING, _("ring")),
    (RIB, _("rib")),
    (DISC, _("disc")),
    (DISCS, _("discs")),
    (SHOT, _("shot")),
    (TAPENADE, _("tapenade")),
    (SPLASH, _("splash")),
    (ROD, _("rod")),
    (STALK, _("stalk")),
    (STALKS, _("stalks")),
    (PIECE, _("piece")),
    (CULM, _("culm")),
    (CHALKBOARD, _("chalkboard")),
    (CHALKBOARDS, _("chalkboards")),
    (CUP2, _("cup2")),
    (CUPS, _("cups")),
    (PART, _("part")),
    (TL, _("tl.")),
    (HEAPEDTL, _("heaped tl.")),
    (LEVELTL, _("level tl.")),
    (POT, _("pot")),
    (DROP, _("drop")),
    (TUBE, _("tube")),
    (BAG2, _("bag2")),
    (LOTS, _("lots")),
    (FEW, _("few")),
    (ROOT, _("root")),
    (ROOTS, _("roots")),
    (CUBE, _("cube")),
    (TOE, _("toe")),
    (BRACE, _("brace")),
)