import React, {useEffect, useState} from "react";
import useApi from "../common/useApi";
import {ComponenteSistemaDto} from "../openapi/api";
import {Table} from "react-bootstrap";
import "./ComponentesSistema.scss"
import {ComponenteSistema} from "./ComponenteSistema";
import {useNavigate} from "react-router-dom";

interface ComponentesSistemaProps {
    sistemaId?: string | undefined
}


export const ComponentesSistema = ({sistemaId}: ComponentesSistemaProps) => {
    const api = useApi();
    const [componentes, setComponentes] = useState([] as Array<ComponenteSistemaDto>);
    const navigate = useNavigate()

    useEffect(() => {
        if (sistemaId && api) {
            api.sistemas.getComponentesSistemaInformacion(sistemaId)
                .then(res => res.data)
                .then(data => {
                    setComponentes(data);
                })
                .catch(err => console.error(err));
        }
    }, [api, sistemaId, setComponentes]);


    function selectComponente(componente_id: string) {
        navigate(`/sistemas/${sistemaId}/componentes/${componente_id}`)
    }


    return (
        <>
            <Table bordered>
                <thead>
                <tr>
                    <th>#</th>
                    <th>Nombre</th>
                </tr>
                </thead>
                <tbody>
                {componentes?.map(s =>
                    <tr style={{cursor: "pointer"}} key={s.componente_id}
                        onClick={() => selectComponente(s.componente_id)}>
                        <td > {s.componente_id}</td>
                        <td >{s.nombre}</td>
                    </tr>)}
                </tbody>
            </Table>
            <p  className="text-light-emphasis">Seleccione un componente para
                editarlo</p>

        </>
    )
}
