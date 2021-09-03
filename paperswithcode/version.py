class Version:
    __slots__ = ("major", "minor", "build")

    def __init__(self, major, minor, build):
        self.major = major
        self.minor = minor
        self.build = build

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.build}"

    def __repr__(self):
        return (
            f"Version(major={self.major}, minor={self.minor}, "
            f"build={self.build})"
        )


version = Version(0, 2, 2)
__version__ = str(version)
