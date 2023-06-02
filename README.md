<h2> What about automating losing the games? </h2>

This bot is designed to lose on chess.com by using any chess engine with the Python-chess library to calculate and play the worst moves on the board. In this example, we use Stockfish, but you can use any engine that is supported by the Python-chess library.

<h3> Setup </h3>

- Download any chess engine and rename it to fish.exe
- setup the Pythonic stuff:

  ```bash
      python -m venv env
      source env/Scripts/activate
      pip install -r requirements.txt

      cp player.example.py player.py
  ```

- Add you're account in the file you just created player.py and feel free to configure you're settings

<h3> Run The Code </h3>

```bash
    python main.py {account number}
```

<hr>

I am not responsible for any misuse of my scripts. These scripts were created for research and data collection purposes only.
