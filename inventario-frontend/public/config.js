var PUBLIC_URL = "/inventario";
var REACT_APP_BASE_URL = "http://localhost:3000/inventario";
var REACT_APP_OIDC_REALM = "https://ssokcpre.jcyl.es/auth/realms/GSS-conciliacion-extranet";
var REACT_APP_OIDC_CLIENT_ID = "familias";
var REACT_APP_OIDC_REDIRECT_URI = REACT_APP_BASE_URL;
var REACT_APP_OIDC_SCOPE = "email profile openid";
var REACT_APP_BACKEND_BASE_URL = "http://localhost:3000/inventario/api/v1";

// var Configuration = {
//     baseUrl: REACT_APP_BASE_URL,
//     oidc: {
//         realm: REACT_APP_OIDC_REALM,
//         client_id: REACT_APP_OIDC_CLIENT_ID,
//         redirect_uri: REACT_APP_OIDC_REDIRECT_URI,
//         scope: REACT_APP_OIDC_SCOPE,
//         post_logout_redirect_uri: REACT_APP_OIDC_REDIRECT_URI,
//     },
//     backend: {
//         baseUrl: REACT_APP_BACKEND_BASE_URL,
//     }
// };
// exports.Configuration = Configuration;