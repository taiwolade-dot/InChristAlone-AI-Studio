# ==============================
# INCHRISTALONE AI
# LAYOUT INTELLIGENCE ENGINE
# ==============================


class FlyerLayout:

    def __init__(
            self,
            width=1080,
            height=1350,
            speakers=0
    ):

        self.width = width
        self.height = height
        self.speakers = speakers


    def title_position(self):

        return (
            70,
            80
        )


    def verse_position(self):

        return (
            70,
            280
        )


    def event_info_position(self):

        return (
            70,
            450
        )


    def speaker_position(self):

        if self.speakers == 1:

            return [
                (
                    (self.width-240)//2,
                    int(self.height*0.58)
                )
            ]


        elif self.speakers == 2:

            return [
                (
                    int(self.width*0.18),
                    int(self.height*0.60)
                ),
                (
                    int(self.width*0.58),
                    int(self.height*0.60)
                )
            ]


        elif self.speakers == 3:

            return [
                (
                    (self.width-240)//2,
                    int(self.height*0.48)
                ),
                (
                    int(self.width*0.18),
                    int(self.height*0.70)
                ),
                (
                    int(self.width*0.58),
                    int(self.height*0.70)
                )
            ]

        elif self.speakers == 4:

            return [
                (int(self.width*0.16), int(self.height*0.52)),
                (int(self.width*0.56), int(self.height*0.52)),
                (int(self.width*0.16), int(self.height*0.74)),
                (int(self.width*0.56), int(self.height*0.74))
            ]

        else:

            positions = []

            cols = 3
            x_margin = int(self.width * 0.12)
            y_start = int(self.height * 0.52)
            x_spacing = (self.width - 2 * x_margin) // (cols - 1)
            y_spacing = int(self.height * 0.22)

            for i in range(self.speakers):

                row = i // cols
                col = i % cols

                positions.append(
                    (
                        x_margin + col * x_spacing - 120,
                        y_start + row * y_spacing
                    )
                )

            return positions
