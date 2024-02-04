from pydantic import BaseModel


class ListPagination(BaseModel):
    total_records: int
    count: int
    limit: int
    offset: int
