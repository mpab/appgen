const express = require('express');
const app = express();
const db = require('../database');
const response = require('../response');

// API
const apiPath = "/__ENTITY_PASCAL__"
const selfNavPath = `/api${apiPath}/`

const API_UUID = "30125261-A5CA-48E4-997E-3935C07BED5D"

// ---------------------------------------------------------------------------------------------------------------------------------------
// NAVIGATION/PAGING

// helper functions

const retPagingData = (entities, pageSize) => {
    return {
        entities: entities,
        page_size: parseInt(pageSize), //entities.rows.length,
        prev_cursor: entities.rows[0].__ENTITY_ID__,
        next_cursor: entities.rows.at(-1).__ENTITY_ID__
    };
}

const getPagingDataByPageSize = async (pageSize, pageCursor) => {
    const entities = await db.query(`select * from __ENTITY_SNAKE__ where "__ENTITY_ID__" > ${pageCursor} order by __ENTITY_ID__ limit ${pageSize};`);
    return retPagingData(entities, pageSize);
}

const getPagingDataByPageSizePrevCursor = async (pageSize, pageCursor) => {
    const entities = await db.query(`select * from (select * from __ENTITY_SNAKE__ where "__ENTITY_ID__" < ${pageCursor} order by __ENTITY_ID__ desc limit ${pageSize}) order by __ENTITY_ID__;`);
    return retPagingData(entities, pageSize);
}

const getPagingDataByPageSizeLastCursor = async (pageSize, pageCursor, entityCount) => {
    let window = entityCount % pageSize;
    if (!window) window = pageSize;

    const entities = await db.query(`select * from (select * from __ENTITY_SNAKE__ where "__ENTITY_ID__" <= ${pageCursor} order by __ENTITY_ID__ desc limit ${window}) order by __ENTITY_ID__;`);

    let pd = retPagingData(entities, pageSize);
    pd.isLastPage = true; // signal that next page link should be removed
    return pd;
}

const getPagingDataByPageSizeFirstCursor = async (pageSize, pageCursor) => {
    const entities = await db.query(`select * from __ENTITY_SNAKE__ where "__ENTITY_ID__" >= ${pageCursor} order by __ENTITY_ID__ limit ${pageSize};`);
    return retPagingData(entities, pageSize);
}

const getPagingDataByCursor = async (pageStartCursor, pageEndCursor) => {
    const entities = await db.query(`select * from __ENTITY_SNAKE__ where "__ENTITY_ID__" >= ${pageStartCursor} and "__ENTITY_ID__" <= ${pageEndCursor} order by __ENTITY_ID__;`);
    return retPagingData(entities, entities.rows.length);
}

const getFirstEntity = async () => {
    let result = await db.query(`select * from __ENTITY_SNAKE__ order by __ENTITY_ID__ asc limit 1;`);
    return result.rows[0];
}

const getLastEntity = async () => {
    let result = await db.query(`select * from __ENTITY_SNAKE__ order by __ENTITY_ID__ desc limit 1;`);
    return result.rows[0];
}

const getEntityCount = async () => {
    let result = await db.query(`select count(*) from __ENTITY_SNAKE__;`);
    return parseInt(result.rows[0].count);
}

const enrichPagingData = async (pagingData) => {
    const firstEntity = await getFirstEntity();
    pagingData.first_cursor = parseInt(firstEntity.__ENTITY_ID__); // start of data
    const lastEntity = await getLastEntity();
    pagingData.last_cursor = parseInt(lastEntity.__ENTITY_ID__);
    const entityCount = await getEntityCount();
    pagingData.entity_count = entityCount;
    pagingData._links = makeLinks(pagingData);
    return pagingData;
}

const makeResult = async (pagingData) => {
        const [
__SQL_READ_B4FE_PROMISE_RESULTS___
        ] = await Promise.all([
__SQL_READ_B4FE__
        ]);

    return {
        version: {
            shape: API_UUID,
            major: 0,
            minor: 0,
            revision: 1
        },
        entities: pagingData.entities.rows,
            entity_fields: __ENTITY_FIELDS_TABLE_VECTOR__,
            references: {
__SQL_READ_B4FE_CONSTRAINTS___
            },
        _links: pagingData._links,
        _paging: {
            entity_count: pagingData.entity_count,
            page_size: pagingData.page_size,
            prev_cursor: pagingData.prev_cursor,
            next_cursor: pagingData.next_cursor,
            first_cursor: pagingData.first_cursor,
            last_cursor: pagingData.last_cursor
        }
    };
}

const makeLinks = (pagingData) => {
    const self = `${selfNavPath}?page_size=${pagingData.page_size}&prev_cursor=${pagingData.prev_cursor}&next_cursor=${pagingData.next_cursor}`;
    let next = `${selfNavPath}?page_size=${pagingData.page_size}&next_cursor=${pagingData.next_cursor}`;
    let prev = `${selfNavPath}?page_size=${pagingData.page_size}&prev_cursor=${pagingData.prev_cursor}`;
    const first = `${selfNavPath}?page_size=${pagingData.page_size}&first_cursor=${pagingData.first_cursor}`;
    const last = `${selfNavPath}?page_size=${pagingData.page_size}&last_cursor=${pagingData.last_cursor}`;

    // remove invalid links
    if (pagingData.prev_cursor <= pagingData.first_cursor) prev = '';
    if (pagingData.isLastPage || pagingData.next_cursor >= pagingData.last_cursor) next = '';

    return {
        self: self,
        next: next,
        prev: prev,
        first: first,
        last: last
    }
}

// ---------------------------------------------------------------------------------------------------------------------------------------
// CRUD API

// ---------------------------------------------------------------------------------------------------------------------------------------
// Create (and reset index)
app.post(apiPath, async (req, res) => {
    let request = `create __ENTITY_PASCAL__`;
    try {
        const sql_get_index = __SQL_GET_INDEX__;
        const index_result = await db.query(sql_get_index);
        const index_name = index_result.rows[0]['pg_get_serial_sequence'];
        const sql_reset_idx = __SQL_RESET_INDEX__;
        console.log(await db.query(sql_reset_idx));
        __JS_BODY__
        const sql_create_item = __SQL_CREATE_ITEM__;
        console.log(sql_create_item);
        const results = await db.query(sql_create_item);
        response.success(res, results.rows, request);
    } catch (err) {
        response.error(res, err, request);
    }
});

// ---------------------------------------------------------------------------------------------------------------------------------------
// Read ALL, including constraints
// http://localhost:3000/api/__ENTITY_PASCAL__
module.exports = app.get(apiPath, async (req, res) => {
    let request = `be4fe: read all __ENTITY_PASCAL__`;
    try {
        const pageSize = req.query.page_size ? req.query['page_size'] : 5;
        let pd;
        if (req.query.prev_cursor && req.query.next_cursor ) {
            const prev_cursor = parseInt(req.query.prev_cursor);
            const next_cursor = parseInt(req.query.next_cursor);
            pd = await getPagingDataByCursor(prev_cursor, next_cursor);
        } else if (req.query.next_cursor) {
            const cursor = parseInt(req.query.next_cursor);
            pd = await getPagingDataByPageSize(pageSize, cursor);
        } else if (req.query.prev_cursor) {
            const cursor = parseInt(req.query.prev_cursor);
            pd = await getPagingDataByPageSizePrevCursor(pageSize, cursor);
        } else if (req.query.first_cursor) {
            const cursor = parseInt(req.query.first_cursor);
            pd = await getPagingDataByPageSizeFirstCursor(pageSize, cursor);
        } else if (req.query.last_cursor) {
            const cursor = parseInt(req.query.last_cursor);
            const entityCount = await getEntityCount();
            pd = await getPagingDataByPageSizeLastCursor(pageSize, cursor, entityCount);
        } else {
            pd = await getPagingDataByPageSize(pageSize, -1); // initial data set
        }
        const epd = await enrichPagingData(pd);
        result = await makeResult(epd);
        response.success(res, result, request);
    } catch (err) {
        response.error(res, err, request);
    }
});

// ---------------------------------------------------------------------------------------------------------------------------------------
// Read ID
// http://localhost:3000/api/__ENTITY_PASCAL__/1
module.exports = app.get(apiPath + "/:__ENTITY_ID__", async (req, res) => {
    let request = `read __ENTITY_PASCAL__/__ENTITY_ID__`;
    try {
        const { __ENTITY_ID__ } = req.params;
        request = `read __ENTITY_PASCAL__/${__ENTITY_ID__}`;
        const sql_read_item = __SQL_READ_ITEM__;
        console.log(sql_read_item);
        const results = await db.query(sql_read_item);
        response.success(res, results.rows, request);
    } catch (err) {
        response.error(res, err, request);
    }
});

// ---------------------------------------------------------------------------------------------------------------------------------------
// Update
module.exports = app.put(apiPath, async (req, res) => {
    let request = `update __ENTITY_PASCAL__`;
    try {
        const { __ENTITY_ID__ } = req.body;
        __JS_BODY__
        request = `update __ENTITY_PASCAL__/${__ENTITY_ID__}`;
        const sql_update_item = __SQL_UPDATE_ITEM__;
        console.log(sql_update_item);
        const results = await db.query(sql_update_item);
        response.success(res, results.rows, request);
    } catch (err) {
        response.error(res, err, request);
    }
});

// ---------------------------------------------------------------------------------------------------------------------------------------
// Delete
module.exports = app.delete(apiPath + "/:__ENTITY_ID__", async (req, res) => {
    let request = `delete __ENTITY_PASCAL__`;
    try {
        const { __ENTITY_ID__ } = req.params;
        request = `delete __ENTITY_PASCAL__/${__ENTITY_ID__}`;
        const sql_delete_item = __SQL_DELETE_ITEM__;
        console.log(sql_delete_item);
        const results = await db.query(sql_delete_item);
        response.success(res, results.rows, request);
    } catch (err) {
        response.error(res, err, request);
    }
});
