from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/max_number/{numbers:path}")
def max_numbers(numbers: str):
    try:
        num_as_num = (int(it) for it in numbers.split("/"))
        return f"Максимальное переданное число <i>{max(num_as_num)}</i>"
    except ValueError:
        raise HTTPException(status_code=400, detail="Все параметры пути должны быть целыми числами")

