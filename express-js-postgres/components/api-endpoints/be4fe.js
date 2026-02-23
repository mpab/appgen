const express = require('express');
const app = express();
const db = require('../database');
const response = require('../response');

// CRUD API
const apiPath = "/__ENTITY_PASCAL__"

// Create
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

// Read ALL, including constraints
// http://localhost:3000/api/__ENTITY_PASCAL__
module.exports = app.get(apiPath, async (req, res) => {
    let request = `be4fe: read all __ENTITY_PASCAL__`;
    try {
        const [
__SQL_READ_B4FE_PROMISE_RESULTS___
        ] = await Promise.all([
__SQL_READ_B4FE__
        ]);
        result = {
            version: {
                shape: "BB9D0245-82F4-4E65-BD6E-D7A2A1694656",
                major: 0,
                minor: 0,
                revision: 1
            },
            entities: __ENTITY_SNAKE__.rows,
            entity_fields: __ENTITY_FIELDS_TABLE_VECTOR__,
            references: {
__SQL_READ_B4FE_CONSTRAINTS___
            }
        };
        response.success(res, result, request);
    } catch (err) {
        response.error(res, err, request);
    }
});

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
