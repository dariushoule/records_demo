from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def home():
    return {"message": "Hey rest client, you are looking dandy today"}


def cli_entry():
    print('Hey world, you are looking dandy today')


if __name__ == '__main__':
    cli_entry()
