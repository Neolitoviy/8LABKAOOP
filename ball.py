class Ball:
    def __init__(self, num_sectors, colors=None):
        self.num_sectors = num_sectors
        if colors is None:
            self.colors = ['AliceBlue', 'AntiqueWhite', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque', 'Black',
                           'BlanchedAlmond', 'Blue', 'BlueViolet',
                           'Brown', 'BurlyWood', 'CadetBlue', 'Chartreuse', 'Chocolate', 'Coral', 'CornflowerBlue',
                           'Cornsilk', 'Crimson', 'Cyan', 'DarkBlue', 'DarkCyan', 'DarkGoldenRod', 'DarkGray',
                           'DarkGreen',
                           'DarkKhaki', 'DarkMagenta', 'DarkOliveGreen', 'DarkOrange', 'DarkOrchid', 'DarkRed',
                           'DarkSalmon',
                           'DarkSeaGreen', 'DarkSlateBlue', 'DarkSlateGray', 'DarkTurquoise',
                           'DarkViolet', 'DeepPink', 'DeepSkyBlue', 'DimGray', 'DodgerBlue', 'FireBrick', 'FloralWhite',
                           'ForestGreen',
                           'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'GoldenRod', 'Gray', 'Green',
                           'GreenYellow', 'HoneyDew', 'HotPink', 'IndianRed', 'Indigo', 'Ivory',
                           'Khaki', 'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue',
                           'LightCoral', 'LightCyan', 'LightGoldenRodYellow', 'LightGray',
                           'LightGreen', 'LightPink', 'LightSalmon', 'LightSeaGreen',
                           'LightSkyBlue', 'LightSlateGray', 'LightSteelBlue', 'LightYellow',
                           'Lime', 'LimeGreen', 'Linen',
                           'Magenta', 'Maroon', 'MediumAquaMarine', 'MediumBlue',
                           'MediumOrchid', 'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue',
                           'MediumSpringGreen', 'MediumTurquoise', 'MediumVioletRed', 'MintCream',
                           'MistyRose', 'Moccasin',
                           'NavajoWhite', 'Navy',
                           'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed', 'Orchid',
                           'PaleGoldenRod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed',
                           'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple',
                           'RebeccaPurple', 'Red', 'RosyBrown', 'RoyalBlue',
                           'SaddleBrown', 'Salmon', 'SandyBrown', 'SeaGreen', 'SeaShell',
                           'Sienna', 'Silver', 'SkyBlue', 'SlateBlue', 'SlateGray', 'Snow',
                           'SpringGreen', 'SteelBlue',
                           'Tan', 'Teal', 'Thistle', 'Tomato', 'Turquoise',
                           'Violet',
                           'Wheat', 'White', 'WhiteSmoke',
                           'Yellow', 'YellowGreen']
        else:
            self.colors = colors
        self.stripes = [None] * num_sectors

    def color_stripes(self):
        i = 0
        l = len(self.colors)

        for stripe in range(self.num_sectors):
            colors = []
            j = 0
            while j < l - 2:
                colors.append(self.colors[i % l])
                i += 1
                j += 1
            colors.append(self.colors[i % l])
            i -= 1
            colors.append(self.colors[i % l])
            i += 2
            self.stripes[stripe] = colors

    def __str__(self):
        output = ""
        for stripe, colors in enumerate(self.stripes):
            output += f"Sector {stripe + 1}:\n"
            output += ", ".join(colors) + ".\n"
        return output
