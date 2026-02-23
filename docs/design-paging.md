# Design: Cursor-Based Pagination

<https://playbooks.com/rules/postgresql>
<https://ignaciochiazzo.medium.com/paginating-requests-in-apis-d4883d4c1c4c>

## Backend

### SQL

Using index as starting point of query

page_size=10
page_cursor =  000000000000 # index or query discriminant
entity_count = 000000000100 # rows in table: select count (*) from entity

entity_count_enc = btoa(entity_count)
page_cursor_enc = btoa(page_cursor)

```sql
select * from ${entity} where ${entity_id} > ${page_cursor} order by ${entity_id} limit ${PAGE_SIZE};
```


GET $project_api/$entity?page_size=100

},
  "_links": {
    "self": "/items?page=2&size=10",
    "next": "$project_api/$entity?page_size=100&cursor=count_enc-index_enc",
    "prev": "$project_api/$entity?page_size=100&cursor=00000000-0000-0000-0000-000000000000",
    "first": "$project_api/$entity?page_size=100&cursor=00000000-0000-0000-0000-000000000000",
    "last": "/items?page=100&size=10"
  }

  $project_api/$entity?page_size=100&cursor=00000000-0000-0000-0000-000000000000>; rel="first",
  $project_api/$entity?page_size=100&cursor=30f8507f-40e6-44b9-924f-5f814e3f072e>; rel="next"

GET $project_api/$entity?page_size=100&cursor=30f8507f-40e6-44b9-924f-5f814e3f072e

## Frontend

## References

