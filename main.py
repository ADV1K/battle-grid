import asyncio
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sse_starlette.sse import EventSourceResponse, ServerSentEvent

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

state = ['' for _ in range(9)]
current_move = "x"
client_streams = []


class Stream:
    def __init__(self) -> None:
        self._queue = asyncio.Queue[ServerSentEvent]()

    def __aiter__(self) -> "Stream":
        return self

    async def __anext__(self) -> ServerSentEvent:
        return await self._queue.get()

    async def asend(self, value: ServerSentEvent) -> None:
        await self._queue.put(value)


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.jinja", {"request": request, "state": state})


@app.get("/move/{move}")
async def move(move: int):
    global current_move

    # if move is out of range
    if move < 1 or move > 9:
        return HTTPException(status_code=400, detail="Move out of range")

    # if move has already been made
    if state[move - 1]:
        print(f"-> Move already made at {move - 1}")
    else:
        print(f"-> New Move at {move - 1}")
        # save the move & return it
        state[move - 1] = current_move

        # change the current move
        current_move = "o" if current_move == "x" else "x"
        
        # update all clients
        print("-> Sending update to clients")
        current_board = await get_board_on_update()
        print(current_board)
        for stream in client_streams:
            await stream.asend(ServerSentEvent(data=current_board))
        
    # debugging
    for i in range(9):
        if i % 3 == 0:
            print()
        print(state[i].upper() or "-", end="")
    print()


async def get_board_on_update():
    return templates.get_template("board.jinja").render(state=state)


@app.get("/updates")
async def updates(response: Response):
    stream = Stream()
    client_streams.append(stream)
    return EventSourceResponse(stream)
