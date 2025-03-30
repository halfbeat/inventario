import React, {useEffect, useState} from "react";
import {withAuthenticationRequired} from "react-oidc-context";
import {ListadoPaginadoSistemasDto} from "../openapi/api";
import {Link} from "react-router-dom";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import useApi from "../common/useApi";

const ListadoSistemas = () => {
    const [sistemas, setSistemas] = useState({} as ListadoPaginadoSistemasDto);
    const api = useApi();
    useEffect(() => {
        if (api) {
            api.sistemas.getSistemasInformacion()
                .then(res => res.data)
                .then(data => {
                    setSistemas(data);
                })
                .catch(err => console.error(err));
        }
    },[api]);

    const listaSistemas = sistemas?.items?.map(s =>
        <li key={s.sistema_id}>
            <Link to={s.sistema_id}>{s.nombre}</Link>
        </li>)
    return (
        <div>
            <p className={"h4 border border-2 rounded p-2"}>Sistemas registrados</p>
            <ul>{listaSistemas}</ul>
            <p hidden={sistemas?.total !== 0}>No se ha encontrado ningún sistema</p>
            <div className={"text-end mt-3"}>
                <Link className={"btn btn-primary"} to={"registro"}><FontAwesomeIcon icon={"plus"}/> Registrar
                    sistema</Link>
            </div>
        </div>
    )
}

export default withAuthenticationRequired(ListadoSistemas, {
    OnRedirecting: () => (<div>Redirecting to the login page...</div>)
});