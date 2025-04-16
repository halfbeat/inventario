import {withAuthenticationRequired} from "react-oidc-context";
import React from "react";
import {useParams} from "react-router-dom";
import {ComponentesSistema} from "./ComponentesSistema";
import {SistemaHeader} from "./SistemaHeader";


const ComponentesSistemaPage = () => {
    let params = useParams();
    return (
        <>
            <SistemaHeader/>
            <p className={"h4 p-2"}>Componentes del sistema </p>
            <ComponentesSistema sistemaId={params.sistema_id}></ComponentesSistema>
        </>

    )
}


export default withAuthenticationRequired(ComponentesSistemaPage, {
    OnRedirecting: () => (<div>Redirecting to the login page...</div>)
});