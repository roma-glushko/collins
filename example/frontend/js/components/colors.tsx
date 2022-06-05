const availableColors: string[] = [
    "Beige",
    "FloralWhite",
    "GhostWhite",
    "LavenderBlush",
    "MintCream",
    "Moccasin",
    "OldLace",
    "LightBlue",
    "LightCoral",
    "LightCyan",
    "LightGoldenRodYellow",
    "LightGray",
    "LightGreen",
    "LightPink",
    "LightSalmon",
    "LightSeaGreen",
    "LightSkyBlue",
    "LightSlateGray",
    "LightSteelBlue",
    "LightYellow",
    "PaleGreen",
    "PeachPuff",
    "Linen",
    "Pink",
    "Plum",
    "PowderBlue",
    "Snow",
    "Tan",
    "Wheat",
    "WhiteSmoke",
]

export const getRandomColor = (): string => {
    return availableColors[Math.floor(Math.random() * availableColors.length)]
}