import React from 'react';
import './App.scss';
import {useAuth} from "react-oidc-context";
import {Template} from "./layout/Template";

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


    return (<Template/>);
}

export default App;
