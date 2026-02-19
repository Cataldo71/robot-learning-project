# Dual L298N Motor Wiring Diagram (4 Motors)

This is the equivalent of an M1/M2/M3/M4 motor map, but for **2x L298N drivers** as used in this project.

## Motor Position Layout

```mermaid
flowchart TB
  subgraph ROBOT[Top View Robot Front at top]
    direction TB
    subgraph F[Front]
      direction LR
      M1[M1 Front-Left]
      M3[M3 Front-Right]
    end
    subgraph R[Rear]
      direction LR
      M2[M2 Back-Left]
      M4[M4 Back-Right]
    end
  end
```

## Driver Assignment

- **L298N Controller A** = Left side motors
  - Motor A output (OUT1/OUT2) → **M1 (Front-Left)**
  - Motor B output (OUT3/OUT4) → **M2 (Back-Left)**
- **L298N Controller B** = Right side motors
  - Motor A output (OUT1/OUT2) → **M3 (Front-Right)**
  - Motor B output (OUT3/OUT4) → **M4 (Back-Right)**

## Signal Wiring (Pi GPIO → L298N IN Pins)

```mermaid
flowchart LR
    subgraph PI[Raspberry Pi GPIO]
      G21[GPIO21 Pin40]
      G20[GPIO20 Pin38]
      G16[GPIO16 Pin36]
      G26[GPIO26 Pin37]
      G19[GPIO19 Pin35]
      G13[GPIO13 Pin33]
      G6[GPIO6 Pin31]
      G5[GPIO5 Pin29]
      GND1[Pi GND]
    end

    subgraph A[L298N Controller A Left Side]
      AIN1[IN1]
      AIN2[IN2]
      AIN3[IN3]
      AIN4[IN4]
      AOUT12[OUT1 OUT2]
      AOUT34[OUT3 OUT4]
      APWR[12V GND]
    end

    subgraph B[L298N Controller B Right Side]
      BIN1[IN1]
      BIN2[IN2]
      BIN3[IN3]
      BIN4[IN4]
      BOUT12[OUT1 OUT2]
      BOUT34[OUT3 OUT4]
      BPWR[12V GND]
    end

    M1[M1 Front-Left Motor]
    M2[M2 Back-Left Motor]
    M3[M3 Front-Right Motor]
    M4[M4 Back-Right Motor]
    PSU[12V Battery or PSU]

    G21 --> AIN1
    G20 --> AIN2
    G16 --> AIN3
    G26 --> AIN4

    G19 --> BIN1
    G13 --> BIN2
    G6 --> BIN3
    G5 --> BIN4

    AOUT12 --> M1
    AOUT34 --> M2
    BOUT12 --> M3
    BOUT34 --> M4

    PSU --> APWR
    PSU --> BPWR
    GND1 --- APWR
    GND1 --- BPWR
```

### GPIO to L298N Pin Mapping

| Motor | Wheel Position | GPIO Forward | GPIO Backward | Driver | L298N Input Pins |
|---|---|---|---|---|---|
| M1 | Front-Left | GPIO 21 (Pin 40) | GPIO 20 (Pin 38) | Controller A | IN1 / IN2 |
| M2 | Back-Left | GPIO 16 (Pin 36) | GPIO 26 (Pin 37) | Controller A | IN3 / IN4 |
| M3 | Front-Right | GPIO 19 (Pin 35) | GPIO 13 (Pin 33) | Controller B | IN1 / IN2 |
| M4 | Back-Right | GPIO 6 (Pin 31) | GPIO 5 (Pin 29) | Controller B | IN3 / IN4 |

## Motor Output Wiring (L298N OUT Pins → Motor Posts)

### Top-Down Motor Post Wiring (Exact OUTx → Motor Terminals)

To avoid mixing wires, label each motor's two tabs before wiring:

- **Inner post (I)** = motor tab facing the center of the robot
- **Outer post (O)** = motor tab facing the outside edge of the robot

Use this reference orientation while labeling: robot front at top, viewed from above.

```mermaid
flowchart TB
    subgraph TOP[Top View Robot Front at top]
      direction TB

      subgraph ROW1[Front Motors]
        direction LR
        subgraph M1[M1 Front-Left]
          M1I[Inner post I]
          M1O[Outer post O]
        end
        subgraph M3[M3 Front-Right]
          M3I[Inner post I]
          M3O[Outer post O]
        end
      end

      subgraph DRIVERS[L298N Output Terminals]
        direction LR
        subgraph A[L298N A Left Side]
          AOUT1[OUT1]
          AOUT2[OUT2]
          AOUT3[OUT3]
          AOUT4[OUT4]
        end
        subgraph B[L298N B Right Side]
          BOUT1[OUT1]
          BOUT2[OUT2]
          BOUT3[OUT3]
          BOUT4[OUT4]
        end
      end

      subgraph ROW2[Rear Motors]
        direction LR
        subgraph M2[M2 Back-Left]
          M2I[Inner post I]
          M2O[Outer post O]
        end
        subgraph M4[M4 Back-Right]
          M4I[Inner post I]
          M4O[Outer post O]
        end
      end
    end

    AOUT1 --> M1I
    AOUT2 --> M1O
    AOUT3 --> M2I
    AOUT4 --> M2O

    BOUT1 --> M3I
    BOUT2 --> M3O
    BOUT3 --> M4I
    BOUT4 --> M4O
```

### Output-to-Post Table

| Motor | Driver Output | Connect To Motor Post |
|---|---|---|
| M1 Front-Left | A OUT1 | M1 Inner (I) |
| M1 Front-Left | A OUT2 | M1 Outer (O) |
| M2 Back-Left | A OUT3 | M2 Inner (I) |
| M2 Back-Left | A OUT4 | M2 Outer (O) |
| M3 Front-Right | B OUT1 | M3 Inner (I) |
| M3 Front-Right | B OUT2 | M3 Outer (O) |
| M4 Back-Right | B OUT3 | M4 Inner (I) |
| M4 Back-Right | B OUT4 | M4 Outer (O) |

If one wheel spins opposite of expected, swap only that motor's two wires (I/O) or invert in software.

## Power Wiring (Separate Pi + Motor Supplies)

### Power Notes

- Keep **ENA/ENB jumpers installed** on both L298N boards unless you wire separate PWM speed control to EN pins.
- Connect both L298N grounds and Raspberry Pi ground together (common ground).
- Do **not** power motors from Raspberry Pi 5V.

### Separate Power Supplies (Pi + Motors)

Use two independent supplies:

- **Pi PSU**: 5V USB-C supply to Raspberry Pi only
- **Motor PSU**: 6-12V (or your motor rated voltage) to both L298N boards

```mermaid
flowchart LR
  PIPSU[Pi Power Supply 5V USB-C]
  PI[Raspberry Pi]
  MPSU[Motor Power Supply 6-12V]
  A[L298N A]
  B[L298N B]

  PIPSU --> PI

  MPSU -- +V --> A
  MPSU -- +V --> B
  MPSU -- GND --> A
  MPSU -- GND --> B

  PI -- GPIO control lines --> A
  PI -- GPIO control lines --> B

  PI -- one GND wire --> A
  PI -- one GND wire --> B
```

### Critical dual-supply rules

- Keep **positive rails separate**: do not connect Pi 5V to motor +V.
- **Grounds must be common**: Pi GND must connect to L298N GND/motor PSU GND.
- Prefer a star ground point at motor PSU negative or a clean GND bus.
- Keep high-current motor wires away from Pi signal wires when possible.

### Terminal-by-Terminal Power Wiring (Detailed)

For each L298N board, the 3-pin power screw terminal is typically labeled:

- **`+12V`** (sometimes `VS`, `Vmotor`, or `+V`) = motor supply positive input
- **`GND`** = motor supply negative / common ground
- **`5V`** = logic 5V rail on the module (behavior depends on jumper)

### 3-Terminal Block Detail (12V setup)

```mermaid
flowchart LR
  BAT[12V Battery]
  PI[Raspberry Pi]
  GBUS[Ground Bus or Star Ground]

  subgraph A[L298N A Power Terminal]
    A12[+12V]
    AG[GND]
    A5[+5V]
  end

  subgraph B[L298N B Power Terminal]
    B12[+12V]
    BG[GND]
    B5[+5V]
  end

  BAT -- Battery + --> A12
  BAT -- Battery + --> B12

  BAT -- Battery - --> GBUS
  PI -- Pi GND --> GBUS
  GBUS --> AG
  GBUS --> BG

  A5 -. leave disconnected in typical 12V mode .- PI
  B5 -. leave disconnected in typical 12V mode .- PI
```

In this 12V configuration:

- L298N `+12V` gets only battery positive.
- L298N `GND` gets battery negative and Pi ground (prefer via ground bus/star point).
- L298N `+5V` is not used as a motor input.
- Pi stays on its own 5V USB-C power supply.

### Exactly where to connect each power wire

For **L298N A** and **L298N B**:

1. Motor PSU `+` → L298N `+12V` (or `VS/+V`) terminal
2. Motor PSU `-` → L298N `GND` terminal
3. Raspberry Pi GND pin → L298N `GND` terminal (or same ground bus)

Repeat for both driver boards so all grounds are tied together.

### Practical terminal note

Most screw terminals hold one wire best. If needed, use a small terminal block/WAGO as a ground splitter so battery `-` and Pi GND both reach each L298N `GND` cleanly.

### Does GPIO mapping change with separate supplies?

No. GPIO mapping is unchanged. Power wiring and signal wiring are independent as long as grounds are common.

Use the same mapping already defined:

- GPIO21/20 → Controller A IN1/IN2 (M1)
- GPIO16/26 → Controller A IN3/IN4 (M2)
- GPIO19/13 → Controller B IN1/IN2 (M3)
- GPIO6/5 → Controller B IN3/IN4 (M4)

### About the L298N `5V` pin and jumper

- If `5V-EN` (or `EN-5V`) jumper is installed, the module's onboard regulator usually powers logic from motor input.
- In that common setup, leave Pi 5V disconnected from the L298N `5V` pin.
- If your board requires external 5V logic (jumper removed), provide a stable 5V logic source to L298N `5V` and keep common ground.
- Do not use L298N `5V` pin to power the Raspberry Pi.
