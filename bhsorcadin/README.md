# Divine Paladin Source

`setup-bhsorcadin.tp2` is the WeiDU installer.

Important source files:

- `setup-bhsorcadin.tp2`: kit definition, CLAB generation, spell conversion,
  passive effects, and BG2EE proficiency text repair.
- `lib/fl#add_kit_ee.tpa`: public-domain EE `ADD_KIT` helper by Wisp and
  Argent77.
- `spells/`: prebuilt custom Magic Missile SPL resources used during install.
- `tools/extend_magic_missile.py`: developer utility for regenerating the
  custom Magic Missile resources.
