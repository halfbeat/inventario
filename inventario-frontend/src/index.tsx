import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.scss';
import App from './App';
import reportWebVitals from './reportWebVitals';

import {AuthProvider, AuthProviderProps} from "react-oidc-context";

const oidcConfig: AuthProviderProps = {
    authority: "https://ssokc2pre.jcyl.es/realms/GSS",
    client_id: "familias",
    redirect_uri: "http://localhost:3000",
    scope: "email profile openid",
    post_logout_redirect_uri: "http://localhost:3000"
};

const root = ReactDOM.createRoot(
    document.getElementById('root') as HTMLElement
);
root.render(
    <React.StrictMode>
        <AuthProvider {...oidcConfig}>
            <App/>
        </AuthProvider>
    </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
