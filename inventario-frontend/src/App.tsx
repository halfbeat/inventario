import React from 'react';
import './App.scss';
import {useAuth} from "react-oidc-context";
import {Layout} from "./layout/Layout";

function App() {
    const auth = useAuth();

    switch (auth.activeNavigator) {
        case "signinSilent":
            return <div>Signing you in...</div>;
        case "signoutRedirect":
            return <div>Signing you out...</div>;
    }

    if (auth.isLoading) {
        return <div>Loading...</div>;
    }


    return (<Layout/>);
}

export default App;
