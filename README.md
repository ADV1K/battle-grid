# Battle Grid
A multiplayer tic-tac-toe game made with FastAPI and HTMX.
It uses server sent events to update the game state in real time, and HTMX to update the game board.
The events are sent as api calls to the server, and the server sends the updated game state to all the clients.

## How to run
```shell
poetry install
poetry shell
uvicorn main:app --reload
```

## How to play
Open two separate browser windows and go to `http://localhost:8000/`. The game will start when both players are connected.

## A Picture is Worth a Thousand Words, but a Video is Worth a Million
<iframe src="./screenrecord.mp4" width="560" height="315" frameborder="0" allowfullscreen ></iframe>

