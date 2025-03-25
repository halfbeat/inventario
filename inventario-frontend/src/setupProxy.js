const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function (app) {
    app.use(
        '/inventario/api/v1',
        createProxyMiddleware({
            target: 'http://localhost:5000/api/v1',
            changeOrigin: true,
        })
    );
};