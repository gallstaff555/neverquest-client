# TODO Debug Account Creation 

# python virtual env
python3 -m venv .venv
source .venv/bin/activate

# Login
cd client
./login.py

# Start client test character
./main.py --name "player_one" --player_class "sword" --race "elf" --color "3"

# TODO
handle server disconnects