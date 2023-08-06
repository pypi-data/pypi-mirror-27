
Sample Configuration file
===============================

Sample `~/.asxterminus.yaml` file

```yaml
    refresh_interval: 300
    codes:
      - KGN
      - A2M
      - APX
    assets:
      KGN:
        -
          - 1.48
          - 10000
        -
          - 1.34
          - 5000
      A2M:
        -
          - 2.7
          - 5000
      APX:
        -
          - 2.5
          - 10000
    columns:
      - code
      - last_price
      - open_price
      - day_high_price
      - day_low_price
```

