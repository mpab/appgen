const expose = require('./index');

// Info Endpoint - requires no database
expose(require('./endpoints/info.js'));
// ---------------------------------------------------------------------------

