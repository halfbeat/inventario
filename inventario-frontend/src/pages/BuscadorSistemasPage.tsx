import React, {useEffect, useState} from "react";
import {withAuthenticationRequired} from "react-oidc-context";
import {ListadoPaginadoResumenSistemasDto} from "../openapi/api";
import {Link} from "react-router-dom";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import useApi from "../common/useApi";
import {Table} from "react-bootstrap";

const BuscadorSistemasPage = () => {
    const [sistemas, setSistemas] = useState({} as ListadoPaginadoResumenSistemasDto);
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
    }, [api]);

    return (
        <div>
            <p className={"h4 border border-2 rounded p-2"}>Sistemas registrados</p>
            <Table bordered>
                <thead>
                <tr>
                    <th>Id.</th>
                    <th>Nombre</th>
                </tr>
                </thead>
                <tbody>
                {sistemas?.items?.map(s =>
                    <tr style={{cursor: "pointer"}} key={s.sistema_id}>
                        <td>
                            <Link to={s.sistema_id}>{s.sistema_id}</Link>
                        </td>
                        <td>{s.nombre}</td>
                    </tr>)}
                </tbody>
            </Table>
            <p hidden={sistemas?.total !== 0}>No se ha encontrado ningún sistema</p>
            <div className={"text-end mt-3"}>
                <Link className={"btn btn-primary"} to={"registro"}><FontAwesomeIcon icon={"plus"}/> Registrar
                    sistema</Link>
            </div>
        </div>
    )
}

export default withAuthenticationRequired(BuscadorSistemasPage, {
    OnRedirecting: () => (<div>Redirecting to the login page...</div>)
});