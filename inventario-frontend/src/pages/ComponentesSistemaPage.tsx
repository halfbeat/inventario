import {withAuthenticationRequired} from "react-oidc-context";
import React from "react";
import {Link, useParams} from "react-router-dom";
import {SistemaHeader} from "./SistemaHeader";
import {ComponentesSistema} from "../componentes/ComponentesSistema";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";


const ComponentesSistemaPage = () => {
    let params = useParams();
    return (
        <>
            <SistemaHeader/>
            <p className={"h4 p-2"}>Componentes del sistema </p>
            <ComponentesSistema sistemaId={params.sistema_id}></ComponentesSistema>
            <div className={"text-end mt-3"}>
                <Link className={"btn btn-primary btn-sm"} to={"registro"}><FontAwesomeIcon icon={"plus"}/> Registrar
                    componente</Link>
            </div>
        </>

    )
}


export default withAuthenticationRequired(ComponentesSistemaPage, {
    OnRedirecting: () => (<div>Redirecting to the login page...</div>)
});