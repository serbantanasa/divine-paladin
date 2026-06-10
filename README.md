# Divine Paladin

A custom WeiDU kit for Baldur's Gate: Enhanced Edition, Baldur's Gate II:
Enhanced Edition, and EET.

The Divine Paladin is intentionally overpowered: a Paladin kit with Cavalier,
Inquisitor, and Undead Hunter benefits, hidden Use Any Item, improved turning,
armor use, five-pip proficiency caps, and sorcerer-style arcane innate spell
progression.

The internal kit id is `BHSORC` for save compatibility. The in-game display
name is `Divine Paladin`.

## Requirements

- BGEE, BG2EE, or EET
- WeiDU

## Install

Copy the `bhsorcadin` folder into the game installation directory, next to
`chitin.key`.

Then run WeiDU against the TP2 file:

```sh
weidu bhsorcadin/setup-bhsorcadin.tp2
```

Alternatively, copy or symlink your WeiDU binary into the game directory as
`setup-bhsorcadin` on Linux/macOS or `setup-bhsorcadin.exe` on Windows, then run
it from the game directory.

Example Linux install:

```sh
cp /path/to/weidu ./setup-bhsorcadin
chmod +x ./setup-bhsorcadin
./setup-bhsorcadin
```

## Where It Appears

Create a new character and choose `Paladin`. The kit should appear as
`Divine Paladin`.

## Major Features

- Counts as a Paladin for class checks and BG2 Paladin quest behavior.
- Uses Paladin THAC0, saves, hit dice, and XP progression.
- Requires Strength 18, Constitution 18, Wisdom 13, and Charisma 17.
- Gains Cavalier anti-dragon and anti-demon bonuses, fear and poison immunity,
  fire and acid resistance, and Remove Fear.
- Gains Inquisitor charm/hold immunity, Dispel Magic, and True Sight.
- Gains Undead Hunter undead bonuses, hold immunity, and level-drain immunity.
- Turns undead at effective Paladin level +2.
- Can use any item through a hidden passive effect, including arcane scrolls
  and wands.
- Gains escalating arcane innate spells as level-up grants.
- Uses a custom Magic Missile wrapper that continues scaling past the normal
  level 9 cap.

## Notes

The scaling Magic Missile resources are included as prebuilt SPL files, so
Python is not required for normal installation. The Python script in `tools/`
is kept only as a developer utility for regenerating those SPL files.

Do not commit WeiDU-generated `backup` folders, `SETUP-*.DEBUG`, `WeiDU.log`,
`override`, or game data files.
